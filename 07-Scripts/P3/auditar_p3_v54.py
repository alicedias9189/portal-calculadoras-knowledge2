#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v5.4: nova expansão fechada de 100 IDs da fila sem Ouro pós v5.3.

Rodar na raiz do pacote extraído com fontes 08-Entregas/P3-v5.3 presentes:
    python 07-Scripts/P3/auditar_p3_v54.py
Sem perda de IDs canônicos nem de dados Google Ads; Ouro é filtro operacional reversível.
"""
from pathlib import Path
from collections import Counter
import csv, io, zipfile, json, re, shutil
HERE=Path(__file__).resolve(); ROOT=HERE.parents[2]
SRC=ROOT/'08-Entregas/P3-v5.3';OUT=ROOT/'08-Entregas/P3-v5.4'
OUT.mkdir(parents=True,exist_ok=True)
RULES={
 'GESTACAO_FERRAMENTAS':[56073,124842,33774,37056,37073,37078,37083,37089,37090,43610,76760,82573,103622,278047,60171],
 'DIREITOS_GESTANTE':[164971,164997,165042,165052,178415,199522,146594,136285,178133,178446,188626,188627,188632,188635,189697],
 'PRAZOS_CALCULADORAS':[34980,34983,208652,34970,34971,34974,34975,39189,34972,34976,34982,34956],
 'JUROS_E_FATURAS_CARTAO':[216032,216033,216036,216039,14348,175931,175936,175937,176122,197412,197460,152171,174317,117963],
 'PLANILHAS_ORCAMENTO':[148323,184208,202633,202634,203236,203330,203611,203841,203923,203930,196068,203445,203448,203449,203453],
 'SIMULADORES_INVESTIMENTOS':[172075,264169,263019,263045,267764,262936,172191,256006,29706,171981,248796,249064,266225,172186],
 'ESTATISTICA_E_MEDIA_ENEM':[34577,45058,50137,79576,123313,186940,252541,253475,253522,73452,73518,146995,182404,182406,189385]
}
PLAN={str(i):rule for rule,items in RULES.items() for i in items}
assert sum(map(len,RULES.values()))==len(PLAN)==100
TRACE=['status_p3_v5_4','regra_p3_v5_4','justificativa_p3_v5_4','area_final_p3_v5_4','cluster_final_p3_v5_4','subcluster_final_p3_v5_4','tipo_intencao_final_p3_v5_4','classificacao_alterada_p3_v5_4']
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
PREFIX={'informacional':'Consultar ou entender: ','busca de ferramenta':'Encontrar ferramenta: ','cálculo contextual':'Calcular com parâmetros: '}
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r),list(r.fieldnames)
def save(p,rows,fields=None):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
def new_class(old,rule):
 kw=old['Keyword'];k=kw.casefold(); conf='média'
 if rule=='GESTACAO_FERRAMENTAS':
  area='Saúde';cluster='Gestação e idade gestacional'
  sub='Cálculo de idade gestacional por ultrassom' if 'ultrassom' in k else 'Cálculo de idade gestacional pela DUM' if 'dum' in k else 'Contagem e cálculo de idade gestacional'
  typ='busca de ferramenta' if any(t in k for t in ('calculadora','online')) else 'informacional' if 'como calcular' in k else 'cálculo contextual'
  note='Idade gestacional exige DUM, laudo de ultrassom ou outro marco clínico apropriado; não inferir semana ou data de parto nem fornecer avaliação médica a partir de uma consulta sem dados.'
  if 'ultrassom' in k:note+=' Ultrassom pode embasar estimativa, mas não substituir o dado específico do exame.'
  if 'dum' in k:note+=' DUM significa data da última menstruação; a data concreta não foi informada.'
 elif rule=='DIREITOS_GESTANTE':
  area='Trabalho';cluster='Legislação e direitos'
  sub='Direitos e estabilidade no emprego durante a gestação'
  if any(w in k for w in ('mandada embora','pedir as contas','justa causa','experiencia','pedir demiss','demitid')):sub='Demissão, estabilidade e rescisão na gestação'
  typ='informacional'
  note='A palavra-chave trata de direitos ou vínculo de trabalho de gestantes, não de cálculo de semanas de gravidez. Regras e exceções trabalhistas exigem situação contratual e norma aplicável; não afirmar conclusão jurídica individual.'
  if '2022' in k:note+=' Referência histórica a 2022 não deve ser substituída por legislação atual.'
 elif rule=='PRAZOS_CALCULADORAS':
  area='Datas';cluster='Prazos e dias úteis';sub='Calculadoras de prazos judiciais e processuais' if any(t in k for t in ('judiciais','processuais')) else 'Calculadoras de prazos em dias úteis' if 'uteis' in k or 'úteis' in k else 'Calculadoras de prazos em meses' if 'meses' in k else 'Calculadoras de prazos e datas'
  typ='busca de ferramenta'
  note='Termo calculadora identifica busca por ferramenta, não cálculo pronto. Prazo depende de marco inicial, unidade, calendário, feriados e, em contexto judicial, rito e jurisdição; não fixar data ou regra processual sem esses dados.'
 elif rule=='JUROS_E_FATURAS_CARTAO':
  area='Finanças';cluster='Dívidas e cartões'
  sub='Taxas de juros de cartão por instituição' if any(x in k for x in ('nubank','santander','itau','itaú')) and ('taxa' in k or 'juros' in k) else 'Antecipação ou adiantamento de fatura' if 'adiantamento' in k else 'Financiamento ou parcelamento de fatura' if ('fatura' in k or 'financiamento' in k) else 'Juros em compras e parcelamento de cartão'
  typ='informacional'
  note='Busca sobre juros/condições financeiras do cartão, não rentabilidade de investimentos, criptomoedas ou empréstimo imobiliário. Taxas e incidência variam com emissor, modalidade e contrato; a consulta não fornece parâmetros para cálculo.'
  if 'adiantamento' in k:note='Adiantamento de fatura Nubank é uma operação do cartão; não se trata de cotação de criptomoedas. Sem valores ou confirmação contratual, manter como informação sobre fatura.'
 elif rule=='PLANILHAS_ORCAMENTO':
  area='Finanças';cluster='Planejamento financeiro';sub='Planilhas de orçamento e organização financeira empresarial' if any(x in k for x in ('empresa','empresarial','microempresa')) else 'Planilhas de orçamento e organização financeira pessoal'
  typ='busca de ferramenta'
  note='A expressão planilha indica procura por modelo ou ferramenta de orçamento, não por cálculo de rendimentos de CDB nem simulador de investimentos. Destino pessoal ou empresarial segue qualificador explícito; não inventar valores.'
 elif rule=='SIMULADORES_INVESTIMENTOS':
  area='Finanças';cluster='Investimentos'
  sub='Simulação de carteira e aportes em investimentos' if 'simulador' in k or 'simula' in k else 'Rentabilidade e condições de investimento'
  if 'ações' in k or 'acoes' in k:sub='Simuladores de investimentos em ações'
  if 'excel' in k:sub='Planilhas e simuladores de investimentos no Excel'
  if 'lci' in k:sub='Investimentos em LCI'
  if 'liquidez' in k:sub='Liquidez de investimentos'
  if 'prazo' in k:sub='Simulação de investimentos de longo prazo'
  if 'tesouro' in k:sub='Simulação de títulos do Tesouro IPCA'
  typ='busca de ferramenta' if any(x in k for x in ('simula','simulador','calculadora')) else 'informacional'
  note='Consulta sobre investimento, rendimento ou ferramenta financeira, não prazos judiciais, energia solar, datas ou crédito ao consumidor. Para projetar retorno são necessários principal, aportes, horizonte, taxas, impostos e risco; não apresentar resultado certo.'
  if 'ipca' in k:note+=' Tesouro IPCA+ pode envolver preço de mercado e retorno diferente na venda antecipada.'
 elif rule=='ESTATISTICA_E_MEDIA_ENEM':
  area='Matemática';cluster='Estatística e probabilidade'
  sub='Cálculo e conceito de moda estatística' if 'moda' in k else 'Métodos de probabilidade' if 'probabilidade' in k else 'Média e notas do ENEM' if 'enem' in k else 'Cálculo de média aritmética'
  typ='busca de ferramenta' if 'calculadora' in k or 'online' in k else 'informacional' if 'enem' in k or 'probabilidade' in k or 'como' in k else 'cálculo contextual'
  note='Busca vinculada à estatística, moda, média ou notas do ENEM, não moda vestuário, energia em kWh nem cálculos de datas. Sem série de valores ou notas não há resultado numérico; média do ENEM também pode referir nota de corte ou indicador publicado, requer contexto.'
  if 'moda' in k:note+=' A moda pode ser multimodal ou inexistir quando não há repetição.'
 else:raise ValueError(rule)
 out={'area_principal':area,'cluster':cluster,'subcluster':sub,'tipo_intencao':typ,'intencao_principal':PREFIX[typ]+sub,'dominio_ou_grandeza':sub,'confianca':conf,'revisao_manual':'sim','justificativa_curta':note+' Palavra-chave: «'+kw+'». (P3 v5.4: proposta técnica; homologação editorial pendente.)'}
 return out,note

def update_zip(src,dst,qi,filter_mode):
 seen=set();stats=[];base=controls=0;deltas={}
 with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  assert zin.testzip() is None and len(zin.namelist())==30
  for fname in zin.namelist():
   rd=csv.DictReader(io.StringIO(zin.read(fname).decode('utf-8-sig')),delimiter=';');columns=list(rd.fieldnames)
   tmp=io.StringIO(newline='');wr=csv.DictWriter(tmp,fieldnames=columns,delimiter=';',lineterminator='\n');wr.writeheader();b=c=p=0
   for prev in rd:
    rid=prev['id_global'];b+=prev['tipo_registro']=='base';c+=prev['tipo_registro']!='base';new=prev
    if rid in PLAN:
     assert rid not in seen and prev['tipo_registro']=='base';seen.add(rid)
     assert prev['Keyword']==qi[rid]['Keyword'] and prev['familia_id']==qi[rid]['familia_id']
     after,note=new_class(prev,PLAN[rid]);new=prev.copy();new.update(after);delta={k:(prev[k],new[k]) for k in columns if prev[k]!=new[k]}
     assert delta and set(delta)<=EDIT,(rid,delta)
     deltas[rid]=delta;p+=1
    wr.writerow(new)
   zout.writestr(fname.replace('v5.3','v5.4'),('\ufeff'+tmp.getvalue()).encode('utf-8'))
   stats.append({'base':filter_mode,'lote':fname.replace('v5.3','v5.4'),'bases':b,'controles':c,'patches':p,'status':'PASSOU'})
   base+=b;controls+=c
 assert seen==set(PLAN) and controls==2190 and base==(291296 if filter_mode=='filtrada_ouro' else 294905)
 return deltas,stats

def update_queue(src,dst,qi):
 seen=set();n=0
 with src.open(encoding='utf-8-sig',newline='') as fin,dst.open('w',encoding='utf-8-sig',newline='') as fout:
  rd=csv.DictReader(fin,delimiter=';');hist=list(rd.fieldnames)
  assert len(hist)==406 and not set(TRACE)&set(hist)
  wr=csv.DictWriter(fout,fieldnames=hist+TRACE,delimiter=';',lineterminator='\n');wr.writeheader()
  for prev in rd:
   rid=prev['id_global'];new=prev.copy();more=dict.fromkeys(TRACE,'')
   if rid in PLAN:
    assert rid not in seen;seen.add(rid)
    x,note=new_class({'Keyword':prev['Keyword']},PLAN[rid])
    more.update(status_p3_v5_4='TRATADO',regra_p3_v5_4=PLAN[rid],justificativa_p3_v5_4=note,
       area_final_p3_v5_4=x['area_principal'],cluster_final_p3_v5_4=x['cluster'],subcluster_final_p3_v5_4=x['subcluster'],
       tipo_intencao_final_p3_v5_4=x['tipo_intencao'],classificacao_alterada_p3_v5_4='sim')
   new.update(more);wr.writerow(new);n+=1
 assert seen==set(PLAN)
 return {'fila':dst.name,'linhas':n,'colunas_historicas':406,'novas_colunas':8,'status':'PASSOU'}

def main():
 q,cols=read(SRC/'p3-v5.3-fila-23865-sem-ouro.csv');qi={r['id_global']:r for r in q}
 sts=[x for x in cols if x.startswith('status_p3_v') and x!='status_p3_v1']
 eligible={x['id_global'] for x in q if x['prioridade']=='P3' and x['status_p3_v1']=='FORA_DO_PILOTO' and not any(x[s] for s in sts)}
 assert len(eligible)==19462,(len(eligible),len(eligible&set(PLAN)))
 assert set(PLAN)<=eligible,sorted(set(PLAN)-eligible)
 back,_=read(SRC/'backlog-global-98-com-parecer-v27.csv');assert len(back)==98 and set(PLAN).isdisjoint({x['id_global'] for x in back})
 canonical,rc=update_zip(SRC/'lotes-001-a-030-p3-v5.3.zip',OUT/'lotes-001-a-030-p3-v5.4.zip',qi,'canonica')
 filterd,rf=update_zip(SRC/'lotes-001-a-030-p3-v5.3-sem-ouro.zip',OUT/'lotes-001-a-030-p3-v5.4-sem-ouro.zip',qi,'filtrada_ouro')
 assert canonical==filterd and len(canonical)==100
 queuefiles=[('p3-v5.3-fila-23965.csv','p3-v5.4-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.3.csv','fila-geral-p0-p1-p2-p3-v5.4.csv',52046),('p3-v5.3-fila-23865-sem-ouro.csv','p3-v5.4-fila-23865-sem-ouro.csv',23865),('fila-geral-v5.3-sem-ouro-51884.csv','fila-geral-v5.4-sem-ouro-51884.csv',51884)]
 qs=[update_queue(SRC/a,OUT/b,qi) for a,b,_ in queuefiles];assert [i['linhas'] for i in qs]==[a[2] for a in queuefiles]
 decisions=[];patches=[]
 for rid in sorted(PLAN,key=int):
  r=qi[rid];rule=PLAN[rid];new,note=new_class({'Keyword':r['Keyword']},rule);d=canonical[rid]
  patches.append({'id_global':rid,'lote_id':'L'+r['lote'].zfill(3),'familia_id':r['familia_id'],'Keyword':r['Keyword'],'regra':rule,'campos_modificados':','.join(sorted(d)),
   'antes_json':json.dumps({k:v[0] for k,v in d.items()},ensure_ascii=False,sort_keys=True),
   'depois_json':json.dumps({k:v[1] for k,v in d.items()},ensure_ascii=False,sort_keys=True)})
  decisions.append({'id_global':rid,'lote_id':'L'+r['lote'].zfill(3),'familia_id':r['familia_id'],'Keyword':r['Keyword'],'regra':rule,'parecer':'PROPOSTA_COM_RESSALVA',
   'justificativa_individual':note,'area_anterior':r['area'],'area_nova':new['area_principal'],'cluster_anterior':r['cluster'],'cluster_novo':new['cluster'],'subcluster_anterior':r['subcluster'],
   'subcluster_novo':new['subcluster'],'tipo_anterior':r['tipo_intencao_atual'],'tipo_novo':new['tipo_intencao'],'campos_modificados':','.join(sorted(d)),
   'homologacao_editorial':'PENDENTE'})
 save(OUT/'p3-v5.4-pareceres-100.csv',decisions);save(OUT/'p3-v5.4-patches-100.csv',patches)
 save(OUT/'p3-v5.4-plano-por-id.csv',[{'id_global':r['id_global'],'Keyword':r['Keyword'],'familia_id':r['familia_id'],'regra':r['regra'],'justificativa':r['justificativa_individual']} for r in decisions])
 save(OUT/'p3-v5.4-regressao-inicial-60-lotes.csv',rc+rf)
 save(OUT/'p3-v5.4-qa-por-grupo.csv',[{'grupo':rule,'registros':len(items),'familias':len({qi[str(i)]['familia_id'] for i in items}),'status':'PROPOSTO_COM_RESSALVA','homologacao_editorial':'PENDENTE'} for rule,items in RULES.items()])
 shutil.copyfile(SRC/'backlog-global-98-com-parecer-v27.csv',OUT/'backlog-global-98-com-parecer-v27.csv')
 summary={'versao':'P3 v5.4','fonte':'P3 v5.3 + filtro Ouro DEC-089','novos_ids':100,'familias':len({r['familia_id'] for r in decisions}),'grupos':len(RULES),
  'por_grupo':{k:len(v) for k,v in RULES.items()},'elegiveis_operacionais_antes':19462,'elegiveis_operacionais_depois':19362,'elegiveis_canonicos_antes':19562,'elegiveis_canonicos_depois':19462,
  'lotes_canonicos':30,'lotes_filtrados':30,'base_canonica':294905,'base_filtrada':291296,'controles_preservados_em_cada_versao':2190,'ids_ouro_excluidos_so_operacional':3609,
  'filas':qs,'colunas_historicas':406,'colunas_novas':8,'p2_pendentes':4660,'backlog_global':98,'homologacao_editorial':'PENDENTE','status':'AUDITORIA_TECNICA_AGUARDA_REGRESSAO'}
 (OUT/'p3-v5.4-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()