#!/usr/bin/env python3
"""Verificação independente P3 v1.4 linha a linha; não usa classificador de regras."""
import argparse,csv,io,json,hashlib,zipfile,collections
from pathlib import Path
ALLOW={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
def read_csv(data):return list(csv.DictReader(io.StringIO(data.decode('utf-8-sig')),delimiter=';'))
def csvpath(p):return read_csv(p.read_bytes())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--antes',type=Path,required=True);ap.add_argument('--depois',type=Path,required=True);a=ap.parse_args();p=a.depois
 patches=csvpath(p/'p3-v1.4-patches.csv');expected={x['id_global']:x for x in patches}; assert len(expected)==len(patches) and len(patches)>0
 with zipfile.ZipFile(a.antes) as za,zipfile.ZipFile(p/'lotes-001-a-030-p3-v1.4.zip') as zb:
  aa=sorted(za.namelist());bb=sorted(zb.namelist());assert len(aa)==len(bb)==30
  rep=[];seen=set();base=controls=0;fullprotected=hashlib.sha256()
  for before,after in zip(aa,bb):
   ra=read_csv(za.read(before));rb=read_csv(zb.read(after));assert len(ra)==len(rb);assert [x['id_global'] for x in ra]==[x['id_global'] for x in rb]
   changed=[];controllot=0;baselot=0
   for x,y in zip(ra,rb):
    assert list(x)==list(y)
    id_=x['id_global'];diff={k for k in x if x[k]!=y[k]}
    if x['tipo_registro']!='base':
     controls+=1;controllot+=1;assert not diff;continue
    base+=1;baselot+=1
    assert diff.issubset(ALLOW),(id_,diff-ALLOW)
    if diff:
     assert id_ in expected;assert id_ not in seen;seen.add(id_);changed.append(id_)
     q=expected[id_];assert q['Keyword']==x['Keyword'] and q['familia_id']==x['familia_id']
     assert diff==set(q['campos_alterados'].split(',')),(id_,diff,q['campos_alterados'])
     old=json.loads(q['antes_json']);new=json.loads(q['depois_json'])
     assert all(x[k]==v for k,v in old.items())
     assert all(y[k]==v for k,v in new.items())
    else:assert id_ not in expected
    protected={k:x[k] for k in x if k not in ALLOW};assert protected=={k:y[k] for k in y if k not in ALLOW}
    fullprotected.update(json.dumps(protected,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode());fullprotected.update(b'\n')
   rep.append({'arquivo_fonte':before,'arquivo_saida':after,'base':baselot,'controles':controllot,'alterados':len(changed),'status':'PASSOU'})
 assert seen==set(expected),(len(seen),len(expected),list(set(expected)-seen)[:5]);assert (base,controls)==(294905,2190)
 import csv
 path=p/'regressao-independente-30-lotes-p3-v1.4.csv'
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rep[0]),delimiter=';');w.writeheader();w.writerows(rep)
 j={'status':'PASSOU','base':base,'controles':controls,'patches':len(seen),'lotes':len(rep),'sha256_colunas_protegidas':fullprotected.hexdigest()}
 (p/'regressao-independente-resumo-v1.4.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(j,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
