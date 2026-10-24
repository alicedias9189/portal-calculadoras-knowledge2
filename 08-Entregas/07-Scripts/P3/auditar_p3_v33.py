#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v3.3: revisão contextual independente dos 68 registros da v3.2.

Execução: python 07-Scripts/P3/auditar_p3_v33.py
Usa somente as FONTES-REPRODUCAO contidas no mesmo pacote, não altera originais.
Regra: somente IDs nas duas filas P3 e nos lotes; apenas 9 campos analíticos.
"""
from __future__ import annotations
import csv, io, json, zipfile, hashlib, re
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'08-Entregas/P3-v3.3'
SRC=OUT/'FONTES-REPRODUCAO/08-Entregas/P3-v3.2'
OUT.mkdir(parents=True,exist_ok=True)
EDITABLE={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
FIXES={
 '53900':('Supressão de horas extras','cálculo contextual','Supressão de horas extras tem objeto específico; não presumir regra de indenização nem vínculo sem dados.'),
 '79798':('Décimo terceiro e reflexos de horas extras','informacional','O termo 13 com horas extras remete ao décimo terceiro e seus reflexos; pedido é por método, não valores fornecidos.'),
 '204931':('Percentuais e adicionais de horas extras','informacional','Busca por porcentagem de horas extras indica consulta a percentuais, não cálculo com operandos informados.'),
 '52231':('Percentuais e adicionais de horas extras','cálculo contextual','Cálculo de horas extras a 50 requer jornada, salário e norma; não presumir percentual explícito ou direito.'),
 '167000':('Percentuais e adicionais de horas extras','informacional','Horas extras 100 como calcular é consulta ao método e adicional aplicável; contexto incompleto.'),
 '96006':('Fórmulas de horas extras no Excel','informacional','Como somar horas extras no Excel é pedido por método/fórmula, não apuração com horas informadas.'),
 '53188':('Reflexos de horas extras','cálculo contextual','Reflexos de horas extras não são necessariamente apenas DSR; sem verbas especificadas manter categoria ampla.'),
 '78252':('Reflexos de horas extras','informacional','Seus reflexos não identifica DSR isoladamente; busca informacional do método.'),
 '198199':('Payback na calculadora HP 12C','informacional','Consulta específica sobre operação na HP 12C; não há fluxos de caixa ou taxa para apuração direta.'),
 '198201':('Payback na calculadora HP 12C','informacional','Consulta específica sobre uso da HP 12C para payback, sem operandos.'),
}

def load_csv(path):
 with path.open('r',encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f,delimiter=';');return list(rd),list(rd.fieldnames)
def zip_rows(z,name):
 raw=z.read(name).decode('utf-8-sig');rd=csv.DictReader(io.StringIO(raw),delimiter=';');return list(rd),list(rd.fieldnames)
def write_csv(path,rows,fields):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=fields,delimiter=';',lineterminator='\n',extrasaction='ignore');wr.writeheader();wr.writerows(rows)
def lotnum(value):
 m=re.search(r'(?:lote-)?(\d{3})(?:-p0|$)',str(value))
 if m:return m.group(1)
 return str(value).zfill(3)
def intent(sub,tipo):
 return {'informacional':'Consultar informação: ','cálculo contextual':'Calcular com contexto: ','cálculo direto':'Calcular: ','simulação/projeção':'Simular: '}.get(tipo,'Consultar informação: ')+sub

def other_note(r,rule):
 k=r['Keyword'].lower()
 if rule=='P3V32_IPVA':
  return ('Consulta sobre pagamento, calendário ou imposto; ano e estado determinam as regras. '\
          'Não prometer parcelamento ou valor sem exercício e UF.')
 if rule=='P3V32_PAYBACK':
  if 'descontado' in k:return 'Payback descontado exige fluxos de caixa, investimento inicial e taxa de desconto; sem dados não há resultado.'
  if 'hp12c' in k:return 'Referência à HP 12C indica instrução de uso; sem dados, não calcular o retorno.'
  if any(a in k for a in ('como calcular','como fazer')):return 'Pedido de explicação do método de payback; não há fluxos de caixa nem investimento para resolver.'
  return 'Payback é retorno de investimento, mas fluxos, prazos e investimento inicial não foram fornecidos.'
 if rule=='P3V32_DIAS_EXCEL':
  return 'Operação ou fórmula de intervalo entre datas no Excel; nenhuma dupla de datas informada. Distinguir tutorial de ferramenta.'
 if rule=='P3V32_ENERGIA':return 'Preço por kWh é tarifa, não juros; depende de distribuidora, categoria, bandeiras e impostos.'
 if rule=='P3V32_CARTAO':return 'Como calcular juros do cartão é pedido por método; taxa, período, saldo e modalidade não estão informados.'
 if 'modelo' in k or 'planilha' in k or 'tabela de controle' in k or 'controle de ponto' in k:
  return 'Busca por modelo, ferramenta ou controle; não usar como cálculo de jornada já fornecida.'
 if 'clt' in k or 'acima de' in k:
  return 'Consulta a regras trabalhistas com dependência de jornada, legislação vigente e norma coletiva.'
 if 'reflexo' in k or 'repouso' in k or 'descanso remunerado' in k:
  return 'Reflexos de horas extras exigem identificar verba, período e regras aplicáveis, sem presumir resultado.'
 if 'como calcular' in k or 'passo a passo' in k:
  return 'Busca por explicação do método; não tratar como cálculo fechado sem entradas.'
 return 'Domínio trabalhista claro; cálculos exigem base salarial, jornada, período e regras aplicáveis.'

# Read v3.2 decisions and queue memberships
old_dec,old_fields=load_csv(SRC/'p3-v3.2-decisoes-68.csv')
assert len(old_dec)==68 and len({r['id_global'] for r in old_dec})==68
byid={r['id_global']:r for r in old_dec}
q3,q3cols=load_csv(SRC/'p3-v3.2-fila-23965.csv')
qall,qallcols=load_csv(SRC/'fila-geral-p0-p1-p2-p3-v3.2.csv')
assert len(q3)==23965 and len(qall)==52046
qi={r['id_global']:r for r in q3}
qa={r['id_global']:r for r in qall}
assert set(byid).issubset(qi) and set(byid).issubset(qa)
assert all(qi[id]['prioridade']=='P3' and qa[id]['prioridade']=='P3' for id in byid)
for id,d in byid.items():
 for q in (qi[id],qa[id]):
  assert q['Keyword']==d['Keyword'] and q['familia_id']==d['familia_id'] and lotnum(q['lote'])==lotnum(d['lote']),(id,q['lote'],d['lote'])

after={}; opinions=[]; patches=[]; summary_lots=[]; encountered=set();base_total=controls_total=0
with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v3.2.zip') as za, zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v3.3.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
 assert len(za.namelist())==30
 for old_name in za.namelist():
  rows,fields=zip_rows(za,old_name)
  outrows=[];count_changes=count_base=count_ctrl=0
  for r in rows:
   id=r['id_global'];modified=r
   if r['tipo_registro']=='base':count_base+=1
   else:count_ctrl+=1
   if id in byid:
    assert r['tipo_registro']=='base' and id not in encountered
    encountered.add(id)
    d=byid[id]
    assert r['Keyword']==d['Keyword'] and r['familia_id']==d['familia_id']
    assert lotnum(r['lote_id'])==lotnum(d['lote'])
    if id in FIXES:
     sub,tipo,reason=FIXES[id]
     modified=r.copy()
     modified['subcluster']=sub;modified['dominio_ou_grandeza']=sub;modified['tipo_intencao']=tipo
     modified['intencao_principal']=intent(sub,tipo)
     modified['revisao_manual']='sim'
     modified['confianca']='média'
     modified['justificativa_curta']=reason+' (P3 v3.3; revisão técnica, homologação editorial pendente.)'
     dif=[f for f in fields if r[f]!=modified[f]]
     assert dif and set(dif).issubset(EDITABLE)
     count_changes+=1
     patches.append({'id_global':id,'lote':old_name,'familia_id':r['familia_id'],'Keyword':r['Keyword'],
       'regra_origem':d['regra'],'campos_modificados':','.join(dif),
       'antes_json':json.dumps({f:r[f] for f in dif},sort_keys=True,ensure_ascii=False),
       'depois_json':json.dumps({f:modified[f] for f in dif},sort_keys=True,ensure_ascii=False),
       'fundamento':reason})
     opinion='CORRIGIDO';note=reason
    else:
     opinion='MANTIDO_COM_RESSALVA';note=other_note(r,d['regra'])
    after[id]=modified
    opinions.append({'id_global':id,'lote':d['lote'],'familia_id':d['familia_id'],'Keyword':r['Keyword'],
      'regra_v32':d['regra'],'parecer_v33':opinion,'fundamento_critico':note,
      'area_v32':r['area_principal'],'area_v33':modified['area_principal'],
      'cluster_v32':r['cluster'],'cluster_v33':modified['cluster'],
      'subcluster_v32':r['subcluster'],'subcluster_v33':modified['subcluster'],
      'tipo_intencao_v32':r['tipo_intencao'],'tipo_intencao_v33':modified['tipo_intencao'],
      'alteracao_lote':'sim' if id in FIXES else 'não','homologacao_editorial':'pendente'})
   outrows.append(modified)
  buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(outrows)
  zb.writestr(old_name.replace('v3.2','v3.3'),('\ufeff'+buf.getvalue()).encode('utf-8'))
  summary_lots.append({'lote':old_name,'bases':count_base,'controles':count_ctrl,'patches':count_changes,'status':'PASSOU'})
  base_total+=count_base;controls_total+=count_ctrl
assert encountered==set(byid) and base_total==294905 and controls_total==2190
assert len(patches)==len(FIXES)==10 and len(opinions)==68
opinions.sort(key=lambda r:int(r['id_global']));patches.sort(key=lambda r:int(r['id_global']))
write_csv(OUT/'p3-v3.3-pareceres-68.csv',opinions,list(opinions[0]))
write_csv(OUT/'p3-v3.3-patches.csv',patches,list(patches[0]))
write_csv(OUT/'p3-v3.3-regressao-30-lotes.csv',summary_lots,list(summary_lots[0]))
# append-only queue columns
newcols=['status_p3_v3_3','parecer_p3_v3_3','justificativa_p3_v3_3','area_final_p3_v3_3','cluster_final_p3_v3_3','subcluster_final_p3_v3_3','tipo_intencao_final_p3_v3_3','classificacao_alterada_p3_v3_3']
notes={p['id_global']:p for p in opinions}
for srcname,destname,rows,fields in [
 ('p3-v3.2-fila-23965.csv','p3-v3.3-fila-23965.csv',q3,q3cols),
 ('fila-geral-p0-p1-p2-p3-v3.2.csv','fila-geral-p0-p1-p2-p3-v3.3.csv',qall,qallcols)]:
 assert not any(c in fields for c in newcols)
 out=[]
 for r in rows:
  x=r.copy();q=dict.fromkeys(newcols,'')
  id=r['id_global']
  if id in notes:
   nr=after[id]
   q.update({'status_p3_v3_3':'REVISADO' if id in FIXES else 'PRESERVADO',
      'parecer_p3_v3_3':notes[id]['parecer_v33'],
      'justificativa_p3_v3_3':notes[id]['fundamento_critico'],
      'area_final_p3_v3_3':nr['area_principal'],
      'cluster_final_p3_v3_3':nr['cluster'],
      'subcluster_final_p3_v3_3':nr['subcluster'],
      'tipo_intencao_final_p3_v3_3':nr['tipo_intencao'],
      'classificacao_alterada_p3_v3_3':'sim' if id in FIXES else 'não'})
  x.update(q);out.append(x)
 write_csv(OUT/destname,out,fields+newcols)
# Global separation: source bytes exact, never process items.
(OUT/'backlog-global-98-com-parecer-v27.csv').write_bytes((SRC/'backlog-global-98-com-parecer-v27.csv').read_bytes())
byrule=Counter(r['regra_v32'] for r in opinions)
byrule_fix=Counter(r['regra_v32'] for r in opinions if r['parecer_v33']=='CORRIGIDO')
rule_rows=[{'regra':r,'revisados':str(n),'refinamentos':str(byrule_fix.get(r,0)),
    'taxa_de_refinamento_na_amostra':f'{byrule_fix.get(r,0)}/{n}',
    'nota':'Revisão integral e direcionada dos 68; refinamento não equivale a falso positivo de área.'} for r,n in sorted(byrule.items())]
write_csv(OUT/'p3-v3.3-qa-regras.csv',rule_rows,list(rule_rows[0]))
sumdata={'versao':'P3 v3.3','status':'PASSOU','revisados':len(opinions),'patches':len(patches),
 'pareceres':dict(Counter(r['parecer_v33'] for r in opinions)),
 'regras':dict(byrule),'patches_por_regra':dict(byrule_fix),'lotes':30,'bases':base_total,'controles':controls_total,
 'p3_fora_dos_pilotos':20204,'p2_pendencias':4660,'global_quarentena':98,
 'criterio':'Revisão semântica individual com homologação editorial humana pendente; nenhuma expansão.'}
(OUT/'p3-v3.3-resumo.json').write_text(json.dumps(sumdata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(sumdata,ensure_ascii=False))
