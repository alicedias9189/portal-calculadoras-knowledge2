#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reabre fontes v3.0, destino v3.1, filas e patches e verifica TODOS os registros.
Independente da implementação do script de auditoria. Usa somente biblioteca padrão.
"""
from pathlib import Path
import csv,io,zipfile,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v3.1/FONTES-REPRODUCAO/08-Entregas/P3-v3.0'
OUT=ROOT/'08-Entregas/P3-v3.1'
VALID={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta'}

def csv_path(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def csv_zip(z,n):
 txt=z.read(n).decode('utf-8-sig');rd=csv.DictReader(io.StringIO(txt),delimiter=';');return list(rd),list(rd.fieldnames)
def write(path,rows,fields):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,delimiter=';',fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
patches,_=csv_path(OUT/'p3-v3.1-patches.csv');byid={p['id_global']:p for p in patches}
assert len(byid)==len(patches)==8
beforehash=hashlib.sha256();afterhash=hashlib.sha256()
base=ctrl=0;changed=set();qa=[]
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v3.0.zip') as za,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v3.1.zip') as zb:
 assert za.testzip() is None and zb.testzip() is None and len(za.namelist())==len(zb.namelist())==30
 for oldname in za.namelist():
  newname=oldname.replace('v3.0','v3.1')
  oldrows,oldcols=csv_zip(za,oldname);newrows,newcols=csv_zip(zb,newname)
  assert oldcols==newcols and len(oldrows)==len(newrows)
  nb=nc=na=0
  for p,q in zip(oldrows,newrows):
   assert p['id_global']==q['id_global'] and p['tipo_registro']==q['tipo_registro']
   if p['tipo_registro']=='base':nb+=1
   else:nc+=1
   dif={k for k in p if p[k]!=q[k]}
   assert not dif or (p['tipo_registro']=='base' and p['id_global'] in byid and dif<=VALID),(oldname,p['id_global'],dif)
   if dif:
    rid=p['id_global']; pp=byid[rid]
    assert rid not in changed and set(pp['campos_modificados'].split(','))==dif
    assert json.loads(pp['antes_json'])=={k:p[k] for k in dif}
    assert json.loads(pp['depois_json'])=={k:q[k] for k in dif}
    assert pp['Keyword']==p['Keyword']==q['Keyword'] and pp['familia_id']==p['familia_id']
    changed.add(rid);na+=1
   for k in oldcols:
    if k not in VALID:
     beforehash.update((k+'\0'+p[k]+'\x1e').encode());afterhash.update((k+'\0'+q[k]+'\x1e').encode())
  qa.append({'lote':oldname,'registros_base':nb,'controles':nc,'patches_verificados':na,'status':'PASSOU'})
  base+=nb;ctrl+=nc
assert changed==set(byid) and (base,ctrl)==(294905,2190) and beforehash.hexdigest()==afterhash.hexdigest()
# Every existing field and row in both queues preserved; only 8 new tracking cols added.
queues={}
for oldname,newname,count in [
 ('p3-v3.0-fila-23965.csv','p3-v3.1-fila-23965.csv',23965),
 ('fila-geral-p0-p1-p2-p3-v3.0.csv','fila-geral-p0-p1-p2-p3-v3.1.csv',52046),
]:
 old,oldfields=csv_path(SRC/oldname);new,newfields=csv_path(OUT/newname)
 assert len(old)==len(new)==count and newfields[:len(oldfields)]==oldfields and len(newfields)-len(oldfields)==8
 changes_in_queue=set()
 for r,s in zip(old,new):
  assert r['id_global']==s['id_global'] and all(r[k]==s[k] for k in oldfields),(oldname,r['id_global'])
  if r['id_global'] in byid:
   assert s['classificacao_alterada_p3_v3_1']=='sim';changes_in_queue.add(r['id_global'])
 assert changes_in_queue==changed
 queues[oldname]=count
# Global quarantine unchanged byte-to-byte.
a=SRC/'backlog-global-98-com-parecer-v27.csv';b=OUT/'backlog-global-98-com-parecer-v27.csv'
assert a.read_bytes()==b.read_bytes()
# Semantically reviewed 36 entries, exactly the v3.0 decision set.
review,_=csv_path(OUT/'p3-v3.1-pareceres-36.csv');orig,_=csv_path(SRC/'p3-v3.0-decisoes.csv')
assert len(review)==len(orig)==36
assert {r['id_global'] for r in orig}=={r['id_global'] for r in review}
assert collections.Counter(r['parecer_p3_v3_1'] for r in review)=={'CORRIGIDO':8,'MANTIDO_COM_RESSALVA':28}
write(OUT/'p3-v3.1-regressao-independente-30-lotes.csv',qa,list(qa[0]))
summary={'status':'PASSOU','lotes':30,'bases':base,'controles':ctrl,'patches_verificados':len(changed),
 'pareceres_verificados':36,'fila_P3':23965,'fila_geral':52046,'colunas_historicas':'identicas',
 'backlog_global_98':'identico_byte_a_byte','sha256_campos_protegidos':beforehash.hexdigest(),
 'observacao':'Não é homologação editorial; revisão técnica por ID de 36 decisões já classificadas'}
(OUT/'p3-v3.1-regressao-independente-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
