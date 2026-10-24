#!/usr/bin/env python3
# coding: utf-8
"""Regressão independente integral P3 v3.0: 30 lotes, patches, filas e dados protegidos.
Executar da raiz do pacote: python 07-Scripts/P3/regressao_independente_p3_v30.py
"""
import csv,io,zipfile,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2]
A=R/'08-Entregas/P3-v3.0/FONTES-REPRODUCAO/08-Entregas/P3-v2.9'
B=R/'08-Entregas/P3-v3.0'
VALID={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta'}

def rcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  dr=csv.DictReader(f,delimiter=';');return list(dr),list(dr.fieldnames)
def zcsv(z,name):
 return list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';'))
def writecsv(path,rows):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
patches,pc=rcsv(B/'p3-v3.0-patches.csv');byid={r['id_global']:r for r in patches}
assert len(byid)==len(patches)==36
seen=set();h1=hashlib.sha256();h2=hashlib.sha256();lotchecks=[]
with zipfile.ZipFile(A/'lotes-001-a-030-p3-v2.9.zip') as za,zipfile.ZipFile(B/'lotes-001-a-030-p3-v3.0.zip') as zb:
 assert len(za.namelist())==len(zb.namelist())==30 and za.testzip() is None and zb.testzip() is None
 for oldname in za.namelist():
  newname=oldname.replace('v2.9','v3.0'); assert newname in zb.namelist()
  left=zcsv(za,oldname);right=zcsv(zb,newname)
  assert len(left)==len(right)
  nb=nc=changed=0
  for p,q in zip(left,right):
   assert p.keys()==q.keys() and p['id_global']==q['id_global'] and p['tipo_registro']==q['tipo_registro']
   if p['tipo_registro']=='base':nb+=1
   else:nc+=1
   dif={f for f in p if p[f]!=q[f]}
   assert not(dif-VALID),('CAMPO PROTEGIDO',oldname,p['id_global'],dif-VALID)
   if dif:
    id=p['id_global']; assert id in byid and id not in seen and p['tipo_registro']=='base'
    pat=byid[id];assert set(pat['campos_modificados'].split(','))==dif
    assert json.loads(pat['antes_json'])=={f:p[f] for f in dif},('ANTES',id)
    assert json.loads(pat['depois_json'])=={f:q[f] for f in dif},('DEPOIS',id)
    assert pat['Keyword']==p['Keyword']==q['Keyword'] and pat['familia_id']==p['familia_id']==q['familia_id']
    seen.add(id);changed+=1
   for f in p:
    if f not in VALID:
     h1.update((f+'\x00'+p[f]+'\x1e').encode('utf-8'))
     h2.update((f+'\x00'+q[f]+'\x1e').encode('utf-8'))
  lotchecks.append({'lote':oldname,'base':nb,'controles':nc,'alteracoes':changed,'campos_protegidos':'PRESERVADOS','status':'PASSOU'})
assert seen==set(byid)
assert sum(r['base'] for r in lotchecks)==294905
assert sum(r['controles'] for r in lotchecks)==2190
assert h1.hexdigest()==h2.hexdigest()
writecsv(B/'p3-v3.0-regressao-independente-30-lotes.csv',lotchecks)
queuechecks=[]
for left,right,expected in [('p3-v2.9-fila-23965.csv','p3-v3.0-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.9.csv','fila-geral-p0-p1-p2-p3-v3.0.csv',52046)]:
 old,of=rcsv(A/left);new,nf=rcsv(B/right)
 assert len(old)==len(new)==expected and nf[:len(of)]==of and len(nf)==len(of)+9
 old_ids={r['id_global'] for r in old}; assert set(byid)<=old_ids
 for p,q in zip(old,new):
  assert all(p[k]==q[k] for k in of),('COLUNA ANTIGA',p['id_global'])
  assert (q['classificacao_alterada_p3_v3_0']=='sim')==(q['id_global'] in byid)
 queuechecks.append({'arquivo':right,'linhas':expected,'colunas_historicas':len(of),'novas_colunas':9,'status':'PASSOU'})
# quarantine global must remain identical
srcglob=A/'backlog-global-98-com-parecer-v27.csv';dstglob=B/srcglob.name
assert srcglob.read_bytes()==dstglob.read_bytes()
# confirm all 36 authorized P3 and initial status no revisions
p3,_=rcsv(A/'p3-v2.9-fila-23965.csv');gen,_=rcsv(A/'fila-geral-p0-p1-p2-p3-v2.9.csv')
idx3={r['id_global']:r for r in p3};idxg={r['id_global']:r for r in gen}
status=[c for c in p3[0] if c.startswith('status_p3_')]
for id in seen:
 a=idx3[id];b=idxg[id]
 assert a['prioridade']==b['prioridade']=='P3'
 assert a['status_p3_v1']==b['status_p3_v1']=='FORA_DO_PILOTO'
 assert all(not a[x] and not b[x] for x in status if x!='status_p3_v1')
assert sum(r['status_p3_v1']=='FORA_DO_PILOTO' and all(not r[x] for x in status if x!='status_p3_v1') for r in p3)==20308
result={'status':'PASSOU','lotes':len(lotchecks),'alteracoes_autorizadas':len(seen),'bases':294905,'controles':2190,'filas':queuechecks,'global_98':'identico','campos_protegidos_sha256':h1.hexdigest(),'p3_restante':20272,'p2_preservada':4660}
(B/'p3-v3.0-regressao-independente-resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
