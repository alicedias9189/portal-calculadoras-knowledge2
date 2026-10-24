#!/usr/bin/env python3
"""Gera planilha de auditoria P2 v7 centralizada com artifact_tool. CSVs completos ficam no ZIP de auditoria."""
import csv,io,zipfile,json,collections,random
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE/'08-Entregas/P2-v7';ROOT.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ROOT/'auditoria-p2-v7-csv-integral.zip') as z:
 def rows(name):
  with z.open(name) as b:return list(csv.DictReader(io.TextIOWrapper(b,encoding='utf-8-sig',newline=''),delimiter=';'))
 p=rows('p2-v7-patches.csv');pending=rows('p2-v7-pendencias-restantes.csv');families=rows('p2-v7-familias-analisadas.csv');qa=rows('p2-v7-qa-regressao-30-lotes.csv');fila=rows('p2-v7-fila-geral.csv')
summary=json.loads((ROOT/'resumo-p2-v7.json').read_text())
reg=collections.Counter(patch['regra'] for patch in p)
random.seed(20261020)
bycluster=collections.defaultdict(list)
for x in pending:bycluster[x['cluster']].append(x)
selection=[]
for cluster,l in sorted(bycluster.items(),key=lambda kv:-len(kv[1])):
 selection += l[:min(9,len(l))]
 if len(selection)>270:break
if len(selection)<280:
 rr=[x for x in pending if x not in selection];selection+=random.sample(rr,min(280-len(selection),len(rr)))
p3=[x for x in fila if x['prioridade']=='P3'];p3dist=collections.Counter(x['cluster'] for x in p3)
w=Workbook.create()
def make(title,headers,items,widths=None):
 s=w.worksheets.add(title)
 n=len(headers)
 s.get_range_by_indexes(0,0,1,n).values=[headers]
 chunk=400
 for i in range(0,len(items),chunk):
  data=[[str(v) if v is not None else '' for v in line] for line in items[i:i+chunk]]
  s.get_range_by_indexes(i+1,0,len(data),n).values=data
 used=s.get_range_by_indexes(0,0,len(items)+1,n)
 used.format.horizontal_alignment='center';used.format.vertical_alignment='center';used.format.row_height=24
 s.get_range_by_indexes(0,0,1,n).format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':30}
 for j in range(n): s.get_range_by_indexes(0,j,len(items)+1,1).format.column_width=(widths[j] if widths and j<len(widths) else 22)
 s.freeze_panes.freeze_rows(1)
 return s
make('Resumo',['Indicador','Valor','Observação'],[
 ['Versão','P2 v7','Revisão conservadora sobre P2 v6'],['Universo P2','25050','Keywords sob prioridade P2'],['Pendências recebidas','4761','Não classificadas após v6'],['Classificadas nesta passagem',str(summary['reclassificadas']),'Apenas por evidência explícita'],['Sem ressalva',str(summary['sem_ressalva']),'Alta confiança da regra; não homologação humana'],['Com ressalva',str(summary['com_ressalva']),'Necessita inputs/condições ou revisão editorial'],['Restantes',str(summary['pendencias_restantes']),'Conservar como pendente contextual'],['Famílias alteradas',str(summary['familias_com_patches']),'Nenhum ajuste automático por herança de família'],['Percentual resolvido',f"{100*summary['reclassificadas']/4761:.2f}%",'Indicador de rendimento desta passada'],['IDs base preservados','294905','Não perdeu nenhum registro'],['Controles preservados','2190','73 por lote'],['Lotes aprovados','30/30','Regressão independente'],['Golden Set','Não reexecutado','Teste estrutural não equivale a teste semântico completo'],['P3 aguardando',str(len(p3)),'Oportunidade de priorização após esta P2'],['P3 famílias',str(len({x['familia_id'] for x in p3})),'Não assumir que todas são calculadoras'],['Próxima decisão','Iniciar P3','P2 manter backlog 4660 para revisão específica'],['Dados completos','ZIP CSV + lotes','Esta planilha contém patches e amostra, não todos os 294905 registros']],[34,25,80])
make('Regras',['Regra','Quantidade','Exemplo da consulta'],[[k,str(n),next((v['Keyword'] for v in p if v['regra']==k),'')] for k,n in reg.most_common()],[40,16,66])
make('Patches 101',['ID','Lote','Família','Keyword','Regra','Status','Área anterior','Área final','Intenção final','Justificativa'],[[x['id_global'],x['lote'],x['familia_id'],x['Keyword'],x['regra'],x['status'],json.loads(x['antes']).get('area_principal',''),json.loads(x['depois']).get('area_principal',''),json.loads(x['depois']).get('tipo_intencao',''),x['justificativa']] for x in p],[16,14,25,52,37,18,24,24,29,68])
make('QA 30 lotes',['Lote','Registros base','Controles','Alterações','Status'],[[x['lote'],x['base'],x['controles'],x['alteracoes'],x['integridade']] for x in qa],[17,21,17,18,17])
make('Famílias restantes',['Família','Pendentes v6','Corrigidos v7','Restantes','Exemplos restantes'],[[x['familia_id'],x['pendentes_v6'],x['reclassificadas_v7'],x['ainda_pendentes'],x['exemplos_pendentes']] for x in families[:220]],[29,20,20,17,83])
make('Amostra pendente',['ID','Keyword','Família','Área','Cluster','Risco','Buscas mensais'],[[x['id_global'],x['Keyword'],x['familia_id'],x['area'],x['cluster'],x['riscos_detectados'],x['Avg. monthly searches']] for x in selection[:280]],[15,53,27,23,30,50,18])
make('P3 potencial',['Cluster P3','Keywords','Observação'],[[k,str(v),'P3 ainda não revisada; exige auditagem própria'] for k,v in p3dist.most_common(30)],[42,20,55])
out=ROOT/'qa-revisao-p2-v7-centralizada.xlsx';SpreadsheetFile.export_xlsx(w).save(str(out)); print(out,out.stat().st_size)
print(w.inspect({'kind':'table','range':'Resumo!A1:C8','include':'values','table_max_rows':8,'table_max_cols':3}).ndjson[:700]);print(w.inspect({'kind':'match','search_term':'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A','options':{'use_regex':True,'max_results':10}}).ndjson[:250]);
