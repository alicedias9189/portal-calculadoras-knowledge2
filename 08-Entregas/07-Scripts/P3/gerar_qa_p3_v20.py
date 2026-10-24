#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA centralizada P3 v2.0. Requer artifact_tool; CSV completos são fonte canônica."""
import argparse,csv,json,collections
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
pa=argparse.ArgumentParser();pa.add_argument('--resultados',type=Path,required=True);pa.add_argument('--saida',type=Path,required=True);a=pa.parse_args()
B=a.resultados;sumr=json.loads((B/'p3-v2.0-resumo.json').read_text(encoding='utf-8'))

def rows(name):
 with (B/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

patch=rows('p3-v2.0-patches.csv');regras=rows('p3-v2.0-regras-resumo.csv');samples=rows('p3-v2.0-amostra-qa.csv');reg=rows('p3-v2.0-regressao-independente-30-lotes.csv')
details=[]
for p in patch:
 d=json.loads(p['diff_json'])
 for k,v in d.items():details.append([p['id_global'],p['Keyword'],p['regra'],k,v['antes'],v['depois']])
wb=Workbook.create()

def add(name,head,data,widths=None):
 sh=wb.worksheets.add(name)
 matrix=[head]+[[str(v) if v is not None else '' for v in rr] for rr in data]
 nrow=len(matrix);ncol=len(head)
 if len(matrix)>1:
  step=250
  for i in range(0,nrow,step):sh.get_range_by_indexes(i,0,min(step,nrow-i),ncol).values=matrix[i:i+step]
 else:sh.get_range_by_indexes(0,0,1,ncol).values=matrix
 rg=sh.get_range_by_indexes(0,0,nrow,ncol)
 rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=23
 rg.format.wrap_text=True
 hdr=sh.get_range_by_indexes(0,0,1,ncol)
 hdr.format={'fill':'#153A54','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':31}
 sh.freeze_panes.freeze_rows(1)
 if widths:
  for idx,w in enumerate(widths):sh.get_range_by_indexes(0,idx,nrow,1).format.column_width=w
 return sh

overview=[
 ['Versão','P3 v2.0'],['Base','P3 v1.9'],['Total P3',sumr['universo_p3']],
 ['Fora dos pilotos antes',sumr['pendentes_fora_pilotos_antes']],['Alterações',sumr['reclassificados']],
 ['Fora dos pilotos depois',sumr['pendentes_fora_pilotos_depois']],['Famílias alteradas',sumr['familias_afetadas']],
 ['Regras semânticas',len(sumr['regras'])],['Amostra estratificada',sumr['amostra_qa']],
 ['Lotes auditados',30],['IDs da base preservados',sumr['registros_base']],['Controles preservados',sumr['controles']],
 ['Homologação editorial','PENDENTE'],['Pendências P2 preservadas',4660],
 ['Cautela','Classificação por regras, revisão editorial individual não concluída']]
add('Resumo',['Indicador','Valor'],overview,[36,78])
add('Regras',['Regra','Registros','Triagem de amostra'],[[r['regra'],int(r['quantidade']),r['amostra_qa_revisada']] for r in regras],[39,15,30])
add('Decisoes P3',["ID","Keyword","Família","Lote","Regra","Ressalva","Motivo"],
 [[p['id_global'],p['Keyword'],p['familia_id'],p['lote'],p['regra'],p['confianca_regra'],p['justificativa']] for p in patch],
 [15,48,28,12,40,18,70])
add('Alteracoes por campo',['ID','Keyword','Regra','Campo','Antes','Depois'],details,[14,47,38,31,50,50])
add('Amostra QA',['ID','Keyword','Família','Regra','Ressalva','Justificativa'],
 [[p['id_global'],p['Keyword'],p['familia_id'],p['regra'],p['confianca_regra'],p['justificativa']] for p in samples],[14,52,26,39,20,70])
add('Regressao 30 lotes',['Lote','IDs base','Controles','Patches','Status'],
 [[int(r['lote']),int(r['base']),int(r['controles']),int(r['patches']),r['status']] for r in reg],[12,15,16,16,20])
a.saida.parent.mkdir(parents=True,exist_ok=True)
SpreadsheetFile.export_xlsx(wb).save(str(a.saida))
print('PLANILHA',a.saida,'folhas',6,'linhas patches',len(patch),'linhas diff',len(details),'amostra',len(samples))
