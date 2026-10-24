#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planilha QA com células centralizadas em todas as abas (artifact_tool)."""
from pathlib import Path
import csv,json
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[2]
O=ROOT/'08-Entregas/P3-v5.2'
def csv_matrix(name):
 with (O/name).open(encoding='utf-8-sig',newline='') as f:
  d=csv.DictReader(f,delimiter=';');return [list(d.fieldnames)]+[[x[k] for k in d.fieldnames] for x in d]
a=json.loads((O/'p3-v5.2-resumo.json').read_text(encoding='utf-8'))
b=json.loads((O/'p3-v5.2-regressao-independente-resumo.json').read_text(encoding='utf-8'))
wb=Workbook.create()
def sheet(name,matrix,widths=None,height=32):
 s=wb.worksheets.add(name);rows=len(matrix);cols=max(map(len,matrix))
 s.get_range_by_indexes(0,0,rows,cols).values=[list(r)+['']*(cols-len(r)) for r in matrix]
 allr=s.get_range_by_indexes(0,0,rows,cols)
 allr.format.horizontal_alignment='center';allr.format.vertical_alignment='center';allr.format.wrap_text=True;allr.format.row_height=height
 header=s.get_range_by_indexes(0,0,1,cols);header.format.fill='#17324B';header.format.font.color='#FFFFFF';header.format.font.bold=True;header.format.row_height=35
 for c in range(cols):s.get_range_by_indexes(0,c,rows,1).format.column_width=widths[c] if widths and c<len(widths) else 23
 s.freeze_panes.freeze_rows(1)
 return s
sheet('Resumo',[
 ['Indicador','Resultado','Observação'],
 ['Versão',a['versao'],'Expansão seletiva nova, a partir da P3 v5.1'],
 ['Novos registros',75,'IDs antes elegíveis, sem modificar pareceres de v5.1'],
 ['Famílias',a['familias'],'Grupos familiares cobertos pela expansão'],
 ['Temas',a['grupos'],'Agrupamentos descritos na aba por tema'],
 ['P3 elegíveis antes',a['elegiveis_antes'],'Critério histórico estrito'],
 ['P3 elegíveis depois',a['elegiveis_depois'],'Redução de 75 casos'],
 ['P2 pendentes',4660,'Não reabertos'],
 ['Lotes validados','30/30','Regressão independente'],
 ['Keywords-base',294905,'Preservadas fora de alterações autorizadas'],
 ['Controles',2190,'Intactos'],
 ['Fila P3',23965,'Linhas anteriores preservadas'],
 ['Fila geral',52046,'Linhas anteriores preservadas'],
 ['Colunas anteriores',390,'Idênticas nas duas filas'],
 ['Novas colunas',8,'Rastreabilidade v5.2'],
 ['Backlog global',98,'Arquivo íntegro byte a byte'],
 ['Homologação','PENDENTE','Pareceres automatizados, aguardando avaliação editorial']
],widths=[30,29,79],height=28)
sheet('Pareceres 75',csv_matrix('p3-v5.2-decisoes-75.csv'),widths=[14,13,23,47,36,31,89,30,30,39,39,47,47,27,27,36,24],height=76)
sheet('Patches 75',csv_matrix('p3-v5.2-patches-75.csv'),widths=[14,44,22,48,35,54,88,88],height=92)
sheet('Plano por ID',csv_matrix('p3-v5.2-plano-por-id.csv'),widths=[14,50,23,14,39,22,18,84],height=68)
sheet('QA por tema',csv_matrix('p3-v5.2-qa-por-grupo.csv'),widths=[44,17,17,31,29],height=29)
sheet('Regressão 30',csv_matrix('p3-v5.2-regressao-independente-30-lotes.csv'),widths=[52,18,18,18,18,17],height=25)
sheet('Semântica',[
 ['Tema','Cuidado interpretativo','Consequência da auditoria'],
 ['Gestação/meses','Não converter semanas em meses civis fixos; nem inferir gestação quando ela não consta na consulta.','Saúde se explicitamente gestacional; conversor temporal nos termos genéricos.'],
 ['Cartão/juros','Sem valor financiado, taxa e prazo não há cálculo. Taxas bancárias dependem de condições e momento.','Separar consulta de taxa, planilha de controle e simulador.'],
 ['Salário','Bruto, base e líquido diferem; descontos dependem de contexto e competência.','Evitar classificar como construção, geometria, investimentos ou rescisão sem evidência.'],
 ['Jornada semanal','Horários semanais não são intervalos entre duas datas; horas por dia requerem dias trabalhados.','Cálculo só contextual; jornada como trabalho.'],
 ['Moda/mediana/média','Conceitos e fórmulas sem amostra não são pedidos de resultado numérico.','Intenção informacional; não inventar dados.'],
 ['BTU/h e W','BTU/h corresponde à potência térmica; consumo elétrico depende de eficiência e modelo.','Separar conversão térmica da demanda de energia elétrica.'],
 ['Arredondamento','Arredondamento de números e Excel é operação matemática, não calendário.','Classificação por aritmética/uso de ferramenta.'],
 ['Homologação','A revisão individual editorial não foi executada nesta expansão.','P3 v5.3 proposta para a revisão crítica das 75 decisões.']
],widths=[31,104,92],height=71)
sheet('Integridade',[
 ['Verificação','Resultado','Detalhes'],
 ['Regressão independente',b['status'],'Comparação completa 30 lotes e filas, registro a registro'],
 ['Patches',b['ids_alterados'],'Apenas 75 IDs elegíveis'],
 ['Bases',b['base'],'294.905 IDs-base em ordem original'],
 ['Controles',b['controles'],'2.190 intactos'],
 ['Filas','2 de 2 PASSOU','390 colunas históricas intactas, 8 adicionadas'],
 ['Backlog 98',b['backlog_global_98_byte_a_byte'],'Identidade byte a byte'],
 ['SHA-256 das fontes',b['sha256_fontes_protegidas'],'Protege as duas filas e backlog original v5.1'],
 ['Homologação','PENDENTE','Separar validação técnica de aprovação editorial']
],widths=[34,74,84],height=32)
print('INSPECT',wb.inspect({'kind':'table','range':'Resumo!A1:C8','include':'values','table_max_rows':8,'table_max_cols':3}).ndjson[:800])
path=O/'qa-auditoria-P3-v5.2-centralizada.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(path))
print('EXPORT',path.name,path.stat().st_size)