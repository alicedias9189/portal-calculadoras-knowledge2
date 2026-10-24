#!/usr/bin/env python3
"""Gera a planilha de auditoria P2 v4 (resumo, regras, patches e amostras).
Os CSVs completos, sem amostragem, permanecem no ZIP de auditoria.
Requer artifact_tool. Todas as células usadas ficam centralizadas.
"""
import csv, io, json, zipfile
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'08-Entregas/P2-v4'
DATA=zipfile.ZipFile(OUT/'auditoria-p2-v4-csv-integral.zip')
SUMMARY=json.loads((OUT/'resumo-p2-v4.json').read_text(encoding='utf-8'))
def rows(name):
    return list(csv.DictReader(io.TextIOWrapper(DATA.open(name),encoding='utf-8-sig',newline=''),delimiter=';'))
wb=Workbook.create()
def add(name,header,rs,widths):
    sheet=wb.worksheets.add(name)
    matrix=[header]+rs
    sheet.get_range_by_indexes(0,0,len(matrix),len(header)).values=matrix
    block=sheet.get_range_by_indexes(0,0,len(matrix),len(header))
    block.format.horizontal_alignment='center';block.format.vertical_alignment='center'
    block.format.row_height=20
    h=sheet.get_range_by_indexes(0,0,1,len(header))
    h.format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':29}
    for i,w in enumerate(widths):sheet.get_range_by_indexes(0,i,len(matrix),1).format.column_width=w
    sheet.freeze_panes.freeze_rows(1)
    return sheet
info=[['Métrica','Resultado'],['P2 — universo',SUMMARY['universo_p2']],['Pendências analisadas',SUMMARY['pendencias_entrada_v3']],['Reclassificadas nesta revisão',SUMMARY['reclassificadas']],['Sem ressalva (regra)',SUMMARY['sem_ressalva']],['Com ressalva operacional',SUMMARY['com_ressalva']],['Ainda pendentes',SUMMARY['pendencias_restantes']],['Famílias com pendências de entrada',SUMMARY['familias_totais_com_pendencias']],['Famílias que receberam correção',SUMMARY['familias_com_correcao']],['Registros-base preservados',SUMMARY['registros_base']],['Controles preservados',SUMMARY['controles']],['Lotes aprovados no QA',SUMMARY['lotes']],['Natureza da auditoria','Revisão por regras sem homologação editorial'],['Dados integrais','Ver CSVs dentro de auditoria-p2-v4-csv-integral.zip']]
add('Resumo',info[0],info[1:],[40,68])
rule_rows=[[k,v,' | '.join(SUMMARY['exemplos'].get(k,[])[:3])] for k,v in sorted(SUMMARY['regras'].items(),key=lambda kv:-kv[1])]
add('Regras e amostras',['Regra','Registros','Exemplos'],rule_rows,[34,14,100])
patches=rows('p2-v4-patches.csv')
patch_rows=[[x[k] for k in ['id_global','lote','familia_id','Keyword','regra','status','justificativa']] for x in patches]
add(f'Patches {len(patches)}',['ID','Lote','Família','Keyword','Regra','Estado','Justificativa'],patch_rows,[14,10,24,63,30,18,73])
families=rows('p2-v4-familias-analisadas.csv')
family_rows=[[x[k] for k in ['familia_id','pendentes_v3','classificados_v4','ainda_abertos','regras','amostras_abertas']] for x in families[:300]]
add('Familias prioritarias',['Família','Antes','Corrigidas','Restantes','Regras','Amostras ainda abertas'],family_rows,[25,12,14,14,43,96])
pending=rows('p2-v4-pendencias-restantes.csv')
pending_rows=[[x.get(k,'') for k in ['id_global','familia_id','Keyword','cluster','subcluster','status_p2_v4']] for x in pending[:300]]
add('Amostra pendencias',['ID','Família','Keyword','Cluster anterior','Subcluster anterior','Status'],pending_rows,[14,25,70,37,43,24])
SpreadsheetFile.export_xlsx(wb).save(str(OUT/'qa-validacao-p2-v4-centralizada.xlsx'))
print('PLANILHA',OUT/'qa-validacao-p2-v4-centralizada.xlsx',flush=True)
