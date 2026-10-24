#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v1.5: revisão da amostra 98 + propagação limitada + expansão conservadora.
Uso: python auditar_p3_v1_5.py --fonte DIR_EXTRAIDO --saida DIR
Fonte contém 08-Entregas/P3-v1.4/ do pacote anterior. Não sobrescreve originais.
"""
import argparse,csv,io,hashlib,json,collections,zipfile,re
from pathlib import Path
from classificador_p3_v15 import expandir_p3,revisar_p3_v14,norm
CAN=('area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta')
SEMANTIC=('area_principal','cluster','subcluster','intencao_principal','tipo_intencao')
TRACK=['status_p3_v1_5','regra_p3_v1_5','justificativa_p3_v1_5','area_final_p3_v1_5','cluster_final_p3_v1_5','subcluster_final_p3_v1_5','tipo_intencao_final_p3_v1_5','classificacao_alterada_p3_v1_5']
def load(p):
 with open(p,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f,delimiter=';'))
def parse(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def encode(rows,cols):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=cols,delimiter=';',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows);return ('\ufeff'+s.getvalue()).encode('utf-8')
def outcsv(p,rows,cols):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(encode(rows,cols))
def main():
 p=argparse.ArgumentParser();p.add_argument('--fonte',type=Path,required=True);p.add_argument('--saida',type=Path,required=True);a=p.parse_args()
 base=a.fonte/'08-Entregas/P3-v1.4';dest=a.saida;dest.mkdir(parents=True,exist_ok=True)
 fila=load(base/'p3-v1.4-fila-23965.csv'); assert len(fila)==23965
 old=load(base/'p3-v1.4-decisoes-por-id.csv'); past={r['id_global']:r for r in old}
 eligible={x['id_global'] for x in fila if x['status_p3_v1']=='FORA_DO_PILOTO' and not x['status_p3_v1_3'] and not x['status_p3_v1_4']};assert len(eligible)==20985,len(eligible)
 sample=load(a.fonte/'98-AMOSTRA-extraida.csv');assert len(sample)==98 and len({x['id_global'] for x in sample})==98
 sample_ids={x['id_global'] for x in sample}
 update={}; patches=[];decisions=[];byrule=collections.Counter();base_count=controls=0;perlot=[]
 with zipfile.ZipFile(base/'lotes-001-a-030-p3-v1.4.zip') as src,zipfile.ZipFile(dest/'lotes-001-a-030-p3-v1.5.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as dst:
  names=src.namelist();assert len(names)==30 and len(set(names))==30
  for name in names:
   rows=parse(src.read(name));cols=list(rows[0]);touched=0
   for r in rows:
    if r['tipo_registro']!='base':controls+=1;continue
    base_count+=1;rid=r['id_global'];choice=None
    if rid in past and past[rid]['regra'] in ('consulta_taxa_credito_instituicao','simulacao_aposentadoria_previdencia','jornada_trabalho_semanal'):
     choice=revisar_p3_v14(r)
     if choice: rule,change,why=choice; origin='QA_REGRA_P3_V14';stat='CORRECAO_QA'
    elif rid in eligible:
     choice=expandir_p3(r)
     if choice:rule,change,why=choice; origin='EXPANSAO_NOVA_P3';stat='PROPOSTA_COM_RESSALVA'
    if not choice:continue
    # Manter conflitos temporais de 'hoje' e ano histórico para triagem, não auto-validar.
    if origin=='EXPANSAO_NOVA_P3' and rule=='salario_minimo_valor':
     s=norm(r['Keyword'])
     if 'hoje' in s and re.search(r'\b20(?:0\d|1\d|2[0-5])\b',s):continue
    before=dict(r);r.update(change)
    changed=[key for key in CAN if before.get(key)!=r.get(key)]
    assert changed and any(c in SEMANTIC for c in changed),(rid,choice)
    touched+=1;byrule[rule]+=1
    patches.append(dict(id_global=rid,lote=r['lote_id'],familia_id=r['familia_id'],Keyword=r['Keyword'],origem=origin,regra=rule,campos_alterados=','.join(changed),antes_json=json.dumps({k:before[k] for k in changed},ensure_ascii=False),depois_json=json.dumps({k:r[k] for k in changed},ensure_ascii=False)))
    decisions.append(dict(id_global=rid,lote=r['lote_id'],familia_id=r['familia_id'],Keyword=r['Keyword'],origem=origin,regra=rule,status=stat,area_antes=before['area_principal'],area_depois=r['area_principal'],cluster_antes=before['cluster'],cluster_depois=r['cluster'],subcluster_antes=before['subcluster'],subcluster_depois=r['subcluster'],tipo_antes=before['tipo_intencao'],tipo_depois=r['tipo_intencao'],justificativa=why))
    update[rid]=(rule,stat,why,dict(r))
   dst.writestr(name.replace('v1.4.csv','v1.5.csv'),encode(rows,cols))
   perlot.append({'arquivo_fonte':name,'arquivo_saida':name.replace('v1.4.csv','v1.5.csv'),'bases':sum(x['tipo_registro']=='base' for x in rows),'controles':sum(x['tipo_registro']!='base' for x in rows),'alteracoes':touched,'status':'AGUARDANDO_REGRESSAO_INDEPENDENTE'})
 assert (base_count,controls)==(294905,2190),(base_count,controls)
 assert len(decisions)==len(patches)==sum(x['alteracoes'] for x in perlot)==len(update)
 amostra=[]
 for r in sample:
  rid=r['id_global'];u=update.get(rid)
  reason=(u[2] if u else 'Interpretação compatível com o texto da consulta; ainda sem homologação editorial individual.')
  status=('CORRIGIDO_COM_PATCH' if u and u[1]=='CORRECAO_QA' else 'MANTER_COM_RESSALVA' if r['regra'] in ('rendimento_conta_digital','direitos_trabalhistas_gestante') else 'MANTER_SEM_ERRO_EVIDENTE')
  amostra.append({'id_global':rid,'familia_id':r['familia_id'],'Keyword':r['Keyword'],'regra_v1_4':r['regra'],'area_v1_4':r['area_depois'],'tipo_v1_4':r['tipo_depois'],'parecer_v1_5':status,'justificativa':reason,'area_v1_5':u[3]['area_principal'] if u else r['area_depois'],'tipo_v1_5':u[3]['tipo_intencao'] if u else r['tipo_depois']})
 assert len(amostra)==98
 for name in ['p3-v1.4-fila-23965.csv','fila-geral-p0-p1-p2-p3-v1.4.csv']:
  rows=load(base/name);cols=list(rows[0]);assert not (set(TRACK)&set(cols))
  for x in rows:
   x.update(dict.fromkeys(TRACK,''))
   if x['id_global'] in update:
    rule,st,why,full=update[x['id_global']]
    x.update(dict(zip(TRACK,[st,rule,why,full['area_principal'],full['cluster'],full['subcluster'],full['tipo_intencao'],'sim'])))
  outcsv(dest/name.replace('v1.4','v1.5'),rows,cols+TRACK)
 outcsv(dest/'p3-v1.5-amostra-98-pareceres.csv',amostra,list(amostra[0]))
 outcsv(dest/'p3-v1.5-decisoes-por-id.csv',decisions,list(decisions[0]))
 outcsv(dest/'p3-v1.5-patches.csv',patches,list(patches[0]))
 outcsv(dest/'p3-v1.5-regressao-30-lotes.csv',perlot,list(perlot[0]))
 corr=[x for x in decisions if x['origem']=='QA_REGRA_P3_V14'];new=[x for x in decisions if x['origem']=='EXPANSAO_NOVA_P3']
 result={'etapa':'P3 v1.5','amostra_critica':98,'corrigidos_na_amostra':sum(r['parecer_v1_5']=='CORRIGIDO_COM_PATCH' for r in amostra),'propagacao_qa_total':len(corr),'expansao_novas_keywords':len(new),'expansao_familias':len({x['familia_id'] for x in new}),'patches_totais':len(patches),'p3_fora_pilotos_antes':20985,'p3_fora_pilotos_depois':20985-len(new),'p3_universo':23965,'regras':dict(byrule),'registros_base':base_count,'controles':controls,'lotes':len(perlot),'ressalva':'Revisão contextual de uma amostra de 98 e propagação estrita de suas correções, com expansão apenas por regras de domínio. Integração de dados não implica aprovação editorial ou legal. Conflitos temporais excluídos da automação.'}
 (dest/'p3-v1.5-resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
