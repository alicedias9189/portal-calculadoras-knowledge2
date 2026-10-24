#!/usr/bin/env python3
"""Regressão independente do auditor da P3 v2.7. Python padrão."""
import pathlib,zipfile,io,csv,json,hashlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[2]
E=ROOT/'08-Entregas/P3-v2.7'
S=E/'FONTES-REPRODUCAO/08-Entregas/P3-v2.6'
ANALYTIC={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}

def rr(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def zz(z,name):
 return list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';'))
patches=rr(E/'p3-v2.7-patches.csv');assert len(patches)==1
byid={p['id_global']:p for p in patches}; assert set(byid)=={'190795'}
h1=hashlib.sha256();h2=hashlib.sha256();c=collections.Counter();changed=set()
with zipfile.ZipFile(S/'lotes-001-a-030-p3-v2.6.zip') as a, zipfile.ZipFile(E/'lotes-001-a-030-p3-v2.7.zip') as b:
 assert len(a.namelist())==len(b.namelist())==30
 for name in a.namelist():
  r1=zz(a,name);r2=zz(b,name.replace('v2.6','v2.7'))
  assert len(r1)==len(r2)
  for old,new in zip(r1,r2):
   assert old.keys()==new.keys() and old['id_global']==new['id_global'] and old['tipo_registro']==new['tipo_registro']
   c[old['tipo_registro']]+=1
   different={k for k in old if old[k]!=new[k]}
   assert not different or (old['id_global']=='190795' and different<=ANALYTIC)
   if different:
    changed.add(old['id_global']);p=byid[old['id_global']]
    assert different==set(p['campos_modificados'].split(','))
    assert {k:old[k] for k in different}==json.loads(p['antes_json'])
    assert {k:new[k] for k in different}==json.loads(p['depois_json'])
   for field in old:
    if field not in ANALYTIC:
     h1.update((field+'\0'+old[field]+'\x1e').encode())
     h2.update((field+'\0'+new[field]+'\x1e').encode())
assert changed=={'190795'} and c['base']==294905 and c['controle']==2190 and h1.hexdigest()==h2.hexdigest(),(changed,c)
# both queues retain historical columns in identical order and values
for old,new,n in [('p3-v2.6-fila-23965.csv','p3-v2.7-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.6.csv','fila-geral-p0-p1-p2-p3-v2.7.csv',52046)]:
 a=rr(S/old);b=rr(E/new);assert len(a)==len(b)==n
 for x,y in zip(a,b):assert all(x[k]==y[k] for k in x)
# global classification remains untouched
raw=rr(S/'backlog-global-98-com-parecer-50.csv');new=rr(E/'backlog-global-98-com-parecer-v27.csv')
assert len(raw)==len(new)==98
for x,y in zip(raw,new):assert all(x[k]==y[k] for k in x)
review=rr(E/'global-v27-pareceres-48.csv');assert len(review)==48
assert all(r['aplicacao_lotes_v27']=='NAO' for r in review)
assert not {r['id_global'] for r in new}&{r['id_global'] for r in rr(S/'p3-v2.6-fila-23965.csv')}
print(json.dumps({'regressao':'PASSOU','lotes':30,'base':c['base'],'controles':c['controle'],'patches_P3':len(changed),'globais_revisados':len(review),'globais_aplicados':0,'colunas_protegidas_sha256':h1.hexdigest()},ensure_ascii=False))
