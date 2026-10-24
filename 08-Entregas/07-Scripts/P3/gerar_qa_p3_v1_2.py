#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cria planilha QA centralizada a partir dos CSVs produzidos por auditar_p3_v1_2.py.
Deps: artifact_tool. Uso: python gerar_qa_p3_v1_2.py --dados <pasta results>.
"""
import argparse,csv,json
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def ler(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def sheet(wb,title,cols,rows,max_col_width=42):
 sh=wb.worksheets.add(title)
 mat=[cols]+[[str(row.get(c,'')) for c in cols] for row in rows]
 sh.get_range_by_indexes(0,0,len(mat),len(cols)).values=mat
 rng=sh.get_range_by_indexes(0,0,len(mat),len(cols));rng.format.horizontal_alignment='center';rng.format.vertical_alignment='center';rng.format.row_height=23
 sh.get_range_by_indexes(0,0,1,len(cols)).format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':31}
 for i,c in enumerate(cols):
  width= min(max_col_width, 14 if c in ('id_global','lote','instituicao','tipo_intencao','resultado','acao','status_qa') else (38 if 'Keyword' in c else (44 if any(s in c for s in ('justificativa','ressalva','nota','evidencia','classificacao')) else 25)))
  sh.get_range_by_indexes(0,i,len(mat),1).format.column_width=width
 sh.freeze_panes.freeze_rows(1)
 return sh

def main():
 p=argparse.ArgumentParser();p.add_argument('--dados',type=Path,required=True);a=p.parse_args();d=a.dados
 result=json.loads((d/'resumo-p3-v1.2.json').read_text(encoding='utf-8'))
 wb=Workbook.create()
 metrics=[('Métrica','Valor'),('Versão',result['versao']),('Saúde: aplicações',result['total_saude']),('Saúde: suspensas da v1.1',result['saude_suspensos_anteriores']),('Saúde: falsos negativos da amostra',result['saude_falsos_negativos_amostra']),('Alertas bancários revisados',result['alertas_bancarios_auditados']),('Navegacionais aplicados',result['navegacionais_aplicados']),('Intenções mistas preservadas',result['intencao_mista_preservada']),('Registros alterados',result['ids_alterados']),('Registros-base preservados',result['registros_base']),('Controles preservados',result['controles']),('Lotes validados',result['lotes_testados']),('P3 não incluída no piloto',result['p3_fora_piloto']),('P2 pendências restantes',result['p2_pendencias_remanescentes']),('Revisão editorial','Pendente; resultados técnicos em versão paralela')]
 sheet(wb,'Resumo',['Métrica','Valor'],[dict(zip(['Métrica','Valor'],r)) for r in metrics[1:]])
 for title,filename in [('Simuladores (43)','auditoria-43-simuladores.csv'),('Saude (187)','auditoria-saude-187.csv'),('Patches (214)','patches-214-p3-v1.2.csv'),('Regressao (30)','regressao-30-lotes-p3-v1.2.csv')]:
  rs=ler(d/filename);sheet(wb,title,list(rs[0]),rs)
 out=d/'qa-p3-v1.2-centralizada.xlsx'
 SpreadsheetFile.export_xlsx(wb).save(str(out))
 print('EXPORTED',out,out.stat().st_size)
 print('SHEETS',wb.inspect({'kind':'sheet','include':'id,name'}).ndjson[:1300])
 print('SUMMARY',wb.inspect({'kind':'table','range':'Resumo!A1:B9','include':'values','table_max_rows':9,'table_max_cols':2}).ndjson[:1300])
if __name__=='__main__':main()
