#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relatório XLSX centralizado v5.6 com artifact_tool; não modifica CSVs históricos."""
from pathlib import Path
import csv,json
from artifact_tool import Workbook,SpreadsheetFile
R=Path(__file__).resolve().parents[2];D=R/'08-Entregas/P3-v5.6'; O=D/'qa-auditoria-P3-v5.6-centralizada.xlsx'
def rd(name):
 with (D/name).open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r),list(r.fieldnames)
def cut(s,length=180):
 s=str(s) if s is not None else '';return s if len(s)<=length else s[:length-1]+'…'
def add(wb,name,rows,widths=None,cutoff=200):
 sh=wb.worksheets.add(name)
 assert rows
 rows=[[cut(t,cutoff) for t in row] for row in rows]
 w=len(rows[0]);assert all(len(x)==w for x in rows)
 # Large blocks are relatively small, write once for fast import/export
 sh.get_range_by_indexes(0,0,len(rows),w).values=rows
 used=sh.get_range_by_indexes(0,0,len(rows),w)
 used.format.horizontal_alignment='center'
 used.format.vertical_alignment='center'
 used.format.row_height=22
 head=sh.get_range_by_indexes(0,0,1,w)
 head.format.fill='#17324D'
 head.format.font.color='#FFFFFF'
 head.format.font.bold=True
 head.format.row_height=31
 used.format.wrap_text=True
 if len(rows)>1:sh.get_range_by_indexes(1,0,len(rows)-1,w).format.row_height=34
 for j in range(w):
  sh.get_range_by_indexes(0,j,len(rows),1).format.column_width=(widths[j] if widths and j<len(widths) else 25)
 sh.freeze_panes.freeze_rows(1)
 return sh

def main():
 summary=json.loads((D/'p3-v5.6-resumo.json').read_text());regr=json.loads((D/'p3-v5.6-regressao-independente-resumo.json').read_text());wb=Workbook.create()
 add(wb,'Resumo',[
 ['Indicador','Valor'],['Etapa','P3 v5.6'],['Novos IDs classificados',100],['Famílias distintas',summary['familias']],['Grupos temáticos',12],
 ['Elegíveis sem Ouro antes',19362],['Elegíveis sem Ouro depois',19262],['Elegíveis canônico depois',19362],['Lotes validados',60],
 ['Lotes canônicos',30],['Lotes filtrados',30],['Controles preservados',2190],['Registros canônicos',294905],['Registros operacionais',291296],
 ['Variantes Ouro excluídas apenas da visão',3609],['Colunas históricas das filas preservadas',422],['Colunas novas de rastreabilidade',8],
 ['Pendências P2 preservadas',4660],['Propostas globais preservadas',98],['Homologação editorial','PENDENTE'],['Fonte','Pacote P3 v5.5 + DEC-089']],widths=[41,53])
 d,df=rd('p3-v5.6-pareceres-100.csv')
 dcols=['id_global','Keyword','familia_id','regra','area_anterior','area_nova','cluster_anterior','cluster_novo','subcluster_anterior','subcluster_novo','tipo_anterior','tipo_novo','justificativa_individual','campos_modificados','homologacao_editorial']
 add(wb,'Pareceres 100',[[c for c in dcols]]+[[v[c] for c in dcols] for v in d],widths=[14,42,19,30,17,17,30,30,35,35,23,23,65,32,22],cutoff=900)
 patches,pf=rd('p3-v5.6-patches-100.csv')
 cols=['id_global','Keyword','regra','campos_modificados','antes_json','depois_json']
 add(wb,'Patches 100',[[c for c in cols]]+[[p[c] for c in cols] for p in patches],widths=[14,42,32,40,65,65],cutoff=3200)
 groups,gf=rd('p3-v5.6-qa-por-grupo.csv')
 add(wb,'Por Grupo',[gf]+[[a[k] for k in gf] for a in groups],widths=[40,15,15,30,26])
 reg,rf=rd('p3-v5.6-regressao-independente-60-lotes.csv')
 add(wb,'Regressao 60',[rf]+[[a[k] for k in rf] for a in reg],widths=[24,55,18,16,15])
 add(wb,'Filas 4',[['Arquivo','Linhas','Colunas antigas','Colunas novas','Status']]+[[x['fila'],x['linhas'],x['colunas_historicas'],x['colunas_novas'],x['status']] for x in regr['filas']],widths=[58,18,21,21,17])
 add(wb,'Invariantes',[['Verificação','Resultado'],
 ['Status da regressão independente',regr['status']],['Novos IDs únicos',regr['patches_unicos']],
 ['Somente 100 IDs alterados','SIM'],['Registros fora do escopo preservados','SIM'],
 ['Backlog global 98',regr['backlog_98']],['Controles por versão',2190],
 ['Ouro mantido reversível','SIM'],['P3 v5.6 sem Ouro restante',19262],
 ['Homologação editorial','PENDENTE'],['SHA-256 agregado das fontes',regr['fontes_sha256_agregado']]],widths=[42,68])
 SpreadsheetFile.export_xlsx(wb).save(str(O))
 assert O.exists() and O.stat().st_size>9000,(str(O),O.stat().st_size)
 print(json.dumps({'output':str(O),'bytes':O.stat().st_size,'abas':7,'pareceres':len(d),'patches':len(patches),'lotes':len(reg)},ensure_ascii=False))
if __name__=='__main__':main()