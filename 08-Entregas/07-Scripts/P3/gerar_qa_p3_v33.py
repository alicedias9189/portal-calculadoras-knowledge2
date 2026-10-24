#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planilha QA P3 v3.3, todas as células usadas horizontal e verticalmente centradas.
Uso: python 07-Scripts/P3/gerar_qa_p3_v33.py
"""
from pathlib import Path
import csv,collections
from artifact_tool import Workbook, SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v3.3'

def read_rows(filename):
 with (OUT/filename).open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f,delimiter=';');return list(reader),list(reader.fieldnames)

def sheet_for(wb,name,rows,fields):
 sh=wb.worksheets.add(name)
 values=[fields]+[[str(r.get(f,'')) for f in fields] for r in rows]
 allcells=sh.get_range_by_indexes(0,0,len(values),len(fields))
 allcells.values=values
 allcells.format.horizontal_alignment='center';allcells.format.vertical_alignment='center'
 allcells.format.wrap_text=True
 heading=sh.get_range_by_indexes(0,0,1,len(fields))
 heading.format.fill='#153047';heading.format.font.color='#FFFFFF';heading.format.font.bold=True;heading.format.row_height=30
 for j,f in enumerate(fields):
  column=sh.get_range_by_indexes(0,j,len(values),1)
  column.format.column_width=(42 if f in ('Keyword','fundamento_critico','justificativa','fundamento') else
                              28 if f in ('antes_json','depois_json','fundamento_critico') else 19)
 try:sh.freeze_panes.freeze_rows(1)
 except Exception: pass
 return sh

reviews,reviewfields=read_rows('p3-v3.3-pareceres-68.csv')
patches,patchfields=read_rows('p3-v3.3-patches.csv')
rules,rulefields=read_rows('p3-v3.3-qa-regras.csv')
regression,regressionfields=read_rows('p3-v3.3-regressao-independente-30-lotes.csv')
summary=[
 {'Indicador':'Versão','Valor':'P3 v3.3','Observação':'Revisão crítica da expansão v3.2, sem novas classificações'},
 {'Indicador':'Itens revisados','Valor':'68','Observação':'32 horas extras, 18 payback, 9 datas Excel, 7 IPVA, 1 cartão, 1 energia'},
 {'Indicador':'Refinamentos','Valor':str(len(patches)),'Observação':'Refinamentos de subtipo/intenções; não 10 falsos positivos de domínio'},
 {'Indicador':'Mantidos com ressalvas','Valor':str(sum(r['parecer_v33']=='MANTIDO_COM_RESSALVA' for r in reviews)),'Observação':'Pendentes de homologação editorial'},
 {'Indicador':'P3 fora dos pilotos','Valor':'20204','Observação':'Sem expansão; contagem inalterada'},
 {'Indicador':'P2 pendente','Valor':'4660','Observação':'Sem alteração'},
 {'Indicador':'Global fora da fila','Valor':'98','Observação':'Arquivo preservado byte a byte'},
 {'Indicador':'Regressão','Valor':'30/30','Observação':'294905 registros-base; 2190 controles; campos protegidos preservados'}
]
wb=Workbook.create()
sheet_for(wb,'Resumo',summary,['Indicador','Valor','Observação'])
sheet_for(wb,'QA-por-regra',rules,rulefields)
sheet_for(wb,'Pareceres-68',reviews,reviewfields)
sheet_for(wb,'Patches-10',patches,patchfields)
sheet_for(wb,'Regressao-30',regression,regressionfields)
# Requisite explicit pending QA, not automatic approval
pending=[{'ID':r['id_global'],'Keyword':r['Keyword'],'Regra':r['regra_v32'],'Pendência':'Homologação editorial humana pendente'} for r in reviews]
sheet_for(wb,'Pendencia-editorial',pending,['ID','Keyword','Regra','Pendência'])
SpreadsheetFile.export_xlsx(wb).save(str(OUT/'qa-auditoria-P3-v3.3-centralizada.xlsx'))
print('Excel exportado: 6 abas, centralizado, pareceres 68, patches 10')
