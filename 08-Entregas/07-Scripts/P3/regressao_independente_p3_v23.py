#!/usr/bin/env python3
# coding: utf-8
"""Auditoria independente, comparando os ZIPs e as filas reais P3 v2.2/v2.3.
Reexecutável após extrair o pacote na raiz do repositório.
"""
import csv,io,json,hashlib
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[2]
S=ROOT/'08-Entregas/P3-v2.3/FONTES-REPRODUCAO/08-Entregas/P3-v2.2'
O=ROOT/'08-Entregas/P3-v2.3'
VALID={'area_principal','cluster','subcluster','dominio_ou_grandeza','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta'}
def rr(s):return list(csv.DictReader(io.StringIO(s),delimiter=';'))
def read(path):return rr(path.read_text(encoding='utf-8-sig'))
patch=read(O/'p3-v2.3-patches.csv'); byid={x['id_global']:x for x in patch}
assert len(byid)==len(patch)==100
h_before=hashlib.sha256();h_after=hashlib.sha256();changed=set();rep=[]
with ZipFile(S/'lotes-001-a-030-p3-v2.2.zip') as za, ZipFile(O/'lotes-001-a-030-p3-v2.3.zip') as zb, ZipFile(S/'lotes-001-a-030-p3-v2.1.zip') as zold:
 assert len(za.namelist())==len(zb.namelist())==len(zold.namelist())==30
 for name in za.namelist():
  nn=name.replace('v2.2','v2.3'); historical=name.replace('v2.2','v2.1')
  x=rr(za.read(name).decode('utf-8-sig'));y=rr(zb.read(nn).decode('utf-8-sig'));h=rr(zold.read(historical).decode('utf-8-sig'))
  assert len(x)==len(y)==len(h)
  nbase=nctrl=nchanged=0
  for before,after,old in zip(x,y,h):
   assert before.keys()==after.keys()==old.keys()
   assert before['id_global']==after['id_global']==old['id_global']
   assert before['tipo_registro']==after['tipo_registro']==old['tipo_registro']
   id=before['id_global'];d=[k for k in before if before[k]!=after[k]]
   if before['tipo_registro']=='base':nbase+=1
   else:nctrl+=1
   if d:
    assert id in byid and set(d)<=VALID,(name,id,d)
    assert id not in changed
    changed.add(id);nchanged+=1
    p=byid[id]
    assert set(p['campos_modificados'].split(','))==set(d)
    assert json.loads(p['antes_json'])=={k:before[k] for k in d}
    assert json.loads(p['depois_json'])=={k:after[k] for k in d}
    if p['natureza']=='FORA_DA_FILA_P3_RESTAURADO':
     assert all(after[k]==old[k] for k in before),(name,id,'não restaurado à versão v2.1')
   else: assert id not in byid
   for k in before:
    if k not in VALID:
     h_before.update((k+'\0'+before[k]+'\x1e').encode())
     h_after.update((k+'\0'+after[k]+'\x1e').encode())
  rep.append({'lote':name,'base':nbase,'controles':nctrl,'alteracoes':nchanged,'campos_protegidos':'SIM','status':'PASSOU'})
assert changed==set(byid)
assert sum(int(r['base']) for r in rep)==294905 and sum(int(r['controles']) for r in rep)==2190
assert h_before.hexdigest()==h_after.hexdigest()
# Filas: somente oito campos novos; todos os campos históricos preservados linha a linha.
for old,new,expected in [('p3-v2.2-fila-23965.csv','p3-v2.3-fila-23965.csv',23965),
                         ('fila-geral-p0-p1-p2-p3-v2.2.csv','fila-geral-p0-p1-p2-p3-v2.3.csv',52046)]:
 a=read(S/old);b=read(O/new)
 assert len(a)==len(b)==expected
 for x,y in zip(a,b):
  assert x['id_global']==y['id_global']
  assert len(y)-len(x)==8
  assert all(x[k]==y[k] for k in x),(old,x['id_global'])
qids={r['id_global'] for r in read(S/'p3-v2.2-fila-23965.csv')}
quar=read(O/'p3-v2.3-quarentena-98-propostas.csv')
assert len(quar)==98 and not ({r['id_global'] for r in quar}&qids)
with (O/'p3-v2.3-regressao-independente.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rep[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rep)
result={'status':'PASSOU','lotes':30,'base':294905,'controles':2190,
        'patches':len(changed),'reversoes_fora_da_P3':98,'refinamentos_P3':2,
        'hash_protegidos_antes':h_before.hexdigest(),'hash_protegidos_depois':h_after.hexdigest(),
        'filas':'23.965 e 52.046; 100% das colunas antigas preservadas',
        'versao_anterior_comparada':'v2.2; reversões restauradas v2.1'}
(O/'p3-v2.3-regressao-independente.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
