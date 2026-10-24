#!/usr/bin/env python3
# coding: utf-8
"""Planilha QA P3 v3.0, todas as células centralizadas, via artifact_tool.
Executar: python 07-Scripts/P3/gerar_qa_p3_v30.py
"""
import csv,json,collections
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
R=Path(__file__).resolve().parents[2]; O=R/'08-Entregas/P3-v3.0'
def rows(name):
 with (O/name).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r)
summary=json.loads((O/'p3-v3.0-resumo.json').read_text(encoding='utf-8'))
wb=Workbook.create()

def sheet(title,head,data,widths=None):
 sh=wb.worksheets.add(title)
 matrix=[head]+[[str(v) if v is not None else '' for v in row] for row in data]
 nr=len(matrix);nc=len(head)
 rng=sh.get_range_by_indexes(0,0,nr,nc);rng.values=matrix
 rng.format.horizontal_alignment='center';rng.format.vertical_alignment='center';rng.format.wrap_text=True
 rng.format.row_height=30
 hdr=sh.get_range_by_indexes(0,0,1,nc)
 hdr.format={'fill':'#233954','font':{'color':'#FFFFFF','bold':True},'horizontal_alignment':'center','vertical_alignment':'center','row_height':35,'wrap_text':True}
 for j in range(nc):
  sh.get_range_by_indexes(0,j,nr,1).format.column_width=(widths[j] if widths else 24)
 sh.freeze_panes.freeze_rows(1)
 return sh

sheet('Resumo',['Indicador','Resultado'],[
 ('Versão',summary['versao']),('Novos ajustes',summary['novos_ajustes']),('Famílias afetadas',summary['familias']),
 ('P3 pendente antes',summary['fora_do_piloto_antes']),('P3 pendente depois',summary['fora_do_piloto_depois']),
 ('P2 preservada',summary['P2_pendentes']),('Global em quarentena',summary['globais_separados']),
 ('Registros-base',summary['base']),('Registros de controle',summary['controles']),('Lotes aprovados',30),
 ('Status editorial',summary['homologacao'])],[29,40])
sheet('Regras',['Regra','Alterações'],sorted(summary['regras'].items()),[42,18])
decs=rows('p3-v3.0-decisoes.csv')
sheet('Decisões_36',['ID','Palavra-chave','Família','Regra','Área anterior','Cluster anterior','Área proposta','Cluster proposto','Subcluster proposto','Tipo proposto','Justificativa'],[
 [r['id_global'],r['Keyword'],r['familia_id'],r['regra'],r['area_anterior'],r['cluster_anterior'],r['area_proposta'],r['cluster_proposto'],r['subcluster_proposto'],r['tipo_proposto'],r['justificativa']] for r in decs],[12,46,20,43,19,27,19,27,40,26,70])
qa=rows('p3-v3.0-revisao-qa-36.csv')
sheet('QA_integral_36',['ID','Palavra-chave','Regra','Parecer','Risco residual','Elegibilidade'],[
 [r['id_global'],r['Keyword'],r['regra'],r['parecer_tecnico'],r['risco_residual'],r['validacao_de_escopo']] for r in qa],[12,48,42,30,70,23])
pat=rows('p3-v3.0-patches.csv')
sheet('Patches_36',['ID','Palavra-chave','Regra','Campos modificados','Antes (JSON)','Depois (JSON)'],[
 [r['id_global'],r['Keyword'],r['regra'],r['campos_modificados'],r['antes_json'],r['depois_json']] for r in pat],[12,48,42,47,90,90])
reg=rows('p3-v3.0-regressao-independente-30-lotes.csv')
sheet('Regressão_30',['Lote','Base','Controles','Patches','Campos protegidos','Resultado'],[
 [r['lote'],r['base'],r['controles'],r['alteracoes'],r['campos_protegidos'],r['status']] for r in reg],[45,14,14,13,25,17])
tests=rows('p3-v3.0-testes-escopo.csv')
sheet('Testes_escopo',['Teste','Resultado','Status'],[[r['teste'],r['resultado'],r['status']] for r in tests],[49,29,17])
output=O/'qa-auditoria-P3-v3.0-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(output))
print('EXPORTADO',output,output.stat().st_size,'abas',7)
