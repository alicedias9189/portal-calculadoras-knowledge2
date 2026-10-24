#!/usr/bin/env python3
# coding: utf-8
"""P3 v1.7: auditoria estratificada das 152 decisões novas da P3 v1.6.
Não expande P3, não altera P0/P1/P2, nem registros P3 fora dos 152 IDs.
Uso: python3 auditar_p3_v17.py --fonte <dir com 08-Entregas/P3-v1.6> --saida <dir>
Somente Python stdlib.
"""
import argparse, csv, io, json, random, collections, zipfile, hashlib
from pathlib import Path

CAN=('area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta')
TRACK=['status_p3_v1_7','regra_p3_v1_7','justificativa_p3_v1_7','area_final_p3_v1_7','cluster_final_p3_v1_7','subcluster_final_p3_v1_7','tipo_intencao_final_p3_v1_7','classificacao_alterada_p3_v1_7']

# Revisões explícitas por ID: não há inferência de alíquotas, taxa vigente ou base de dados.
FIXES={
 '3627':({'subcluster':'INSS sobre 13º salário','intencao_principal':'Calcular INSS incidente sobre 13º salário com competência e valores informados'},'A menção a 13º salário exige tratamento previdenciário próprio; não equiparar automaticamente ao salário mensal.'),
 '41022':({'tipo_intencao':'cálculo contextual','intencao_principal':'Calcular alíquota de INSS mediante base, regime e competência informados'},'O verbo calcular indica operação, mas faltam base e competência; não é apenas consulta de tabela.'),
 '80190':({'subcluster':'Descontos de INSS e IRRF','intencao_principal':'Consultar procedimento para calcular INSS e IRRF em folha'},'A consulta cita dois descontos distintos; a explicação precisa contemplar ambos.'),
 '131479':({'subcluster':'Descontos de INSS e IRRF','intencao_principal':'Consultar descontos de INSS e IRRF da competência de 2022'},'Dois tributos e ano histórico explícitos; não reduzir a apenas INSS.'),
 '132132':({'subcluster':'Descontos de INSS e IRRF','intencao_principal':'Consultar descontos de INSS e IRRF da competência de 2021'},'Dois tributos e ano histórico explícitos; não reduzir a apenas INSS.'),
 '193057':({'subcluster':'Destino da contribuição previdenciária','intencao_principal':'Entender a destinação dos descontos previdenciários'},'Pergunta sobre destino da contribuição e não cálculo de desconto.'),
 '78806':({'subcluster':'Como calcular juros do financiamento imobiliário','intencao_principal':'Consultar o método de cálculo dos juros do financiamento imobiliário'},'Como calcular pergunta pelo método, não por comparação de taxas de mercado.'),
 '80499':({'subcluster':'Como calcular juros do financiamento imobiliário','intencao_principal':'Consultar o método de cálculo dos juros do financiamento imobiliário'},'Como calcular pergunta pelo método, não por comparação de taxas de mercado.'),
 '184077':({'subcluster':'Comparação de financiamentos imobiliários','intencao_principal':'Comparar alternativas de financiamento para compra de casa'},'A palavra melhor inclui condições além da taxa nominal de juros.'),
 '273446':({'subcluster':'Custo Efetivo Total (CET) imobiliário','intencao_principal':'Consultar custo efetivo total do financiamento, incluindo encargos'},'CET não equivale à taxa nominal de juros.'),
 '276500':({'subcluster':'Selic e financiamento imobiliário','intencao_principal':'Consultar relação entre Selic e financiamento imobiliário'},'Selic não é a taxa contratual do financiamento; sem inferir valor atual.'),
 '280108':({'subcluster':'Tipos de juros em financiamento imobiliário','intencao_principal':'Entender modalidades de juros no financiamento imobiliário'},'Busca sobre tipos de juros, não comparação de taxas de um banco.'),
 '42443':({'tipo_intencao':'cálculo contextual','intencao_principal':'Calcular variância e desvio padrão após fornecer a amostra ou população'},'Para calcular variância e desvio padrão é necessário fornecer os dados.'),
 '48454':({'tipo_intencao':'cálculo contextual','intencao_principal':'Calcular variância e desvio padrão após fornecer a amostra ou população'},'Para calcular variância e desvio padrão é necessário fornecer os dados.'),
 '34643':({'tipo_intencao':'conversão contextual','intencao_principal':'Usar ferramenta de conversão de numeração romana com sentido selecionável'},'É um conversor; a consulta não fixa o sentido da transformação.'),
 '13149':({'area_principal':'Fora de escopo','cluster':'Consulta ambígua','subcluster':'Abertura de conta sem serviço identificado','tipo_intencao':'ambígua/revisão','intencao_principal':'Identificar qual serviço oferece a conta antes de classificar','confianca':'baixa'},'Abrir conta pelo site não identifica um banco nem o tipo de conta; não classificar como serviço bancário sem contexto.'),
 '16214':({'subcluster':'Alíquota de INSS acima do teto','intencao_principal':'Consultar limite e regra de incidência previdenciária acima do teto'},'Acima do teto é uma dúvida sobre limite de contribuição, não alíquota aplicada irrestritamente.'),
}
RULE_NOTES={
'inss_desconto_folha':'Revisar regime, ano, base e a distinção entre tabela informativa e cálculo em folha.',
'taxa_financiamento_imobiliario':'Distinguir taxa nominal, CET, Selic, comparação de ofertas e método de cálculo; não inferir taxas atuais.',
'variancia_desvio_padrao':'Separar consulta didática de cálculo com dados; diferenciar amostra e população.',
'abertura_conta_bancaria':'Verificar se a conta é bancária e se a busca indica ação ou tutorial.',
'arranjo_combinacao':'Material didático/teoria de combinatória; não tratar como operação numérica explícita.',
'referencia_numerais_romanos':'Distinguir tabela estática de conversor interativo e manter direção em aberto.',
'raiz_cubica_valor_explicito':'Operando numérico explícito; cálculo direto verificável.'
}

