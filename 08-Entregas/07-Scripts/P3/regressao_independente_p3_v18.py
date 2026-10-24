#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Regressão independente P3 v1.7→v1.8, usando diffs reais de CSV, sem classificador."""
import argparse,csv,io,json,zipfile,collections,hashlib
from pathlib import Path
CAN={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta','proposta_taxonomia'}
def parse(data):return list(csv.DictReader(io.StringIO(data.decode('utf-8-sig')),delimiter=';'))
def file_rows(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def run(src,dst):
 oldzip=src/'08-Entregas/P3-v1.7/lotes-001-a-030-p3-v1.7.zip';newzip=dst/'lotes-001-a-030-p3-v1.8.zip'
 patches=file_rows(dst/'p3-v1.8-patches.csv');patch_byid={r['id_global']:r for r in patches}
 assert len(patch_byid)==len(patches)>0
 report=[];base=ctrl=changed=0
 with zipfile.ZipFile(oldzip) as za,zipfile.ZipFile(newzip) as zb:
  names=sorted(x for x in za.namelist() if x.endswith('.csv'))
  assert len(names)==30 and len(zb.namelist())==30
  for name in names:
   a=parse(za.read(name));b=parse(zb.read(name.replace('v1.7','v1.8')))
   assert len(a)==len(b),name
   if not a:raise AssertionError('lote vazio')
   assert list(a[0])==list(b[0]),name
   lote_b=lote_c=lote_m=0
   for old,new in zip(a,b):
    assert old['tipo_registro']==new['tipo_registro'] and old['id_global']==new['id_global'],('chave',name)
    delta={k for k in old if old[k]!=new[k]}
    if old['tipo_registro']!='base':
     assert not delta,('controle modificado',name,old['controle_id'],delta)
     ctrl+=1;lote_c+=1;continue
    base+=1;lote_b+=1
    if not delta:continue
    assert delta<=CAN,('coluna protegida modificada',name,old['id_global'],delta-CAN)
    rid=old['id_global'];assert rid in patch_byid,('mudança sem patch',rid)
    patch=patch_byid[rid];assert old['Keyword']==new['Keyword']==patch['Keyword']
    assert delta==set(patch['campos_alterados'].split(',')),('divergência diff',rid,delta)
    assert {k:old[k] for k in delta}==json.loads(patch['antes_json']),('antes',rid)
    assert {k:new[k] for k in delta}==json.loads(patch['depois_json']),('depois',rid)
    changed+=1;lote_m+=1
   report.append({'arquivo':name,'base':lote_b,'controles':lote_c,'ids_modificados':lote_m,'status':'PASSOU'})
 assert (base,ctrl,changed)==(294905,2190,len(patches)),(base,ctrl,changed,len(patches))
 # conferir rastreamento adicionado sem alterar colunas anteriores em ambas as filas
 queues=[('p3-v1.7-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v1.7.csv',52046)]
 for old_name,expected in queues:
  old=file_rows(src/'08-Entregas/P3-v1.7'/old_name);new=file_rows(dst/old_name.replace('v1.7','v1.8'))
  assert len(old)==len(new)==expected,(old_name,len(old),len(new))
  count=0
  for x,y in zip(old,new):
   assert all(x[k]==y[k] for k in x),('fila histórica alterada',old_name,x['id_global'])
   v=y.get('classificacao_alterada_p3_v1_8','')
   assert (v=='sim')==(x['id_global'] in patch_byid)
   if v:count+=1
  assert count==len(patches),('fila faltando patch',old_name,count)
 results={'resultado':'PASSOU','lotes':30,'base':base,'controles':ctrl,'patches':changed,'filas_validas':2,'p3_nova_fora':20755-changed,'casos_p2_inalterados':'fila geral histórica idêntica'}
 with open(dst/'p3-v1.8-regressao-independente-30-lotes.csv','w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(report[0]),delimiter=';');w.writeheader();w.writerows(report)
 (dst/'p3-v1.8-regressao-independente-resumo.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fonte',required=True,type=Path);p.add_argument('--saida',required=True,type=Path);a=p.parse_args();run(a.fonte,a.saida)
