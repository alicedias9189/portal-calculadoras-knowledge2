#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressão independente P3 v1.2->v1.3; usa ZIPs e CSVs realmente gravados."""
import csv,io,json,zipfile,collections,hashlib,sys,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--fonte',type=Path,default=BASE/'source/08-Entregas/P3-v1.2')
ap.add_argument('--saida',type=Path,default=BASE/'out')
args=ap.parse_args()
SRC=args.fonte
OUT=args.saida
CHANGABLE={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
TRACK=['status_p3_v1_3','regra_p3_v1_3','justificativa_p3_v1_3','area_final_p3_v1_3','cluster_final_p3_v1_3','subcluster_final_p3_v1_3','tipo_intencao_final_p3_v1_3','classificacao_alterada_p3_v1_3']

def rows(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def hashes(b):return hashlib.sha256(b).hexdigest()
p=rows((OUT/'p3-v1.3-patches.csv').read_bytes());ids={x['id_global'] for x in p};assert len(ids)==len(p)
qa=rows((OUT/'p3-v1.3-decisoes-por-id.csv').read_bytes());reg=collections.Counter();new_modified=set(); lrows=[];base=ctrl=0
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v1.2.zip') as zin,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v1.3.zip') as zout:
 a=zin.namelist();b=zout.namelist();assert len(a)==len(b)==30
 for old,new in zip(a,b):
  A=rows(zin.read(old));B=rows(zout.read(new));assert len(A)==len(B),(old,len(A),len(B))
  changed=[]; protected=hashlib.sha256(); protected_new=hashlib.sha256()
  for x,y in zip(A,B):
   assert set(x)==set(y) and x['id_global']==y['id_global'] and x['tipo_registro']==y['tipo_registro']
   delta={k for k in x if x[k]!=y[k]};assert delta<=CHANGABLE,(x['id_global'],delta)
   assert not delta or x['id_global'] in ids
   if x['tipo_registro']!='base':assert x==y;ctrl+=1
   else:base+=1
   if delta:
    changed.append(x['id_global']);new_modified.add(x['id_global'])
    rec=next(t for t in p if t['id_global']==x['id_global']);act=json.loads(rec['antes_json']);nxt=json.loads(rec['depois_json']);assert set(act)==delta==set(nxt)
    assert all(x[k]==v for k,v in act.items()) and all(y[k]==v for k,v in nxt.items())
   old_prot=json.dumps([x[k] for k in x if k not in CHANGABLE],ensure_ascii=False,separators=(',',':')).encode('utf-8')
   new_prot=json.dumps([y[k] for k in y if k not in CHANGABLE],ensure_ascii=False,separators=(',',':')).encode('utf-8')
   protected.update(old_prot+b'\n');protected_new.update(new_prot+b'\n')
  assert protected.digest()==protected_new.digest()
  lrows.append({'lote':old,'registros':len(A),'bases':sum(x['tipo_registro']=='base' for x in A),'controles':sum(x['tipo_registro']!='base' for x in A),'IDs_modificados':len(changed),'hash_SHA256_campos_protegidos':protected.hexdigest(),'resultado':'PASSOU'})
assert base==294905 and ctrl==2190
assert new_modified==ids,(len(new_modified),len(ids))
assert len(qa)==319 and len(p)==317
for oldfile,newfile in [('p3-v1.2-fila-23965.csv','p3-v1.3-fila-23965.csv'),('fila-geral-p0-p1-p2-p3-v1.2.csv','fila-geral-p0-p1-p2-p3-v1.3.csv')]:
 old=rows((SRC/oldfile).read_bytes());new=rows((OUT/newfile).read_bytes());assert len(old)==len(new);assert list(new[0])==list(old[0])+TRACK
 for x,y in zip(old,new):assert all(x[k]==y[k] for k in x)
 assert {x['id_global'] for x in new if x['classificacao_alterada_p3_v1_3']=='sim'}==ids
with open(OUT/'regressao-independente-30-lotes-p3-v1.3.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(lrows[0]),delimiter=';');w.writeheader();w.writerows(lrows)
print(json.dumps({'status':'PASSOU','lotes':30,'bases':base,'controles':ctrl,'patches':len(p),'decisoes':len(qa),'fila_p3':23965,'protegidos_iguais':True,'patches_exatos':True,'filas_colunas_historicas_iguais':True},ensure_ascii=False))
