#!/usr/bin/env python3
"""Gera planilha centralizada de auditoria de marcas Ouro/Ouro escuro 1.
Fonte: CSVs gerados por auditar_e_filtrar_ouro.py; não modifica ODS/CSV originais.
"""
import csv,json
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parent
with (ROOT/'resumo.json').open(encoding='utf8') as f:meta=json.load(f)

def load(n):
 with (ROOT/n).open(encoding='utf-8-sig',newline='') as f:
  reader=csv.reader(f,delimiter=';');return list(reader)
wb=Workbook.create()

def write(name,rows,widths=None):
 sheet=wb.worksheets.add(name)
 rr=len(rows);cc=len(rows[0]);assert all(len(x)==cc for x in rows)
 sheet.get_range_by_indexes(0,0,rr,cc).values=rows
 body=sheet.get_range_by_indexes(0,0,rr,cc)
 body.format.horizontal_alignment='center';body.format.vertical_alignment='center'
 head=sheet.get_range_by_indexes(0,0,1,cc)
 head.format={'fill':'#17324D','font':{'color':'#FFFFFF','bold':True},'horizontal_alignment':'center','vertical_alignment':'center','row_height':27}
 sheet.freeze_panes.freeze_rows(1)
 if widths:
  for i,w in enumerate(widths):
   sheet.get_range_by_indexes(0,i,rr,1).format.column_width=w
 return sheet
summary=[['Métrica','Valor'],
 ['Arquivos ODS inspecionados',meta['arquivos_ods']],
 ['Células com Ouro',meta['ouro']],
 ['Células com Ouro escuro 1',meta['ouro_escuro_1']],
 ['Total de células coloridas',meta['celulas_douradas']],
 ['Sementes distintas normalizadas',meta['sementes_normalizadas_unicas']],
 ['Sementes encontradas na base',meta['sementes_encontradas_na_base']],
 ['Sementes ausentes na base',meta['sementes_nao_encontradas']],
 ['IDs-base encontrados',meta['ids_correspondentes_base']],
 ['IDs marcados para exclusão na cópia de trabalho',meta['ids_exclusao_segura']],
 ['IDs retidos para revisão (origem dupla)',meta['ids_origem_duplicada_revisar']],
 ['Base original (registros)',meta['base_antes']],
 ['Base de trabalho filtrada',meta['base_trabalho_depois']],
 ['Controles preservados',meta['controles']],
 ['P3 pendentes antes',meta['p3_elegiveis_antes']],
 ['P3 retiradas por marcas Ouro',meta['p3_removidos']],
 ['P3 pendentes após filtro',meta['p3_elegiveis_depois']],
 ['Homologação editorial',meta['aprovacao_editorial']]]
write('Resumo',summary,[48,35])
write('Planilhas ODS',load('estatistica-planilhas-ods.csv'),[32,18,24])
p3=load('ids-p3-ouro-removidos-100.csv')
# planilha de trabalho: colunas úteis e rastreabilidade completas nos CSVs
fields=['id_global','Keyword','area_principal','cor','arquivo_ods','aba_ods','linha_ods','match','decisao']
idx=[p3[0].index(k) for k in fields]
write('P3 removidas 100', [fields]+[[row[i] for i in idx] for row in p3[1:]], [16,57,18,20,32,18,15,15,30])
allbase=load('ids-ouro-cruzados-3621.csv')
fields2=['id_global','Keyword','area_principal','cor','lote_id','origens_douradas','tambem_aparece_sem_dourado','decisao']
indices=[allbase[0].index(k) for k in fields2]
write('Base 3621', [fields2]+[[r[i] for i in indices] for r in allbase[1:]], [14,51,19,19,14,18,28,36])
manual=load('ids-ouro-revisar-12.csv')
write('Revisão origem dupla', [fields2]+[[r[i] for i in indices] for r in manual[1:]], [14,51,19,19,14,18,28,36])
write('Sementes ausentes 9',load('sementes-douradas-sem-match-na-base-9.csv'),[42,54,23,31])
write('Regressão 30 lotes',load('regressao-30-lotes.csv'),[42,22,25,20,24,23])
path=ROOT/'qa-cores-ouro-p3-v5.2-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(path))
print(path, path.stat().st_size,'bytes')
print(wb.inspect({'kind':'table','range':'Resumo!A1:B18','include':'values','table_max_rows':18,'table_max_cols':2}).ndjson[:500])