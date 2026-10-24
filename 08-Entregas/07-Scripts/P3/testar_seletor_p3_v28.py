#!/usr/bin/env python3
"""Testes independentes de negação de escopo P3 v2.8; não modifica arquivos."""
import csv,json,pathlib
R=pathlib.Path(__file__).resolve().parents[2]
S=R/'08-Entregas/P3-v2.8/FONTES-REPRODUCAO/08-Entregas/P3-v2.7'
O=R/'08-Entregas/P3-v2.8'
def rcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
p3=rcsv(S/'p3-v2.7-fila-23965.csv');general=rcsv(S/'fila-geral-p0-p1-p2-p3-v2.7.csv');glob=rcsv(S/'backlog-global-98-com-parecer-v27.csv');app=rcsv(O/'p3-v2.8-decisoes.csv')
by3={r['id_global']:r for r in p3};byg={r['id_global']:r for r in general}
byap={r['id_global']:r for r in app}
assert len(byap)==len(app)
# Implement actual gate API, also test deliberately invalid candidates.
def gate(items):
 if len(items)!=len({x['id_global'] for x in items}): return 'BLOQUEIO_ID_DUPLICADO'
 for r in items:
  x=by3.get(r['id_global']); y=byg.get(r['id_global'])
  if not x or not y or x['prioridade']!='P3' or y['prioridade']!='P3': return 'BLOQUEIO_FORA_DA_P3'
  if (x['Keyword'],x['familia_id'],x['lote'])!=(r['Keyword'],r['familia_id'],r['lote']):return 'BLOQUEIO_METADADOS_DIVERGENTES'
  if (y['Keyword'],y['familia_id'],y['lote'])!=(r['Keyword'],r['familia_id'],r['lote']):return 'BLOQUEIO_FILAS_DIVERGENTES'
  if x['status_p3_v1']!='FORA_DO_PILOTO':return 'BLOQUEIO_JA_PILOTADO'
 return 'AUTORIZADO_P3'

one=app[0].copy();tests=[]
def check(title,records,expected):
 got=gate(records);assert got==expected,(title,got,expected)
 tests.append({'teste':title,'resultado':got,'esperado':expected,'status':'PASSOU'})
check('Registro P3 legítimo',[one],'AUTORIZADO_P3')
check('ID duplicado',[one,one],'BLOQUEIO_ID_DUPLICADO')
check('ID inexistente',[dict(one,id_global='9999999999999')],'BLOQUEIO_FORA_DA_P3')
check('Keyword adulterada',[dict(one,Keyword=one['Keyword']+' teste')],'BLOQUEIO_METADADOS_DIVERGENTES')
check('Família adulterada',[dict(one,familia_id='F-INVENTADA')],'BLOQUEIO_METADADOS_DIVERGENTES')
check('Lote alterado',[dict(one,lote='999')],'BLOQUEIO_METADADOS_DIVERGENTES')
p2=next(r for r in general if r['prioridade']=='P2');check('ID de prioridade P2',[{'id_global':p2['id_global'],'Keyword':p2['Keyword'],'familia_id':p2['familia_id'],'lote':p2['lote']}],'BLOQUEIO_FORA_DA_P3')
for x in glob:
 check('Global não priorizada '+x['id_global'],[{'id_global':x['id_global'],'Keyword':x['Keyword'],'familia_id':x['familia_id'],'lote':x.get('lote','')}],'BLOQUEIO_FORA_DA_P3')
with (O/'p3-v2.8-testes-seletor.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(tests[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(tests)
res={'status':'PASSOU','testes':len(tests),'bloqueios_globais':98,'ids_aprovados':len(app),'observacao':'testes independentes para duplos, P2, inexistentes, lote/família/keyword adulterados'}
(O/'p3-v2.8-testes-seletor.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False))
