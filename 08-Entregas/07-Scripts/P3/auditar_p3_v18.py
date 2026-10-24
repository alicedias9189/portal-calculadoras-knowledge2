#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""P3 v1.8: QA quantitativo por regra e expansão conservadora de famílias selecionadas.
Ex.: python auditar_p3_v18.py --fonte RAIZ_COM_08-ENTREGAS --saida PASTA
Somente stdlib. Lê P3 v1.7; não altera P0/P1/P2 ou colunas protegidas.
"""
import argparse,csv,io,json,re,hashlib,zipfile,unicodedata,collections
from pathlib import Path

TRACK=['status_p3_v1_8','regra_p3_v1_8','justificativa_p3_v1_8','area_final_p3_v1_8','cluster_final_p3_v1_8','subcluster_final_p3_v1_8','tipo_intencao_final_p3_v1_8','classificacao_alterada_p3_v1_8']
CAN=('area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','unidade_origem','unidade_destino','direcao_conversao','confianca','revisao_manual','justificativa_curta','proposta_taxonomia')

def nrm(v):
 return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFKD',v.lower()) if not unicodedata.combining(c))).strip()

def readcsv(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def parse(b):return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig')),delimiter=';'))
def encode(rows,cols):
 out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=cols,delimiter=';',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows);return ('\ufeff'+out.getvalue()).encode('utf-8')
def write(path,rows,cols):path.write_bytes(encode(rows,cols))

def classify(q,old):
 s=nrm(q); change={};rule='';why='';risk=''
 def fill(area,clu,sub,typ,intent,reason,r,confidence='média',extra=None):
  d=dict(area_principal=area,cluster=clu,subcluster=sub,tipo_intencao=typ,intencao_principal=intent,confianca=confidence,revisao_manual='sim',justificativa_curta='P3 v1.8 — '+reason)
  if extra:d.update(extra)
  return d,r,reason
 # Imposto retido na fonte, sem confundir com descontos previdenciários ou juros compostos.
 if re.search(r'\birrf\b',s) and 'cdb' not in s and 'receita federal' not in s:
  if any(x in s for x in ('adiantamento salarial','no adiantamento','sobre adiantamento','inss e irrf')):
   area,clu,sub='Trabalho','Remuneração','IRRF na folha e adiantamento salarial'
  elif 'aluguel' in s:
   area,clu,sub='Finanças','Tributos','IRRF sobre rendimentos de aluguel'
  elif 'pensao alimenticia' in s:
   area,clu,sub='Finanças','Tributos','Deduções da base de IRRF'
  else:area,clu,sub='Finanças','Tributos','IRRF e base de cálculo'
  if re.search(r'\b(como|qual|base|aliquota|tabela|desconto|declarar|deducao|passo a passo)\b',s) and not re.search(r'\b(calculadora|simulador|simulacao)\b',s):
   typ='informacional';intent='Consultar critérios, alíquotas ou método de apuração do IRRF'
  else:typ='cálculo contextual';intent='Calcular ou simular IRRF após informar base, deduções, regime e competência'
  return fill(area,clu,sub,typ,intent,'IRRF identificado como tributo, não energia solar, construção ou matemática; regras dependem da competência.','irrf_tributario_contextual',extra={'dominio_ou_grandeza':'imposto de renda retido na fonte'})
 # Média ponderada: sem amostra/pesos, operação contextual; explicações/tutoriais informativos.
 if 'media ponderada' in s:
  if any(x in s for x in ('tabela','exemplo','formula','como fazer','como funciona','o que significa','como calcular','na hp','no excel','tabela dinamica','libreoffice','estatistica','media ponderada do enem','enem media ponderada')):
   typ='tabela/referência' if 'tabela media ponderada'==s else 'informacional';intent='Entender a média ponderada, sua fórmula ou procedimento de uso'
  else:typ='cálculo contextual';intent='Calcular média ponderada após fornecer valores e respectivos pesos'
  return fill('Matemática','Estatística e probabilidade','Médias e estatística descritiva',typ,intent,'Média ponderada exige observações e pesos; tutorial não é cálculo com números explícitos.','media_ponderada', 'alta', {'dominio_ou_grandeza':'estatística descritiva'})
 # Regra de três precisa permanecer no domínio matemático e material didático não equivale cálculo direto.
 if 'regra de tres' in s and (old['area_principal']!='Matemática' or any(x in s for x in ('problemas','simples ou composta','simples composta','como resolver'))):
  typ='informacional' if any(x in s for x in ('problemas','simples ou composta','simples composta','como resolver')) else 'cálculo contextual'
  return fill('Matemática','Porcentagem e proporções','Regra de três e proporções',typ,'Consultar método e exemplos de regra de três' if typ=='informacional' else 'Resolver proporção depois de informar grandezas','Regra de três é uma proporção matemática, não aplicação de juros simples.','regra_tres', 'alta')
 # Pares seguros de GRANDEZA HOMOGÊNEA explicitamente indicados; W<>kWh não é direto.
 pairs=[(r'\bconverter kwh em mwh\b','kWh','MWh'),(r'\bconverter w em kw\b','W','kW'),(r'\bconverter wh em kwh\b','Wh','kWh'),(r'\bcomo converter wh em kwh\b','Wh','kWh'),(r'\bcomo converter kwh em wh\b','kWh','Wh'),(r'\bconverter kwh para joules\b','kWh','J')]
 for pat,u,v in pairs:
  if re.search(pat,s):
   return fill('Conversores','Unidades físicas','Energia, potência e calor','conversão direta',f'Converter {u} em {v}',f'Unidades de mesma dimensão declaradas na consulta ({u} → {v}).','conversao_energia_dimensional','alta',{'unidade_origem':u,'unidade_destino':v,'direcao_conversao':f'{u}→{v}','dominio_ou_grandeza':'energia' if u not in ('W','kW') else 'potência'})
 # Dia útil: diferenciar calendário/referência de cálculo e corrigir classificações em domínio incompatível.
 if 'dias uteis' in s or 'dia util' in s:
  if s.startswith('calendario') and 'com contagem' not in s:
   return fill('Datas','Dias úteis','Calendário de dias úteis e feriados','tabela/referência','Consultar calendário de dias úteis para o período selecionado','Calendário é consulta de referência e pode depender de município e feriados.','dias_uteis_calendario','média')
  if old['area_principal'] not in ('Datas','Trabalho') or 'quantos dias uteis entre' in s or 'dias uteis que separam' in s:
   return fill('Datas','Dias úteis','Contagem de dias úteis e feriados','cálculo contextual','Contar dias úteis entre datas informadas considerando feriados','A contagem depende das datas e calendário de feriados selecionados.','dias_uteis_contagem','média')
 # Médias que integram remuneração das férias não são estatística genérica sem contexto laboral.
 if 'ferias' in s and 'media' in s and any(x in s for x in ('horas extras','hora extra','adicional noturno','dsr','insalubridade')):
  typ='informacional' if s.startswith('como calcular') else 'cálculo contextual'
  return fill('Trabalho','Férias','Médias remuneratórias para férias',typ,'Entender composição das médias de férias' if typ=='informacional' else 'Calcular média remuneratória com histórico de parcelas e competência','Médias de adicionais/horas extras integram cálculo trabalhista e dependem do período.','ferias_medias','média')
 # Rentabilidade e taxa poupança Banco do Brasil: pergunta sobre índice, não busca de URL nem empréstimo.
 if 'poupanca' in s and 'banco do brasil' in s and 'simulador' not in s and 'abrir conta' not in s:
  if any(x in s for x in ('juros','porcentagem','quanto rende','rendendo','rendimento mensal','rende quanto')):
   return fill('Finanças','Investimentos','Poupança','informacional','Consultar taxa, regra ou rendimento da poupança no período informado','Consulta de taxa/rendimento não é necessariamente navegação ou simulação com capital informado.','poupanca_taxa_informacao','média')
 return None

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',required=True,type=Path);ap.add_argument('--saida',required=True,type=Path);a=ap.parse_args()
 src=a.fonte/'08-Entregas/P3-v1.7';o=a.saida;o.mkdir(parents=True,exist_ok=True)
 queue=readcsv(src/'p3-v1.7-fila-23965.csv'); unvisited={r['id_global']:r for r in queue if r['status_p3_v1']=='FORA_DO_PILOTO' and not any(r['status_p3_'+p] for p in ['v1_3','v1_4','v1_5','v1_6'])}
 assert len(queue)==23965 and len(unvisited)==20755,(len(queue),len(unvisited))
 decisions={};selected={}
 for r in unvisited.values():
  # queue area isn't necessarily final if outside pilots, only use keyword and consistency checks at lote level
  old={'area_principal':r['area'],'cluster':r['cluster'],'subcluster':r['subcluster']}
  result=classify(r['Keyword'],old)
  if result:selected[r['id_global']]=result
 # Derive risk QA using last staged v1.7 review 152; purposeful sample, not random population estimate
 review=readcsv(src/'p3-v1.7-revisao-152.csv');report=[]
 for rule in sorted(set(r['regra_v16'] for r in review)):
  total=[r for r in review if r['regra_v16']==rule];sample=[r for r in total if r['na_amostra_estratificada']=='sim']; corrected=[r for r in total if r['parecer_v17'] in ('CORRIGIDA','REABERTA_POR_AMBIGUIDADE')]; samp_corr=[r for r in sample if r in corrected]
  report.append({'regra':rule,'total_regra_v16':len(total),'amostra_estratificada_v17':len(sample),'corrigidos_na_amostra':len(samp_corr),'corrigidos_em_todos_152':len(corrected),'taxa_observada_amostra_pct':round(100*len(samp_corr)/len(sample),2) if sample else 0,'interpretacao':'amostra dirigida; não estimador populacional'})
 write(o/'p3-v1.8-qa-taxas-por-regra.csv',report,list(report[0]))
 patched=[];tests=[];nbase=nctrl=0;review_candidates=[]
 with zipfile.ZipFile(src/'lotes-001-a-030-p3-v1.7.zip') as zin,zipfile.ZipFile(o/'lotes-001-a-030-p3-v1.8.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as zout:
  names=sorted(x for x in zin.namelist() if x.endswith('.csv'));assert len(names)==30,len(names)
  for filename in names:
   rows=parse(zin.read(filename)); cols=list(rows[0]);mut=nb=nc=0
   for row in rows:
    if row['tipo_registro']!='base':nctrl+=1;nc+=1;continue
    nbase+=1;nb+=1;rid=row['id_global']
    if rid not in selected:continue
    proposed,rule,reason=selected[rid]
    assert row['Keyword']==unvisited[rid]['Keyword']
    changes={k:v for k,v in proposed.items() if row[k]!=v}
    if not changes:continue
    before={k:row[k] for k in changes};row.update(changes);mut+=1
    assert any(c in changes for c in ('area_principal','cluster','subcluster','tipo_intencao','intencao_principal'))
    decisions[rid]=(rule,reason,dict(row))
    patched.append({'id_global':rid,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra_v18':rule,'campos_alterados':','.join(changes),'antes_json':json.dumps(before,ensure_ascii=False,sort_keys=True),'depois_json':json.dumps({k:row[k] for k in changes},ensure_ascii=False,sort_keys=True)})
    review_candidates.append({'id_global':rid,'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra':rule,'area_anterior':before.get('area_principal',row['area_principal']),'area_proposta':row['area_principal'],'tipo_anterior':before.get('tipo_intencao',row['tipo_intencao']),'tipo_proposto':row['tipo_intencao'],'justificativa':reason,'status':'PROPOSTA_CONTEXTUAL','revisao_editorial_final':'pendente'})
   dest=filename.replace('v1.7','v1.8');zout.writestr(dest,encode(rows,cols))
   tests.append({'lote_origem':filename,'lote_v18':dest,'base':nb,'controles':nc,'patches':mut,'status':'PENDENTE_REGRESSAO_INDEPENDENTE'})
 assert (nbase,nctrl)==(294905,2190),(nbase,nctrl)
 assert len(patched)==len(decisions) and sum(x['patches'] for x in tests)==len(patched)
 # preserve historical columns; track each changed P3 row with new append-only fields
 for inputname in ('p3-v1.7-fila-23965.csv','fila-geral-p0-p1-p2-p3-v1.7.csv'):
  destname=inputname.replace('v1.7','v1.8')
  with open(src/inputname,encoding='utf-8-sig',newline='') as inp,open(o/destname,'w',encoding='utf-8-sig',newline='') as out:
   rd=csv.DictReader(inp,delimiter=';');cols=rd.fieldnames
   assert not set(TRACK)&set(cols)
   wr=csv.DictWriter(out,fieldnames=cols+TRACK,delimiter=';',lineterminator='\n');wr.writeheader()
   for r in rd:
    for k in TRACK:r[k]=''
    if r['id_global'] in decisions:
     rule,reason,new=decisions[r['id_global']];r.update(dict(zip(TRACK,['PROPOSTA_COM_RESSALVA' if new['confianca']!='alta' else 'PROPOSTA_SEM_RESSALVA',rule,reason,new['area_principal'],new['cluster'],new['subcluster'],new['tipo_intencao'],'sim'])))
    wr.writerow(r)
 patched.sort(key=lambda x:int(x['id_global']));review_candidates.sort(key=lambda x:int(x['id_global']))
 write(o/'p3-v1.8-patches.csv',patched,list(patched[0]));write(o/'p3-v1.8-decisoes.csv',review_candidates,list(review_candidates[0]));write(o/'p3-v1.8-regressao-30-lotes.csv',tests,list(tests[0]))
 sums={'etapa':'P3 v1.8','amostra_v17_analisada':103,'amostra_v17_correcoes_observadas':17,'p3_universo':23965,'p3_fora_piloto_antes':20755,'p3_expansao_corrigidos':len(patched),'p3_fora_piloto_depois':20755-len(patched),'familias_distintas':len({x['familia_id'] for x in patched}),'por_regra':dict(collections.Counter(x['regra_v18'] for x in patched)),'p2_pendencias_inalteradas':4660,'regressao_independente':'executar script independente','base':nbase,'controles':nctrl,'nota':'Confianca das regras não equivale a aprovação editorial; amostra V17 foi estratificada e incluiu exceções propositalmente.'}
 (o/'p3-v1.8-resumo.json').write_text(json.dumps(sums,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(sums,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
