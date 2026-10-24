#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera planilha de QA P3 v5.5 (oito abas) com células centralizadas via artifact_tool."""
from pathlib import Path
import csv,json
from collections import Counter
from artifact_tool import Workbook,SpreadsheetFile
R=Path(__file__).resolve().parents[2];D=R/'08-Entregas/P3-v5.5';OUTPUT=D/'qa-auditoria-P3-v5.5-centralizada.xlsx'
def rd(name):
 with (D/name).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r),list(r.fieldnames)
def clip(x,limit=3000):
 if x is None:return ''
 if isinstance(x,(float,int)):return x
 s=str(x);return s if len(s)<limit else s[:limit-1]+'…'
def add(wb,name,rows,widths=None,limit=3200):
 assert rows
 sh=wb.worksheets.add(name)
 arr=[[clip(x,limit) for x in row] for row in rows];width=len(arr[0]);assert all(len(x)==width for x in arr)
 content=sh.get_range_by_indexes(0,0,len(arr),width);content.values=arr
 content.format.horizontal_alignment='center';content.format.vertical_alignment='center'
 content.format.wrap_text=True;content.format.row_height=30
 hd=sh.get_range_by_indexes(0,0,1,width);hd.format.fill='#17324D';hd.format.font.color='#FFFFFF';hd.format.font.bold=True;hd.format.row_height=36
 for j in range(width):sh.get_range_by_indexes(0,j,len(arr),1).format.column_width=widths[j] if widths and j<len(widths) else 26
 sh.freeze_panes.freeze_rows(1)
 return sh

def main():
 summary=json.loads((D/'p3-v5.5-resumo.json').read_text());reg=json.loads((D/'p3-v5.5-regressao-independente-resumo.json').read_text())
 opinions,_=rd('p3-v5.5-pareceres-100.csv');patches,_=rd('p3-v5.5-patches-23.csv');results,_=rd('p3-v5.5-regressao-independente-60-lotes.csv')
 w=Workbook.create()
 add(w,'Resumo',[
 ['Indicador','Valor'],['Versão','P3 v5.5'],['Registros revisados',100],['Refinamentos',23],['Mantidos com ressalvas',77],['Novos IDs',0],
 ['Famílias revistas',34],['Grupos temáticos',7],['P3 operacionais elegíveis',19362],['P3 canônicos elegíveis',19462],
 ['Lotes validados',60],['Controles por versão',2190],['Base canônica',294905],['Base sem Ouro',291296],
 ['IDs Ouro apenas removidos de cópias operacionais',3609],['Colunas históricas intactas',414],['Novas colunas de rastreabilidade',8],
 ['Pendências P2 mantidas',4660],['Propostas globais intactas',98],['Homologação editorial','PENDENTE']],widths=[56,55])
 col=['id_global','Keyword','familia_id','regra_v5_4','parecer_v5_5','area_v5_4','area_v5_5','cluster_v5_4','cluster_v5_5','subcluster_v5_4','subcluster_v5_5','tipo_v5_4','tipo_v5_5','justificativa_individual','campos_modificados','homologacao_editorial']
 add(w,'Pareceres 100',[col]+[[r[k] for k in col] for r in opinions],widths=[14,46,18,33,25,17,17,30,30,42,42,23,23,75,38,22])
 col=['id_global','Keyword','campos_modificados','antes_json','depois_json','justificativa']
 add(w,'Patches 23',[col]+[[r[k] for k in col] for r in patches],widths=[14,48,38,75,75,70])
 groups=Counter((x['regra_v5_4'],x['parecer_v5_5']) for x in opinions)
 gr=sorted({x['regra_v5_4'] for x in opinions})
 add(w,'Por grupo',[['Tema','Revisados','Refinados','Mantidos com ressalvas']]+[[g,sum(groups[g,p] for p in ('REFINADO','MANTIDO_COM_RESSALVA')),groups[g,'REFINADO'],groups[g,'MANTIDO_COM_RESSALVA']] for g in gr],widths=[43,18,18,28])
 headers=['base','lote','registros','refinamentos','status']
 add(w,'Regressao 60',[headers]+[[r[k] for k in headers] for r in results],widths=[22,62,18,19,17])
 add(w,'Filas 4',[['Arquivo','Linhas','Colunas históricas','Colunas novas','Status']]+[[r['fila'],r['linhas'],r['colunas_historicas'],r['colunas_novas'],r['status']] for r in reg['filas']],widths=[64,18,24,20,16])
 add(w,'Invariantes',[['Teste','Resultado'],['Regressão independente','PASSOU'],['Pareceres individualizados','100/100'],['Patches com antes/depois','23/23'],
 ['IDs externos à lista mantidos','SIM'],['Quatro filas intactas nas 414 colunas anteriores','SIM'],['Controles por versão','2190'],
 ['Filtro Ouro reversível','SIM'],['Backlog de 98 propostas','Idêntico byte a byte'],['Homologação editorial','PENDENTE'],
 ['Hash SHA-256 das fontes',reg['fontes_sha256_agregado']]],widths=[60,76])
 add(w,'Ressalvas críticas',[['Assunto','IDs / exemplo','Ressalva'],
 ['Direitos gerais de gestantes','136285, 164997, 178133, 178415, 178446, 188626','O âmbito jurídico não está explicitado; não presumir estabilidade do emprego nem concluir direito individual.'],
 ['Condições de trabalho','165052, 188627, 188635','Retorno, adaptação e afastamento não são equivalentes; contexto ocupacional e clínico ausente.'],
 ['Simulações de investimento','172075, 266225, 267764','Simular não prova procura por software; não inventar rentabilidade ou condições de mercado.'],
 ['Liquidez de investimento','171981','Liquidez mensal pode significar janela de resgate ou recebimento periódico de rendimentos.'],
 ['Planilhas genéricas','184208, 202634, 203445, 203453, 203923, 203930','Não presumir uso pessoal quando não há indicação de público.'],
 ['Média do ENEM','73452, 182404, 182406, 189385, 253475, 253522','Média de notas não é automaticamente nota de corte; distinção entre média simples e ponderada.'],
 ['Calendário gestacional','60171','Material de referência não representa cálculo já parametrizado.'],
 ['Juros de fatura','152171','A existência de juros não implica parcelamento formal ou modalidade específica.']],widths=[42,42,88])
 SpreadsheetFile.export_xlsx(w).save(str(OUTPUT))
 assert OUTPUT.exists() and OUTPUT.stat().st_size>10000
 print(json.dumps({'arquivo':str(OUTPUT),'bytes':OUTPUT.stat().st_size,'abas':8,'pareceres':len(opinions),'patches':len(patches)},ensure_ascii=False))
if __name__=='__main__':main()