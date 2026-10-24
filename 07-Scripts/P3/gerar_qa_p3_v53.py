#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cria workbook QA P3 v5.3 com células usadas centralizadas (artifact_tool)."""
from pathlib import Path
import csv,json
from artifact_tool import Workbook,SpreadsheetFile
HERE=Path(__file__).resolve(); R=HERE.parents[2] if HERE.parent.name=='P3' and HERE.parent.parent.name=='07-Scripts' else HERE.parent
O=R/'08-Entregas/P3-v5.3'; G=R/'auditoria-ouro'
def get(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
rv=get(O/'p3-v5.3-pareceres-75.csv');pt=get(O/'p3-v5.3-patches-6.csv');qg=get(O/'p3-v5.3-qa-por-grupo.csv');reg=get(O/'p3-v5.3-regressao-independente-60-lotes.csv');oro=get(G/'ids-ouro-revisar-12.csv')
sumry=json.loads((O/'p3-v5.3-regressao-independente-resumo.json').read_text(encoding='utf-8'))
wb=Workbook.create()
def letter(i):
 s='';i+=1
 while i:s=chr(65+(i-1)%26)+s;i=(i-1)//26
 return s
def create(name,header,data,widths=None,row_height=26):
 sheet=wb.worksheets.add(name)
 values=[header]+[[str(x) if x is not None else '' for x in row] for row in data]
 sheet.get_range_by_indexes(0,0,len(values),len(header)).values=values
 region=sheet.get_range(f'A1:{letter(len(header)-1)}{len(values)}')
 region.format.horizontal_alignment='center';region.format.vertical_alignment='center'
 region.format.row_height=row_height
 region.format.wrap_text=True
 h=sheet.get_range(f'A1:{letter(len(header)-1)}1')
 h.format={'fill':'#163A5F','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':37,'wrap_text':True}
 for i,w in enumerate(widths or [22]*len(header)):
  sheet.get_range(f'{letter(i)}1:{letter(i)}{len(values)}').format.column_width=w
 sheet.freeze_panes.freeze_rows(1)
 return sheet
create('Resumo',['Indicador','Valor','Observação'],[
 ['Versão','P3 v5.3','Revisão dos 75 pareceres da v5.2'],
 ['Revisados','75','Sem novas palavras analisadas'],
 ['Refinados','6','Patches restritos aos IDs especificados'],
 ['Mantidos','69','Ressalvas individualizadas'],
 ['Famílias','32','Sete grupos temáticos'],
 ['Lotes canônicos','30','294.905 bases, 2.190 controles'],
 ['Lotes filtrados Ouro','30','291.296 bases, 2.190 controles'],
 ['Exclusão reversível Ouro','3609','Somente visão de trabalho'],
 ['Fila P3 canônica','23965','Antes de retirar as variantes Ouro'],
 ['Fila P3 operacional','23865','Depois do filtro Ouro'],
 ['Elegíveis para próxima expansão','19462','O mesmo número que ao fechar a DEC-089'],
 ['P2 pendentes','4660','Sem alterações'],
 ['Backlog global','98','Preservado byte a byte'],
 ['Status regressão','PASSOU','60 lotes e 4 filas'],
 ['Homologação editorial','PENDENTE','Pareceres técnicos não equivalem a aprovação humana'],
 ['Próxima etapa','P3 v5.4','Nova expansão de 100 IDs filtrados']
],widths=[33,23,58],row_height=30)
create('Pareceres 75',['ID','Keyword','Grupo','Parecer','Tipo anterior','Tipo revisado','Área','Subcluster anterior','Subcluster revisado','Justificativa individual','Campos modificados','Homologação'],[
 [x['id_global'],x['Keyword'],x['regra_v5_2'],x['parecer_v5_3'],x['tipo_v5_2'],x['tipo_v5_3'],x['area_v5_3'],x['subcluster_v5_2'],x['subcluster_v5_3'],x['justificativa_individual'],x['campos_modificados'],x['homologacao_editorial']] for x in rv
],widths=[14,46,32,23,21,21,19,36,40,82,32,19],row_height=47)
create('Patches 6',['ID','Keyword','Campos alterados','Antes JSON','Depois JSON','Motivo','Lote'],[
 [x['id_global'],x['Keyword'],x['campos_modificados'],x['antes_json'],x['depois_json'],x['justificativa'],x['lote_id']] for x in pt
],widths=[15,45,37,76,76,75,15],row_height=66)
create('Grupos QA',['Grupo','Revisados','Refinados','Mantidos','Homologação'],[
 [x['grupo'],x['registros'],x['refinados'],x['mantidos'],x['homologacao_editorial']] for x in qg
],widths=[36,19,19,19,22],row_height=30)
create('Regressão 60',['Base','Lote','Registros','Refinamentos','Status'],[
 [x['base'],x['lote'],x['registros'],x['refinamentos'],x['status']] for x in reg
],widths=[20,60,17,18,17],row_height=25)
create('Filas conferidas',['Fila','Linhas','Colunas históricas','Colunas novas','Status'],[
 [x['fila'],x['linhas'],x['colunas_protegidas'],x['colunas_adicionais'],x['status']] for x in sumry['filas']
],widths=[59,18,27,20,20],row_height=34)
if oro:
 keys=list(oro[0]); cols=['id_global','Keyword','cor','cor_hex','texto_dourado','tambem_aparece_sem_dourado','decisao']
 cols=[c for c in cols if c in keys]
 create('Ouro revisão 12',[x.replace('_',' ').title() for x in cols],[[r[c] for c in cols] for r in oro],widths=[14,42,18,18,42,23,44][:len(cols)],row_height=42)
create('Controles',['Invariante','Resultado'],[
 ['IDs revisados','75, exatos; nenhum pertence ao filtro Ouro'],
 ['Linhas base canônica','294.905'],['Linhas base operacional','291.296'],['Controles por versão','2.190'],
 ['Campos permitidos em patches','area_principal, cluster, subcluster, intencao_principal, tipo_intencao, dominio_ou_grandeza, confianca, revisao_manual, justificativa_curta'],
 ['Filas','398 colunas históricas intactas e 8 colunas novas'],
 ['Backlog global','98 propostas; bytes idênticos'],
 ['Homologação','Pendente'],
 ['Fontes','P3 v5.2 e auditoria de cores Ouro DEC-089']
],widths=[35,95],row_height=38)
output=O/'qa-auditoria-P3-v5.3-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(output))
print('QA_EXPORTADA',output,output.stat().st_size,'bytes')
try:print(wb.inspect({'kind':'table','range':'Resumo!A1:C5','include':'values','table_max_rows':5,'table_max_cols':3}).ndjson[:800])
except Exception as e:print('inspect-not-supported:',str(e)[:140])