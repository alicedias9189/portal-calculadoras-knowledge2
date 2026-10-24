#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v5.6: verificação independente contra v5.5, linha a linha e campo a campo."""
from pathlib import Path
import csv,io,json,zipfile,hashlib
R=Path(__file__).resolve().parents[2];S=R/'08-Entregas/P3-v5.5';O=R/'08-Entregas/P3-v5.6'
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_6','regra_p3_v5_6','justificativa_p3_v5_6','area_final_p3_v5_6','cluster_final_p3_v5_6','subcluster_final_p3_v5_6','tipo_intencao_final_p3_v5_6','classificacao_alterada_p3_v5_6']
def read(f):
 with f.open(encoding='utf-8-sig',newline='') as h:
  x=csv.DictReader(h,delimiter=';');return list(x),list(x.fieldnames)
pch,_=read(O/'p3-v5.6-patches-100.csv');dec,_=read(O/'p3-v5.6-pareceres-100.csv');ids={r['id_global'] for r in dec};pmap={r['id_global']:r for r in pch}
assert len(ids)==len(pmap)==100 and set(pmap)==ids
assert all(r['parecer']=='PROPOSTA_COM_RESSALVA' and r['homologacao_editorial']=='PENDENTE' and r['justificativa_individual'] for r in dec)
originals=[S/'lotes-001-a-030-p3-v5.5.zip',S/'lotes-001-a-030-p3-v5.5-sem-ouro.zip'];updated=[O/'lotes-001-a-030-p3-v5.6.zip',O/'lotes-001-a-030-p3-v5.6-sem-ouro.zip']
rows_out=[];base_sets=[]
for group,a_path,b_path,nb in zip(['canonica','filtrada_ouro'],originals,updated,[294905,291296]):
 with zipfile.ZipFile(a_path) as za,zipfile.ZipFile(b_path) as zb:
  assert za.testzip() is None and zb.testzip() is None and len(za.namelist())==len(zb.namelist())==30
  b_total=c_total=0;changed=set();seen=set();baseids=set()
  for fa,fb in zip(za.namelist(),zb.namelist()):
   assert fb==fa.replace('v5.5','v5.6'),(fa,fb)
   a=csv.DictReader(io.StringIO(za.read(fa).decode('utf-8-sig')),delimiter=';');b=csv.DictReader(io.StringIO(zb.read(fb).decode('utf-8-sig')),delimiter=';')
   assert a.fieldnames==b.fieldnames
   lc=0;cp=0
   for old,new in zip(a,b):
    lc+=1;id=old['id_global'];assert id==new['id_global']
    assert old['Keyword']==new['Keyword'] and old['familia_id']==new['familia_id']
    if old['tipo_registro']=='base': b_total+=1;baseids.add(id)
    else:c_total+=1
    if id in ids:
     assert id not in seen and old['tipo_registro']=='base';seen.add(id)
    delta={k for k in a.fieldnames if old[k]!=new[k]}
    if delta:
     assert id in ids and id not in changed and delta<=EDIT,(id,delta)
     changed.add(id);cp+=1
     log=pmap[id];assert set(log['campos_modificados'].split(','))==delta
     assert json.loads(log['antes_json'])=={k:old[k] for k in delta}
     assert json.loads(log['depois_json'])=={k:new[k] for k in delta}
    else:assert old==new
   assert next(a,None) is None and next(b,None) is None
   rows_out.append({'base':group,'lote':fb,'registros':lc,'patches':cp,'status':'PASSOU'})
  assert b_total==nb and c_total==2190 and seen==ids and changed==ids,(group,b_total,c_total,len(seen),len(changed))
  base_sets.append(baseids)
assert len(base_sets[0]-base_sets[1])==3609 and not ids.intersection(base_sets[0]-base_sets[1])
queues=[('p3-v5.5-fila-23965.csv','p3-v5.6-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.5.csv','fila-geral-p0-p1-p2-p3-v5.6.csv',52046),('p3-v5.5-fila-23865-sem-ouro.csv','p3-v5.6-fila-23865-sem-ouro.csv',23865),('fila-geral-v5.5-sem-ouro-51884.csv','fila-geral-v5.6-sem-ouro-51884.csv',51884)]
qreports=[]
for fn,gn,expected in queues:
 a,ac=read(S/fn);b,bc=read(O/gn)
 assert len(a)==len(b)==expected and len(ac)==422 and bc==ac+TRACE
 seen=set()
 for r,t in zip(a,b):
  assert r=={k:t[k] for k in ac},(gn,r['id_global'])
  id=r['id_global']
  if id in ids:
   assert id not in seen;seen.add(id)
   assert t['status_p3_v5_6']=='TRATADO' and t['regra_p3_v5_6'] and t['classificacao_alterada_p3_v5_6']=='sim'
   assert all(t[k] for k in TRACE)
  else:assert not any(t[k] for k in TRACE)
 assert seen==ids
 qreports.append({'fila':gn,'linhas':expected,'colunas_historicas':422,'colunas_novas':8,'status':'PASSOU'})
assert (O/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(S/'backlog-global-98-com-parecer-v27.csv').read_bytes()
with (O/'p3-v5.6-regressao-independente-60-lotes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows_out[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows_out)
sha=hashlib.sha256()
for p in originals+[S/'p3-v5.5-pareceres-100.csv',S/'backlog-global-98-com-parecer-v27.csv']:
 sha.update(p.name.encode());sha.update(hashlib.sha256(p.read_bytes()).digest())
result={'status':'PASSOU','lotes':len(rows_out),'patches_unicos':100,'campos_modificados_apenas_ids_autorizados':True,'filas':qreports,'base_canonica':294905,'base_filtrada_ouro':291296,'controles_preservados_por_versao':2190,'ouro_excluidos_apenas_visao_operacional':3609,'backlog_98':'BYTE_A_BYTE_IDENTICO','elegiveis_operacionais':19262,'fontes_sha256_agregado':sha.hexdigest(),'homologacao_editorial':'PENDENTE'}
(O/'p3-v5.6-regressao-independente-resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))