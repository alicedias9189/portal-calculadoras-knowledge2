#!/usr/bin/env python3
# coding: utf-8
"""Validação independente P3 v2.1: os únicos campos que podem mudar são analíticos, nos IDs listados.
Reabre os ZIPs e CSVs originais e finais em vez de confiar na trilha gerada pelo auditor.
"""
import pathlib,csv,zipfile,io,json,collections,hashlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
A=ROOT/'08-Entregas/P3-v2.1/FONTES-REPRODUCAO/08-Entregas/P3-v2.0';B=ROOT/'08-Entregas/P3-v2.1'
with (B/'p3-v2.1-patches.csv').open(encoding='utf-8-sig',newline='') as f:diffs=list(csv.DictReader(f,delimiter=';'))
byid={q['id_global']:q for q in diffs};assert len(byid)==len(diffs)==13
VALID={'area_principal','cluster','subcluster','dominio_ou_grandeza','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta'}

def rows_from_zip(z,name):
 return list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';'))
summary=[];changed=set();protected_before=hashlib.sha256();protected_after=hashlib.sha256()
with zipfile.ZipFile(A/'lotes-001-a-030-p3-v2.0.zip') as za, zipfile.ZipFile(B/'lotes-001-a-030-p3-v2.1.zip') as zb:
 assert len(za.namelist())==len(zb.namelist())==30
 for oldname in za.namelist():
  newname=oldname.replace('v2.0','v2.1');x=rows_from_zip(za,oldname);y=rows_from_zip(zb,newname)
  assert len(x)==len(y); nbase=nctrl=nchanges=0
  for p,q in zip(x,y):
   assert p.keys()==q.keys() and p['id_global']==q['id_global'] and p['tipo_registro']==q['tipo_registro']
   if p['tipo_registro']=='base':nbase+=1
   else:nctrl+=1
   unexpected=[f for f in p if p[f]!=q[f] and (p['id_global'] not in byid or f not in VALID)]
   assert not unexpected,(oldname,p['id_global'],unexpected)
   if p!=q:
    assert p['tipo_registro']=='base';id=p['id_global'];d=byid[id]
    assert id not in changed;changed.add(id);nchanges+=1
    fields=set(d['campos_modificados'].split(','));actual={f for f in p if p[f]!=q[f]};assert fields==actual,(id,fields,actual)
    assert json.loads(d['antes_json'])=={f:p[f] for f in fields}
    assert json.loads(d['depois_json'])=={f:q[f] for f in fields}
   for f in p:
    if f not in VALID:
     protected_before.update((f+'\x00'+p[f]+'\x1e').encode())
     protected_after.update((f+'\x00'+q[f]+'\x1e').encode())
  summary.append(dict(lote=oldname,base=nbase,controles=nctrl,alteracoes=nchanges,protegidos_ok='SIM',status='PASSOU'))
assert changed==set(byid)
assert sum(v['base'] for v in summary)==294905 and sum(v['controles'] for v in summary)==2190
assert protected_before.hexdigest()==protected_after.hexdigest()
# Fila P3 e geral: garantir colunas antigas byte a byte por valor (em cada ID), e só campos v2.1 preenchidos para a amostra completa das 272 decisões.
for nam1,nam2,nrows in [('p3-v2.0-fila-23965.csv','p3-v2.1-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v2.0.csv','fila-geral-p0-p1-p2-p3-v2.1.csv',52046)]:
 with (A/nam1).open(encoding='utf-8-sig',newline='') as f: before=list(csv.DictReader(f,delimiter=';'))
 with (B/nam2).open(encoding='utf-8-sig',newline='') as f: after=list(csv.DictReader(f,delimiter=';'))
 assert len(before)==len(after)==nrows
 for old,new in zip(before,after):
  assert old['id_global']==new['id_global']
  assert all(old[k]==new[k] for k in old),(old['id_global'],nam1)
  assert len(new)-len(old)==8
  if old['id_global'] in byid: assert new['classificacao_alterada_p3_v2_1']=='sim'
# Amostra e pareceres
with (B/'p3-v2.1-revisao-amostra-165.csv').open(encoding='utf-8-sig',newline='') as f: sample=list(csv.DictReader(f,delimiter=';'))
assert len(sample)==165
summary_data={'status':'PASSOU','lotes':len(summary),'base':294905,'controles':2190,'alteracoes':len(changed),'alteracoes_na_amostra':sum(x['parecer_qa_p3_v2_1']=='CORRIGIDO' for x in sample),'sha256_protegidos':protected_before.hexdigest(),'filas':'23965 + 52046; colunas históricas preservadas','observacao':'Revisão semântica por ID sem homologação editorial; ZIPs comparados integralmente'}
with (B/'p3-v2.1-regressao-independente.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,delimiter=';',fieldnames=list(summary[0]),lineterminator='\n');w.writeheader();w.writerows(summary)
(B/'p3-v2.1-regressao-independente.json').write_text(json.dumps(summary_data,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(summary_data,ensure_ascii=False))
