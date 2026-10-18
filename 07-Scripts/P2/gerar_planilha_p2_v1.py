#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera planilha P2 via artifact_tool, com todas as células utilizadas centralizadas.
Uso: python gerar_planilha_p2_v1.py --dir /pasta/outputs
"""
import csv,collections,json,argparse
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
P=argparse.ArgumentParser();P.add_argument('--dir',default='/mnt/data/p2_work/out'); args=P.parse_args();folder=Path(args.dir)
def read(name):
 with (folder/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
rows=read('p2-validacao-semantica-25050.csv'); qa=read('qa-regressao-30-lotes-p2.csv');patches=read('p2-patches.csv')
summary=json.loads((folder/'resumo-p2-v1.json').read_text());rules=collections.Counter(x['regra_p2'] for x in rows)
w=Workbook.create()
NAVY='#17324D';BLUE='#1E5C81';WHITE='#FFFFFF';GRAY='#EFF4F8';GREEN='#DFEFE7';ORANGE='#FAE7CF';RED='#F9E0E0'

def make(name,headers,data,widths=None,chunk=2200):
 s=w.worksheets.add(name);nc=len(headers);s.get_range_by_indexes(0,0,1,nc).values=[headers]
 for pos in range(0,len(data),chunk):
  s.get_range_by_indexes(pos+1,0,min(chunk,len(data)-pos),nc).values=data[pos:pos+chunk]
 # all used rows/columns horizontally & vertically aligned center.
 used=s.get_range_by_indexes(0,0,len(data)+1,nc)
 used.format.horizontal_alignment='center';used.format.vertical_alignment='center'
 s.get_range_by_indexes(0,0,1,nc).format={'fill':NAVY,'font':{'bold':True,'color':WHITE},'horizontal_alignment':'center','vertical_alignment':'center','row_height':31,'wrap_text':True}
 if widths:
  for j,v in enumerate(widths):s.get_range_by_indexes(0,j,len(data)+1,1).format.column_width=v
 s.freeze_panes.freeze_rows(1)
 print('SHEET',name,len(data),'X',nc,flush=True)
 return s

header=['Métrica','Resultado','Interpretação']
stat=summary['status']
a=[['Total de keywords P2',summary['total_p2'],'Triagem sobre 30 lotes'],['Validado por regra',stat['VALIDADO'],'Não é revisão humana independente'],['Com ressalva',stat['VALIDADO_COM_RESSALVA'],'Requer seleção/contexto antes de operar'],['Pendente contextual',stat['PENDENTE_CONTEXTUAL'],'Não houve correção sem evidência'],['Registros alterados',summary['alteracoes'],'Campos analíticos apenas'],['Registros-base preservados',summary['registros_base'],'IDs/keywords/dados Ads protegidos'],['Controles idênticos',summary['controles'],'Nenhum controle alterado'],['Origem','P0 + P1 v2','Versões P0 e P1 anteriores preservadas'],['Validação','Regras contextuais','Auditoria editorial independente ainda necessária']]
make('Resumo',header,a,[35,25,64])
# Complete review trail, including ALL original priority queue columns.
# Audit sheet is a stratified and deterministic sample; the complete 25,050-row CSV with all fields ships in the ZIP.
from collections import defaultdict
buckets=defaultdict(list)
for r in rows:buckets[(r['regra_p2'],r['status_p2'])].append(r)
import random
rng=random.Random(20261017)
audit=[]
for key,g in sorted(buckets.items(),key=lambda a:-len(a[1])):
 audit+=rng.sample(g,min(len(g),25))
cols=['prioridade','lote','id_global','familia_id','Keyword','area','tipo_intencao_atual','status_p2','regra_p2','area_final_p2','tipo_intencao_final_p2','confianca_p2','justificativa_p2','classificacao_alterada_p2']
make('Amostra P2',cols,[[r.get(f,'') for f in cols] for r in audit],[14,11,14,19,39,19,25,25,25,20,25,17,42,20],chunk=1000)
# One record per unresolved ambiguity, not duplicated in other reference artifact collections.
pending=[x for x in rows if x['status_p2']=='PENDENTE_CONTEXTUAL'][:1100]
chosen=['lote','id_global','Keyword','area','cluster','tipo_intencao_atual','riscos_detectados','regra_p2','justificativa_p2']
make('Pendencias',chosen,[[r.get(f,'') for f in chosen] for r in pending],[12,15,40,20,25,22,32,27,42],chunk=1800)
chosen2=['regra','quantidade','nota'];make('Regras',chosen2,[[k,v,'Revisão automatizada'] for k,v in rules.most_common()],[38,18,32])
fields=list(qa[0]);make('Regressao 30',fields,[[r.get(f,'') for f in fields] for r in qa],[18]*len(fields))
# Sample of before/after changes provides a compact visual QA outside big full table.
from collections import defaultdict
by=defaultdict(list)
for r in patches:by[r['regra_p2']].append(r)
import random
rr=random.Random(92);sam=[]
for key,g in sorted(by.items(),key=lambda x:-len(x[1])):
 for r in rr.sample(g,min(5,len(g))):sam.append(r)
f=['id_global','lote','Keyword','regra_p2','antes_area','depois_area','antes_intencao','depois_intencao','campos_alterados']
make('Amostra patches',f,[[r.get(k,'') for k in f] for r in sam],[16,12,40,28,22,22,25,25,44])
print('EXPORTANDO',flush=True)
output=folder/'qa-revisao-p2-centralizada.xlsx'
SpreadsheetFile.export_xlsx(w).save(str(output))
print('XLSX',output,output.stat().st_size,flush=True)
print('INSPECAO',w.inspect({'kind':'table','range':'Resumo!A1:C10','include':'values','table_max_rows':10,'table_max_cols':3}).ndjson[:1800],flush=True)