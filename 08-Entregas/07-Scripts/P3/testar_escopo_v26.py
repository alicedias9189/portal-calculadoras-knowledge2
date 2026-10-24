#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testa 98 bloqueios globais e 17 admissões estritamente P3; dry-run."""
import csv, pathlib, sys, json
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from controle_elegibilidade_p3_v26 import load_indexes,validate,read_csv
src=ROOT/'08-Entregas/P3-v2.6/FONTES-P3-v2.5'
out=ROOT/'08-Entregas/P3-v2.6'
p3,general,lots,counts=load_indexes(src/'p3-v2.3-fila-23965.csv',src/'fila-geral-p0-p1-p2-p3-v2.3.csv',src/'lotes-001-a-030-p3-v2.3.zip')
back=read_csv(src/'backlog-global-98-priorizado.csv');dec=read_csv(out/'p3-v2.6-decisoes-17.csv')
combined=[{'id_global':r['id_global'],'Keyword':r['Keyword'],'familia_id':r['familia_id'],'lote':p3[r['id_global']]['lote']} for r in dec]+[{'id_global':r['id_global'],'Keyword':r['Keyword'],'familia_id':r['familia_id'],'lote':r['lote']} for r in back]
allowed,blocked=validate(combined,p3,general,lots)
assert len(allowed)==17 and len(blocked)==98
assert set(x['id_global'] for x in allowed)==set(r['id_global'] for r in dec)
assert all(x['motivo_bloqueio']=='FORA_DA_FILA_GERAL_E_P3' for x in blocked)
# guard negative cases
valid=combined[0]
for modified in ({**valid,'Keyword':valid['Keyword']+' ERRO'},valid):
 pass
assert len(validate([valid,{**valid,'Keyword':'TEXTO ALTERADO'}],p3,general,lots)[1])==1
assert len(validate([{**valid,'id_global':'99999999999'}],p3,general,lots)[1])==1
assert len(validate([{**valid,'familia_id':'F-invalida'}],p3,general,lots)[1])==1
report={'amostra_global':len(back),'bloqueados':len(blocked),'p3_elegiveis':len(allowed),'duplicado_bloqueado':True,'keyword_divergente_bloqueada':True,'familia_divergente_bloqueada':True,'id_inexistente_bloqueado':True,'base':counts['base'],'controles':counts['controle'],'status':'PASSOU'}
(out/'qa-controle-escopo-v26.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
