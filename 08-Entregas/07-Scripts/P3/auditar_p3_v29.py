#!/usr/bin/env python3
# coding: utf-8
"""P3 v2.9: Revisão crítica individual das 66 decisões introduzidas na P3 v2.8.
Dependências: somente Python 3.10+ stdlib. Não altera arquivos-fonte.
Uso a partir da raiz do pacote: python 07-Scripts/P3/auditar_p3_v29.py
Pacote contém fontes em 08-Entregas/P3-v2.9/FONTES-REPRODUCAO/08-Entregas/P3-v2.8.
"""
import csv, io, json, zipfile, hashlib, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2] if '07-Scripts' in str(Path(__file__).resolve()) else Path(__file__).resolve().parent/'package'
SOURCE=ROOT/'08-Entregas/P3-v2.9/FONTES-REPRODUCAO/08-Entregas/P3-v2.8'
OUT=ROOT/'08-Entregas/P3-v2.9'; OUT.mkdir(parents=True,exist_ok=True)
BASE='lotes-001-a-030-p3-v2.8.zip'
WRITE={'area_principal','cluster','subcluster','dominio_ou_grandeza','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta'}
P3_NEW=['status_p3_v2_9','parecer_p3_v2_9','nota_qa_p3_v2_9','area_final_p3_v2_9','cluster_final_p3_v2_9','subcluster_final_p3_v2_9','tipo_intencao_final_p3_v2_9','classificacao_alterada_p3_v2_9']
FIXES={
 '47729':{
  'subcluster':'Cálculo da taxa implícita de financiamento de veículos',
  'intencao_principal':'Calcular com contexto: Taxa implícita de financiamento de veículos',
  'justificativa_curta':'A busca pede calcular a taxa implícita de um financiamento de veículo; depende de principal, parcelas, prazos e custos. Não é apenas consulta de taxa anunciada. (Revisão P3 v2.9; homologação editorial pendente).',
 },
 '78698':{
  'subcluster':'Método de cálculo de juros do financiamento de veículos',
  'intencao_principal':'Consultar explicação: Método de cálculo dos juros de financiamento de veículos',
  'justificativa_curta':'A pergunta "como calcular" procura explicação do método; não contém valores para cálculo imediato nem consulta uma taxa anunciada. (Revisão P3 v2.9; homologação editorial pendente).',
 }
}

def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  dr=csv.DictReader(f,delimiter=';'); return list(dr),list(dr.fieldnames)
def writecsv(path,rows,fields):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
def fromzip(z,name):
 txt=z.read(name).decode('utf-8-sig')
 dr=csv.DictReader(io.StringIO(txt),delimiter=';');return list(dr),list(dr.fieldnames)
