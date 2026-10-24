#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera Excel QA P3 v3.2 com todas as células usadas centralizadas.
Uso: python 07-Scripts/P3/gerar_qa_p3_v32.py
Depende de artifact_tool; não modifica arquivos originais.
"""
from pathlib import Path
import csv,json,collections
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v3.2'
def readrows(filename):
 with (OUT/filename).open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def write_sheet(wb,name,rows,fields):
 sh=wb.worksheets.add(name)
 values=[fields]+[[str(row.get(f,'')) for f in fields] for row in rows]
 if not values:return
 rng=sh.get_range_by_indexes(0,0,len(values),len(fields))
 rng.values=values
 rng.format.horizontal_alignment='center'
 rng.format.vertical_alignment='center'
 rng.format.wrap_text=True
 hdr=sh.get_range_by_indexes(0,0,1,len(fields))
 hdr.format.fill='#16324F'
 hdr.format.font.color='#FFFFFF'
 hdr.format.font.bold=True
 hdr.format.row_height=28
 # Narrow long audit text columns to avoid a very wide workbook.
 for i,f in enumerate(fields):
  col=sh.get_range_by_indexes(0,i,len(values),1)
  col.format.column_width=36 if f in ('Keyword','justificativa') else (28 if f in ('antes_json','depois_json','campos_modificados') else 19)
 try:sh.freeze_panes.freeze_rows(1)
 except Exception:pass
 return sh

dec,df=readrows('p3-v3.2-decisoes-68.csv')
pat,pf=readrows('p3-v3.2-patches.csv')
audit,af=readrows('p3-v3.2-qa-regras-anteriores.csv')
reg,rf=readrows('p3-v3.2-regressao-independente-30-lotes.csv')
counts=collections.Counter(r['regra'].replace('P3V32_','') for r in dec)
rule_rows=[{'Regra':k,'Total':v,'Revisão':'Decisão individual documentada; homologação editorial pendente'} for k,v in sorted(counts.items())]
summary=[
 {'Indicador':'Versão','Valor':'P3 v3.2','Observação':'Expansão seletiva, sem P0/P1/P2/global'},
 {'Indicador':'Decisões novas','Valor':str(len(dec)),'Observação':'IDs elegíveis e exclusivos'},
 {'Indicador':'Famílias','Valor':str(len(set(r['familia_id'] for r in dec))),'Observação':'Famílias distintas'},
 {'Indicador':'P3 fora dos pilotos — antes','Valor':'20272','Observação':'Reconciliado pelos status históricos'},
 {'Indicador':'P3 fora dos pilotos — depois','Valor':'20204','Observação':'20272 - 68'},
 {'Indicador':'Lotes íntegros','Valor':'30/30','Observação':'Regressão independente'},
 {'Indicador':'Registros-base','Valor':'294905','Observação':'Preservados'},
 {'Indicador':'Controles','Valor':'2190','Observação':'Preservados'},
 {'Indicador':'P2 pendentes','Valor':'4660','Observação':'Separadas'},
 {'Indicador':'Quarentena global','Valor':'98','Observação':'Bytes idênticos'},
]
wb=Workbook.create()
write_sheet(wb,'Resumo',summary,['Indicador','Valor','Observação'])
write_sheet(wb,'Regras-v32',rule_rows,['Regra','Total','Revisão'])
write_sheet(wb,'Decisoes-68',dec,df)
write_sheet(wb,'Patches-68',pat,pf)
write_sheet(wb,'QA-v31-por-regra',audit,af)
write_sheet(wb,'Regressao-30',reg,rf)
SpreadsheetFile.export_xlsx(wb).save(str(OUT/'qa-auditoria-P3-v3.2-centralizada.xlsx'))
print('QA Excel exportado, 6 abas, alinhamento central')
