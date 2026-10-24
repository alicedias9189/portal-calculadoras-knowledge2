#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressão independente v5.1 x v5.0; verifica todos os registros, filas e 30 lotes.
Rodar da raiz: python 07-Scripts/P3/regressao_independente_p3_v51.py
"""
from pathlib import Path
from collections import Counter
import csv,zipfile,io,hashlib,json
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'08-Entregas/P3-v5.1/FONTES-REPRODUCAO/08-Entregas/P3-v5.0'
B=ROOT/'08-Entregas/P3-v5.1'
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
HIST=['status_p3_v5_1','parecer_p3_v5_1','justificativa_p3_v5_1','area_final_p3_v5_1','cluster_final_p3_v5_1','subcluster_final_p3_v5_1','tipo_intencao_final_p3_v5_1','classificacao_alterada_p3_v5_1']
def entries(path):
 with open(path,encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r),list(r.fieldnames)
review,rc=entries(B/'p3-v5.1-pareceres-75.csv')
patches,pc=entries(B/'p3-v5.1-patches-19.csv')
assert len(review)==75 and len(patches)==19
reviewids={x['id_global'] for x in review};patchids={x['id_global'] for x in patches}
assert len(reviewids)==75 and len(patchids)==19 and patchids<=reviewids
assert {x['id_global'] for x in review if x['parecer_v5_1']=='REFINADO_COM_RESSALVA'}==patchids
assert all(x['homologacao_editorial']=='PENDENTE' for x in review)
assert all(x['justificativa_individual'] and x['Keyword'] for x in review)
patchmap={x['id_global']:x for x in patches}
lotestats=[];allids=set();modified_ids=set();base=ctrl=0
with zipfile.ZipFile(A/'lotes-001-a-030-p3-v5.0.zip') as za,zipfile.ZipFile(B/'lotes-001-a-030-p3-v5.1.zip') as zb:
 assert len(za.namelist())==len(zb.namelist())==30
 assert za.testzip() is None and zb.testzip() is None
 for na,nb in zip(za.namelist(),zb.namelist()):
  assert nb==na.replace('v5.0','v5.1')
  ra=csv.DictReader(io.StringIO(za.read(na).decode('utf-8-sig')),delimiter=';')
  rb=csv.DictReader(io.StringIO(zb.read(nb).decode('utf-8-sig')),delimiter=';')
  assert ra.fieldnames==rb.fieldnames
  nr=changed=nc=nctrl=0
  for a,b in zip(ra,rb):
   nr+=1
   assert a['id_global']==b['id_global'] and a['tipo_registro']==b['tipo_registro']
   if a['tipo_registro']=='base':nc+=1
   else:nctrl+=1
   delta={col for col in ra.fieldnames if a[col]!=b[col]}
   rid=a['id_global']
   if delta:
    assert rid in patchids and a['tipo_registro']=='base',(nb,rid,delta)
    assert delta<=EDIT,(rid,delta)
    p=patchmap[rid];assert sorted(delta)==sorted(p['campos_modificados'].split(','))
    bef=json.loads(p['antes_json']);aft=json.loads(p['depois_json'])
    assert bef=={c:a[c] for c in delta} and aft=={c:b[c] for c in delta}
    assert rid not in modified_ids;modified_ids.add(rid);changed+=1
   if rid in reviewids:
    assert rid not in allids;allids.add(rid)
  assert nr==nc+nctrl
  assert next(ra,None) is None and next(rb,None) is None
  base+=nc;ctrl+=nctrl
  lotestats.append(dict(lote=nb,linhas=nr,base=nc,controles=nctrl,alteracoes=changed,status='PASSOU'))
assert allids==reviewids and modified_ids==patchids
assert base==294905 and ctrl==2190
rows_results=[]
for old,new,expected in [('p3-v5.0-fila-23965.csv','p3-v5.1-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.0.csv','fila-geral-p0-p1-p2-p3-v5.1.csv',52046)]:
 ra,ca=entries(A/old);rb,cb=entries(B/new)
 assert len(ra)==len(rb)==expected and len(ca)==382 and cb==ca+HIST
 checked=set();traced=set()
 for a,b in zip(ra,rb):
  rid=a['id_global'];assert a=={col:b[col] for col in ca},(new,rid)
  if rid in reviewids:
   assert rid not in checked;checked.add(rid)
   assert b['status_p3_v5_1']=='REVISADO'
   assert b['classificacao_alterada_p3_v5_1']==('sim' if rid in patchids else 'não')
   assert all(b[c] for c in HIST)
   traced.add(rid)
  else:
   assert not any(b[c] for c in HIST),(new,rid)
 assert checked==reviewids and traced==reviewids
 rows_results.append({'arquivo':new,'linhas':expected,'colunas_historicas_intactas':len(ca),'colunas_novas':8,'status':'PASSOU'})
assert (A/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(B/'backlog-global-98-com-parecer-v27.csv').read_bytes()
sha=hashlib.sha256()
# Concatenação de checksum das fontes protegidas, com ordem explícita
for path in ['p3-v5.0-fila-23965.csv','fila-geral-p0-p1-p2-p3-v5.0.csv','backlog-global-98-com-parecer-v27.csv']:
 sha.update(path.encode());sha.update(hashlib.sha256((A/path).read_bytes()).digest())
summary={'status':'REGRESSAO_INDEPENDENTE_PASSOU','lotes':30,'base':base,'controles':ctrl,'ids_revisados':len(allids),'ids_refinados':len(modified_ids),'ids_preservados':len(allids)-len(modified_ids),'filas':rows_results,'backlog_global_98_byte_a_byte':'IDÊNTICO','checksum_fontes_protegidas':sha.hexdigest()}
with (B/'p3-v5.1-regressao-independente-30-lotes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(lotestats[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(lotestats)
(B/'p3-v5.1-regressao-independente-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))