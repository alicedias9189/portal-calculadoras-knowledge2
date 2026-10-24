#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica v5.3 independentemente do código de aplicação de patches."""
from pathlib import Path
import csv,io,json,zipfile,hashlib
HERE=Path(__file__).resolve(); R=HERE.parents[2] if HERE.parent.name=='P3' and HERE.parent.parent.name=='07-Scripts' else HERE.parent
S=R/'08-Entregas/P3-v5.2';G=R/'auditoria-ouro';O=R/'08-Entregas/P3-v5.3'
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_3','parecer_p3_v5_3','justificativa_p3_v5_3','area_final_p3_v5_3','cluster_final_p3_v5_3','subcluster_final_p3_v5_3','tipo_intencao_final_p3_v5_3','classificacao_alterada_p3_v5_3']
def records(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  d=csv.DictReader(f,delimiter=';');return list(d),d.fieldnames
patchrows,_=records(O/'p3-v5.3-patches-6.csv');pareceres,_=records(O/'p3-v5.3-pareceres-75.csv')
ids={r['id_global'] for r in pareceres};patchmap={r['id_global']:r for r in patchrows};patchids=set(patchmap)
assert len(ids)==75 and len(patchids)==6 and patchids<=ids
assert sum(x['parecer_v5_3']=='REFINADO' for x in pareceres)==6
assert sum(x['parecer_v5_3']=='MANTIDO_COM_RESSALVA' for x in pareceres)==69
assert all(x['justificativa_individual'] and x['homologacao_editorial']=='PENDENTE' for x in pareceres)
excluded,_=records(G/'ids-ouro-excluir-3609.csv');exids={r['id_global'] for r in excluded}
assert len(exids)==3609 and not (exids&ids)
oldpaths=[S/'lotes-001-a-030-p3-v5.2.zip', G/'lotes-30-trabalho-sem-ouro.zip']
newpaths=[O/'lotes-001-a-030-p3-v5.3.zip',O/'lotes-001-a-030-p3-v5.3-sem-ouro.zip']
reports=[];oldids_full=set();newids_filter=set()
for label,src,dst,baseexp in zip(['canonica','filtrada_ouro'],oldpaths,newpaths,[294905,291296]):
 with zipfile.ZipFile(src) as zi,zipfile.ZipFile(dst) as zo:
  assert zi.testzip() is None and zo.testzip() is None and len(zi.namelist())==len(zo.namelist())==30
  seen=set();changed=set();bases=controls=0
  for name_old,name_new in zip(zi.namelist(),zo.namelist()):
   assert name_new==name_old.replace('v5.2','v5.3')
   a=csv.DictReader(io.StringIO(zi.read(name_old).decode('utf-8-sig')),delimiter=';')
   b=csv.DictReader(io.StringIO(zo.read(name_new).decode('utf-8-sig')),delimiter=';')
   assert a.fieldnames==b.fieldnames
   count=0;changed_n=0
   for x,y in zip(a,b):
    count+=1;id=x['id_global'];assert id==y['id_global'] and x['Keyword']==y['Keyword']
    bases+=x['tipo_registro']=='base';controls+=x['tipo_registro']!='base'
    if label=='canonica' and x['tipo_registro']=='base':oldids_full.add(id)
    if label=='filtrada_ouro' and x['tipo_registro']=='base':newids_filter.add(id)
    diff={k for k in a.fieldnames if x[k]!=y[k]}
    assert diff<=EDIT,(name_old,id,diff)
    if id in ids:
     assert id not in seen;seen.add(id)
    if diff:
     assert id in patchids and id not in changed;changed.add(id);changed_n+=1
     pr=patchmap[id]
     assert sorted(diff)==sorted(pr['campos_modificados'].split(',')),(id,diff)
     assert json.loads(pr['antes_json'])=={k:x[k] for k in diff}
     assert json.loads(pr['depois_json'])=={k:y[k] for k in diff}
    else:assert x==y
   assert next(a,None) is None and next(b,None) is None
   reports.append({'base':label,'lote':name_new,'registros':count,'refinamentos':changed_n,'status':'PASSOU'})
  assert bases==baseexp and controls==2190 and seen==ids and changed==patchids
assert oldids_full-newids_filter==exids
assert len(oldids_full)==294905 and len(newids_filter)==291296
qrs=[]
for src,dst,n in [(S/'p3-v5.2-fila-23965.csv',O/'p3-v5.3-fila-23965.csv',23965),
 (S/'fila-geral-p0-p1-p2-p3-v5.2.csv',O/'fila-geral-p0-p1-p2-p3-v5.3.csv',52046),
 (G/'fila-p3-v5.2-sem-ouro-23865.csv',O/'p3-v5.3-fila-23865-sem-ouro.csv',23865),
 (G/'fila-geral-v5.2-sem-ouro-51884.csv',O/'fila-geral-v5.3-sem-ouro-51884.csv',51884)]:
 a,ca=records(src);b,cb=records(dst)
 assert len(a)==len(b)==n and len(ca)==398 and cb==ca+TRACE
 seen=set()
 for x,y in zip(a,b):
  id=x['id_global'];assert x=={k:y[k] for k in ca},(dst.name,id)
  if id in ids:
   assert id not in seen;seen.add(id)
   assert y['status_p3_v5_3']=='REVISADO' and all(y[k] for k in TRACE)
   assert (y['classificacao_alterada_p3_v5_3']=='sim')==(id in patchids)
   assert (y['parecer_p3_v5_3']=='REFINADO')==(id in patchids)
  else:assert not any(y[k] for k in TRACE)
 assert seen==ids
 qrs.append({'fila':dst.name,'linhas':n,'colunas_protegidas':398,'colunas_adicionais':8,'status':'PASSOU'})
assert (S/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(O/'backlog-global-98-com-parecer-v27.csv').read_bytes()
sha=hashlib.sha256()
for p in oldpaths+[S/'p3-v5.2-decisoes-75.csv',G/'ids-ouro-excluir-3609.csv']:
 sha.update(p.name.encode());sha.update(hashlib.sha256(p.read_bytes()).digest())
with (O/'p3-v5.3-regressao-independente-60-lotes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(reports[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(reports)
result={'status':'PASSOU','lotes_canonicos':30,'lotes_filtrados':30,'pareceres':75,'refinamentos':6,'mantidos':69,
  'bases_canonicas':294905,'bases_filtradas':291296,'controles_em_cada_versao':2190,'ouro_excluido_somente_da_visao':3609,
  'registros_originais_nao_ouro_inalterados':True,'filas':qrs,'historico_colunas_intacto':398,
  'p3_elegiveis_canonico':19562,'p3_elegiveis_filtrado':19462,'backlog_98_byte_a_byte':'IDENTICO',
  'sha256_fontes':sha.hexdigest(),'homologacao_editorial':'PENDENTE'}
(O/'p3-v5.3-regressao-independente-resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))