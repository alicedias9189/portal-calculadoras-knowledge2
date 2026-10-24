#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificacao independente P3 v1.6; compara dados CSV reais sem usar classificadores."""
import argparse,csv,io,zipfile,json,hashlib,collections
from pathlib import Path
CAN={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta'}
TRACK=['status_p3_v1_6','regra_p3_v1_6','justificativa_p3_v1_6','area_final_p3_v1_6','cluster_final_p3_v1_6','subcluster_final_p3_v1_6','tipo_intencao_final_p3_v1_6','classificacao_alterada_p3_v1_6']
def parsed(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def load(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def outcsv(p,rows,keys):
 with open(p,'w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,delimiter=';',fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 p=argparse.ArgumentParser();p.add_argument('--fonte',type=Path,required=True);p.add_argument('--saida',type=Path,required=True);a=p.parse_args()
 base=a.fonte/'08-Entregas/P3-v1.5';out=a.saida
 patches=load(out/'p3-v1.6-patches.csv');patches_by_id={x['id_global']:x for x in patches};assert len(patches_by_id)==len(patches)==163
 found=set();records=[];changed=0;nbase=ctrl=0;h_old=hashlib.sha256();h_new=hashlib.sha256()
 with zipfile.ZipFile(base/'lotes-001-a-030-p3-v1.5.zip') as old,zipfile.ZipFile(out/'lotes-001-a-030-p3-v1.6.zip') as new:
  names=sorted(old.namelist());assert len(names)==len(new.namelist())==30
  for name in names:
   target=name.replace('v1.5.csv','v1.6.csv');a1=parsed(old.read(name));b1=parsed(new.read(target));assert len(a1)==len(b1)
   changed_lote=bs=cs=0
   for x,y in zip(a1,b1):
    assert set(x)==set(y),(name,'COLUNAS');assert x['id_global']==y['id_global'] and x['tipo_registro']==y['tipo_registro']
    assert x['Keyword']==y['Keyword'] and x['lote_id']==y['lote_id']
    protected={k:x[k] for k in x if k not in CAN}
    protected_after={k:y[k] for k in y if k not in CAN}
    assert protected==protected_after,(name,x['id_global'],'PROTEGIDO')
    bb=json.dumps(protected,ensure_ascii=False,sort_keys=True).encode('utf8');h_old.update(bb);h_new.update(json.dumps(protected_after,ensure_ascii=False,sort_keys=True).encode('utf8'))
    if x['tipo_registro']!='base':cs+=1;ctrl+=1;assert x==y;continue
    bs+=1;nbase+=1;diff=[k for k in x if x[k]!=y[k]]
    rid=x['id_global'];should=patches_by_id.get(rid)
    if diff:
     assert should and rid not in found,(rid,'SEM PATCH');found.add(rid);changed+=1;changed_lote+=1
     assert set(diff)==set(should['campos_alterados'].split(',')),(rid,'CAMPOS DIFERENTES')
     assert json.loads(should['antes_json'])=={k:x[k] for k in diff},(rid,'ANTES ERRADO')
     assert json.loads(should['depois_json'])=={k:y[k] for k in diff},(rid,'DEPOIS ERRADO')
    else:assert not should,(rid,'PATCH SEM ALTERACAO')
   records.append({'lote':name,'bases':bs,'controles':cs,'alteracoes':changed_lote,'status':'PASSOU'})
 assert len(found)==len(patches_by_id)==changed==163
 assert (nbase,ctrl)==(294905,2190)
 assert h_old.hexdigest()==h_new.hexdigest()
 oldque=load(base/'p3-v1.5-fila-23965.csv');newque=load(out/'p3-v1.6-fila-23965.csv');assert len(oldque)==len(newque)==23965
 for a,b in zip(oldque,newque):
  assert all(a[k]==b[k] for k in a),(a['id_global'],'FILA ORIGINAL MUDOU')
  assert list(b)[-8:]==TRACK
  if a['id_global'] in found:assert b['classificacao_alterada_p3_v1_6']=='sim'
  else:assert all(b[k]=='' for k in TRACK),(a['id_global'],'COLUNA NOVA FORA ALVO')
 assert len(load(out/'p3-v1.6-amostra-78-pareceres.csv'))==78
 report={'lotes_aprovados':30,'registros_base':nbase,'controles':ctrl,'ids_alterados':changed,'ids_esperados':len(patches),'protegidoss_sha256':h_old.hexdigest(),'status':'PASSOU','checagem':['30 lotes ordem e colunas','controles iguais','colunas protegidas iguais','alteracoes somente em CAN','patch exato antes/depois','fila historica igual','78 pareceres presentes']}
 outcsv(out/'p3-v1.6-regressao-independente-30-lotes.csv',records,list(records[0]));(out/'p3-v1.6-regressao-independente-resumo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