def tozip(rows,fields):
 b=io.StringIO();w=csv.DictWriter(b,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
 return ('\ufeff'+b.getvalue()).encode('utf-8')

def qa_note(dec):
 k=dec['Keyword'].lower();rule=dec['regra']
 if dec['id_global']=='47729':return ('CORRIGIDO','Taxa a CALCULAR a partir das condições financeiras, distinta de uma taxa anunciada. Faltam capital, parcelas e prazo.')
 if dec['id_global']=='78698':return ('CORRIGIDO','Pedido de EXPLICAÇÃO do cálculo de juros, sem parâmetros para calcular e sem pedido de taxa anunciada.')
 if rule=='P3V28_TAXAS_VEICULOS':
  if 'tabela' in k or 'banco central' in k or ' bc' in k:
   note='Consulta a tabela ou fonte de taxas, não simulação de parcela; banco, modalidade, data e taxa devem vir da fonte. Sigla BC isolada não identifica necessariamente um serviço específico.'
  elif any(w in k for w in ['bv financeira','panamericano']):
   note='Taxa associada a instituição citada: informação dependente de modalidade, perfil, data e contrato. Nome da instituição não transforma busca informacional em navegação automática.'
  elif any(w in k for w in ['melhor','mais baixa','menor','bancos']):
   note='Comparação informacional entre taxas: não indicar menor taxa real ou ranking sem dados de instituições e período. CET pode diferir da taxa nominal.'
  elif any(w in k for w in ['hoje','atual','2022']):
   note='Taxa temporal (atual ou histórica) informacional. Período explícito deve ser preservado, e nenhuma taxa deve ser inferida.'
  elif any(w in k for w in ['média','media','medio']):
   note='Pede estatística/resumo de juros de financiamento, não cálculo da prestação. Fonte, ano e amostra não estão presentes.'
  else:
   note='Consulta sobre taxa/juros de financiamento de veículo, sem principal, prazo ou valores de parcelas. Não simular nem informar taxas concretas.'
  return ('MANTIDO_COM_RESSALVA',note)
 if rule=='P3V28_INSS_OBRA':
  return ('MANTIDO_COM_RESSALVA','INSS ligado à obra/construção civil, não contribuição em folha genérica. Recolhimento, regularização e alíquota dependem de regime, período e dados da obra; não presumir valor.')
 if rule=='P3V28_BASES_NUMERICAS':
  return ('MANTIDO_COM_RESSALVA','Conversão entre bases de representação; sem número fornecido, não calcular resultado. "Com vírgula" pode requerer parte fracionária; direção só onde textual.')
 if rule=='P3V28_CELSIUS_FAHRENHEIT':
  return ('MANTIDO_COM_RESSALVA','Fahrenheit e Celsius explícitos, mas "x" não fixa direção. Não preencher unidade de origem/destino sem evidência.')
 if rule=='P3V28_POTENCIA_ENERGIA':
  return ('MANTIDO_COM_RESSALVA','Potência (W) e energia (kWh) são grandezas distintas: operação exige duração; não rotular como conversão direta de unidades.')
 if rule=='P3V28_TEMPO_VIAGEM':
  return ('MANTIDO_COM_RESSALVA','Duração de viagem depende de distância e velocidade, não informadas na palavra-chave; cálculo contextual, não diferença entre datas.')
 if rule=='P3V28_DESVIO_PADRAO':
  return ('MANTIDO_COM_RESSALVA','Consulta informacional de estatística; valores de amostra ou população não foram fornecidos.')
 raise AssertionError(rule)

old_dec,df=readcsv(SOURCE/'p3-v2.8-decisoes.csv')
assert len(old_dec)==66 and len({r['id_global'] for r in old_dec})==66
byid={r['id_global']:r for r in old_dec}
assert set(FIXES).issubset(byid)
old_p3,p3_cols=readcsv(SOURCE/'p3-v2.8-fila-23965.csv')
old_gen,gen_cols=readcsv(SOURCE/'fila-geral-p0-p1-p2-p3-v2.8.csv')
assert len(old_p3)==23965 and len(old_gen)==52046
p3idx={r['id_global']:r for r in old_p3};genidx={r['id_global']:r for r in old_gen}
assert len(p3idx)==23965 and len(genidx)==52046
for id,r in byid.items():
 a=p3idx[id];g=genidx[id]
 assert a['prioridade']==g['prioridade']=='P3'
 assert a['Keyword']==g['Keyword']==r['Keyword']
 assert a['familia_id']==g['familia_id']==r['familia_id']
 assert a['status_p3_v2_8'] and a['classificacao_alterada_p3_v2_8']=='sim'

# Unpacks 30 actual lots once; validates unchanged global ledger independently
infiles=[]; references={}; base=ctrl=0
with zipfile.ZipFile(SOURCE/BASE) as za:
 assert za.testzip() is None and len(za.namelist())==30
 for name in za.namelist():
  rows,fields=fromzip(za,name)
  for row in rows:
   if row['tipo_registro']=='base':
    base+=1
    if row['id_global'] in byid:
     assert row['id_global'] not in references
     references[row['id_global']]=(name,row)
   else:ctrl+=1
  infiles.append((name,rows,fields))
assert (base,ctrl)==(294905,2190)
assert set(references)==set(byid)

# individual review of all 66 with actual before/after
reviews=[];patches=[]; revised={}; stat=collections.Counter()
for r in old_dec:
 id=r['id_global'];name,old=references[id]
 assert old['Keyword']==r['Keyword'] and old['familia_id']==r['familia_id']
 after=dict(old); after.update(FIXES.get(id,{}))
 changed=[f for f in old if old[f]!=after[f]]
 assert all(f in WRITE for f in changed)
 st,note=qa_note(r)
 assert (st=='CORRIGIDO')==bool(changed)
 stat[st]+=1
 if changed:
  revised[id]=after
  patches.append({'id_global':id,'lote':name,'familia_id':old['familia_id'],'Keyword':old['Keyword'],'regra_origem':r['regra'],'parecer_v29':st,'nota_qa':note,'campos_modificados':','.join(changed),'antes_json':json.dumps({f:old[f] for f in changed},ensure_ascii=False,sort_keys=True),'depois_json':json.dumps({f:after[f] for f in changed},ensure_ascii=False,sort_keys=True)})
 reviews.append({'id_global':id,'lote':name,'familia_id':old['familia_id'],'Keyword':old['Keyword'],'regra_v28':r['regra'],'parecer_v29':st,'nota_qa_v29':note,'area_v28':old['area_principal'],'cluster_v28':old['cluster'],'subcluster_v28':old['subcluster'],'tipo_v28':old['tipo_intencao'],'area_v29':after['area_principal'],'cluster_v29':after['cluster'],'subcluster_v29':after['subcluster'],'tipo_v29':after['tipo_intencao'],'mudou_lote':'sim' if changed else 'não','revisao_editorial_final':'pendente'})
assert len(reviews)==66 and len(patches)==2
writecsv(OUT/'p3-v2.9-revisao-66.csv',reviews,list(reviews[0]))
writecsv(OUT/'p3-v2.9-patches.csv',patches,list(patches[0]))

# preserve controls and old classifications verbatim except authorized IDs/fields
rows_reg=[]
with zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v2.9.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
 for name,rows,fields in infiles:
  newer=[];cbase=cctrl=modified=0
  for row in rows:
   new = revised.get(row['id_global'],row)
   if row['tipo_registro']=='base':cbase+=1
   else:cctrl+=1
   if new!=row:
    assert row['tipo_registro']=='base' and row['id_global'] in revised
    modified+=1
   newer.append(new)
  zb.writestr(name.replace('v2.8','v2.9'),tozip(newer,fields))
  rows_reg.append({'lote':name,'base':cbase,'controles':cctrl,'patches':modified,'status':'PASSOU'})
assert sum(int(x['patches']) for x in rows_reg)==2
writecsv(OUT/'p3-v2.9-regressao-30-lotes.csv',rows_reg,list(rows_reg[0]))

notes={r['id_global']:r for r in reviews}
for src,src_rows,cols,dest,expected in [
 ('p3-v2.8-fila-23965.csv',old_p3,p3_cols,'p3-v2.9-fila-23965.csv',23965),
 ('fila-geral-p0-p1-p2-p3-v2.8.csv',old_gen,gen_cols,'fila-geral-p0-p1-p2-p3-v2.9.csv',52046)]:
 assert len(src_rows)==expected and not (set(P3_NEW)&set(cols))
 newrows=[];affected=0
 for old in src_rows:
  r=dict(old);id=old['id_global']
  if id in byid:
   q=notes[id];after=revised.get(id,references[id][1]);affected+=1
   v={'status_p3_v2_9':'REVISADO','parecer_p3_v2_9':q['parecer_v29'],'nota_qa_p3_v2_9':q['nota_qa_v29'],'area_final_p3_v2_9':after['area_principal'],'cluster_final_p3_v2_9':after['cluster'],'subcluster_final_p3_v2_9':after['subcluster'],'tipo_intencao_final_p3_v2_9':after['tipo_intencao'],'classificacao_alterada_p3_v2_9':'sim' if id in revised else 'não'}
  else:v=dict.fromkeys(P3_NEW,'')
  r.update(v);newrows.append(r)
 assert affected==66
 writecsv(OUT/dest,newrows,cols+P3_NEW)

# Global quarantine copy unchanged by design
q=SOURCE/'backlog-global-98-com-parecer-v27.csv'
if q.exists():
 (OUT/'backlog-global-98-com-parecer-v27.csv').write_bytes(q.read_bytes())

# audit summaries: pending P3 unchanged in v2.9, because this is review not expansion
source_summary=json.loads((SOURCE/'p3-v2.8-resumo.json').read_text(encoding='utf-8'))
summary={'versao':'P3 v2.9','decisoes_criticadas':66,'corrigidas':2,'mantidas_com_ressalvas':64,'novas_familias':0,
 'regras':dict(collections.Counter(r['regra'] for r in old_dec)),
 'contagem_p3_fora_dos_pilotos':20308,'contagem_p3_metodo':'reconciliação v2.8; nenhuma nova inclusão/exclusão de escopo',
 'p2_pendentes':4660,'globais_quarentena':98,'base':base,'controles':ctrl,'lotes':30,
 'criterio':'revisão semântica direcionada de 66 IDs; não homologação editorial','status':'AUDITORIA_EXECUTADA'}
(OUT/'p3-v2.9-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
