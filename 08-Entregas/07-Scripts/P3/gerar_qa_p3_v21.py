#!/usr/bin/env python3
# coding: utf-8
"""Gera XLSX P3 v2.1 somente com artifact_tool, células centralizadas."""
import csv,json,pathlib,collections
from artifact_tool import Workbook,SpreadsheetFile
ROOT=pathlib.Path(__file__).resolve().parents[2]; OUT=ROOT/'08-Entregas/P3-v2.1'

def read(name):
 with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
wb=Workbook.create()
def sheet(name,cols,rows,widths=None):
 s=wb.worksheets.add(name)
 data=[cols]+[[str(r.get(k,'')) for k in cols] for r in rows]
 nr=len(data);nc=len(cols)
 # Write in batches to avoid size limits.
 for i in range(0,nr,100):
  chunk=data[i:i+100]
  s.get_range_by_indexes(i,0,len(chunk),nc).values=chunk
 rg=s.get_range_by_indexes(0,0,nr,nc)
 rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=23
 head=s.get_range_by_indexes(0,0,1,nc)
 head.format={'fill':'#183451','font':{'color':'#FFFFFF','bold':True},'horizontal_alignment':'center','vertical_alignment':'center','row_height':31}
 for i,k in enumerate(cols):
  w=(widths or {}).get(k, 24 if len(k)>25 else 20)
  s.get_range_by_indexes(0,i,nr,1).format.column_width=min(52,w)
 s.freeze_panes.freeze_rows(1)
 return s
meta=json.loads((OUT/'p3-v2.1-resumo.json').read_text())
counts=collections.Counter(x['regra'] for x in read('p3-v2.1-revisao-amostra-165.csv'))
ct=collections.Counter(x['parecer_qa_p3_v2_1'] for x in read('p3-v2.1-revisao-amostra-165.csv'))
summary=[
 {'Indicador':'Versão','Resultado':'P3 v2.1'},
 {'Indicador':'Registros da amostra revisados','Resultado':meta['amostra_revisada']},
 {'Indicador':'Decisões P3 v2.0 avaliadas no total','Resultado':meta['universo_auditado']},
 {'Indicador':'Correções na amostra','Resultado':meta['patches_amostra']},
 {'Indicador':'Correções fora da amostra (CET)','Resultado':1},
 {'Indicador':'Total de patches','Resultado':meta['patches']},
 {'Indicador':'Mantidas sem novos alertas','Resultado':ct['MANTIDO']},
 {'Indicador':'Mantidas com ressalvas','Resultado':ct['MANTIDO_COM_RESSALVA']},
 {'Indicador':'P3 fora dos pilotos','Resultado':meta['P3_fora_dos_pilotos']},
 {'Indicador':'P2 pendências','Resultado':meta['P2_pendentes']},
 {'Indicador':'Lotes de regressão','Resultado':30},
 {'Indicador':'Controle e IDs preservados','Resultado':'294.905 registros-base / 2.190 controles'},
 {'Indicador':'Escopo','Resultado':'Revisão contextual por ID; não homologação editorial'}]
sheet('Resumo',['Indicador','Resultado'],summary,{'Indicador':44,'Resultado':52})
cols=['id_global','lote','familia_id','Keyword','regra','confianca_regra','parecer_qa_p3_v2_1','nota_qa_p3_v2_1','alteracao_no_lote']
sheet('Amostra 165',cols,read('p3-v2.1-revisao-amostra-165.csv'),{'Keyword':48,'nota_qa_p3_v2_1':52,'parecer_qa_p3_v2_1':25,'regra':32})
sheet('Pareceres 272',cols,read('p3-v2.1-pareceres-272.csv'),{'Keyword':48,'nota_qa_p3_v2_1':52,'parecer_qa_p3_v2_1':25,'regra':32})
patch_cols=['id_global','lote','familia_id','Keyword','regra_anterior','justificativa','campos_modificados','antes_json','depois_json']
sheet('Patches 13',patch_cols,read('p3-v2.1-patches.csv'),{'Keyword':48,'justificativa':52,'campos_modificados':50,'antes_json':52,'depois_json':52})
regr=[]
for name in sorted(counts):
 rr=[r for r in read('p3-v2.1-revisao-amostra-165.csv') if r['regra']==name]
 states=collections.Counter(q['parecer_qa_p3_v2_1'] for q in rr)
 regr.append({'Regra':name,'Amostra':len(rr),'Corrigidos':states['CORRIGIDO'],'Mantidos':states['MANTIDO'],'Com ressalvas':states['MANTIDO_COM_RESSALVA'],'Taxa na amostra':f"{states['CORRIGIDO']/len(rr):.1%}",'Nota':'Amostra estratificada, não representativa de todos os 294.905 registros'})
sheet('Regras',list(regr[0]),regr,{'Regra':33,'Nota':51})
sheet('Regressao 30', ['lote','base','controles','alteracoes','protegidos_ok','status'],read('p3-v2.1-regressao-independente.csv'),{'lote':49})
out=OUT/'qa-P3-v2.1-centralizada.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(out))
print('Excel',out,out.stat().st_size)
