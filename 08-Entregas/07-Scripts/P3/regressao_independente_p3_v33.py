#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressão P3 v3.3 independente do auditor: 30 lotes, filas, controles, QA.
Uso: python 07-Scripts/P3/regressao_independente_p3_v33.py
"""
from pathlib import Path
import csv,io,zipfile,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v3.3'
SRC=OUT/'FONTES-REPRODUCAO/08-Entregas/P3-v3.2'
EDITABLE={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
def csv_file(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f,delimiter=';');return list(reader),reader.fieldnames
def zip_rows(z,n):
 reader=csv.DictReader(io.StringIO(z.read(n).decode('utf-8-sig')),delimiter=';');return list(reader),reader.fieldnames
def write_csv(path,rows,fields):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
patches,_=csv_file(OUT/'p3-v3.3-patches.csv')
reviews,_=csv_file(OUT/'p3-v3.3-pareceres-68.csv')
assert len(patches)==10 and len(reviews)==68
byid={x['id_global']:x for x in patches};opids={r['id_global'] for r in reviews}
assert len(byid)==10 and len(opids)==68 and set(byid).issubset(opids)
assert sum(r['parecer_v33']=='CORRIGIDO' for r in reviews)==len(byid)
beforehash=hashlib.sha256();afterhash=hashlib.sha256();changed=set();summ=[];ids_all=set();p3_selected=set()
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v3.2.zip') as a,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v3.3.zip') as b:
 assert len(a.namelist())==len(b.namelist())==30
 assert a.testzip() is None and b.testzip() is None
 for oldname in a.namelist():
  newname=oldname.replace('v3.2','v3.3')
  assert newname in b.namelist()
  x,xf=zip_rows(a,oldname);y,yf=zip_rows(b,newname)
  assert xf==yf and len(x)==len(y)
  base=ctr=modified=0
  for before,after in zip(x,y):
   assert before['id_global']==after['id_global'] and before['tipo_registro']==after['tipo_registro']
   assert before['familia_id']==after['familia_id'] and before['Keyword']==after['Keyword']
   if before['tipo_registro']=='base':base+=1
   else:ctr+=1
   diff={k for k in xf if before[k]!=after[k]}
   if diff:
    assert before['tipo_registro']=='base' and before['id_global'] in byid,(oldname,before['id_global'])
    assert not (diff-EDITABLE),(oldname,before['id_global'],diff-EDITABLE)
    patch=byid[before['id_global']]
    patch_fields=set(patch['campos_modificados'].split(','))
    assert patch_fields==diff
    assert json.loads(patch['antes_json'])=={k:before[k] for k in patch_fields}
    assert json.loads(patch['depois_json'])=={k:after[k] for k in patch_fields}
    assert before['id_global'] not in changed
    changed.add(before['id_global']);modified+=1
   for k in xf:
    if k not in EDITABLE:
     beforehash.update((k+'\0'+before[k]+'\x1e').encode('utf-8'))
     afterhash.update((k+'\0'+after[k]+'\x1e').encode('utf-8'))
   if before['id_global'] in opids:
    assert before['tipo_registro']=='base'
    assert before['id_global'] not in p3_selected
    p3_selected.add(before['id_global'])
  summ.append({'lote':oldname,'bases':base,'controles':ctr,'patches':modified,'status':'PASSOU'})
assert changed==set(byid) and p3_selected==opids
assert sum(s['bases'] for s in summ)==294905 and sum(s['controles'] for s in summ)==2190
assert beforehash.hexdigest()==afterhash.hexdigest()
qnew=['status_p3_v3_3','parecer_p3_v3_3','justificativa_p3_v3_3','area_final_p3_v3_3','cluster_final_p3_v3_3','subcluster_final_p3_v3_3','tipo_intencao_final_p3_v3_3','classificacao_alterada_p3_v3_3']
for oldname,newname,expected in [
 ('p3-v3.2-fila-23965.csv','p3-v3.3-fila-23965.csv',23965),
 ('fila-geral-p0-p1-p2-p3-v3.2.csv','fila-geral-p0-p1-p2-p3-v3.3.csv',52046)]:
 before,fc=csv_file(SRC/oldname);after,nc=csv_file(OUT/newname)
 assert len(before)==len(after)==expected and nc==fc+qnew,(oldname,len(fc),len(nc))
 count_visited=count_changed=0
 for b,a in zip(before,after):
  assert b['id_global']==a['id_global']
  assert all(b[k]==a[k] for k in fc),(oldname,b['id_global'])
  if b['id_global'] in opids:
   count_visited+=1
   assert a['parecer_p3_v3_3'] in ('CORRIGIDO','MANTIDO_COM_RESSALVA')
   if b['id_global'] in changed:
    count_changed+=1
    assert a['classificacao_alterada_p3_v3_3']=='sim'
   else: assert a['classificacao_alterada_p3_v3_3']=='não'
  else:
   assert all(a[k]=='' for k in qnew)
 assert count_visited==68 and count_changed==10
assert (SRC/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(OUT/'backlog-global-98-com-parecer-v27.csv').read_bytes()
write_csv(OUT/'p3-v3.3-regressao-independente-30-lotes.csv',summ,list(summ[0]))
result={'status':'PASSOU','lotes':30,'bases':294905,'controles':2190,'revisados':68,'patches':10,
 'sha256_campos_protegidos':beforehash.hexdigest(),
 'filas':'23965 P3 e 52046 geral, 238 colunas históricas de cada fila intocadas; 8 novas colunas',
 'global_98':'idêntico em bytes','homologacao_editorial':'pendente'}
(OUT/'p3-v3.3-regressao-independente-resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
