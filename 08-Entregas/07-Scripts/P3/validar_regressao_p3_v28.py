#!/usr/bin/env python3
"""Regressão independente P3 v2.8; verifica lotes, patches, filas, escopo P3 e global."""
import pathlib,csv,zipfile,io,hashlib,json,collections
ROOT=pathlib.Path(__file__).resolve().parents[2]
E=ROOT/'08-Entregas/P3-v2.8';S=E/'FONTES-REPRODUCAO/08-Entregas/P3-v2.7'
ALLOWED={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}

def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def zi(z,name):
 return list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';'))
def write(path,rows):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
patches=read(E/'p3-v2.8-patches.csv');byid={r['id_global']:r for r in patches}
assert len(patches)==len(byid), 'Patches duplicados'
p3=read(S/'p3-v2.7-fila-23965.csv');general=read(S/'fila-geral-p0-p1-p2-p3-v2.7.csv')
p3map={r['id_global']:r for r in p3}; genmap={r['id_global']:r for r in general}
global_rows=read(S/'backlog-global-98-com-parecer-v27.csv')
global_ids={r['id_global'] for r in global_rows}
assert len(p3map)==23965 and len(genmap)==52046 and len(global_ids)==98
assert not global_ids.intersection(byid)
for rid,p in byid.items():
 assert rid in p3map and rid in genmap
 assert p3map[rid]['prioridade']==genmap[rid]['prioridade']=='P3'
 assert p3map[rid]['status_p3_v1']=='FORA_DO_PILOTO'
 assert p3map[rid]['Keyword']==p['Keyword']==genmap[rid]['Keyword']
 assert p3map[rid]['familia_id']==p['familia_id']==genmap[rid]['familia_id']
 assert p3map[rid]['lote']==genmap[rid]['lote']==p['lote']
assert len(read(E/'p3-v2.8-revisao-qa-integral.csv'))==len(byid)
changed=set();hb=hashlib.sha256();ha=hashlib.sha256();reg=[]
with zipfile.ZipFile(S/'lotes-001-a-030-p3-v2.7.zip') as a,zipfile.ZipFile(E/'lotes-001-a-030-p3-v2.8.zip') as b:
 assert len(a.namelist())==len(b.namelist())==30
 for oldname in a.namelist():
  x=zi(a,oldname);y=zi(b,oldname.replace('v2.7','v2.8'))
  assert len(x)==len(y)
  nb=nc=md=0
  for old,new in zip(x,y):
   assert list(old)==list(new) and old['tipo_registro']==new['tipo_registro'] and old['id_global']==new['id_global']
   if old['tipo_registro']=='base':nb+=1
   else:nc+=1
   diff={f for f in old if old[f]!=new[f]}
   if diff:
    rid=old['id_global'];assert rid in byid and diff<=ALLOWED and old['tipo_registro']=='base', (oldname,rid,diff)
    p=byid[rid];assert rid not in changed
    changed.add(rid);md+=1
    assert diff==set(p['campos_modificados'].split(','))
    assert {f:old[f] for f in diff}==json.loads(p['antes_json'])
    assert {f:new[f] for f in diff}==json.loads(p['depois_json'])
    assert old['familia_id']==p['familia_id'] and old['Keyword']==p['Keyword']
   for f in old:
    if f not in ALLOWED:
     hb.update((f+'\0'+old[f]+'\x1e').encode())
     ha.update((f+'\0'+new[f]+'\x1e').encode())
  reg.append({'lote':oldname,'base':nb,'controles':nc,'alteracoes':md,'campos_protegidos':'OK','status':'PASSOU'})
assert set(byid)==changed
assert sum(r['base'] for r in reg)==294905 and sum(r['controles'] for r in reg)==2190
assert sum(r['alteracoes'] for r in reg)==len(byid) and hb.hexdigest()==ha.hexdigest()
write(E/'p3-v2.8-regressao-independente.csv',reg)
# For queues, guarantee all 196 former fields are unchanged, every row in original order.
for old,new,count in [('p3-v2.7-fila-23965.csv','p3-v2.8-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.7.csv','fila-geral-p0-p1-p2-p3-v2.8.csv',52046)]:
 x=read(S/old);y=read(E/new);assert len(x)==len(y)==count
 newcols=set(y[0])-set(x[0]);assert len(newcols)==8
 for a,b in zip(x,y):
  assert a['id_global']==b['id_global']
  assert all(a[k]==b[k] for k in a),('histórico divergente',old,a['id_global'])
  if a['id_global'] in byid:assert b['classificacao_alterada_p3_v2_8']=='sim'
  else:assert all(b[k]=='' for k in newcols)
# global proposals byte-identically copied and not promoted
assert (S/'backlog-global-98-com-parecer-v27.csv').read_bytes()==(E/'backlog-global-98-com-parecer-v27.csv').read_bytes()
# Actual count of untouched P3 in v2.7 (not previously reported aggregate)
HIST=['status_p3_v1_3','status_p3_v1_4','status_p3_v1_5','status_p3_v1_6','status_p3_v1_8','status_p3_v2_0','status_p3_v2_2','status_p3_v2_6']
base_untouched=[q for q in p3 if q['status_p3_v1']=='FORA_DO_PILOTO' and not any(q[c] for c in HIST)]
assert len(base_untouched)==20374
assert len({q['id_global'] for q in base_untouched}-changed)==20374-len(byid)
res={'status':'PASSOU','lotes':30,'base':294905,'controles':2190,'alteracoes':len(byid),'P3_v27_untouched_recomputed':20374,'P3_v28_untouched':20374-len(byid),
 'historical_report_v27':20383,'diferenca_historico':9,'globais_bloqueadas':98,'p2_pendentes':4660,'sha256_campos_protegidos':hb.hexdigest(),'filas':'23965 e 52046; 100% das colunas históricas mantidas'}
(E/'p3-v2.8-regressao-independente.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
s=(E/'p3-v2.8-resumo.json');data=json.loads(s.read_text(encoding='utf-8'));data['status']='PASSOU';data['regressao_independente']=res;s.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False))
