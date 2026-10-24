#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v5.2 — expansão de 75 IDs fechados sobre snapshot v5.1.
Rodar na raiz do pacote: python 07-Scripts/P3/auditar_p3_v52.py
As linhas/colunas históricas das filas são invariáveis. Classificações técnicas
são propostas; não constituem homologação editorial humana.
"""
from pathlib import Path
from collections import Counter
import csv, io, zipfile, json, re, shutil
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v5.2'
SRC=OUT/'FONTES-REPRODUCAO/08-Entregas/P3-v5.1'
RULES={
 'GESTACAO_E_CONVERSAO_TEMPORAL':[7111,4447,4476,72324,72327,4473,37093,39856,39861,39862,47574,47583,76247,83462,5932,8450,8921,9464,165270,7610],
 'JUROS_E_CONTROLE_CARTAO':[157569,175314,175918,175919,175920,175923,267849,98272,174320,174617,44430,98419,204061,202524,202797],
 'SALARIO_BRUTO_E_ADICIONAIS':[195785,254125,254160,254173,255409,254149,12164,155122],
 'JORNADA_SEMANAL':[7232,167314,167320,167391,52269,74391,7793,11045],
 'ESTATISTICA_INTENCAO':[186977,182412,186979,189381,189389,189391,189393,189396,194610,194617,159146,159229],
 'BTU_TERMICO_VS_ELETRICO':[19956,19957,20016,206329,207405,207408,207413,207417,270768,239158],
 'ARREDONDAMENTO_DE_NÚMEROS':[21237,148231],
}
PLAN={str(v):k for k,arr in RULES.items() for v in arr}
assert len(PLAN)==75 and sum(map(len,RULES.values()))==75
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_2','regra_p3_v5_2','justificativa_p3_v5_2','area_final_p3_v5_2','cluster_final_p3_v5_2','subcluster_final_p3_v5_2','tipo_intencao_final_p3_v5_2','classificacao_alterada_p3_v5_2']
PREFIX={'informacional':'Consultar ou entender: ','busca de ferramenta':'Encontrar ferramenta: ','cálculo contextual':'Calcular com parâmetros: '}
def read(path):
 with path.open('r',encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def write(path,items,cols=None):
 path.parent.mkdir(parents=True,exist_ok=True)
 if cols is None:cols=list(items[0])
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(items)
def classify(old,rule):
 kw=old['Keyword']; k=kw.casefold(); conf='média'
 if rule=='GESTACAO_E_CONVERSAO_TEMPORAL':
  gest=bool(re.search(r'gesta[çc][aã]o|gestacional|gravidez|gr[aá]vida',k))
  area='Saúde' if gest else 'Conversores'
  cluster='Gestação e idade gestacional' if gest else 'Conversões de tempo'
  sub='Semanas e meses na idade gestacional' if gest else 'Semanas, meses e dias (conversão contextual)'
  typ='busca de ferramenta' if 'calculadora' in k else 'informacional' if ('como calcular' in k or 'tabela' in k or k in {'17 semanas meses','calculadora semanas meses'}) else 'cálculo contextual' if any(ch.isdigit() for ch in k) else 'informacional'
  if 'calculadora' in k:typ='busca de ferramenta'
  conf='baixa' if not gest else 'média'
  note=('Termos explícitos de gravidez/gestação justificam idade gestacional; converter semanas e dias sem fixar universalmente meses gestacionais. '
        if gest else 'A busca não menciona gravidez; não pressupor contexto gestacional a partir de semanas e meses. ')
  note+='Mês civil tem duração variável; equivalências em meses são aproximadas quando não há datas de referência.'
 elif rule=='JUROS_E_CONTROLE_CARTAO':
  area='Finanças'
  if 'planilha' in k:
   cluster,sub,typ='Gestão financeira','Planilhas de controle de cartão de crédito','busca de ferramenta'
   note='Busca por planilha/controle, não por rentabilidade de investimento nem por cálculo numérico com dados fornecidos.'
  elif 'juros' in k and any(b in k for b in ('banco do brasil','bradesco','caixa','santander')):
   cluster,sub,typ='Dívidas e cartões','Juros de cartão de crédito por instituição','informacional'
   note='Consulta a taxas/condições do emissor, sem números para simulação; não classificar como CDB, investimento nem juros compostos automaticamente.'
  elif 'simula' in k:
   cluster,sub,typ='Dívidas e cartões','Simulador de parcelamento do cartão','busca de ferramenta'
   note='Consulta sobre simulação de parcelamento; a taxa, parcelas e total não foram informados, logo não produzir parcelas fictícias.'
  elif 'tem juros' in k:
   cluster,sub,typ='Dívidas e cartões','Incidência de juros em compras parceladas','informacional'
   note='Pergunta se compras parceladas têm juros; depende de contrato, modalidade e emissor, não é rendimento de CDB.'
  elif 'fatura' in k and 'calcular' in k:
   cluster,sub,typ='Dívidas e cartões','Cálculo de juros da fatura','cálculo contextual'
   note='Pede cálculo de encargos de fatura, que exige saldo, datas, taxas e composição; não assumir taxa ou regime.'
  elif 'fatura' in k:
   cluster,sub,typ='Dívidas e cartões','Financiamento ou parcelamento de fatura','informacional'
   note='Financiamento de fatura é crédito rotativo/parcelamento conforme contrato; consulta sem valores nem taxas explícitas.'
  else:
   cluster,sub,typ='Dívidas e cartões','Juros em compras e parcelamento de cartão','informacional'
   note='Juros de parcelamento de cartão não são investimento nem necessariamente juros compostos com taxa conhecida; faltam contrato, taxa e prazos.'
 elif rule=='SALARIO_BRUTO_E_ADICIONAIS':
  area='Trabalho'
  if 'insalubridade' in k:
   cluster,sub,typ='Jornada e adicionais','Base de cálculo do adicional de insalubridade','informacional'
   note='Consulta sobre base de incidência do adicional, dependente das regras aplicáveis; não é operação geométrica nem fórmula com números.'
  else:
   cluster,sub='Remuneração','Salário base, bruto e líquido'
   typ='busca de ferramenta' if 'ferramenta' in k else 'informacional'
   note='Busca sobre remuneração bruta, base ou descontos; não é pintura, geometria, rendimento financeiro nem rescisão por si só. Sem folha, competência e descontos não há valor líquido.'
  if '2022' in k:note+=' A referência a 2022 não autoriza aplicar automaticamente regras atuais.'
 elif rule=='JORNADA_SEMANAL':
  area,cluster='Trabalho','Jornada e adicionais'
  sub='Distribuição de horas semanais em dias' if 'por dia' in k or 'diarias' in k else 'Cálculo e organização da jornada semanal'
  typ='informacional' if ('como calcular' in k or k in {'30 horas semanal','horas semanal','horas trabalho semanal','horas semanal trabalhadas','8 horas diarias e 44 semanal'}) else 'cálculo contextual'
  note='Jornada de trabalho semanal não é intervalo entre datas. Para dividir em dias, informar número de dias e eventual escala; não deduzir horas diárias por padrão.'
 elif rule=='ESTATISTICA_INTENCAO':
  area,cluster,typ='Matemática','Estatística e probabilidade','informacional'
  sub='Fórmula e interpretação da moda' if 'formula' in k or 'fórmula' in k else 'Conceitos de média, mediana e moda'
  note='O texto não fornece amostra de valores. Lista de conceitos ou pedido de fórmula representa estudo/método; diferenciar média, mediana e moda, sem calcular resultados fictícios.'
 elif rule=='BTU_TERMICO_VS_ELETRICO':
  area='Conversores' if 'tabela convers' in k else 'Energia'
  cluster='Energia, potência e calor' if area=='Conversores' else 'Climatização e potência'
  sub='Conversão BTU/h em W térmicos' if 'tabela convers' in k else 'Potência térmica versus consumo elétrico de ar-condicionado'
  typ='informacional' if 'tabela' in k else 'cálculo contextual' if 'consome' in k or 'gasta' in k else 'informacional'
  note='BTU/h é taxa de transferência de calor e pode ser expressa em W térmicos (~0,293071 W por BTU/h). Isso NÃO determina os W elétricos consumidos: requer COP/EER, modelo e condições. Não supor que potência solicitada seja consumo.'
 elif rule=='ARREDONDAMENTO_DE_NÚMEROS':
  area,cluster,sub='Matemática','Números e operações','Arredondamento de números e casas decimais'
  typ='busca de ferramenta' if 'online' in k else 'informacional'
  note='Arredondamento numérico é aritmética; não se relaciona a dias úteis nem operações com datas. No Excel, a consulta indica procedimento de arredondamento, sem valor numérico fornecido.'
 else:raise AssertionError(rule)
 assert typ in PREFIX
 new={'area_principal':area,'cluster':cluster,'subcluster':sub,'intencao_principal':PREFIX[typ]+sub,
      'tipo_intencao':typ,'dominio_ou_grandeza':sub,'confianca':conf,'revisao_manual':'sim',
      'justificativa_curta':note+' Evidência textual: «'+kw+'». (P3 v5.2: proposta técnica, homologação editorial pendente.)'}
 return new,note

def main():
 q,qcols=read(SRC/'p3-v5.1-fila-23965.csv');g,gcols=read(SRC/'fila-geral-p0-p1-p2-p3-v5.1.csv')
 assert len(q)==23965 and len(g)==52046 and qcols==gcols and len(qcols)==390
 qi={a['id_global']:a for a in q};gi={a['id_global']:a for a in g}
 sts=[x for x in qcols if x.startswith('status_p3_v') and x!='status_p3_v1']
 eligible={x['id_global'] for x in q if x['prioridade']=='P3' and x['status_p3_v1']=='FORA_DO_PILOTO' and not any(x[s] for s in sts)}
 assert len(eligible)==19637, len(eligible)
 assert set(PLAN)<=eligible,sorted(set(PLAN)-eligible)
 assert all(qi[r]['familia_id']==gi[r]['familia_id'] and qi[r]['Keyword']==gi[r]['Keyword'] for r in PLAN)
 prior,_=read(SRC/'p3-v5.1-pareceres-75.csv');priorids={x['id_global'] for x in prior}
 assert len(priorids)==75 and set(PLAN).isdisjoint(priorids)
 backlog,_=read(SRC/'backlog-global-98-com-parecer-v27.csv')
 assert len(backlog)==98 and set(PLAN).isdisjoint({x['id_global'] for x in backlog})
 OUT.mkdir(parents=True,exist_ok=True)
 decisions=[];patches=[];results={};stats=[];base_total=ctrl_total=0
 with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v5.1.zip') as zin,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v5.2.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  assert len(zin.namelist())==30 and zin.testzip() is None
  for srcname in zin.namelist():
   rdr=csv.DictReader(io.StringIO(zin.read(srcname).decode('utf-8-sig')),delimiter=';');fields=list(rdr.fieldnames)
   tmp=io.StringIO();wr=csv.DictWriter(tmp,fieldnames=fields,delimiter=';',lineterminator='\n');wr.writeheader()
   bc=cc=cn=0
   for old in rdr:
    rid=old['id_global'];bc+=old['tipo_registro']=='base';cc+=old['tipo_registro']!='base'
    after=old
    if rid in PLAN:
     assert rid not in results and old['tipo_registro']=='base'
     assert old['Keyword']==qi[rid]['Keyword'] and old['familia_id']==qi[rid]['familia_id'] and old['lote_id']=='L'+qi[rid]['lote'].zfill(3)
     newvals,note=classify(old,PLAN[rid]);after=old.copy();after.update(newvals)
     delta=[c for c in fields if old[c]!=after[c]]
     assert delta and set(delta)<=EDIT,(rid,delta)
     results[rid]=after.copy();cn+=1
     patches.append(dict(id_global=rid,lote=srcname.replace('v5.1','v5.2'),familia_id=old['familia_id'],Keyword=old['Keyword'],regra=PLAN[rid],campos_modificados=','.join(delta),antes_json=json.dumps({c:old[c] for c in delta},ensure_ascii=False,sort_keys=True),depois_json=json.dumps({c:after[c] for c in delta},ensure_ascii=False,sort_keys=True)))
     decisions.append(dict(id_global=rid,lote_id=old['lote_id'],familia_id=old['familia_id'],Keyword=old['Keyword'],regra=PLAN[rid],parecer='CLASSIFICADO_COM_RESSALVA',justificativa_individual=note,area_anterior=old['area_principal'],area_nova=after['area_principal'],cluster_anterior=old['cluster'],cluster_novo=after['cluster'],subcluster_anterior=old['subcluster'],subcluster_novo=after['subcluster'],tipo_anterior=old['tipo_intencao'],tipo_novo=after['tipo_intencao'],campos_modificados=','.join(delta),homologacao_editorial='PENDENTE'))
    wr.writerow(after)
   zout.writestr(srcname.replace('v5.1','v5.2'),('\ufeff'+tmp.getvalue()).encode('utf-8'))
   stats.append(dict(lote=srcname.replace('v5.1','v5.2'),bases=bc,controles=cc,patches_aplicados=cn,status='PASSOU'))
   base_total+=bc;ctrl_total+=cc
 assert len(results)==len(decisions)==len(patches)==75
 assert base_total==294905 and ctrl_total==2190
 for srcname,target,expected in [('p3-v5.1-fila-23965.csv','p3-v5.2-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.1.csv','fila-geral-p0-p1-p2-p3-v5.2.csv',52046)]:
  seen=set();n=0
  with (SRC/srcname).open(encoding='utf-8-sig',newline='') as fin,(OUT/target).open('w',encoding='utf-8-sig',newline='') as fout:
   rdr=csv.DictReader(fin,delimiter=';');oldfields=list(rdr.fieldnames)
   assert oldfields==qcols and not set(TRACE)&set(oldfields)
   wr=csv.DictWriter(fout,fieldnames=oldfields+TRACE,delimiter=';',lineterminator='\n');wr.writeheader()
   for old in rdr:
    rid=old['id_global'];new=old.copy();extra=dict.fromkeys(TRACE,'')
    if rid in PLAN:
     assert rid not in seen;seen.add(rid)
     x=results[rid]
     extra.update(status_p3_v5_2='TRATADO',regra_p3_v5_2=PLAN[rid],justificativa_p3_v5_2=x['justificativa_curta'],area_final_p3_v5_2=x['area_principal'],cluster_final_p3_v5_2=x['cluster'],subcluster_final_p3_v5_2=x['subcluster'],tipo_intencao_final_p3_v5_2=x['tipo_intencao'],classificacao_alterada_p3_v5_2='sim')
    new.update(extra);wr.writerow(new);n+=1
  assert seen==set(PLAN) and n==expected
 shutil.copyfile(SRC/'backlog-global-98-com-parecer-v27.csv',OUT/'backlog-global-98-com-parecer-v27.csv')
 decisions.sort(key=lambda x:int(x['id_global']));patches.sort(key=lambda x:int(x['id_global']))
 write(OUT/'p3-v5.2-decisoes-75.csv',decisions);write(OUT/'p3-v5.2-patches-75.csv',patches)
 write(OUT/'p3-v5.2-plano-por-id.csv',[dict(id_global=x['id_global'],Keyword=x['Keyword'],familia_id=x['familia_id'],lote_id=x['lote_id'],regra=x['regra'],status_origem=qi[x['id_global']]['status_p3_v1'],status_v5_2='TRATADO',justificativa=x['justificativa_individual']) for x in decisions])
 write(OUT/'p3-v5.2-regressao-30-lotes.csv',stats)
 qa=[dict(regra=k,registros=len(arr),familias=len({x['familia_id'] for x in decisions if x['regra']==k}),status='PROPOSTO_COM_RESSALVA',homologacao_editorial='PENDENTE') for k,arr in RULES.items()]
 write(OUT/'p3-v5.2-qa-por-grupo.csv',qa)
 summary=dict(versao='P3 v5.2',fonte='P3 v5.1',novas_classificacoes=75,familias=len({x['familia_id'] for x in decisions}),grupos=len(RULES),por_grupo=dict(Counter(x['regra'] for x in decisions)),elegiveis_antes=len(eligible),elegiveis_depois=len(eligible)-75,p2_pendentes_preservados=4660,backlog_global_preservado=98,lotes=30,registros_base=base_total,controles=ctrl_total,linhas_fila_p3=23965,linhas_fila_geral=52046,colunas_historicas_preservadas_por_fila=390,novas_colunas_rastreio=8,homologacao_editorial='PENDENTE',status='AUDITOR_PASSOU')
 (OUT/'p3-v5.2-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()