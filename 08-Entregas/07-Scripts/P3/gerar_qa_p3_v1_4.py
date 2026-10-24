#!/usr/bin/env python3
"""Gera planilha P3 v1.4, todas as células usadas centralizadas, via artifact_tool."""
import argparse,csv,json,collections,random
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def load(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def main():
 a=argparse.ArgumentParser();a.add_argument('--saida',type=Path,required=True);out=a.parse_args().saida
 summary=json.loads((out/'resumo-p3-v1.4.json').read_text()); audit=load(out/'p3-v1.4-amostra-67-pareceres.csv');patches=load(out/'p3-v1.4-patches.csv');decisions=load(out/'p3-v1.4-decisoes-por-id.csv'); reg=load(out/'regressao-independente-30-lotes-p3-v1.4.csv')
 by=collections.defaultdict(list); fam=collections.defaultdict(set)
 for d in decisions:by[d['regra']].append(d);fam[d['regra']].add(d['familia_id'])
 rules=[{'regra':k,'registros':len(v),'familias':len(fam[k]),'tipo':'correção da amostra' if k in ['fracao_calculadora_celular','concreto_piso_garagem'] else 'regra contextual em P3 ainda fora do piloto'} for k,v in sorted(by.items(),key=lambda x:-len(x[1]))]
 rng=random.Random(1404)
 sample=[]
 for k,lst in sorted(by.items()):
  if k in ('fracao_calculadora_celular','concreto_piso_garagem'):sample+=lst
  else:sample+=rng.sample(lst,min(6,len(lst)))
 sample.sort(key=lambda x:int(x['id_global']))
 metr=[['Métrica','Valor'],['Etapa','P3 v1.4'],['Amostra crítica de decisões',summary['amostra_v1_3_verificada']],['Falsos positivos identificados',summary['falsos_positivos_amostra_corrigidos']],['Novas classificações de P3',summary['novos_registros_expandidos']],['Famílias novas',summary['familias_novas_distintas']],['Total de patches',summary['total_patches']],['P3 fora dos pilotos antes',summary['p3_fora_antes']],['P3 fora dos pilotos restante',summary['p3_fora_pilotos_restante']],['Lotes testados',summary['lotes']],['Total bases',summary['registros_base']],['Total controles',summary['controles']],['Limitação','Decisões por regras, ainda não homologadas editorialmente']]
 wb=Workbook.create()
 def add(name,rows):
  s=wb.worksheets.add(name)
  if not rows:return
  if isinstance(rows[0],dict):
   cols=list(rows[0]);v=[cols]+[[str(x.get(k,'')) for k in cols] for x in rows]
  else:cols=rows[0];v=rows
  count=len(v); width=len(v[0]);r=s.get_range_by_indexes(0,0,count,width);r.values=v;r.format.horizontal_alignment='center';r.format.vertical_alignment='center';r.format.row_height=24
  head=s.get_range_by_indexes(0,0,1,width);head.format={'fill':'#17344F','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':30}
  for j,k in enumerate(cols):
   size=20 if j<3 else 25
   if k in ('Keyword','justificativa','motivo','campos_alterados','antes_json','depois_json','regra_original'):size=43
   s.get_range_by_indexes(0,j,count,1).format.column_width=size
  s.freeze_panes.freeze_rows(1)
 add('Resumo',metr)
 add('Amostra critica 67',audit)
 add('Patches antes depois',patches)
 add('Decisoes P3 v1.4',decisions)
 add('Regras e familias',rules)
 add('Amostra expansao',sample)
 add('Regressao 30 lotes',reg)
 path=out/'qa-auditoria-P3-v1.4-centralizada.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(path))
 print(json.dumps({'planilha':str(path),'bytes':path.stat().st_size,'abas':7,'amostra':len(audit),'expansao_amostra':len(sample)},ensure_ascii=False))
if __name__=='__main__':main()
