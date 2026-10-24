#!/usr/bin/env python3
# coding: utf-8
"""Regressão independente P3 v2.9 com fontes incorporadas ao pacote. Python stdlib."""
import csv,io,zipfile,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'08-Entregas/P3-v2.9/FONTES-REPRODUCAO/08-Entregas/P3-v2.8'
B=ROOT/'08-Entregas/P3-v2.9'
VALID={'area_principal','cluster','subcluster','dominio_ou_grandeza','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
def readcsv(path):
 with path.open('r',encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r),list(r.fieldnames)
def getziprows(z,name):
 t=z.read(name).decode('utf-8-sig');d=csv.DictReader(io.StringIO(t),delimiter=';');return list(d),list(d.fieldnames)
def writecsv(path,rows,fields):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
patches,cols=readcsv(B/'p3-v2.9-patches.csv');pmap={r['id_global']:r for r in patches}
assert len(patches)==len(pmap)==2
reviews,_=readcsv(B/'p3-v2.9-revisao-66.csv');rmap={r['id_global']:r for r in reviews}
assert len(reviews)==len(rmap)==66
assert {r['id_global'] for r in reviews if r['parecer_v29']=='CORRIGIDO'}==set(pmap)
assert sum(r['parecer_v29']=='MANTIDO_COM_RESSALVA' for r in reviews)==64
seen=set();protected_before=hashlib.sha256();protected_after=hashlib.sha256();report=[]
with zipfile.ZipFile(A/'lotes-001-a-030-p3-v2.8.zip') as za,zipfile.ZipFile(B/'lotes-001-a-030-p3-v2.9.zip') as zb:
 assert za.testzip() is None and zb.testzip() is None
 assert len(za.namelist())==len(zb.namelist())==30
 for oldname in za.namelist():
  newname=oldname.replace('v2.8','v2.9')
  assert newname in zb.namelist()
  old,cols1=getziprows(za,oldname);new,cols2=getziprows(zb,newname)
  assert cols1==cols2 and len(old)==len(new)
  bb=cc=changed=0
  for x,y in zip(old,new):
   assert x['id_global']==y['id_global'] and x['tipo_registro']==y['tipo_registro']
   if x['tipo_registro']=='base':bb+=1
   else:cc+=1
   diff=[k for k in cols1 if x[k]!=y[k]]
   assert all(k in VALID and x['id_global'] in pmap for k in diff),(oldname,x['id_global'],diff)
   if diff:
    assert x['tipo_registro']=='base'
    id=x['id_global'];assert id not in seen;seen.add(id);changed+=1
    p=pmap[id]
    assert p['lote']==oldname and p['Keyword']==x['Keyword'] and p['familia_id']==x['familia_id']
    assert set(diff)==set(p['campos_modificados'].split(','))
    assert json.loads(p['antes_json'])=={k:x[k] for k in diff}
    assert json.loads(p['depois_json'])=={k:y[k] for k in diff}
   for k in cols1:
    if k not in VALID:
     protected_before.update((k+'\x00'+x[k]+'\x1e').encode('utf-8'))
     protected_after.update((k+'\x00'+y[k]+'\x1e').encode('utf-8'))
  report.append({'lote':oldname,'base':bb,'controles':cc,'patches':changed,'protecao':'SIM','status':'PASSOU'})
assert sum(x['base'] for x in report)==294905
assert sum(x['controles'] for x in report)==2190
assert seen==set(pmap) and protected_before.hexdigest()==protected_after.hexdigest()
# Full queue comparison exact pre-existing values and id order, plus 8 v2.9 columns for 66 ids
for a,b,expected in [('p3-v2.8-fila-23965.csv','p3-v2.9-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.8.csv','fila-geral-p0-p1-p2-p3-v2.9.csv',52046)]:
 before,oldcols=readcsv(A/a);after,newcols=readcsv(B/b)
 assert len(before)==len(after)==expected and newcols[:len(oldcols)]==oldcols
 assert len(newcols)-len(oldcols)==8
 for x,y in zip(before,after):
  assert x['id_global']==y['id_global']
  assert all(x[k]==y[k] for k in oldcols),(a,x['id_global'])
  id=x['id_global'];p=y['classificacao_alterada_p3_v2_9']
  assert (p=='sim')==(id in pmap)
  if id in rmap: assert y['parecer_p3_v2_9']==rmap[id]['parecer_v29']
  else: assert y['status_p3_v2_9']==''
# global quarantine identical bytes
assert (A/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(B/'backlog-global-98-com-parecer-v27.csv').read_bytes()
writecsv(B/'p3-v2.9-regressao-independente-30-lotes.csv',report,list(report[0]))
s={'status':'PASSOU','lotes':30,'base':294905,'controles':2190,'patches':2,'decisoes_qa':66,'filas':'23965 e 52046 linhas: colunas históricas idênticas', 'backlog_global_98':'identico byte a byte','sha256_campos_protegidos':protected_before.hexdigest()}
(B/'p3-v2.9-regressao-independente-resumo.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(s,ensure_ascii=False))
