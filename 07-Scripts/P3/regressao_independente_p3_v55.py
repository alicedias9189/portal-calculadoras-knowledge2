#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressão independente v5.5: reconta e compara fontes v5.4/v5.5 sem chamar script de auditoria."""
from pathlib import Path
import csv,io,zipfile,json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'08-Entregas/P3-v5.4';D=R/'08-Entregas/P3-v5.5'
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_5','parecer_p3_v5_5','justificativa_p3_v5_5','area_final_p3_v5_5','cluster_final_p3_v5_5','subcluster_final_p3_v5_5','tipo_intencao_final_p3_v5_5','classificacao_alterada_p3_v5_5']
def rd(f):
 with f.open(encoding='utf-8-sig',newline='') as h:
  r=csv.DictReader(h,delimiter=';');return list(r),list(r.fieldnames)
opinions,_=rd(D/'p3-v5.5-pareceres-100.csv');patches,_=rd(D/'p3-v5.5-patches-23.csv')
ids={r['id_global'] for r in opinions};patched={p['id_global'] for p in patches};pmap={p['id_global']:p for p in patches}
assert len(ids)==100 and len(patched)==23 and patched<=ids
assert sum(r['parecer_v5_5']=='REFINADO' for r in opinions)==23
assert sum(r['parecer_v5_5']=='MANTIDO_COM_RESSALVA' for r in opinions)==77
assert all(r['homologacao_editorial']=='PENDENTE' and r['justificativa_individual'] for r in opinions)
files=[('canonica','lotes-001-a-030-p3-v5.4.zip','lotes-001-a-030-p3-v5.5.zip',294905),('sem_ouro','lotes-001-a-030-p3-v5.4-sem-ouro.zip','lotes-001-a-030-p3-v5.5-sem-ouro.zip',291296)]
reg=[];id_sets=[];patch_snapshots=[]
for group,f0,f1,expected in files:
 with zipfile.ZipFile(S/f0) as src,zipfile.ZipFile(D/f1) as dest:
  assert src.testzip() is None and dest.testzip() is None and len(src.namelist())==len(dest.namelist())==30
  seen=set();changed=set();bases=controls=0;idset=set();newpatch={}
  for a,b in zip(src.namelist(),dest.namelist()):
   assert b==a.replace('v5.4','v5.5')
   r=csv.DictReader(io.StringIO(src.read(a).decode('utf-8-sig')),delimiter=';')
   t=csv.DictReader(io.StringIO(dest.read(b).decode('utf-8-sig')),delimiter=';')
   assert r.fieldnames==t.fieldnames
   cnt=patch_count=0
   for old,new in zip(r,t):
    cnt+=1;id=old['id_global'];assert id==new['id_global']
    assert old['Keyword']==new['Keyword'] and old['familia_id']==new['familia_id']
    if old['tipo_registro']=='base':
     assert id not in idset;idset.add(id);bases+=1
    else:controls+=1
    if id in ids:
     assert old['tipo_registro']=='base' and id not in seen;seen.add(id)
    changes={k for k in r.fieldnames if old[k]!=new[k]}
    if changes:
     assert id in patched and id not in changed and changes<=ALLOWED,(group,id,changes)
     changed.add(id);patch_count+=1;newpatch[id]={k:new[k] for k in changes}
     patch=pmap[id];assert set(patch['campos_modificados'].split(','))==changes
     assert json.loads(patch['antes_json'])=={k:old[k] for k in changes}
     assert json.loads(patch['depois_json'])=={k:new[k] for k in changes}
    else:assert old==new
   assert next(r,None) is None and next(t,None) is None
   reg.append({'base':group,'lote':b,'registros':cnt,'refinamentos':patch_count,'status':'PASSOU'})
  assert seen==ids and changed==patched and bases==expected and controls==2190,(group,len(seen),len(changed),bases,controls)
  id_sets.append(idset);patch_snapshots.append(newpatch)
assert id_sets[1] <= id_sets[0] and len(id_sets[0]-id_sets[1])==3609
assert patch_snapshots[0]==patch_snapshots[1]
assert ids.isdisjoint(id_sets[0]-id_sets[1])
filesq=[('p3-v5.4-fila-23965.csv','p3-v5.5-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.4.csv','fila-geral-p0-p1-p2-p3-v5.5.csv',52046),('p3-v5.4-fila-23865-sem-ouro.csv','p3-v5.5-fila-23865-sem-ouro.csv',23865),('fila-geral-v5.4-sem-ouro-51884.csv','fila-geral-v5.5-sem-ouro-51884.csv',51884)]
qreg=[]
for a,b,expected in filesq:
 src,cols=rd(S/a);dest,dcols=rd(D/b)
 assert len(src)==len(dest)==expected and len(cols)==414 and dcols==cols+TRACE
 seen=set()
 for old,new in zip(src,dest):
  assert old=={k:new[k] for k in cols},(b,old['id_global'])
  id=old['id_global']
  if id in ids:
   assert id not in seen;seen.add(id)
   assert new['status_p3_v5_5']=='REVISADO' and new['parecer_p3_v5_5']==('REFINADO' if id in patched else 'MANTIDO_COM_RESSALVA')
   assert new['classificacao_alterada_p3_v5_5']==('sim' if id in patched else 'não')
   assert all(new[k] for k in TRACE)
   expected_type=(pmap[id] and json.loads(pmap[id]['depois_json']).get('tipo_intencao',old['tipo_intencao_final_p3_v5_4'])) if id in patched else old['tipo_intencao_final_p3_v5_4']
   assert new['tipo_intencao_final_p3_v5_5']==expected_type
  else: assert not any(new[k] for k in TRACE)
 assert seen==ids
 qreg.append({'fila':b,'linhas':expected,'colunas_historicas':414,'colunas_novas':8,'status':'PASSOU'})
assert (S/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(D/'backlog-global-98-com-parecer-v27.csv').read_bytes()
with (D/'p3-v5.5-regressao-independente-60-lotes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(reg[0]),delimiter=';',lineterminator='\n');writer.writeheader();writer.writerows(reg)
sha=hashlib.sha256()
for path in [S/x[1] for x in files]+[S/'p3-v5.4-pareceres-100.csv',S/'backlog-global-98-com-parecer-v27.csv']:
 sha.update(path.name.encode());sha.update(hashlib.sha256(path.read_bytes()).digest())
result={'status':'PASSOU','lotes':len(reg),'pareceres_individuais':100,'patches_unicos':23,'inalterados_com_ressalvas':77,
 'apenas_ids_autorizados_alterados':True,'filas':qreg,'base_canonica':294905,'base_sem_ouro':291296,
 'controles_por_versao':2190,'excluidos_ouro_somente_operacional':3609,'p3_elegiveis_sem_ouro':19362,
 'p3_elegiveis_canonicos':19462,'backlog_98':'BYTE_A_BYTE_IDENTICO',
 'fontes_sha256_agregado':sha.hexdigest(),'homologacao_editorial':'PENDENTE'}
(D/'p3-v5.5-regressao-independente-resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))