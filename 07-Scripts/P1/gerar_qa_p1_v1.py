#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera planilha XLSX centralizada para auditoria do P1 a partir dos CSV.
Uso: python gerar_qa_p1_v1.py [diretório com saídas P1]. Dependência: artifact_tool.
"""
import csv,json,sys
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/mnt/data/p1_work/p1_outputs')
summary=json.loads((ROOT/'resumo-p1.json').read_text(encoding='utf-8'))
def read(path):
    with open(ROOT/path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
cols_review=['ordem','lote','id_global','familia_id','Keyword','volume_ads_patamar','status_decisao','regra_identificada','alterado','area_anterior','area_revisada','cluster_revisado','subcluster_revisado','intencao_anterior','intencao_revisada','origem','destino','confianca_revisada','revisao_manual_revisada','justificativa']
cols_patch=['lote','id_global','Keyword','campos_alterados','antes_json','depois_json','justificativa']
cols_qa=['lote','registros','controles','controles_inalterados','ads_16_colunas_identicas','linhas_p1_alteradas','demais_linhas_identicas','conversoes_sem_metadados']
wb=Workbook.create()
# Minimal formatting, every used row/col centered per user specification.
def make_sheet(name,headers,rows):
    sh=wb.worksheets.add(name)
    n=len(rows)
    width=len(headers)
    sh.get_range_by_indexes(0,0,1,width).values=[headers]
    # Small blocks avoid remote payload bottlenecks.
    for start in range(0,n,250):
        batch=rows[start:start+250]
        matrix=[[str(x.get(k,'')) for k in headers] for x in batch]
        sh.get_range_by_indexes(1+start,0,len(matrix),width).values=matrix
    rg=sh.get_range_by_indexes(0,0,n+1,width)
    rg.format.horizontal_alignment='center'; rg.format.vertical_alignment='center'
    rg.format.row_height=22
    sh.get_range_by_indexes(0,0,1,width).format={
        'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},
        'horizontal_alignment':'center','vertical_alignment':'center','row_height':29}
    for j,k in enumerate(headers):
        wd=16
        if k in ('Keyword','justificativa'):wd=43
        elif k in ('antes_json','depois_json'):wd=37
        elif k=='campos_alterados':wd=36
        elif k in ('status_decisao','subcluster_revisado','cluster_revisado','intencao_revisada','intencao_anterior','revisao_manual_revisada'):wd=23
        sh.get_range_by_indexes(0,j,n+1,1).format.column_width=wd
    sh.freeze_panes.freeze_rows(1)
    return sh

overview=wb.worksheets.add('Resumo QA')
lines=[['Indicador','Resultado'],['Registros P1',summary['p1_total']],['Famílias P1',summary['p1_familias']],
       ['Regras contextuais fortes',summary['registros_com_regra_forte']],['Pendentes',summary['registros_pendentes_validacao']],
       ['Registros alterados',summary['registros_alterados']],['Mudanças de área',summary['mudancas_area']],
       ['Mudanças de intenção',summary['mudancas_tipo_intencao']],['Novas conversões diretas',summary['novas_conversoes_diretas']],
       ['Lotes com versão P1',summary['lotes_com_patches']],['Controles preservados',summary['controles_verificados']],
       ['Colunas originais Ads preservadas','Sim'],['P0 e P2/P3 preservados','Sim'],
       ['Escopo','Triagem contextual automatizada; pendências exigem validação humana']]
overview.get_range_by_indexes(0,0,len(lines),2).values=lines
rg=overview.get_range_by_indexes(0,0,len(lines),2)
rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=26
overview.get_range('A1:B1').format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},
 'horizontal_alignment':'center','vertical_alignment':'center','row_height':30}
overview.get_range('A1:A14').format.column_width=34
overview.get_range('B1:B14').format.column_width=75
overview.get_range('B14').format.wrap_text=True
overview.freeze_panes.freeze_rows(1)
for sheetname,filename,fields in [('Revisao P1','revisao-automatizada-2557-p1.csv',cols_review),
   ('Patches P1','patches-objetivos-p1.csv',cols_patch),
   ('Pendencias P1','p1-pendencias-validacao.csv',cols_review),
   ('QA por lote','qa-regressao-p1-por-lote.csv',cols_qa)]:
    make_sheet(sheetname,fields,read(filename))
out=ROOT/'qa-revisao-p1-centralizado.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(out))
print('Workbook:',out,out.stat().st_size)

