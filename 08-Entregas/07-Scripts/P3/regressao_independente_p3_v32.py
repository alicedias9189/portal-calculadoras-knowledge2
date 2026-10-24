#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressão independente: v3.1 -> v3.2, reabre e compara todas as linhas.
Execução: python 07-Scripts/P3/regressao_independente_p3_v32.py
"""
from pathlib import Path
from collections import Counter
import csv,io,zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v3.2/FONTES-REPRODUCAO/08-Entregas/P3-v3.1'
OUT=ROOT/'08-Entregas/P3-v3.2'
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def readzip(z,name):
 rd=csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';');return list(rd),list(rd.fieldnames)
def savecsv(path,rows,fields):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  rd=csv.DictWriter(f,delimiter=';',fieldnames=fields,lineterminator='\n');rd.writeheader();rd.writerows(rows)
patches,_=readcsv(OUT/'p3-v3.2-patches.csv'); assert len(patches)==68
byid={r['id_global']:r for r in patches};assert len(byid)==68
before_sha=hashlib.sha256();after_sha=hashlib.sha256();changed=set();summ=[]
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v3.1.zip') as za,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v3.2.zip') as zb:
 assert len(za.namelist())==len(zb.namelist())==30
 assert za.testzip() is None and zb.testzip() is None
 for name in za.namelist():
  x,xcols=readzip(za,name);y,ycols=readzip(zb,name.replace('v3.1','v3.2'))
  assert xcols==ycols and len(x)==len(y)
  bb=cc=nn=0
  for p,q in zip(x,y):
   assert p['id_global']==q['id_global'] and p['tipo_registro']==q['tipo_registro']
   if p['tipo_registro']=='base':bb+=1
   else:cc+=1
   dif={k for k in p if p[k]!=q[k]}
   assert not(dif-ALLOWED),(name,p['id_global'],dif-ALLOWED)
   if dif:
    assert p['tipo_registro']=='base' and p['id_global'] in byid
    id=p['id_global'];assert id not in changed;changed.add(id);nn+=1
    d=byid[id];fields=set(d['campos_modificados'].split(','))
    assert dif==fields
    assert json.loads(d['antes_json'])=={k:p[k] for k in fields}
    assert json.loads(d['depois_json'])=={k:q[k] for k in fields}
   for k in p:
    if k not in ALLOWED:
     before_sha.update((k+'\0'+p[k]+'\x1e').encode())
     after_sha.update((k+'\0'+q[k]+'\x1e').encode())
  summ.append({'lote':name,'bases':bb,'controles':cc,'patches':nn,'status':'PASSOU'})
assert changed==set(byid) and before_sha.hexdigest()==after_sha.hexdigest()
assert sum(int(x['bases']) for x in summ)==294905 and sum(int(x['controles']) for x in summ)==2190
assert sum(int(x['patches']) for x in summ)==68
savecsv(OUT/'p3-v3.2-regressao-independente-30-lotes.csv',summ,list(summ[0]))
# Old queue columns and all old values unchanged, exactly 9 extra columns.
for oldname,newname,num in [('p3-v3.1-fila-23965.csv','p3-v3.2-fila-23965.csv',23965),
 ('fila-geral-p0-p1-p2-p3-v3.1.csv','fila-geral-p0-p1-p2-p3-v3.2.csv',52046)]:
 a,ac=readcsv(SRC/oldname);b,bc=readcsv(OUT/newname)
 assert len(a)==len(b)==num and bc[:len(ac)]==ac and len(bc)-len(ac)==9
 for x,y in zip(a,b):
  assert x['id_global']==y['id_global']
  assert all(x[k]==y[k] for k in ac),(oldname,x['id_global'])
  if x['id_global'] in byid:
   assert y['status_p3_v3_2']=='REVISADO' and y['classificacao_alterada_p3_v3_2']=='sim'
  else:assert y['status_p3_v3_2']==''
# Global backlog byte-identical.
a=(SRC/'backlog-global-98-com-parecer-v27.csv').read_bytes();b=(OUT/'backlog-global-98-com-parecer-v27.csv').read_bytes()
assert a==b
report={'status':'PASSOU','lotes':30,'bases':294905,'controles':2190,'alteracoes':68,
 'sha256_campos_protegidos':before_sha.hexdigest(),
 'filas':'P3 23965 + geral 52046, 9 colunas novas, 229 colunas antigas intocadas',
 'global_98':'idêntico em bytes','homologacao_editorial':'pendente'}
(OUT/'p3-v3.2-regressao-independente-resumo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
