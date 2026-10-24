#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v1.4: audita amostra v1.3 de 67 decisões e expande 581 casos (regra por keyword).
Entradas: diretório com arquivos de 08-Entregas/P3-v1.3 ({lotes, fila P3, fila geral, decisões})
Saídas: novas versões paralelas, patches antes/depois, QA e contagem de integridade.
NÃO sobrescreve fontes, NÃO altera as colunas originais nem aprova editorialmente.
Uso: python auditar_p3_v1_4.py --fonte PASTA --saida PASTA
"""
import argparse,csv,io,json,hashlib,random,collections,zipfile
from pathlib import Path
from classificador_p3_v14 import rule

CAN=['area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta']
SEMANTIC=CAN[:5]
TRACK=['status_p3_v1_4','regra_p3_v1_4','justificativa_p3_v1_4','area_final_p3_v1_4','cluster_final_p3_v1_4','subcluster_final_p3_v1_4','tipo_intencao_final_p3_v1_4','classificacao_alterada_p3_v1_4']
SAMPLE_ALERTS={'56082':'GPS de empregada doméstica em atraso: competência e obrigação (GPS ou DAE/eSocial) dependem do período/vínculo; sinalizar para revisão editorial.', '12838':'Dúvida jurídica sobre dias de abono pecuniário; confirmar contexto e base legal antes de classificar como cálculo.', '199183':'Aviso prévio de pedido de demissão depende de circunstâncias contratuais e legais; manter como orientação informacional.'}
SAMPLE_FP={
'76549': ('concreto_piso_garagem', 'Concreto para piso/garagem refere-se a estimativa de volume de concreto, não à quantidade de placas cerâmicas.', dict(area_principal='Construção',cluster='Concreto e estrutura',subcluster='Dimensionamento de concreto para piso',intencao_principal='Aprender a calcular volume de concreto para piso de garagem',tipo_intencao='informacional',confianca='média',revisao_manual='sim')),
'160013': ('fracao_calculadora_celular', 'Pergunta por uso de calculadora de celular com frações, não solicita um cálculo numérico específico.', dict(area_principal='Matemática',cluster='Números e operações',subcluster='Uso de calculadora para frações',intencao_principal='Aprender a inserir frações na calculadora do celular',tipo_intencao='informacional',confianca='média',revisao_manual='sim'))
}
def ler(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def to_bytes(rr,cols):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=cols,delimiter=';',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rr);return ('\ufeff'+s.getvalue()).encode('utf-8')
def write(p,rr,cols):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(to_bytes(rr,cols))
def load(p):return ler(p.read_bytes())
def pick_sample(decisions):
 by=collections.defaultdict(list)
 for x in decisions:by[x['regra']].append(x)
 five=[x for x in decisions if x['origem']=='AMOSTRA_FALSO_NEGATIVO'];assert len(five)==5
 sample=list(five);rng=random.Random(1303)
 for name,lst in sorted(by.items()):
  if name not in ['algebra_fracoes','dissidio_2022','materiais_reboco','gasolina_online','km_l']:
   sample+=rng.sample(lst,min(6,len(lst)))
 sample=list({x['id_global']:x for x in sample}.values());sample.sort(key=lambda x:int(x['id_global']))
 assert len(sample)==67,len(sample)
 return sample

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args()
 src=args.fonte/'08-Entregas/P3-v1.3';out=args.saida;out.mkdir(exist_ok=True,parents=True)
 fila=load(src/'p3-v1.3-fila-23965.csv');assert len(fila)==23965
 sample=pick_sample(load(src/'p3-v1.3-decisoes-por-id.csv'))
 sampleids={x['id_global'] for x in sample};assert set(SAMPLE_FP).issubset(sampleids)
 eligible={x['id_global'] for x in fila if x['status_p3_v1']=='FORA_DO_PILOTO' and not x['status_p3_v1_3']}
 assert len(eligible)==21561,len(eligible)
 patches=[];choices=[];regression=[];audit=[];updated={};c=collections.Counter();based=controlled=0;sample_lookup={x['id_global']:x for x in sample}
 zold=src/'lotes-001-a-030-p3-v1.3.zip';znew=out/'lotes-001-a-030-p3-v1.4.zip'
 with zipfile.ZipFile(zold) as za,zipfile.ZipFile(znew,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
  assert len(za.namelist())==30
  for name in za.namelist():
   rows=ler(za.read(name));cols=list(rows[0]);changes=0;saw_sample=[]
   for x in rows:
    if x['tipo_registro']!='base': controlled+=1;continue
    based+=1;id_=x['id_global'];before=dict(x)
    if id_ in SAMPLE_FP:
     ruleid,note,d=SAMPLE_FP[id_];d=dict(d,justificativa_curta='P3 v1.4 QA da amostra 67: '+note);status='CORRECAO_FALSO_POSITIVO';origin='REVISAO_AMOSTRA_V1_3'
    elif id_ in eligible:
     ans=rule(x)
     if not ans:continue
     ruleid,status,note,d=ans;origin='EXPANSAO_P3_NOVA_FAMILIA'
    else:continue
    x.update(d);keys=[k for k in CAN if x[k]!=before[k]]
    assert keys and any(k in SEMANTIC for k in keys),('sem modificacao relevante',id_)
    changes+=1;c[ruleid]+=1
    patches.append({'id_global':id_,'lote':x['lote_id'],'familia_id':x['familia_id'],'Keyword':x['Keyword'],'origem':origin,'regra':ruleid,'campos_alterados':','.join(keys),'antes_json':json.dumps({k:before[k] for k in keys},ensure_ascii=False),'depois_json':json.dumps({k:x[k] for k in keys},ensure_ascii=False)})
    choices.append({'id_global':id_,'lote':x['lote_id'],'familia_id':x['familia_id'],'Keyword':x['Keyword'],'origem':origin,'regra':ruleid,'status':status,'area_antes':before['area_principal'],'area_depois':x['area_principal'],'cluster_antes':before['cluster'],'cluster_depois':x['cluster'],'subcluster_antes':before['subcluster'],'subcluster_depois':x['subcluster'],'tipo_antes':before['tipo_intencao'],'tipo_depois':x['tipo_intencao'],'justificativa':note})
    updated[id_]=(ruleid,status,note,dict(x))
   zb.writestr(name.replace('v1.3.csv','v1.4.csv'),to_bytes(rows,cols))
   regression.append({'lote_original':name,'registros_base':sum(v['tipo_registro']=='base' for v in rows),'controles':sum(v['tipo_registro']!='base' for v in rows),'modificados':changes,'status':'AGUARDANDO_VERIFICACAO_INDEPENDENTE'})
 assert (based,controlled)==(294905,2190),(based,controlled)
 assert len(choices)==len(patches)==sum(int(x['modificados']) for x in regression)
 for x in sample:
  id_=x['id_global'];fp=id_ in SAMPLE_FP
  audit.append({'id_global':id_,'familia_id':x['familia_id'],'Keyword':x['Keyword'],'regra_original':x['regra'],'area_v1_3':x['area_depois'],'tipo_v1_3':x['intencao_depois'],'parecer_v1_4':'FALSO_POSITIVO_CORRIGIDO' if fp else ('RESSALVA_EDITORIAL' if id_ in SAMPLE_ALERTS else 'SEM_INCOERENCIA_EVIDENTE_NA_AMOSTRA'),'motivo':SAMPLE_FP[id_][1] if fp else (SAMPLE_ALERTS[id_] if id_ in SAMPLE_ALERTS else 'Interpretação plausível pela consulta; manter ressalvas do domínio; não é homologação editorial independente.'),'novo_tipo':updated[id_][3]['tipo_intencao'] if fp else x['intencao_depois']})
 for fname in ('p3-v1.3-fila-23965.csv','fila-geral-p0-p1-p2-p3-v1.3.csv'):
  rr=load(src/fname);cols=list(rr[0]);assert not (set(TRACK)&set(cols))
  for x in rr:
   u=updated.get(x['id_global']);x.update(dict.fromkeys(TRACK,''))
   if u:
    ruleid,status,note,row=u
    x.update(dict(zip(TRACK,[status,ruleid,note,row['area_principal'],row['cluster'],row['subcluster'],row['tipo_intencao'],'sim'])))
  write(out/fname.replace('v1.3','v1.4'),rr,cols+TRACK)
 for fname,rr in [('p3-v1.4-amostra-67-pareceres.csv',audit),('p3-v1.4-decisoes-por-id.csv',choices),('p3-v1.4-patches.csv',patches),('p3-v1.4-regressao-30-lotes.csv',regression)]:
  write(out/fname,rr,list(rr[0]))
 pilot_new=sum(x['origem']=='EXPANSAO_P3_NOVA_FAMILIA' for x in choices)
 summary={'versao':'P3 v1.4','universo_p3':23965,'p3_fora_antes':21561,'amostra_v1_3_verificada':len(sample),'falsos_positivos_amostra_corrigidos':len(SAMPLE_FP),'novos_registros_expandidos':pilot_new,'familias_novas_distintas':len({x['familia_id'] for x in choices if x['origem']=='EXPANSAO_P3_NOVA_FAMILIA'}),'total_patches':len(patches),'p3_fora_pilotos_restante':21561-pilot_new,'regras_nova_expansao':dict(c),'registros_base':based,'controles':controlled,'lotes':30,'limites':'Revisão contextual assistida de amostra e classificação por regras das novas famílias; nenhuma decisão é aprovação editorial definitiva. V1.2 Saúde requer validação editorial, e P2 permanece separada.'}
 (out/'resumo-p3-v1.4.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
