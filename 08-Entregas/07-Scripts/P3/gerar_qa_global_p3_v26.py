#!/usr/bin/env python3
# coding: utf-8
"""Cria a QA Excel centralizada para o backlog A (50) e expansão P3 (17).
Execução na raiz da entrega: python3 07-Scripts/P3/gerar_qa_global_p3_v26.py
Requer artifact_tool; entradas CSV já geradas pelo auditor da v2.6.
"""
import pathlib, csv, json
from artifact_tool import Workbook,SpreadsheetFile
ROOT=pathlib.Path(__file__).resolve().parents[2]
B=ROOT/'08-Entregas/P3-v2.6'

def csvrows(n):
 with (B/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

review=csvrows('revisao-contextual-global-50-alta.csv')
all98=csvrows('backlog-global-98-com-parecer-50.csv')
new=csvrows('p3-v2.6-decisoes-17.csv')
patches=csvrows('p3-v2.6-patches-17.csv')
reg=csvrows('regressao-independente-30-lotes.csv')
counts=json.loads((B/'resumo-v26.json').read_text())
wb=Workbook.create()

def add(name,header,rows,widths=None):
 sheet=wb.worksheets.add(name)
 matrix=[header]+[[r.get(k,'') for k in header] for r in rows]
 nc=len(header)
 sheet.get_range_by_indexes(0,0,len(matrix),nc).values=matrix
 r=sheet.get_range_by_indexes(0,0,len(matrix),nc)
 r.format.horizontal_alignment='center'
 r.format.vertical_alignment='center'
 r.format.wrap_text=True
 sheet.get_range_by_indexes(0,0,1,nc).format={
 'fill':'#1C344B', 'font':{'bold':True,'color':'#FFFFFF'},
 'horizontal_alignment':'center','vertical_alignment':'center','row_height':30
 }
 sheet.freeze_panes.freeze_rows(1)
 sheet.get_range_by_indexes(1,0,max(1,len(rows)),nc).format.row_height=33
 for i,k in enumerate(header):
  w=(widths or {}).get(k, 16 if i==0 else 24)
  sheet.get_range_by_indexes(0,i,len(matrix),1).format.column_width=w
 return sheet

summ=[
 {'Métrica':'Registros do backlog global','Resultado':98},
 {'Métrica':'Prioridade A revisados','Resultado':50},
 {'Métrica':'Prioridade B/C aguardando','Resultado':48},
 {'Métrica':'Propostas globais aplicadas','Resultado':0},
 {'Métrica':'Mudanças elegíveis à P3','Resultado':17},
 {'Métrica':'Famílias P3 alcançadas','Resultado':9},
 {'Métrica':'P3 fora dos pilotos após v2.6','Resultado':20383},
 {'Métrica':'Pendências P2 preservadas','Resultado':4660},
 {'Métrica':'Lotes aprovados','Resultado':'30/30'},
 {'Métrica':'Registros-base preservados','Resultado':294905},
 {'Métrica':'Controles preservados','Resultado':2190},
 {'Métrica':'Homologação editorial','Resultado':'PENDENTE'},
]
add('Resumo',['Métrica','Resultado'],summ,{'Métrica':40,'Resultado':38})
fields=['ordem_global','id_global','Keyword','regra','origem_area','origem_tipo','proposta_area','proposta_tipo','parecer_tecnico','tipo_intencao_sugerido','subcluster_sugerido','ressalva_individual','justificativa_individual','autoriza_aplicacao','homologacao_editorial']
add('Revisão global A',fields,review,{'Keyword':36,'ressalva_individual':54,'justificativa_individual':64,'regra':30,'parecer_tecnico':32,'subcluster_sugerido':42})
add('Decisões P3', ['id_global','familia_id','Keyword','area_anterior','area_sugerida','cluster_sugerido','subcluster_sugerido','tipo_intencao_sugerido','parecer','aprovacao_editorial','justificativa'],new,{'Keyword':42,'justificativa':66,'subcluster_sugerido':50})
add('Patches', ['id_global','Keyword','campos_modificados','antes_json','depois_json','justificativa'],patches,{'Keyword':42,'antes_json':58,'depois_json':58,'justificativa':56})
add('QA lotes',list(reg[0]),reg,{'lote':50})
add('Backlog 98',[ 'id_global','Keyword','faixa_prioridade_global','ordem_global','status_revisao_A','destino','autoriza_aplicacao','elegivel_p3','elegivel_fila_geral'],all98,{'Keyword':40,'faixa_prioridade_global':28,'status_revisao_A':36,'destino':39})
out=B/'qa-global-A50-e-P3-v2.6-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(out))
print(out, out.stat().st_size)
print(wb.inspect({'kind':'table','range':'Resumo!A1:B8','include':'values','table_max_rows':10,'table_max_cols':2}).ndjson[:750])
