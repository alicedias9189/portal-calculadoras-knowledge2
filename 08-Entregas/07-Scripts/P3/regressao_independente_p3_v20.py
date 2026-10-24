#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent P3 v2.0 comparison without using classification rules. stdlib only."""
import argparse,csv,io,json,zipfile,collections
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--resultado',type=Path,required=True);a=ap.parse_args()
BASE=a.base;O=a.resultado
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta'}
PATCH=O/'p3-v2.0-patches.csv'
def readfile(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r),r.fieldnames
patches,_=readfile(PATCH);pm={p['id_global']:p for p in patches}
assert len(pm)==len(patches)>0
oldzip=BASE/'lotes-001-a-030-p3-v1.9.zip';newzip=O/'lotes-001-a-030-p3-v2.0.zip'
rowsum=collections.Counter();idseen=set();qa=[]
with zipfile.ZipFile(oldzip) as z0, zipfile.ZipFile(newzip) as z1:
 oldnames=sorted(x for x in z0.namelist() if x.endswith('.csv'))
 newnames=sorted(x for x in z1.namelist() if x.endswith('.csv'))
 assert len(oldnames)==len(newnames)==30
 for i,(n0,n1) in enumerate(zip(oldnames,newnames),1):
  a0=list(csv.DictReader(io.StringIO(z0.read(n0).decode('utf-8-sig')),delimiter=';'))
  a1=list(csv.DictReader(io.StringIO(z1.read(n1).decode('utf-8-sig')),delimiter=';'))
  assert len(a0)==len(a1)
  b=c=m=0
  for r0,r1 in zip(a0,a1):
   assert r0['tipo_registro']==r1['tipo_registro'] and r0['id_global']==r1['id_global']
   assert set(r0)==set(r1)
   if r0['tipo_registro']=='controle':c+=1;assert r0==r1
   else:
    b+=1
    idg=r0['id_global']
    if idg in pm:
     assert idg not in idseen
     idseen.add(idg)
     assert pm[idg]['Keyword']==r0['Keyword'] and pm[idg]['lote']==r0['lote_id']
     before=json.loads(pm[idg]['antes_json']);after=json.loads(pm[idg]['depois_json']);diff=json.loads(pm[idg]['diff_json'])
     assert set(before)==set(after)==EDIT
     assert {k:r0[k] for k in EDIT}==before
     assert {k:r1[k] for k in EDIT}==after
     assert set(diff)=={k for k in EDIT if r0[k]!=r1[k]}
     assert all(r0[k]==r1[k] for k in r0 if k not in EDIT)
     if r1['tipo_intencao']=='conversão direta':assert r1['unidade_origem'] and r1['unidade_destino'] and r1['direcao_conversao']
     m+=1
    else:assert r0==r1
  assert c==73
  rowsum.update({'base':b,'controle':c,'patches':m})
  qa.append({'lote':f'{i:03d}','base':b,'controles':c,'patches':m,'status':'PASSOU'})
assert idseen==set(pm)
assert rowsum['base']==294905 and rowsum['controle']==2190
assert rowsum['patches']==len(pm)

# Previous 149 queue columns must be byte-value equal for all 23,965 or 52,046 rows.
checks={}
for basename,dest,count in [('p3-v1.9-fila-23965.csv','p3-v2.0-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v1.9.csv','fila-geral-p0-p1-p2-p3-v2.0.csv',52046)]:
 old,oldkeys=readfile(BASE/basename);new,newkeys=readfile(O/dest)
 assert len(old)==len(new)==count and len(newkeys)==len(oldkeys)+8 and newkeys[:len(oldkeys)]==oldkeys
 impacted=set()
 for a,b in zip(old,new):
  assert all(a[k]==b[k] for k in oldkeys)
  if b['classificacao_alterada_p3_v2_0']=='sim':
   assert a['id_global'] in pm and a['prioridade']=='P3'
   impacted.add(a['id_global'])
  else:
   assert all(not b[k] for k in newkeys[len(oldkeys):])
 assert impacted==set(pm)
 checks[dest]={'linhas':count,'colunas_anteriores':len(oldkeys),'colunas_atualizadas':len(newkeys),'patches':len(impacted),'regressao_historica':'PASSOU'}

# Reproduced structured outputs match counts and statuses.
summary=json.loads((O/'p3-v2.0-resumo.json').read_text(encoding='utf-8'))
assert summary['reclassificados']==len(pm) and summary['pendentes_fora_pilotos_depois']==20672-len(pm)
res={'status':'PASSOU','lotes':30,'base':rowsum['base'],'controles':rowsum['controle'],'patches':rowsum['patches'],'filas':checks,'limite':'Compara integridade, não homologa decisões semânticas.'}
(O/'p3-v2.0-regressao-independente-resumo.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (O/'p3-v2.0-regressao-independente-30-lotes.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(qa[0]),delimiter=';');w.writeheader();w.writerows(qa)
print(json.dumps(res,ensure_ascii=False))
