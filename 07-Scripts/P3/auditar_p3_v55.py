#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v5.5 — revisar exatamente os 100 IDs propostos em v5.4.

Execute da raiz do pacote com 08-Entregas/P3-v5.4 já presente:
    python 07-Scripts/P3/auditar_p3_v55.py
Fonte canônica e visão filtrada Ouro são alteradas apenas em cópias derivadas.
"""
import csv,io,json,zipfile,shutil
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[2]
S=R/'08-Entregas/P3-v5.4';D=R/'08-Entregas/P3-v5.5';D.mkdir(parents=True,exist_ok=True)
# As alterações abaixo são decididas por ID, após revisão de cada palavra-chave.
# Apenas campos semânticos e suas justificativas são editáveis.
PATCH={
'60171':{'tipo_intencao':'informacional','subcluster':'Calendário e tabelas de semanas e meses gestacionais'},
'136285':{'subcluster':'Direitos gerais da gestante (âmbito não indicado)'},
'164997':{'subcluster':'Legislação geral sobre gestação (tema não especificado)'},
'178133':{'subcluster':'Legislação geral sobre gestação (tema não especificado)'},
'178415':{'subcluster':'Legislação geral sobre gestação (tema não especificado)'},
'178446':{'subcluster':'Legislação geral sobre gestação (tema não especificado)'},
'188626':{'subcluster':'Legislação geral sobre gestação (tema não especificado)'},
'165052':{'subcluster':'Retorno e condições de trabalho durante a gestação'},
'188627':{'subcluster':'Afastamento e restrições ao trabalho na gestação'},
'188635':{'subcluster':'Afastamento e restrições ao trabalho na gestação'},
'79576':{'subcluster':'Moda estatística em distribuição salarial'},
'146995':{'tipo_intencao':'informacional'},
'252541':{'tipo_intencao':'cálculo contextual','subcluster':'Resolução de problemas de probabilidade'},
'172075':{'tipo_intencao':'cálculo contextual'},
'266225':{'tipo_intencao':'cálculo contextual'},
'267764':{'tipo_intencao':'cálculo contextual'},
'184208':{'subcluster':'Planilhas de controle de gastos (público não indicado)'},
'202634':{'subcluster':'Planilhas de controle de gastos (público não indicado)'},
'203445':{'subcluster':'Planilhas de controle de gastos (público não indicado)'},
'203453':{'subcluster':'Planilhas de controle de gastos (público não indicado)'},
'203923':{'subcluster':'Planilhas de controle de gastos (público não indicado)'},
'203930':{'subcluster':'Planilhas de controle de gastos (público não indicado)'},
'152171':{'subcluster':'Juros e encargos incidentes na fatura'},
}
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_5','parecer_p3_v5_5','justificativa_p3_v5_5','area_final_p3_v5_5','cluster_final_p3_v5_5','subcluster_final_p3_v5_5','tipo_intencao_final_p3_v5_5','classificacao_alterada_p3_v5_5']
PREFIX={'informacional':'Consultar ou entender: ','busca de ferramenta':'Encontrar ferramenta: ','cálculo contextual':'Calcular com parâmetros: '}

def rd(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f,delimiter=';');return list(reader),list(reader.fieldnames)
def wr(p,rows,headers=None):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=headers or list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)

def justification(row):
 kw=row['Keyword']; s=kw.casefold();rule=row['regra'];id=row['id_global']
 if rule=='GESTACAO_FERRAMENTAS':
  if 'ultrassom' in s:return 'A busca usa ultrassom como referência para estimativa gestacional; não apresenta dados do laudo. Uma calculadora requer data e medidas do exame e não substitui avaliação profissional.'
  if 'dum' in s:return 'DUM significa data da última menstruação. A expressão procura cálculo baseado na DUM, mas não traz uma data efetiva; não inferir idade gestacional.'
  if 'calendario' in s or 'calendário' in s:return 'O substantivo calendário, com meses e semanas, indica quadro de referência gestacional, não uma conta pronta com data inicial. Classificar como consulta à tabela.'
  if 'como calcular' in s:return 'O termo como calcular solicita explicação do método para estimar tempo de gravidez; sem DUM ou ultrassom não é possível dar número de semanas.'
  if 'calculadora' in s:return 'A palavra calculadora identifica procura por ferramenta de estimativa gestacional; nenhum parâmetro pessoal é fornecido.'
  return 'A consulta refere contagem ou cálculo de tempo gestacional; requer data de referência clínica, sem inferir semanas ou resultado concreto.'
 if rule=='DIREITOS_GESTANTE':
  if id in {'136285','164997','178133','178415','178446','188626'}:
   return 'Expressão genérica sobre direitos ou legislação da gestante; não restringir automaticamente a estabilidade no emprego. Manter contexto trabalhista provisório, mas assinalar que pode abranger saúde e benefícios; exige escopo antes de afirmar direitos concretos.' + (' O ano de 2022 impõe referência normativa histórica.' if '2022' in s else '')
  if id in {'188627','188635'}:return 'Pergunta sobre possibilidade de trabalho durante gravidez, não simplesmente estabilidade. Restrições, afastamento ou adaptações dependem da ocupação, condições de saúde e normas aplicáveis; não formular proibição geral.'
  if id=='165052':return 'Retorno ao trabalho de gestante é diferente de dispensa ou estabilidade; momento e condições de retorno não aparecem no termo.'
  if 'justa causa' in s:return 'A pergunta envolve justa causa na gravidez; regras e provas da situação concreta são indispensáveis para eventual conclusão jurídica.'
  if 'experiencia' in s:return 'A consulta menciona contrato de experiência e gravidez; não pressupor vínculo ou extensão de estabilidade sem contexto jurídico.'
  if 'pedir as contas' in s:return 'Demissão a pedido da gestante não equivale a dispensa patronal; efeitos exigem análise das circunstâncias e normas.'
  if 'estabilidade' in s:return 'Busca por estabilidade após gestação; não fixar término da proteção sem referência normativa e datas.'
  return 'Busca informativa sobre gravidez e vínculo/retorno ao trabalho; não fornecer cálculo de semanas nem conclusão jurídica sem contexto.'
 if rule=='PRAZOS_CALCULADORAS':
  if 'judiciais' in s or 'processuais' in s:return 'Prazos judiciais/processuais precisam do rito, jurisdição, marco inicial e calendário forense; a consulta pede ferramenta, não um prazo já calculado.'
  if 'úteis' in s or 'uteis' in s:return 'O texto explicita dias úteis, que dependem de calendário, feriados e dias sem expediente; não trocar por dias corridos.'
  if 'meses' in s:return 'Prazos em meses não têm duração fixa em dias; são necessários marco inicial e regra de contagem.'
  if 'em dias' in s:return 'Indica cálculo de prazo em dias, sem especificar necessariamente se úteis ou corridos; não presumir convenção de contagem.'
  return 'Calculadora de prazos sem data inicial, unidade ou calendário; busca por ferramenta, não resultado numérico.'
 if rule=='JUROS_E_FATURAS_CARTAO':
  if id=='152171':return 'Fatura com juros não demonstra parcelamento ou financiamento formal: os encargos podem decorrer de rotativo, atraso ou outra modalidade. Não presumir tipo nem taxa.'
  if 'adiantamento' in s:return 'Adiantamento de fatura do Nubank não equivale a contratação de empréstimo nem define benefício financeiro; é consulta sobre operação de cartão.'
  if 'qual a taxa' in s:return 'Pergunta pela taxa praticada por emissor específico; ela varia por modalidade, contrato e período e não deve ser inventada ou confundida com rendimento.'
  if 'santander' in s or 'nubank' in s or 'itau' in s:return 'Busca por juros de parcelamento de fatura de emissor nomeado. Tratar como informação sobre taxas/contrato, sem presumir taxa vigente ou valor da fatura.'
  if 'parcelamento' in s:return 'Consulta juros de parcelamento de cartão; parcelas dependem de principal, taxa, prazo e regras do emissor não especificados.'
  return 'Tema relativo à fatura e às condições de crédito do cartão; parâmetros insuficientes para cálculo pronto.'
 if rule=='PLANILHAS_ORCAMENTO':
  if id in {'184208','202634','203445','203453','203923','203930'}:return 'A palavra planilha explicita procura por modelo de controle, mas não indica se será usado em orçamento pessoal ou empresarial. Não inventar público-alvo nem montantes.'
  if any(t in s for t in ('empresa','microempresa','empresarial')):return 'O termo empresa/microempresa/empresarial indica planilha de organização de despesas de negócio, não simulação de investimento.'
  if 'domestica' in s or 'doméstica' in s:return 'Doméstica explicita controle de gastos da casa; busca por ferramenta de organização financeira.'
  return 'A consulta procura planilha de gastos, que é ferramenta de controle financeiro e não operação matemática com números fornecidos.'
 if rule=='SIMULADORES_INVESTIMENTOS':
  if id in {'172075','266225','267764'}:
   return 'O termo simulação/simular descreve a operação de projetar investimento, mas não afirma busca por um site simulador específico. Classificar cálculo contextual: montante, período, taxa, aportes e custos faltam.'+(' Para Tesouro IPCA+, preço de mercado interfere se houver venda antecipada.' if 'ipca' in s else '')
  if 'simulador' in s:return 'O substantivo simulador sinaliza procura por ferramenta de investimentos; instituição e ativo, quando presentes, não autorizam projetar retorno fixo.'
  if 'liquidez' in s:return 'Liquidez mensal é ambígua entre datas de resgate e rendimento mensal; demanda produto e condições concretas.'
  if 'rentabilidade' in s:return 'Rentabilidade de banco ou fundo depende do produto e do período, não sendo taxa única da instituição.'
  return 'Consulta sobre condições de investimentos; estimativas exigem parâmetros financeiros e não devem ser inventadas.'
 if rule=='ESTATISTICA_E_MEDIA_ENEM':
  if id=='146995':return 'Estatística média aritmética apresenta tópicos conceituais sem amostra nem números; não confundir referência de método com pedido de valor.'
  if id=='252541':return 'Resolver probabilidade indica execução de problema/cálculo, mas o evento, o espaço amostral e os dados não estão fornecidos; manter cálculo contextual sem supor independência.'
  if id=='79576':return 'Moda salarial é medida estatística aplicada à distribuição de salários; não tem relação com moda vestuário nem implica média salarial.'
  if 'enem' in s:return 'Média do ENEM pode representar média simples de notas do candidato ou indicador agregado; não calcular sem notas nem confundir com nota de corte ou pesos institucionais.'
  if 'moda' in s:return 'A palavra moda no contexto matemático significa valor mais frequente, não vestuário; sem série de dados não há resultado.'
  if 'como' in s:return 'Como achar média é pergunta sobre procedimento, não fornecimento de dados para calcular um resultado.'
  return 'Consulta estatística sobre média aritmética sem valores; distinguir definição, fórmula e cálculo parametrizado.'
 raise ValueError(rule)

def revised(old,id,decision):
 n=old.copy()
 if id not in PATCH:return n
 n.update(PATCH[id])
 if 'subcluster' in PATCH[id]:n['dominio_ou_grandeza']=n['subcluster']
 n['intencao_principal']=PREFIX[n['tipo_intencao']]+n['subcluster']
 n['justificativa_curta']=justification(decision)+' Evidência: «'+old['Keyword']+'». (P3 v5.5: revisão técnica, homologação editorial pendente.)'
 return n

def revise_zip(src,out,dec):
 seen=set();altered=set();stats=[];num=base=ctrl=0
 with zipfile.ZipFile(src) as z, zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as y:
  assert z.testzip() is None and len(z.namelist())==30
  for name in z.namelist():
   raw=csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';');fields=list(raw.fieldnames)
   buffer=io.StringIO(newline='');w=csv.DictWriter(buffer,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();lcount=patch_count=0
   for old in raw:
    id=old['id_global'];base+=old['tipo_registro']=='base';ctrl+=old['tipo_registro']!='base';lcount+=1
    if id in dec:
     assert id not in seen and old['tipo_registro']=='base';seen.add(id)
     assert old['Keyword']==dec[id]['Keyword']
     n=revised(old,id,dec[id]);delta={k for k in fields if old[k]!=n[k]}
     assert delta<=EDIT,(id,delta)
     if delta:
      assert id in PATCH;altered.add(id);patch_count+=1
    else:n=old
    w.writerow(n)
   y.writestr(name.replace('v5.4','v5.5'),('\ufeff'+buffer.getvalue()).encode('utf-8'))
   stats.append({'lote':name.replace('v5.4','v5.5'),'registros':lcount,'patches':patch_count,'status':'PASSOU'})
 assert seen==set(dec) and altered==set(PATCH) and ctrl==2190 and base in (294905,291296),(len(seen),len(altered),ctrl,base)
 return stats,base,ctrl

def revise_queue(a,b,dec):
 seen=set();n=0
 with a.open(encoding='utf-8-sig',newline='') as f,b.open('w',encoding='utf-8-sig',newline='') as g:
  r=csv.DictReader(f,delimiter=';');historic=list(r.fieldnames)
  assert len(historic)==414 and set(historic).isdisjoint(TRACE),(len(historic))
  w=csv.DictWriter(g,fieldnames=historic+TRACE,delimiter=';',lineterminator='\n');w.writeheader()
  for prev in r:
   id=prev['id_global'];n+=1;trace={k:'' for k in TRACE}
   if id in dec:
    assert id not in seen;seen.add(id)
    typ=prev['tipo_intencao_final_p3_v5_4'];sub=prev['subcluster_final_p3_v5_4']
    area=prev['area_final_p3_v5_4'];cluster=prev['cluster_final_p3_v5_4']
    if id in PATCH:typ=PATCH[id].get('tipo_intencao',typ);sub=PATCH[id].get('subcluster',sub)
    trace.update({'status_p3_v5_5':'REVISADO','parecer_p3_v5_5':'REFINADO' if id in PATCH else 'MANTIDO_COM_RESSALVA',
    'justificativa_p3_v5_5':justification(dec[id]),'area_final_p3_v5_5':area,
    'cluster_final_p3_v5_5':cluster,'subcluster_final_p3_v5_5':sub,
    'tipo_intencao_final_p3_v5_5':typ,'classificacao_alterada_p3_v5_5':'sim' if id in PATCH else 'não'})
   prev.update(trace);w.writerow(prev)
 assert seen==set(dec)
 return {'fila':b.name,'linhas':n,'historicas':414,'novas':8,'status':'PASSOU'}

def main():
 decisions,dh=rd(S/'p3-v5.4-pareceres-100.csv');dec={x['id_global']:x for x in decisions};assert len(dec)==len(decisions)==100 and set(PATCH)<=set(dec)
 # All gold-filtered and canonical sources share these 100 IDs.
 pairs=[('lotes-001-a-030-p3-v5.4.zip','lotes-001-a-030-p3-v5.5.zip'),('lotes-001-a-030-p3-v5.4-sem-ouro.zip','lotes-001-a-030-p3-v5.5-sem-ouro.zip')]
 stats=[]
 for a,b in pairs:
  ss,base,ctrl=revise_zip(S/a,D/b,dec)
  stats += [{'versao':'sem_ouro' if 'sem-ouro' in b else 'canonica',**row} for row in ss]
 queues=[('p3-v5.4-fila-23965.csv','p3-v5.5-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.4.csv','fila-geral-p0-p1-p2-p3-v5.5.csv',52046),('p3-v5.4-fila-23865-sem-ouro.csv','p3-v5.5-fila-23865-sem-ouro.csv',23865),('fila-geral-v5.4-sem-ouro-51884.csv','fila-geral-v5.5-sem-ouro-51884.csv',51884)]
 qreport=[revise_queue(S/a,D/b,dec) for a,b,n in queues];assert [q['linhas'] for q in qreport]==[q[2] for q in queues]
 assert (S/'backlog-global-98-com-parecer-v27.csv').exists();shutil.copyfile(S/'backlog-global-98-com-parecer-v27.csv',D/'backlog-global-98-com-parecer-v27.csv')
 orig={}
 with zipfile.ZipFile(S/'lotes-001-a-030-p3-v5.4.zip') as z:
  for name in z.namelist():
   for r in csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';'):
    if r['id_global'] in dec:orig[r['id_global']]=r
 assert len(orig)==100
 opinions=[];patches=[]
 for id in sorted(dec,key=int):
  o=orig[id];x=dec[id];n=revised(o,id,x);delta={k:(o[k],n[k]) for k in o if o[k]!=n[k]}
  assert bool(delta)==(id in PATCH)
  opinions.append({'id_global':id,'lote_id':x['lote_id'],'familia_id':x['familia_id'],'Keyword':x['Keyword'],'regra_v5_4':x['regra'],
  'parecer_v5_5':'REFINADO' if delta else 'MANTIDO_COM_RESSALVA','justificativa_individual':justification(x),
  'area_v5_4':o['area_principal'],'area_v5_5':n['area_principal'],
  'cluster_v5_4':o['cluster'],'cluster_v5_5':n['cluster'],
  'subcluster_v5_4':o['subcluster'],'subcluster_v5_5':n['subcluster'],
  'tipo_v5_4':o['tipo_intencao'],'tipo_v5_5':n['tipo_intencao'],'confianca_v5_5':n['confianca'],
  'campos_modificados':','.join(sorted(delta)),'homologacao_editorial':'PENDENTE'})
  if delta:patches.append({'id_global':id,'lote_id':x['lote_id'],'Keyword':x['Keyword'],
  'campos_modificados':','.join(sorted(delta)),
  'antes_json':json.dumps({k:v[0] for k,v in delta.items()},ensure_ascii=False,sort_keys=True),
  'depois_json':json.dumps({k:v[1] for k,v in delta.items()},ensure_ascii=False,sort_keys=True),
  'justificativa':justification(x)})
 wr(D/'p3-v5.5-pareceres-100.csv',opinions);wr(D/'p3-v5.5-patches-23.csv',patches)
 wr(D/'p3-v5.5-regressao-inicial-60-lotes.csv',stats)
 report={'etapa':'P3 v5.5','entrada':'P3 v5.4 + filtro Ouro DEC-089','pareceres_revisados':100,'refinamentos':len(PATCH),'mantidos_com_ressalvas':100-len(PATCH),
 'novos_ids':0,'familias_revisadas':len({r['familia_id'] for r in opinions}),'grupos_revisados':len({r['regra_v5_4'] for r in opinions}),
 'p3_elegiveis_sem_ouro':19362,'p3_elegiveis_canonicos':19462,
 'registros_base_canonicos':294905,'registros_base_sem_ouro':291296,'controles_por_versao':2190,
 'linhas_ouro_operacionalmente_excluidas':3609,'filas':qreport,'colunas_historicas':414,'colunas_novas':8,
 'lotes_canonicos':30,'lotes_filtrados':30,'p2_pendentes':4660,'backlog_global':98,'homologacao_editorial':'PENDENTE','status':'AGUARDA_REGRESSAO_INDEPENDENTE'}
 (D/'p3-v5.5-resumo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()