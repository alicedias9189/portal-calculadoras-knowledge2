#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera planilha de QA P3 v1.3 usando artifact_tool, com todas as células centralizadas.
Uso: python gerar_qa_p3_v1_3.py --saida <pasta com CSVs da P3 v1.3>
"""
import argparse,csv,json,collections,random
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

def ler(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();p=a.saida
 resumo=json.loads((p/'resumo-p3-v1.3.json').read_text(encoding='utf-8'))
 decisoes=ler(p/'p3-v1.3-decisoes-por-id.csv');patches=ler(p/'p3-v1.3-patches.csv');cinco=ler(p/'p3-v1.3-cinco-falsos-negativos.csv');reg=ler(p/'regressao-independente-30-lotes-p3-v1.3.csv')
 counts=collections.Counter(x['regra'] for x in decisoes)
 rng=random.Random(1303);por=collections.defaultdict(list)
 for item in decisoes:por[item['regra']].append(item)
 amostra=list(cinco)
 for rule,lst in sorted(por.items()):
  if rule not in ['algebra_fracoes','dissidio_2022','materiais_reboco','gasolina_online','km_l']:
   amostra+=rng.sample(lst,min(6,len(lst)))
 amostra=list({x['id_global']:x for x in amostra}.values());amostra.sort(key=lambda x:int(x['id_global']))
 amostraf=[dict(x,parecer_tecnico='Amostragem estratificada por regra; validar editorialmente antes de homologar') for x in amostra]
 regras=[{'regra':k,'decisões_analisadas':v,'nota':'Regra contextual, com revisão humana editorial ainda recomendada'} for k,v in counts.most_common()]
 sums=[['Métrica','Valor'],['Versão',resumo['versao']],['Base original (IDs)',resumo['registros_base']],['Controles preservados',resumo['controles']],['Universo P3',resumo['p3_total']],['Fora do piloto anterior',resumo['p3_fora_piloto_antes']],['5 falsos negativos avaliados',resumo['falsos_negativos_revistos']],['Falsos negativos com patch',resumo['falsos_negativos_alterados']],['Novas keywords com ajuste',resumo['novos_casos_alterados']],['Novas famílias',resumo['novas_familias_distintas']],['Patches totais',resumo['total_patches']],['P3 fora dos pilotos',resumo['p3_fora_piloto_restante']],['Testes por lote',resumo['lotes']],['Limitação','Automação conservadora; decisões não homologadas editorialmente']]
 wb=Workbook.create()
 def sheet(name, rows):
  s=wb.worksheets.add(name)
  if not rows:return
  if isinstance(rows[0],dict):
   keys=list(rows[0]); vals=[keys]+[[str(x.get(k,'')) for k in keys] for x in rows]
  else:vals=rows
  n=len(vals);m=len(vals[0]);s.get_range_by_indexes(0,0,n,m).values=vals
  rg=s.get_range_by_indexes(0,0,n,m);rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center';rg.format.row_height=24
  s.get_range_by_indexes(0,0,1,m).format={'fill':'#18324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':30}
  for j in range(m):
   width=22 if j<4 else 30
   if (isinstance(rows[0],dict) and list(rows[0])[j] in ['Keyword','justificativa','campos_alterados','justificativa_p3_v1_3']):width=48
   s.get_range_by_indexes(0,j,n,1).format.column_width=width
  s.freeze_panes.freeze_rows(1)
 sheet('Resumo',sums)
 sheet('Cinco falsos negativos',cinco)
 sheet('Decisoes P3 v1.3',decisoes)
 sheet('Patches antes depois',patches)
 sheet('Regras e contagens',regras)
 sheet('Amostra estratificada',amostraf)
 sheet('Regressao 30 lotes',reg)
 path=p/'qa-auditoria-P3-v1.3-centralizada.xlsx';SpreadsheetFile.export_xlsx(wb).save(str(path))
 print(json.dumps({'arquivo':str(path),'folhas':7,'decisoes':len(decisoes),'amostra':len(amostraf),'bytes':path.stat().st_size},ensure_ascii=False))
if __name__=='__main__':main()
