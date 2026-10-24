#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v1.6: revisão crítica das 78 novas decisões v1.5 e expansão restrita.
Uso: python auditar_p3_v16.py --fonte <diretorio com 08-Entregas/P3-v1.5> --saida <dir>
A fonte é o conteúdo do ZIP de entrega P3 v1.5, preservada integralmente.
"""
import argparse,csv,io,collections,json,zipfile,hashlib
from pathlib import Path
from classificador_p3_v16 import corrige_amostra,expandir
CAN=('area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta')
SEMANTIC=('area_principal','cluster','subcluster','intencao_principal','tipo_intencao')
TRACK=['status_p3_v1_6','regra_p3_v1_6','justificativa_p3_v1_6','area_final_p3_v1_6','cluster_final_p3_v1_6','subcluster_final_p3_v1_6','tipo_intencao_final_p3_v1_6','classificacao_alterada_p3_v1_6']
def load(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def parse(data):return list(csv.DictReader(io.StringIO(data.decode('utf-8-sig')),delimiter=';'))
def encode(rows,cols):
    s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=cols,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows);return ('\ufeff'+s.getvalue()).encode('utf-8')
def save(path,rows,cols):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(encode(rows,cols))
def main():
    p=argparse.ArgumentParser();p.add_argument('--fonte',type=Path,required=True);p.add_argument('--saida',type=Path,required=True);a=p.parse_args()
    source=a.fonte/'08-Entregas/P3-v1.5';out=a.saida;out.mkdir(parents=True,exist_ok=True)
    prev=load(source/'p3-v1.5-decisoes-por-id.csv');review78={r['id_global']:r for r in prev if r['origem']=='EXPANSAO_NOVA_P3'}
    assert len(review78)==78
    queue=load(source/'p3-v1.5-fila-23965.csv');assert len(queue)==23965
    eligible={r['id_global'] for r in queue if r['status_p3_v1']=='FORA_DO_PILOTO' and not any(r.get('status_p3_v1_'+i) for i in ['3','4','5'])}
    assert len(eligible)==20907,len(eligible)
    updates={};patches=[];decisions=[];count=collections.Counter();reg=[];nbase=ncontrols=0;sample=[]
    with zipfile.ZipFile(source/'lotes-001-a-030-p3-v1.5.zip') as src,zipfile.ZipFile(out/'lotes-001-a-030-p3-v1.6.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as dest:
        names=sorted(src.namelist());assert len(names)==30
        for name in names:
            rows=parse(src.read(name));cols=list(rows[0]);npatch=0;bases=controls=0
            for row in rows:
                if row['tipo_registro']!='base':controls+=1;ncontrols+=1;continue
                bases+=1;nbase+=1;rid=row['id_global'];choice=None;origin='';status=''
                if rid in review78:
                    choice=corrige_amostra(row);origin='QA_78_V15';status='CORRECAO_QA'
                    original=review78[rid]
                    assert original['Keyword']==row['Keyword']
                    sample.append({'id_global':rid,'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra_v1_5':original['regra'],'area_v1_5':row['area_principal'],'tipo_v1_5':row['tipo_intencao'],'parecer_v1_6':'CORRIGIR' if choice else ('MANTER_COM_RESSALVA' if original['regra'] in ('credito_consignado_dominio','antecipacao_fgts_dominio') else 'MANTER_SEM_ERRO_EVIDENTE'),'justificativa':choice[2] if choice else ('Consulta de credito ou FGTS exige validacao de contexto e parametros; nao permite afirmar que todas as variantes procuram a mesma ferramenta.' if original['regra'] in ('credito_consignado_dominio','antecipacao_fgts_dominio') else 'A classificacao de dominio corresponde ao texto; permanece proposta automatizada, sem aprovacao editorial.'),'area_v1_6':choice[1].get('area_principal',row['area_principal']) if choice else row['area_principal'],'tipo_v1_6':choice[1].get('tipo_intencao',row['tipo_intencao']) if choice else row['tipo_intencao']})
                elif rid in eligible:
                    choice=expandir(row);origin='EXPANSAO_V16';status='PROPOSTA_COM_RESSALVA'
                if not choice:continue
                rule,change,why=choice;before=dict(row);row.update(change)
                diff=[c for c in CAN if before[c]!=row[c]]
                if not diff or not any(c in SEMANTIC for c in diff):
                    row.update(before);continue
                assert rid not in updates,(rid,rule)
                updates[rid]=(rule,status,why,{k:row[k] for k in CAN})
                npatch+=1;count[rule]+=1
                patches.append({'id_global':rid,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'origem':origin,'regra':rule,'campos_alterados':','.join(diff),'antes_json':json.dumps({k:before[k] for k in diff},ensure_ascii=False),'depois_json':json.dumps({k:row[k] for k in diff},ensure_ascii=False)})
                decisions.append({'id_global':rid,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'origem':origin,'regra':rule,'status':status,'area_antes':before['area_principal'],'area_depois':row['area_principal'],'cluster_antes':before['cluster'],'cluster_depois':row['cluster'],'subcluster_antes':before['subcluster'],'subcluster_depois':row['subcluster'],'tipo_antes':before['tipo_intencao'],'tipo_depois':row['tipo_intencao'],'justificativa':why})
            newname=name.replace('v1.5.csv','v1.6.csv')
            dest.writestr(newname,encode(rows,cols))
            reg.append({'arquivo_fonte':name,'arquivo_saida':newname,'bases':bases,'controles':controls,'alteracoes':npatch,'status':'AGUARDANDO_REGRESSAO_INDEPENDENTE'})
    assert len(sample)==78 and len(updates)==len(patches)==len(decisions)==sum(x['alteracoes'] for x in reg)
    assert (nbase,ncontrols)==(294905,2190)
    sample.sort(key=lambda r:int(r['id_global']));decisions.sort(key=lambda r:int(r['id_global']));patches.sort(key=lambda r:int(r['id_global']))
    for oldname in ['p3-v1.5-fila-23965.csv','fila-geral-p0-p1-p2-p3-v1.5.csv']:
        rows=load(source/oldname);cols=list(rows[0]);assert not set(TRACK).intersection(cols)
        for r in rows:
            r.update(dict.fromkeys(TRACK,''))
            if r['id_global'] in updates:
                rule,st,why,full=updates[r['id_global']]
                r.update(dict(zip(TRACK,[st,rule,why,full['area_principal'],full['cluster'],full['subcluster'],full['tipo_intencao'],'sim'])))
        save(out/oldname.replace('v1.5','v1.6'),rows,cols+TRACK)
    save(out/'p3-v1.6-amostra-78-pareceres.csv',sample,list(sample[0]))
    save(out/'p3-v1.6-decisoes-por-id.csv',decisions,list(decisions[0]))
    save(out/'p3-v1.6-patches.csv',patches,list(patches[0]))
    save(out/'p3-v1.6-regressao-30-lotes.csv',reg,list(reg[0]))
    q=sum(x['origem']=='QA_78_V15' for x in decisions);exp=len(decisions)-q
    summary={'etapa':'P3 v1.6','amostra_critica_v15':78,'correcoes_qa':q,'novas_classificacoes':exp,'familias_expansao':len({r['familia_id'] for r in decisions if r['origem']=='EXPANSAO_V16'}),'total_alteracoes':len(decisions),'p3_fora_pilotos_antes':20907,'p3_fora_pilotos_depois':20907-exp,'p3_total':23965,'regras':dict(count),'registros_base':nbase,'controles':ncontrols,'lotes':len(reg),'pendencias_p2_preservadas':4660,'limites':'Aplicacao conservadora de regras linguisticas, sem homologacao editorial de todas as keywords; sem inserir alíquotas, cotacoes ou valores fiscais; variacoes futuras de leis exigem fontes atualizadas.'}
    (out/'p3-v1.6-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
