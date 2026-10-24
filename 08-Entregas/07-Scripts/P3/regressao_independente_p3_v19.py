#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressão independente da geração P3 v1.9: compara ZIPs e filas anteriores.
Uso: python3 regressao_independente_p3_v19.py --fonte /RAIZ --saida /SAIDA
Sem importação do script de classificação; apenas Python stdlib.
"""
import argparse,csv,io,json,zipfile,collections
from pathlib import Path
ALLOWED={'tipo_intencao','intencao_principal','confianca','justificativa_curta'}
TRACK=['status_p3_v1_9','parecer_p3_v1_9','nota_qa_p3_v1_9','area_final_p3_v1_9','cluster_final_p3_v1_9','subcluster_final_p3_v1_9','tipo_intencao_final_p3_v1_9','classificacao_alterada_p3_v1_9']
def records(blob):return list(csv.DictReader(io.StringIO(blob.decode('utf-8-sig')),delimiter=';'))
def get(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',required=True,type=Path);ap.add_argument('--saida',required=True,type=Path);a=ap.parse_args()
 old=a.fonte/'08-Entregas/P3-v1.8';new=a.saida
 patches=get(new/'p3-v1.9-patches-10.csv'); expected={p['id_global']:p for p in patches}; assert len(expected)==10
 reviewed=get(new/'p3-v1.9-pareceres-83.csv'); assert len(reviewed)==len({r['id_global'] for r in reviewed})==83
 exact_ids=set(expected);seen=set();counts=[];base=ctrl=0
 with zipfile.ZipFile(old/'lotes-001-a-030-p3-v1.8.zip') as a1, zipfile.ZipFile(new/'lotes-001-a-030-p3-v1.9.zip') as a2:
  n1=sorted(a1.namelist());n2=sorted(a2.namelist());assert len(n1)==len(n2)==30
  for f1,f2 in zip(n1,n2):
   assert f2==f1.replace('v1.8','v1.9')
   x=records(a1.read(f1));y=records(a2.read(f2));assert len(x)==len(y)
   changed=bc=cc=0
   for u,v in zip(x,y):
    assert list(u)==list(v)
    assert u['id_global']==v['id_global'] and u['Keyword']==v['Keyword']
    if u['tipo_registro']!='base':assert u==v;cc+=1;ctrl+=1;continue
    bc+=1;base+=1; diff={k:(u[k],v[k]) for k in u if u[k]!=v[k]};rid=u['id_global']
    if rid not in exact_ids:assert not diff,(f1,rid,diff)
    else:
     assert diff and set(diff)<=ALLOWED,(rid,diff);p=expected[rid]
     assert set(p['campos_alterados'].split(','))==set(diff)
     assert json.loads(p['antes_json'])=={k:z[0] for k,z in diff.items()}
     assert json.loads(p['depois_json'])=={k:z[1] for k,z in diff.items()}
     if u['unidade_origem'] or u['unidade_destino']:
      assert v['unidade_origem']==u['unidade_origem'] and v['unidade_destino']==u['unidade_destino'] and v['direcao_conversao']==u['direcao_conversao']
     assert rid not in seen;seen.add(rid);changed+=1
   counts.append({'lote':f1,'registros_base':bc,'controles':cc,'patches':changed,'status':'PASSOU'})
 assert seen==exact_ids and base==294905 and ctrl==2190
 qcounts={}
 for oldname in ['p3-v1.8-fila-23965.csv','fila-geral-p0-p1-p2-p3-v1.8.csv']:
  pold=old/oldname;pnew=new/oldname.replace('v1.8','v1.9');r1=get(pold);r2=get(pnew);assert len(r1)==len(r2)
  assert list(r2[0])==list(r1[0])+TRACK
  revised=set()
  for l,r in zip(r1,r2):
   rid=l['id_global']; assert all(r[k]==l[k] for k in l),rid
   if rid in exact_ids:assert r['classificacao_alterada_p3_v1_9']=='sim';revised.add(rid)
   elif rid in {x['id_global'] for x in reviewed}:assert r['classificacao_alterada_p3_v1_9']=='não';revised.add(rid)
   else:assert not any(r[k] for k in TRACK)
  assert revised=={x['id_global'] for x in reviewed}
  qcounts[pnew.name]={'linhas':len(r2),'colunas':len(r2[0]),'historico_inalterado':True,'review_ids':len(revised)}
 assert qcounts['p3-v1.9-fila-23965.csv']['linhas']==23965
 assert qcounts['fila-geral-p0-p1-p2-p3-v1.9.csv']['linhas']==52046
 with (new/'p3-v1.9-regressao-independente-30-lotes.csv').open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(counts[0]),delimiter=';',lineterminator='\n');wr.writeheader();wr.writerows(counts)
 report={'status':'PASSOU','origem':'P3 v1.8','destino':'P3 v1.9','lotes':len(counts),'base':base,'controles':ctrl,'ids_modificados':len(seen),'ids_parecer':len(reviewed),'filas':qcounts,'colunas_protegidas':'idênticas para todos os registros','outros_ids':'inalterados'}
 (new/'p3-v1.9-regressao-independente-resumo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
