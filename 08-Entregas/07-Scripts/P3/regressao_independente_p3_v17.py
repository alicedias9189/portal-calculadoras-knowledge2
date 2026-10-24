#!/usr/bin/env python3
# coding: utf-8
"""Regressão independente por conteúdo linha a linha contra P3 v1.6; stdlib.
python3 regressao_independente_p3_v17.py --fonte <raiz-fontes> --saida <dir-saida>
"""
import argparse,csv,io,json,zipfile,collections,hashlib
from pathlib import Path
CAN=('area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta')
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def zipread(z,n):return csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig',newline=''),delimiter=';')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args()
 src=a.fonte/'08-Entregas/P3-v1.6';out=a.saida
 patch=readcsv(out/'p3-v1.7-patches.csv');patchbyid={r['id_global']:r for r in patch};assert len(patch)==len(patchbyid)==17
 rows=[];checked=set();totbase=totctrl=0;violations=[]
 with zipfile.ZipFile(src/'lotes-001-a-030-p3-v1.6.zip') as old,zipfile.ZipFile(out/'lotes-001-a-030-p3-v1.7.zip') as new:
  oldnames=sorted(old.namelist());newnames=sorted(new.namelist());assert len(oldnames)==len(newnames)==30
  for oname,nname in zip(oldnames,newnames):
   assert nname==oname.replace('v1.6','v1.7')
   r1=zipread(old,oname);r2=zipread(new,nname);assert r1.fieldnames==r2.fieldnames
   rb=rc=changed=0
   for i,(x,y) in enumerate(zip(r1,r2),2):
    if x['id_global']!=y['id_global'] or x['Keyword']!=y['Keyword']:raise AssertionError(('id mismatch',oname,i))
    id=x['id_global'];diff={k for k in x if x[k]!=y[k]}
    if x['tipo_registro']!='base':
     rc+=1;totctrl+=1;assert not diff,('controle modificado',oname,id)
    else:
     rb+=1;totbase+=1
     if diff:
      assert id in patchbyid,('fora-do-alvo',oname,id,sorted(diff))
      assert diff<=set(CAN),('coluna protegida',oname,id,sorted(diff))
      assert id not in checked,('id duplicado',id)
      p=patchbyid[id];assert p['Keyword']==x['Keyword'] and p['lote']==x['lote_id']
      before=json.loads(p['antes_json']);after=json.loads(p['depois_json'])
      assert set(before)==set(after)==diff==set(p['campos_alterados'].split(',')),('patch diffs',id,diff,before)
      for k in diff:assert x[k]==before[k] and y[k]==after[k],('patch valor',id,k)
      checked.add(id);changed+=1
   rows.append({'lote':oname.split('/')[-1].split('-')[1], 'registros_base':rb,'controles':rc,'alteracoes':changed,'status':'PASSOU'})
 assert totbase==294905 and totctrl==2190,(totbase,totctrl)
 assert checked==set(patchbyid),('patches inconsistentes',len(checked))
 # Duas filas devem manter os campos anteriores exatamente; apenas trilha analítica v1.7 acrescentada.
 for name,nrows in [('p3-v1.6-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v1.6.csv',52046)]:
  with (src/name).open(encoding='utf-8-sig',newline='') as f1,(out/name.replace('v1.6','v1.7')).open(encoding='utf-8-sig',newline='') as f2:
   r1=csv.DictReader(f1,delimiter=';');r2=csv.DictReader(f2,delimiter=';');c1=r1.fieldnames;c2=r2.fieldnames
   assert c2[:len(c1)]==c1
   count=marked=0
   for x,y in zip(r1,r2):
    assert all(x[c]==y[c] for c in c1),('fila historica alterada',name,x['id_global'])
    track={c:y[c] for c in c2[len(c1):]};id=x['id_global']
    if id in checked:assert track['classificacao_alterada_p3_v1_7']=='sim' and track['regra_p3_v1_7'];marked+=1
    else:assert not any(track.values()),('trilha em nao-alvo',name,id)
    count+=1
   assert count==nrows and marked==17,(name,count,marked)
 outcsv=out/'p3-v1.7-regressao-independente-30-lotes.csv'
 with outcsv.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
 summary={'status':'PASSOU','lotes':30,'registros_base':totbase,'controles':totctrl,'patches_exatos':len(checked),'campos_protegidos_alterados':0,'IDs_fora_do_alvo_alterados':0,'filas_conferidas':['23965 P3','52046 fila de revisao geral'],'verificacao':'Comparacao independente integral entre ZIPs por coluna, confronto exato dos 17 patches e trilhas das duas filas.'}
 (out/'p3-v1.7-regressao-independente-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