def readcsv(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def parsecsv(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def encode(rows,cols):
 buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=cols,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows);return ('\ufeff'+buf.getvalue()).encode('utf-8')
def save(path,rows,cols):path.write_bytes(encode(rows,cols))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args()
 src=a.fonte/'08-Entregas/P3-v1.6';out=a.saida;out.mkdir(parents=True,exist_ok=True)
 decisions=readcsv(src/'p3-v1.6-decisoes-por-id.csv');original={r['id_global']:r for r in decisions if r['origem']=='EXPANSAO_V16'}
 assert len(original)==152 and len(FIXES)==17 and set(FIXES)<=set(original),(len(original),len(FIXES))
 # Uma amostra estratificada controlada de 100+, forçando inclusão das exceções.
 byrule=collections.defaultdict(list)
 for r in original.values():byrule[r['regra']].append(r['id_global'])
 quotas={'inss_desconto_folha':32,'taxa_financiamento_imobiliario':32,'variancia_desvio_padrao':15,'abertura_conta_bancaria':13,'arranjo_combinacao':5,'referencia_numerais_romanos':5,'raiz_cubica_valor_explicito':1}
 rng=random.Random(1717);chosen=set(FIXES)
 for rule,ids in byrule.items():
  current=set(ids)&chosen;goal=min(len(ids),quotas[rule]);extra=sorted(set(ids)-chosen,key=int);chosen.update(rng.sample(extra,min(max(0,goal-len(current)),len(extra))))
 # Evita excluir mudanças quando amostras por regra já atingirem cotas.
 reviewed=[];byid={};patches=[];test_rows=[];nbase=ncontrol=0
 with zipfile.ZipFile(src/'lotes-001-a-030-p3-v1.6.zip') as zi,zipfile.ZipFile(out/'lotes-001-a-030-p3-v1.7.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as zo:
  names=sorted(zi.namelist());assert len(names)==30
  for name in names:
   rows=parsecsv(zi.read(name));cols=list(rows[0]);mods=0;nb=nc=0
   for r in rows:
    if r['tipo_registro']!='base':ncontrol+=1;nc+=1;continue
    nbase+=1;nb+=1;rid=r['id_global']
    if rid not in original:continue
    origin=original[rid];assert origin['Keyword']==r['Keyword']
    changes,why=FIXES.get(rid,({},''))
    if changes:
     before=dict(r)
     r.update(changes)
     r['revisao_manual']='sim'
     r['justificativa_curta']='P3 v1.7 — QA semântico: '+why
     if rid!='13149':r['confianca']='média'
     diff=[c for c in CAN if before[c]!=r[c]]
     assert diff and any(c in ('area_principal','cluster','subcluster','intencao_principal','tipo_intencao') for c in diff)
     mods+=1
     status='REABERTA_POR_AMBIGUIDADE' if rid=='13149' else 'CORRIGIDA'
     byid[rid]=(status,'qa_semantica_v17',why,{k:r[k] for k in CAN})
     patches.append({'id_global':rid,'lote':r['lote_id'],'familia_id':r['familia_id'],'Keyword':r['Keyword'],'status_qa':status,'campos_alterados':','.join(diff),'antes_json':json.dumps({k:before[k] for k in diff},ensure_ascii=False),'depois_json':json.dumps({k:r[k] for k in diff},ensure_ascii=False)})
    else:
     status='MANTIDA_COM_RESSALVA' if origin['regra'] in ('inss_desconto_folha','taxa_financiamento_imobiliario','abertura_conta_bancaria') else 'MANTIDA_SEM_ERRO_EVIDENTE'
     why=RULE_NOTES[origin['regra']]
    reviewed.append({'id_global':rid,'lote':r['lote_id'],'familia_id':r['familia_id'],'Keyword':r['Keyword'],'regra_v16':origin['regra'],'na_amostra_estratificada':'sim' if rid in chosen else 'nao','parecer_v17':status,'nota_critica':why,'area_v16':origin['area_depois'],'area_v17':r['area_principal'],'cluster_v17':r['cluster'],'subcluster_v17':r['subcluster'],'tipo_v16':origin['tipo_depois'],'tipo_v17':r['tipo_intencao'],'revisao_editorial_final':'nao'})
   newname=name.replace('v1.6','v1.7');zo.writestr(newname,encode(rows,cols))
   test_rows.append({'lote_origem':name,'lote_v17':newname,'registros_base':nb,'controles':nc,'patches':mods,'status':'AGUARDANDO_REGRESSAO_INDEPENDENTE'})
 assert nbase==294905 and ncontrol==2190 and len(reviewed)==152 and len(patches)==len(FIXES)==sum(int(x['patches']) for x in test_rows)
 for file in ['p3-v1.6-fila-23965.csv','fila-geral-p0-p1-p2-p3-v1.6.csv']:
  inputfile=src/file;outfile=out/file.replace('v1.6','v1.7')
  with inputfile.open(encoding='utf-8-sig',newline='') as inf,outfile.open('w',encoding='utf-8-sig',newline='') as outf:
   rr=csv.DictReader(inf,delimiter=';');cols=list(rr.fieldnames);assert not set(TRACK)&set(cols)
   wr=csv.DictWriter(outf,fieldnames=cols+TRACK,delimiter=';',lineterminator='\n');wr.writeheader()
   for r in rr:
    r.update(dict.fromkeys(TRACK,''));rid=r['id_global']
    if rid in byid:
     status,regra,why,full=byid[rid]
     r.update(dict(zip(TRACK,[status,regra,why,full['area_principal'],full['cluster'],full['subcluster'],full['tipo_intencao'],'sim'])))
    wr.writerow(r)
 reviewed.sort(key=lambda r:int(r['id_global']));patches.sort(key=lambda r:int(r['id_global']))
 save(out/'p3-v1.7-revisao-152.csv',reviewed,list(reviewed[0]));save(out/'p3-v1.7-amostra-estratificada.csv',[r for r in reviewed if r['na_amostra_estratificada']=='sim'],list(reviewed[0]));save(out/'p3-v1.7-patches.csv',patches,list(patches[0]));save(out/'p3-v1.7-regressao-30-lotes.csv',test_rows,list(test_rows[0]))
 from collections import Counter
 summ={'etapa':'P3 v1.7 — revisão crítica das 152 novas decisões P3 v1.6','universo_auditado':152,'amostra_estratificada':len(chosen),'por_regra':dict(Counter(r['regra_v16'] for r in reviewed)),'por_regra_amostra':dict(Counter(r['regra_v16'] for r in reviewed if r['na_amostra_estratificada']=='sim')),'correcoes':len(patches),'ambiguidades_reabertas':1,'mantidas':152-len(patches),'p3_fora_dos_pilotos':20755,'p2_pendencias_preservadas':4660,'lotes':30,'base':nbase,'controles':ncontrol,'limites':'Revisão por contexto sem homologação editorial integral; não consultar nem preencher taxa atual, alíquota histórica ou CET bancário sem fonte.'}
 (out/'p3-v1.7-resumo.json').write_text(json.dumps(summ,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summ,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
