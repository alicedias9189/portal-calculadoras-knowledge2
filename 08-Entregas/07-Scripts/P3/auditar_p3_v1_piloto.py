#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piloto P3 v1: seleção por famílias, revisão conservadora e preservação dos 30 lotes.

Uso: python3 auditar_p3_v1_piloto.py --origem /caminho/do/pacote/P2-v7 --saida ./saida
Origem deve conter 'auditoria-p2-v7-csv-integral.zip' e 'lotes-001-a-030-p0-p1-p2-v7.zip'.
Dependências: apenas biblioteca padrão. Nenhum arquivo de origem é sobrescrito.
Decisões são HEURÍSTICAS para QA editorial, não validação humana individual.
"""
import argparse, csv, hashlib, io, json, re, unicodedata, zipfile
from pathlib import Path
from collections import Counter,defaultdict

ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
CATEGORIAS={
'financa':('Finanças','Orçamento pessoal','Controle de despesas','Ferramenta/consulta: orçamento pessoal','navegacional/transacional'),
'planilha':('Finanças','Orçamento pessoal','Planilhas e modelos','Consultar: modelo ou planilha de orçamento','navegacional/transacional'),
'custo_kwh':('Energia','Consumo elétrico','Custo por kWh','Estimar: custo da energia conforme tarifa e consumo','estimativa de custo'),
'calendario':('Datas','Calendário','Calendários mensais','Consultar: calendário mensal','tabela/referência'),
'carnaval':('Datas','Calendário','Datas comemorativas','Consultar: datas de feriados','informacional'),
'material_didatico':('Fora de escopo','Educação','Livros e materiais didáticos','Consultar: material didático de matemática','informacional'),
'gasolina':('Energia','Combustíveis','Consumo e autonomia veicular','Estimar: consumo ou distância com rendimento do veículo','cálculo contextual'),
'gestacao':('Fora de escopo','Saúde','Gestação e equivalência de semanas','Informar: idade gestacional e convenções de meses','fora de escopo'),
'gestante_direitos':('Trabalho','Legislação e direitos','Estabilidade e direitos da gestante','Consultar: direitos trabalhistas da gestante','informacional'),
'cdi_cotacao':('Finanças','Investimentos','Taxa de referência CDI','Consultar: taxa CDI atual/histórica','cotação atual'),
'cdi_historica':('Finanças','Investimentos','Taxa de referência CDI','Consultar: taxa CDI em período anterior','cotação histórica'),
'cdi_simulacao':('Finanças','Investimentos','Rendimento vinculado ao CDI','Simular: rendimento conforme percentual do CDI','simulação/projeção'),
'credito_simulacao':('Finanças','Crédito','Simulação de crédito','Simular: empréstimo e financiamento','simulação/projeção'),
'rendimento_banco':('Finanças','Investimentos','Rendimento de conta e CDB','Simular: rendimento de aplicação em instituição financeira','simulação/projeção'),
'raiz':('Matemática','Potências e funções','Raízes e radicais','Calcular: raiz e potência','cálculo direto'),
'juros_cotacao':('Finanças','Crédito','Taxas de financiamento','Consultar: taxa de juros de financiamento','informacional'),
'igpm':('Finanças','Correção monetária','Reajuste pelo IGP-M','Calcular: reajuste pela série do IGP-M','cálculo contextual'),
'revisao_vida':('Trabalho','Aposentadoria e INSS','Revisão da vida toda','Consultar ou simular: revisão previdenciária','cálculo contextual'),
'gps_previdencia':('Trabalho','Folha e encargos','Contribuição e guia GPS','Calcular: contribuição previdenciária em atraso','cálculo contextual'),
'escada':('Construção','Escadas','Dimensionamento de escadas','Dimensionar: degraus e escadas','dimensionamento'),
'argamassa':('Construção','Argamassa e revestimento','Consumo de argamassa e reboco','Estimar: material de argamassa/reboco','estimativa de quantidade'),
'media_moda':('Matemática','Estatística e probabilidade','Média, mediana e moda','Calcular: medidas de tendência central','cálculo direto'),
'relacoes_metricas':('Matemática','Geometria','Relações métricas em triângulos','Consultar: relações métricas de triângulo retângulo','informacional'),
'decimo_terceiro':('Trabalho','Décimo terceiro','Décimo terceiro proporcional','Calcular: décimo terceiro proporcional','cálculo contextual'),
'dissidio':('Trabalho','Legislação e direitos','Dissídio e reajuste salarial','Calcular: reajuste por dissídio e vigência','cálculo contextual'),
'horas_extras':('Trabalho','Jornada e adicionais','Horas extras e DSR','Calcular: horas extras e reflexos no DSR','cálculo contextual'),
'descontos_salario':('Trabalho','Folha e encargos','Imposto retido sobre salários','Calcular: imposto e descontos salariais','cálculo contextual'),
}

def normalize(s):
    s=unicodedata.normalize('NFKD',s.casefold())
    return re.sub(r'\s+',' ',''.join(c for c in s if not unicodedata.combining(c))).strip()

def has(t,p):return re.search(p,t,re.I) is not None

def decide(original):
    t=normalize(original); r=lambda p:has(t,p)
    # Exceções de segurança em primeiro lugar: gestação cronológica sem objetivo e palavras ambíguas.
    if r(r'\b(semana|semanas)\b') and r(r'\bdias?\b') and not r(r'gesta|gravide|gestant|trabalh|jornada|salari'):return None
    if r(r'\b(kwh|quilowatt.?hora)\b') and r(r'\b(quanto vale|quanto custa|preco|valor|custo|tarifa|reais|r\$)\b'):
        return 'custo_kwh','Tarifa local e data são parâmetros; valor isolado de kWh não é calculável sem tarifa.','COM_RESSALVA'
    if r(r'\bgestant|gravide|gravida\b') and r(r'(demitid|demiss|estabilidad|direitos? da|licenca matern|funcionaria|empregada|empresa pode)'):
        return 'gestante_direitos','Assunto de direito trabalhista explícito, sem cálculo automático de elegibilidade.','COM_RESSALVA'
    if r(r'gestac|gravide|gestant|gravida') and r(r'(\bsemana|\bmes|\bdia|\btempo de gestacao)'):
        return 'gestacao','Contexto explicitamente gestacional; não equiparar semanas a mês calendário com taxa fixa.','COM_RESSALVA'
    if r(r'\bjames stewart\b') and r(r'\b(calculo|livro|pdf|edicao|volume|stewart)\b'):
        return 'material_didatico','Autor/livro explícito; não classificar como cálculo de obra.','SEM_RESSALVA'
    if r(r'\bcalendari[oa]\b') and r(r'\b(janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\b') and not r(r'gestac|gravide'):
        return 'calendario','Consulta de calendário mensal, não calculadora de dias úteis.','SEM_RESSALVA'
    if r(r'\b(carnaval|feriado)\b') and r(r'\b(data|quando|calendario|dia do|dias|feriado|202[0-9])\b') and r('carnaval'):
        return 'carnaval','Consulta de data de Carnaval, não cálculo genérico de dias úteis.','SEM_RESSALVA'
    if r(r'\b(planilha|excel|modelo|template|lista)\b') and r(r'\b(despesas?|gastos?|orcamentos?|contas pessoais|contas domesticas)\b'):
        return 'planilha','Busca por modelo, planilha ou lista de controle financeiro; não consumo energético.','SEM_RESSALVA'
    if r(r'\b(app|aplicativo|aplicacao de controle|software)\b') and r(r'\b(despesas?|gastos?|orcamentos?)\b'):
        return 'financa','Busca por aplicativo de controle financeiro, não investimento nem combustível.','SEM_RESSALVA'
    if r(r'\b(controle|dashboard|organizar|anotar)\b') and r(r'\b(despesas?|gastos?|orcamentos?)\b') and not r(r'\b(calcular|calculadora)\b'):
        return 'financa','Gestão de orçamento/despesas; não operação numérica direta.','SEM_RESSALVA'
    if r(r'\bgasolina|\bcombustivel|\balcool|\betanol') and r(r'\b(km|quilomet|litros?|consumo|gastos?|gasta|autonomia|media de)\b') and not r(r'preco hoje|cotacao|aumento do preco'):
        return 'gasolina','Cálculo de combustível depende do rendimento (km/L) e possivelmente preço por litro.','COM_RESSALVA'
    if r(r'\b(cdi|selic)\b') and r(r'\b(quanto rende|rende quanto|simulador|simular|calculadora.*rendimento|calcular rendimento)\b'):
        return 'cdi_simulacao','Simulação vinculado a índice; taxa deve ser obtida conforme data e produto.','COM_RESSALVA'
    if r(r'\bcdi\b') and r(r'\b(taxa|cotacao|valor|hoje|historico)\b') and not r(r'\b(rende|rendimento|simulador|simular|calculadora|quanto da)\b'):
        if r(r'\b(201[0-9]|202[0-5])\b'):
            return 'cdi_historica','Consulta de taxa CDI em período passado; ignorar o termo hoje se combinado a ano antigo.','COM_RESSALVA'
        return 'cdi_cotacao','Consulta da taxa CDI; depende da data de referência.','COM_RESSALVA'
    if r(r'\b(nubank|inter|banco do brasil|bb|caixa|bradesco|itau)\b') and r(r'\b(quanto rende|rende quanto|rendimento de|simulador de investimento)\b'):
        return 'rendimento_banco','Depende do produto, prazo, taxas e tributação; não assumir rendimento fixo.','COM_RESSALVA'
    if r(r'\b(credito|consignado|emprestimo|financiamento)\b') and r(r'\b(simulador|simulacao|simular|calculadora)\b'):
        return 'credito_simulacao','Intenção operacional de simular crédito, sem pressupor taxas do banco.','COM_RESSALVA'
    if r(r'\b(raiz quadrada|raiz cubica|raiz de)\b') and (r(r'\b(calculadora|calcular|calcule|conta|quanto|resultado|de +[0-9]+|[0-9]+)\b')) and not r(r'\b(pdf|livro|apostila|curso|aula)\b'):
        return 'raiz','Operação matemática explícita; não confundir número 13 com 13º salário.','SEM_RESSALVA'
    if r(r'\b(juros|taxa)\b') and r(r'\b(financiamento|imobiliario|emprestimo)\b') and not r(r'\b(calculadora|simulador|calcular|simular)\b'):
        return 'juros_cotacao','Consulta de taxa de juros de crédito, depende de banco/produto/data.','COM_RESSALVA'
    if r(r'\bigpm\b') and r(r'\b(reajuste|aluguel|corrig|calculadora|calcular)\b'):
        return 'igpm','Reajuste de aluguel/contrato depende do índice e da data-base.','COM_RESSALVA'
    if r(r'\brevisao da vida toda\b|\brevisao vida toda\b|\bcalculo da vida toda\b'):
        return 'revisao_vida','Tema previdenciário, não de energia; cálculos exigem histórico contributivo e regras vigentes.','COM_RESSALVA'
    if r(r'\bgps\b') and r(r'\b(inss|contribui|previdencia|guia|autonom|atraso|atrasado)\b'):
        return 'gps_previdencia','GPS refere-se à Guia da Previdência Social por contexto; exclui navegação por satélite.','COM_RESSALVA'
    if r(r'\bescada(s)?\b') and r(r'\b(calcula|formula|dimensiona|degrau|altura|largura|blondel|quantos)\b'):
        return 'escada','Dimensionamento de escadas requer altura total, piso/espelho e norma local.','COM_RESSALVA'
    if r(r'\b(argamassa|reboco|contrapiso)\b') and r(r'\b(calcula|quantidade|material|rendimento|saco|metro|cobert|area|consumo)\b'):
        return 'argamassa','Estimativa depende de área, espessura e rendimento por embalagem.','COM_RESSALVA'
    if r(r'\b(moda|mediana|media)\b') and r(r'\b(calcula|calculadora|calcule|quanto e|achar|conta)\b') and not r(r'\b(diferenca|conceito|oque e|o que e|explicacao)\b'):
        return 'media_moda','Operação estatística explícita; se faltam dados, solicitá-los.','COM_RESSALVA'
    if r(r'relac(ao|oes) metricas') and r(r'triangulo retangulo') and r(r'\b(definicao|quais sao|teorema|formula|relacoes)\b') and not r(r'\bcalcula|calculadora'):
        return 'relacoes_metricas','Consulta conceitual de geometria; não cálculo direto.','SEM_RESSALVA'
    if r(r'\b13(o|º)?\b|decimo terceiro') and r(r'\bproporcional|calculadora|calcular') and not r(r'\braiz|cubica'):
        return 'decimo_terceiro','Cálculo proporcional requer remuneração e meses trabalhados.','COM_RESSALVA'
    if r(r'\bdissidio\b') and r(r'\b(calcula|calculadora|proporcional|reajuste)\b'):
        return 'dissidio','Reajuste depende de convenção coletiva e data-base.','COM_RESSALVA'
    if r(r'\bdsr\b') and r(r'\b(horas extras|hora extra|calculadora|calcular)\b'):
        return 'horas_extras','Reflexos de horas extras exigem jornada, salário e períodos.','COM_RESSALVA'
    if r(r'\bimposto de renda|\birrf\b') and r(r'\b(salario|folha|holerite|desconto|calculadora)\b'):
        return 'descontos_salario','IRRF sobre folha; alíquotas e deduções variam no tempo.','COM_RESSALVA'
    return None

def readcsv(z,name):
    with z.open(name) as f:return list(csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''),delimiter=';'))
def writecsv(path, rows, cols):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)

def apply(data_root,out):
    pa=data_root/'auditoria-p2-v7-csv-integral.zip';pb=data_root/'lotes-001-a-030-p0-p1-p2-v7.zip'
    assert pa.is_file() and pb.is_file(), (pa,pb)
    with zipfile.ZipFile(pa) as z:
        fila=readcsv(z,'p2-v7-fila-geral.csv')
    base=[r for r in fila if r['prioridade']=='P3']
    assert len(base)==23965, f'P3:{len(base)}'
    families=defaultdict(list)
    for r in base: families[r['familia_id']].append(r)
    selected={k for k,v in sorted(families.items(),key=lambda x:(-len(x[1]),x[0]))[:35]}
    areas=defaultdict(list)
    for fid,rs in families.items():
        dominant=Counter(r['area'] for r in rs).most_common(1)[0][0]
        areas[dominant].append((fid,rs))
    for area,fs in areas.items():
        for fid,rs in sorted(fs,key=lambda x:(-len(x[1]),x[0]))[:8]:selected.add(fid)
    piloto=[r for r in base if r['familia_id'] in selected]
    assert len(selected)==66 and len(piloto)==2090,(len(selected),len(piloto))
    candidates={};review=[]
    for r in piloto:
        decision=decide(r['Keyword']);new_status='SEM_EVIDENCIA_PILOTO';reason='Sem evidência suficiente por regra contextual; não classificado no piloto.'
        if decision:
            key,reason,status=decision
            val=CATEGORIAS[key];new_status='PROPOSTA_'+status
            candidates[r['id_global']]={'rule':key,'reason':reason,'state':new_status,'new':val}
        review.append({'id_global':r['id_global'],'lote':r['lote'],'familia_id':r['familia_id'],'Keyword':r['Keyword'],'area_atual':r['area'],'cluster_atual':r['cluster'],'tipo_intencao_atual':r['tipo_intencao_atual'],'Avg. monthly searches':r['Avg. monthly searches'],'regra':decision[0] if decision else '', 'status':new_status,'justificativa':reason})
    out.mkdir(parents=True,exist_ok=True)
    outl=out/'lotes';outl.mkdir(exist_ok=True)
    changes={}; seen=set(); protected=0;control_count=0;total_base=0;out_of_scope=0; unaffected=0
    with zipfile.ZipFile(pb) as z:
        names=sorted(x for x in z.namelist() if x.endswith('.csv') and x.startswith('lotes/'))
        assert len(names)==30,len(names)
        for file in names:
            rows=readcsv(z,file);cols=list(rows[0]);patched=[]
            for row in rows:
                if row['tipo_registro']=='controle':control_count+=1
                else:total_base+=1
                id_=row['id_global']
                if id_ in candidates:
                    assert row['tipo_registro']=='base' and id_ not in seen
                    seen.add(id_); info=candidates[id_]; old=row.copy();val=info['new']
                    update={'area_principal':val[0],'cluster':val[1],'subcluster':val[2],
                            'intencao_principal':val[3],'tipo_intencao':val[4],
                            'confianca':'média','revisao_manual':'sim','justificativa_curta':'P3 v1 piloto ['+info['rule']+']: '+info['reason']}
                    for k,v in update.items():row[k]=v
                    diffs={k:{'antes':old[k],'depois':row[k]} for k in cols if row[k]!=old[k]}
                    if diffs:
                        assert set(diffs)<=ALLOWED
                        changes[id_]={'id_global':id_,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra':info['rule'],'status':info['state'],'justificativa':info['reason'],'antes_json':json.dumps({k:x['antes'] for k,x in diffs.items()},ensure_ascii=False,sort_keys=True),'depois_json':json.dumps({k:x['depois'] for k,x in diffs.items()},ensure_ascii=False,sort_keys=True),'campos_alterados':', '.join(diffs)}
                    else:unaffected+=1
                patched.append(row)
            writecsv(outl/Path(file).name.replace('-v7.csv','-p3-v1.csv'),patched,cols)
    assert total_base==294905 and control_count==2190 and len(seen)==len(candidates), (total_base,control_count,len(seen),len(candidates))
    patches=sorted(changes.values(),key=lambda x:int(x['id_global']))
    for r in review:
        if r['id_global'] in candidates:
            r['status']=candidates[r['id_global']]['state'] if r['id_global'] in changes else 'JA_ALINHADO'
            r['houve_patch']='sim' if r['id_global'] in changes else 'não'
        else:r['houve_patch']='não'
    writecsv(out/'p3-v1-piloto-2090-decisoes.csv',review,list(review[0]))
    writecsv(out/'p3-v1-patches.csv',patches,list(patches[0]))
    pend=[r for r in review if r['status']=='SEM_EVIDENCIA_PILOTO']
    writecsv(out/'p3-v1-piloto-sem-evidencia.csv',pend,list(review[0]))
    stats=Counter(x['status'] for x in review)
    byrule=Counter(x['regra'] for x in patches)
    summary={'versao':'P3 v1 - piloto','P3_universo':len(base),'familias_P3':len(families),
      'familias_piloto':len(selected),'keywords_piloto':len(piloto),
      'regras_detectadas':len(candidates),'reclassificadas_com_patch':len(patches),
      'ja_alinhadas_sem_patch':unaffected,'sem_evidencia':len(pend),
      'P3_nao_selecionadas':len(base)-len(piloto),'familias_com_patches':len(set(x['familia_id'] for x in patches)),
      'status':dict(stats),'regras_de_patches':dict(byrule),'registros_base':total_base,'controles':control_count,'lotes':len(names),
      'observacao':'Piloto de regras, não aprovação editorial. Outros P3 e todos P0/P1/P2 preservados.'}
    (out/'p3-v1-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--origem',required=True,type=Path);p.add_argument('--saida',required=True,type=Path);a=p.parse_args();print(json.dumps(apply(a.origem,a.saida),ensure_ascii=False,indent=2))
