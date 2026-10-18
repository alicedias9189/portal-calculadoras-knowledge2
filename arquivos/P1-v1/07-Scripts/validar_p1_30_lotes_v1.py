#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoria independente de preservação de P1 vs. acervo versionado P0.
Uso: python validar_p1_30_lotes_v1.py --root ./p0_extracted --out ./p1_outputs
Dependências: apenas Python 3 stdlib. Não altera arquivo nenhum.
"""
import argparse,csv,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--out',required=True)
a=ap.parse_args();root=Path(a.root);out=Path(a.out)
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
orig_cols=['tipo_registro','id_global','lote_id','familia_id','controle_id','Keyword','ocorrencias_origem','areas_origem','qtd_areas','Avg. monthly searches','Mudança em três meses','Mudança YoY','Competition','Competition (indexed value)','Top of page bid (low range)','Top of page bid (high range)']
rev=read(out/'revisao-automatizada-2557-p1.csv');changed={x['id_global'] for x in rev if x['alterado']=='sim'}
assert len(rev)==2557 and len(set(x['id_global'] for x in rev))==2557
stats=[];all_ids=set()
for n in range(1,31):
 lot=f'{n:03d}';before=read(root/'lotes'/f'lote-{lot}-revisado-p0-v1.1-barras-v2.csv')
 afterfile=out/'lotes'/f'lote-{lot}-revisado-p0-p1-v1.1-barras-v2.csv'
 after=read(afterfile) if afterfile.exists() else before
 assert len(before)==len(after),(lot,'linhas')
 errors=0;controls=0;mod=0
 for old,new in zip(before,after):
  assert all(old[c]==new[c] for c in orig_cols),(lot,old['id_global'],'ads')
  if old['tipo_registro']=='controle':assert old==new;(controls:=controls+1)
  else:
   assert old['id_global'] not in all_ids;all_ids.add(old['id_global'])
   if old!=new:
    assert old['id_global'] in changed,(lot,old['id_global'],'mudança não autorizada')
    mod+=1
   else:assert old['id_global'] not in changed,(lot,old['id_global'],'patch ausente')
   if new['tipo_intencao']=='conversão direta':assert all(new[k] for k in ('unidade_origem','unidade_destino','direcao_conversao'))
 assert controls==73,(lot,'controle count',controls)
 stats.append({'lote':lot,'alteracoes':mod,'controles':controls})
assert len(all_ids)==294905
assert sum(x['alteracoes'] for x in stats)==len(changed)
queue0=read(root/'fila-priorizada-30-lotes-com-p0-revisado.csv');queue1=read(out/'fila-priorizada-30-lotes-com-p0-p1.csv')
assert len(queue0)==len(queue1)==52046
for a,b in zip(queue0,queue1):
 assert a['prioridade']==b['prioridade']
 if a['prioridade']!='P1':assert a==b,('fila fora P1',a['id_global'])
 else:assert a['id_global']==b['id_global'] and a['Keyword']==b['Keyword']
print(json.dumps({'status':'PASS','registros_base':len(all_ids),'p1_revisados':len(rev),'p1_patches':len(changed),'controles_inalterados':sum(x['controles'] for x in stats),'fila_total':len(queue0),'p0_p2_p3_inalterados':True},ensure_ascii=False,indent=2))
