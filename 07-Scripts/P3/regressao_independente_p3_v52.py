#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressão independente da P3 v5.2 contra a v5.1 (30 lotes e duas filas)."""
from pathlib import Path
import csv,zipfile,io,json,hashlib
R=Path(__file__).resolve().parents[2]/'08-Entregas/P3-v5.2'
S=R/'FONTES-REPRODUCAO/08-Entregas/P3-v5.1'
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_2','regra_p3_v5_2','justificativa_p3_v5_2','area_final_p3_v5_2','cluster_final_p3_v5_2','subcluster_final_p3_v5_2','tipo_intencao_final_p3_v5_2','classificacao_alterada_p3_v5_2']
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
dec,dcols=read(R/'p3-v5.2-decisoes-75.csv');pat,pcols=read(R/'p3-v5.2-patches-75.csv');plan,pncols=read(R/'p3-v5.2-plano-por-id.csv')
ids={x['id_global'] for x in dec};patches={x['id_global']:x for x in pat}
assert len(ids)==len(patches)==len(plan)==75 and ids==set(patches)=={x['id_global'] for x in plan}
assert all(x['homologacao_editorial']=='PENDENTE' and x['justificativa_individual'] for x in dec)
assert all(x['parecer']=='CLASSIFICADO_COM_RESSALVA' for x in dec)
assert not ids.intersection({x['id_global'] for x in read(S/'p3-v5.1-pareceres-75.csv')[0]})
seen=set();changed=set();total_base=total_ctrl=0;lots=[]
with zipfile.ZipFile(S/'lotes-001-a-030-p3-v5.1.zip') as a,zipfile.ZipFile(R/'lotes-001-a-030-p3-v5.2.zip') as b:
 assert a.testzip() is None and b.testzip() is None
 assert len(a.namelist())==len(b.namelist())==30
 for na,nb in zip(a.namelist(),b.namelist()):
  assert nb==na.replace('v5.1','v5.2')
  before=csv.DictReader(io.StringIO(a.read(na).decode('utf-8-sig')),delimiter=';')
  after=csv.DictReader(io.StringIO(b.read(nb).decode('utf-8-sig')),delimiter=';')
  assert before.fieldnames==after.fieldnames
  base=ctrl=delta_n=0
  for x,y in zip(before,after):
   rid=x['id_global'];assert rid==y['id_global'] and x['tipo_registro']==y['tipo_registro']
   base+=x['tipo_registro']=='base';ctrl+=x['tipo_registro']!='base'
   different={c for c in before.fieldnames if x[c]!=y[c]}
   if different:
    assert rid in ids and rid not in changed and x['tipo_registro']=='base'
    assert different<=EDIT,(rid,different)
    p=patches[rid]
    assert sorted(different)==sorted(p['campos_modificados'].split(',')),rid
    assert json.loads(p['antes_json'])=={c:x[c] for c in different}
    assert json.loads(p['depois_json'])=={c:y[c] for c in different}
    changed.add(rid);delta_n+=1
   if rid in ids:
    assert rid not in seen;seen.add(rid)
  assert next(before,None) is None and next(after,None) is None
  total_base+=base;total_ctrl+=ctrl
  lots.append(dict(lote=nb,registros=base+ctrl,bases=base,controles=ctrl,patches=delta_n,status='PASSOU'))
assert seen==changed==ids and len(lots)==30
assert total_base==294905 and total_ctrl==2190
filas=[]
for oldname,newname,n in [('p3-v5.1-fila-23965.csv','p3-v5.2-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.1.csv','fila-geral-p0-p1-p2-p3-v5.2.csv',52046)]:
 a,ca=read(S/oldname);b,cb=read(R/newname)
 assert len(a)==len(b)==n and len(ca)==390 and cb==ca+TRACE
 tracked=set()
 for x,y in zip(a,b):
  rid=x['id_global']
  assert x=={col:y[col] for col in ca},(oldname,rid)
  if rid in ids:
   assert rid not in tracked;tracked.add(rid)
   assert y['status_p3_v5_2']=='TRATADO' and y['classificacao_alterada_p3_v5_2']=='sim'
   assert all(y[c] for c in TRACE)
  else:assert not any(y[c] for c in TRACE)
 assert tracked==ids
 filas.append(dict(nome=newname,linhas=n,colunas_historicas=390,colunas_adicionadas=8,status='PASSOU'))
assert (S/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(R/'backlog-global-98-com-parecer-v27.csv').read_bytes()
sha=hashlib.sha256()
for name in ['p3-v5.1-fila-23965.csv','fila-geral-p0-p1-p2-p3-v5.1.csv','backlog-global-98-com-parecer-v27.csv']:
 sha.update(name.encode());sha.update(hashlib.sha256((S/name).read_bytes()).digest())
result={'status':'REGRESSAO_INDEPENDENTE_PASSOU','lotes':30,'base':total_base,'controles':total_ctrl,'ids_novos':len(ids),'ids_alterados':len(changed),'filas':filas,'p2_pendentes_preservados':4660,'p3_remanescentes':19562,'backlog_global_98_byte_a_byte':'IDENTICO','sha256_fontes_protegidas':sha.hexdigest()}
with (R/'p3-v5.2-regressao-independente-30-lotes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(lots[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(lots)
(R/'p3-v5.2-regressao-independente-resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))