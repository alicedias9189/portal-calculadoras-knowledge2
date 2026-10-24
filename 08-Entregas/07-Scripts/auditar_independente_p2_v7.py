#!/usr/bin/env python3
"""Regressão independente: compara P2 v6 e v7, IDs e 34 colunas protegidas."""
import argparse,csv,io,json,zipfile,hashlib
from pathlib import Path
ALLOW={'area_principal','cluster','subcluster','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta','unidade_origem','unidade_destino','direcao_conversao'}
def read(z,n):
 with z.open(n) as f:return list(csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''),delimiter=';'))
def normpatch(obj):return {k:str(obj.get(k,'')) for k in ALLOW}
def audit(root,out):
 a=root/'08-Entregas/P2-v6/lotes-001-a-030-p0-p1-p2-v6.zip';b=out/'lotes-001-a-030-p0-p1-p2-v7.zip';c=out/'auditoria-p2-v7-csv-integral.zip'
 za,zb,zc=map(zipfile.ZipFile,[a,b,c]);patch=read(zc,'p2-v7-patches.csv');patch_ids={p['id_global'] for p in patch};assert len(patch_ids)==101
 before_byid={p['id_global']:json.loads(p['antes']) for p in patch};after_byid={p['id_global']:json.loads(p['depois']) for p in patch};counts={'lotes':0,'base':0,'controles':0,'alterados':0,'linhas_inalteradas':0};summary=[]
 for name in sorted(n for n in za.namelist() if n.endswith('.csv')):
  new=name.replace('-v6.csv','-v7.csv');r0=read(za,name);r1=read(zb,new);assert len(r0)==len(r1),(name,'len');assert list(r0[0])==list(r1[0]);delta=0;base=ctl=0
  for old,newrow in zip(r0,r1):
   k=old['id_global'];assert k==newrow['id_global'];assert old['Keyword']==newrow['Keyword'];assert old['tipo_registro']==newrow['tipo_registro'];changed={f for f in old if old[f]!=newrow[f]};assert changed<=ALLOW,(name,k,changed-ALLOW)
   if old['tipo_registro']=='controle':ctl+=1;assert not changed
   if old['tipo_registro']=='base':base+=1
   if k in patch_ids:
    assert changed,(k,'no delta')
    assert normpatch(old)==normpatch(before_byid[k]),(k,'before mismatch')
    assert normpatch(newrow)==normpatch(after_byid[k]),(k,'after mismatch')
    delta+=1
   else:assert not changed,(k,'unpatched change')
   if not changed:counts['linhas_inalteradas']+=1
   if newrow['tipo_intencao']=='conversão direta':
    assert (newrow['unidade_origem'] and newrow['unidade_destino'] and newrow['direcao_conversao']) or old['tipo_intencao']=='conversão direta',(k,'conversion without metadata')
  assert ctl==73;counts['base']+=base;counts['controles']+=ctl;counts['alterados']+=delta;counts['lotes']+=1
  summary.append({'lote':name.split('/')[-1][:8],'base':base,'controles':ctl,'alterados':delta,'teste':'PASSOU'})
 assert counts['lotes']==30 and counts['base']==294905 and counts['controles']==2190 and counts['alterados']==101
 assert len(read(zc,'p2-v7-pendencias-restantes.csv'))==4660
 report={'resultado':'PASSOU','total':counts,'por_lote':summary,'validacoes':['colunas originais preservadas','IDs e keywords preservados','controles intocados','somente 101 IDs P2 alterados','valores antes/depois comparados com CSVs reais','conversões diretas novas com direção e unidades'],'auditoria_patches':len(patch)}
 (out/'regressao-independente-p2-v7.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(counts,ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--raiz',type=Path,required=True);p.add_argument('--saida',type=Path,required=True);args=p.parse_args();audit(args.raiz,args.saida)
