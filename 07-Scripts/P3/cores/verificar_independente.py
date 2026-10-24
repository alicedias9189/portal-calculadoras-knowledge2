#!/usr/bin/env python3
"""Validação independente sem copiar a lógica de reconhecimento de cores."""
import zipfile,csv,io,json,hashlib,collections,sys,argparse
from pathlib import Path
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Verifica a visão derivada com a fonte P3 v5.2 original')
parser.add_argument('--p3-zip',required=True,help='Caminho para o ZIP canônico P3 v5.2')
args=parser.parse_args()
archive=zipfile.ZipFile(args.p3_zip)
f=lambda suffix:next(x for x in archive.namelist() if x.endswith('/'+suffix))
with (root/'ids-ouro-excluir-3609.csv').open(encoding='utf-8-sig',newline='') as r:
 ids={x['id_global'] for x in csv.DictReader(r,delimiter=';')}
assert len(ids)==3609
with (root/'ids-ouro-revisar-12.csv').open(encoding='utf-8-sig',newline='') as r:
 review={x['id_global'] for x in csv.DictReader(r,delimiter=';')}
assert len(review)==12 and ids.isdisjoint(review)
orig=zipfile.ZipFile(io.BytesIO(archive.read(f('lotes-001-a-030-p3-v5.2.zip'))))
deriv=zipfile.ZipFile(root/'lotes-30-trabalho-sem-ouro.zip')
assert set(orig.namelist())==set(deriv.namelist())
from itertools import filterfalse
observed=set();retained=removed=ctrl=0
for name in orig.namelist():
 def load(z):return csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig',newline=''),delimiter=';')
 base=load(orig);from_files=load(deriv)
 after=iter(from_files)
 for r in base:
  if r['id_global'] in ids:
   assert r['tipo_registro']=='base';observed.add(r['id_global']);removed+=1
  else:
   x=next(after,None)
   assert x is not None,(name,r['id_global'])
   assert x==r,(name,r['id_global'])
   if r['tipo_registro']=='base':retained+=1
   else:ctrl+=1
 assert next(after,None) is None,name
assert (removed,retained,ctrl)==(3609,291296,2190)
assert observed==ids

def check_queue(source_file,target_file,expected_removed):
 source=csv.DictReader(io.TextIOWrapper(archive.open(f(source_file)),encoding='utf-8-sig',newline=''),delimiter=';')
 with (root/target_file).open(encoding='utf-8-sig',newline='') as k:
  target=csv.DictReader(k,delimiter=';'); assert source.fieldnames==target.fieldnames
  j=iter(target);rem=set();n=0
  for r in source:
   if r['id_global'] in expected_removed:
    rem.add(r['id_global'])
   else:
    v=next(j,None)
    assert v==r,(source_file,r['id_global'])
    n+=1
  assert next(j,None) is None
  return n,rem
with (root/'ids-p3-ouro-removidos-100.csv').open(encoding='utf-8-sig',newline='') as k:
 p3_ids={r['id_global'] for r in csv.DictReader(k,delimiter=';')}
assert len(p3_ids)==100 and p3_ids<=ids
n_p3,ids_p3=check_queue('p3-v5.2-fila-23965.csv','fila-p3-v5.2-sem-ouro-23865.csv',p3_ids)
assert (n_p3,len(ids_p3))==(23865,100), (n_p3,len(ids_p3))
n_gen,ids_gen=check_queue('fila-geral-p0-p1-p2-p3-v5.2.csv','fila-geral-v5.2-sem-ouro-51884.csv',ids)
assert (n_gen,len(ids_gen))==(51884,162), (n_gen,len(ids_gen))
print('PASSOU: 30/30 lotes; bases mantidas 291296; excluidas 3609; controles 2190; fila P3 removeu 100 (23865 restantes); geral removeu 162 (51884 restantes).')