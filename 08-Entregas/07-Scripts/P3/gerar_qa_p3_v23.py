#!/usr/bin/env python3
# coding: utf-8
"""Gera planilha XLSX auditável e centralizada para P3 v2.3 (artifact_tool).
Execute a partir do ZIP extraído com Python 3 e artifact_tool instalado.
"""
import csv,json
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'08-Entregas/P3-v2.3'

def getrows(name):
    with (P/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=';'))

wb=Workbook.create()
res=json.loads((P/'p3-v2.3-resumo.json').read_text(encoding='utf-8'))
summary=[['Indicador','Resultado'],
 ['Versão',res['versao']],['Decisões P3 v2.2',res['decisoes_v2_2']],
 ['Amostra original',res['amostra_v2_2']],['Fora da fila P3 (amostra)',res['amostra_fora_fila_P3']],
 ['Fora da fila P3 (universo)',res['decisoes_v2_2_fora_fila_P3']],
 ['P3 elegíveis',res['decisoes_dentro_P3']],
 ['Restauradas à v2.1',res['reversoes_de_escopo']],
 ['Refinamentos P3',res['correcoes_de_intencao_dentro_P3']],
 ['Patches totais',res['patches_total']],
 ['P3 fora dos pilotos (estimado)',res['P3_fora_dos_pilotos_estimado']],
 ['Pendências P2',res['P2_pendentes']],
 ['Lotes verificados',res['lotes']],
 ['Registros-base',res['base']],['Controles',res['controles']]]
sh=wb.worksheets.add('Resumo')
sh.get_range_by_indexes(0,0,len(summary),2).values=summary
sh.get_range_by_indexes(0,0,len(summary),2).format.horizontal_alignment='center'
sh.get_range_by_indexes(0,0,len(summary),2).format.vertical_alignment='center'
sh.get_range('A1:B1').format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},
  'horizontal_alignment':'center','vertical_alignment':'center','row_height':26}
sh.get_range('A1:A15').format.column_width=43
sh.get_range('B1:B15').format.column_width=30
sh.freeze_panes.freeze_rows(1)

DATA=[('Amostra 72','p3-v2.3-revisao-amostra-72.csv'),
      ('QA P3 elegiveis','p3-v2.3-QA-10-P3-elegiveis.csv'),
      ('Pareceres 108','p3-v2.3-pareceres-108.csv'),
      ('Patches 100','p3-v2.3-patches.csv'),
      ('Quarentena 98','p3-v2.3-quarentena-98-propostas.csv'),
      ('Regressao','p3-v2.3-regressao-independente.csv')]
for name,file in DATA:
    rows=getrows(file)
    if not rows: continue
    fields=list(rows[0]); matrix=[fields]+[[r[k] for k in fields] for r in rows]
    sheet=wb.worksheets.add(name)
    rg=sheet.get_range_by_indexes(0,0,len(matrix),len(fields));rg.values=matrix
    rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center'
    rg.format.wrap_text=True;rg.format.row_height=30
    sheet.get_range_by_indexes(0,0,1,len(fields)).format={
        'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},
        'horizontal_alignment':'center','vertical_alignment':'center','row_height':31,'wrap_text':True}
    # Cap widths so long JSON remains in cells without giant spreadsheets.
    for j,col in enumerate(fields):
        width=16
        if col in ('Keyword','justificativa','justificativa_qa_p3_v2_3','parecer','motivo') or 'justificativa' in col:
            width=42
        if 'json' in col:width=36
        if 'id_global' in col or col=='lote':width=16
        sheet.get_range_by_indexes(0,j,len(matrix),1).format.column_width=width
    sheet.freeze_panes.freeze_rows(1)
file=P/'qa-P3-v2.3-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(file))
print('Exportado:',file.name,file.stat().st_size)
print(wb.inspect({'kind':'table','range':'Resumo!A1:B9','include':'values','table_max_rows':9,'table_max_cols':2}).ndjson[:1000])
