#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comparação independente P2 v5 x P2 v6, com verificações de 30 lotes e decisões."""
import argparse,csv,io,zipfile,json,hashlib
from pathlib import Path
from collections import Counter
FIELDS=['area_principal','cluster','subcluster','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta','unidade_origem','unidade_destino','direcao_conversao']
def read(z,n):return list(csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig',newline=''),delimiter=';'))
def sha(f):
 h=hashlib.sha256()
 with open(f,'rb') as b:
  for ch in iter(lambda:b.read(1<<20),b''):h.update(ch)
 return h.hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--base',type=Path,required=True);a.add_argument('--novo',type=Path,required=True);args=a.parse_args()
 out=args.novo
 zold=zipfile.ZipFile(args.base/'08-Entregas/P2-v5/lotes-001-a-030-p0-p1-p2-v5.zip');znew=zipfile.ZipFile(out/'lotes-001-a-030-p0-p1-p2-v6.zip');az=zipfile.ZipFile(out/'auditoria-p2-v6-csv-integral.zip');oldmeta=zipfile.ZipFile(args.base/'08-Entregas/P2-v5/auditoria-p2-v5-csv-integral.zip')
 assert all(z.testzip() is None for z in (zold,znew,az,oldmeta))
 patch=read(az,'p2-v6-patches.csv');patchids={x['id_global'] for x in patch};assert len(patch)==len(patchids)==387
 prior=read(oldmeta,'p2-v5-pendencias-restantes.csv'); priorids={x['id_global'] for x in prior};assert len(priorids)==5148;assert patchids<=priorids
 newer=read(az,'p2-v6-pendencias-restantes.csv');assert len(newer)==4761; assert {x['id_global'] for x in newer}==priorids-patchids
 decisions=read(az,'p2-v6-decisoes-25050.csv'); assert len(decisions)==25050 and len({x['id_global'] for x in decisions})==25050
 pmap={x['id_global']:x for x in patch};dmap={x['id_global']:x for x in decisions}
 assert Counter(x['status'] for x in patch)=={'RESOLVIDO':106,'COM_RESSALVA':281}
 counts=Counter();changed=[];qa=[];allids=set();basecnt=controlcnt=0
 for oldname in sorted(x for x in zold.namelist() if x.endswith('.csv')):
  newname=oldname.replace('-v5.csv','-v6.csv');assert newname in znew.namelist()
  o=read(zold,oldname);n=read(znew,newname);assert len(o)==len(n)
  b=c=m=0;bad=[]
  for x,y in zip(o,n):
   assert x['id_global']==y['id_global'] and x['Keyword']==y['Keyword'] and x['tipo_registro']==y['tipo_registro']
   id=x['id_global'];typ=x['tipo_registro']
   if typ=='base':
    assert id not in allids;allids.add(id);b+=1
   if typ=='controle':c+=1
   differences={k for k in x if x[k]!=y[k]}
   if id in patchids and typ=='base':
    assert differences <= set(FIELDS),(oldname,id,differences)
    assert differences,(oldname,id,'no actual diff')
    before=json.loads(pmap[id]['antes']);after=json.loads(pmap[id]['depois'])
    assert all(x[k]==before[k] and y[k]==after[k] for k in FIELDS),(id,'patch mismatch')
    assert dmap[id]['status_p2_v6'] in ('RESOLVIDO','COM_RESSALVA')
    assert dmap[id]['classificacao_alterada_p2_v6']=='sim'
    if y['tipo_intencao']=='conversão direta':
     assert y['unidade_origem'] and y['unidade_destino'] and y['direcao_conversao']
    changed.append(id);m+=1
   else:
    assert not differences,(oldname,id,differences)
   if typ=='controle': assert not differences
  basecnt+=b;controlcnt+=c
  assert c==73
  qa.append({'lote':oldname.split('/')[-1],'base':b,'controles':c,'alteracoes':m,'status':'PASSOU'})
 assert len(qa)==30 and len(changed)==387 and set(changed)==patchids
 assert basecnt==len(allids)==294905 and controlcnt==2190
 # The two explicitly undecidable families must remain 100% intact.
 for x in newer:
  t=x['Keyword'].lower()
  if x['familia_id']=='F-2fc589de45ad':counts['semanas_dias']+=1
  if x['familia_id']=='F-98af3b362ed9':counts['fahrenheit_isolado']+=1
 assert counts['semanas_dias']==157 and counts['fahrenheit_isolado']==68  # A exceção Fahrenheit com K foi resolvida na versão anterior
 final={'status':'PASSOU','lotes':30,'id_base_unicos':basecnt,'controles_intactos':controlcnt,'p2_pendentes_entrada':5148,'alteracoes':387,'p2_pendentes_restantes':4761,'sem_ressalva':106,'com_ressalva':281,'familias_nao_decidiveis_preservadas':dict(counts),'familia_fahrenheit_excecao_explicitamente_resolvida_na_v5':1,'alteracoes_por_lote':qa,'sha256_lotes_v6':sha(out/'lotes-001-a-030-p0-p1-p2-v6.zip'),'sha256_auditoria_v6':sha(out/'auditoria-p2-v6-csv-integral.zip')}
 (out/'regressao-independente-p2-v6.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in final.items() if k!='alteracoes_por_lote'},ensure_ascii=False))
if __name__=='__main__':main()
