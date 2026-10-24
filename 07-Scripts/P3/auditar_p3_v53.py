#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoria P3 v5.3: revisão fechada dos 75 pareceres v5.2.
Sem nova expansão. Atualiza tanto o snapshot canônico quanto a visão reversível
filtrada Ouro da DEC-089, sem tocar nas fontes originais.
Execução: python auditar_p3_v53.py
"""
from pathlib import Path
from collections import Counter
from hashlib import sha256
from copy import deepcopy
import csv, io, json, zipfile, shutil
HERE=Path(__file__).resolve(); ROOT=HERE.parents[2] if HERE.parent.name=='P3' and HERE.parent.parent.name=='07-Scripts' else HERE.parent
SRC=ROOT/'08-Entregas/P3-v5.2'
OURO=ROOT/'auditoria-ouro'
OUT=ROOT/'08-Entregas/P3-v5.3'
OUT.mkdir(parents=True,exist_ok=True)

REASONS={
4447:'O número de semanas está explícito; é conversão aproximada, sem indicação de gravidez e sem equivalência universal em meses civis.',
4473:'A expressão abreviada contém 17 semanas e meses como unidade de destino; apesar de não usar verbo, sugere conversão quantitativa, não mera definição.',
4476:'Pergunta quantos meses correspondem a 17 semanas; converter aproximadamente, sem presumir gestação.',
5932:'Gravidez aparece expressamente; 22 dias podem ser expressos como três semanas e um dia, sem extrapolar a etapa gestacional.',
7111:'O valor de três semanas e três dias está expresso; meses podem ser apenas aproximados sem mês civil ou calendário inicial.',
7232:'Trinta horas semanais é uma referência de jornada, mas não informa escala, dias trabalhados ou pedido numérico inequívoco.',
7610:'Embora haja 32 semanas, a palavra tabela sinaliza busca por quadro de referência gestacional, não medição exata de meses.',
7793:'A pergunta requer converter 35 horas semanais em horas diárias; faltam os dias de trabalho por semana.',
8450:'A expressão gravidez é inequívoca; quarenta dias equivalem a cinco semanas e cinco dias, não uma estimativa clínica individual.',
8921:'Quarenta e seis dias na gravidez podem ser traduzidos em semanas e dias; não inferir início da gestação nem data provável do parto.',
9464:'Cinquenta dias de gravidez são um intervalo em semanas e dias; não confundir contagem com diagnóstico de idade gestacional.',
11045:'O enunciado compara 8 horas diárias e 44 semanais, mas não traz a escala para determinar compatibilidade ou distribuí-las.',
12164:'Pergunta jurídica sobre base do adicional de insalubridade; a resposta depende das normas aplicáveis, sem pressupor base salarial única.',
19956:'A capacidade nominal de 12.000 BTU/h pode ser convertida para watts térmicos, mas potência elétrica exige eficiência do equipamento.',
19957:'A grafia acentuada confirma a mesma ambiguidade entre capacidade térmica e potência elétrica; nenhum consumo pode ser calculado apenas pelo BTU/h.',
20016:'A capacidade nominal de 60.000 BTU/h não informa potência elétrica do aparelho; consulta requer distinguir as duas grandezas.',
21237:'A palavra online pede uma ferramenta de arredondamento de números decimais, sem valor numérico fornecido.',
37093:'A expressão calculadora gestacional remete à ferramenta que usa referência temporal apropriada; a busca não informa data de última menstruação.',
39856:'O termo calculadora aponta ferramenta para semanas e meses, não um resultado específico nem gestação implícita.',
39861:'A consulta por calculadora sem valor numérico é busca por ferramenta, não cálculo já parametrizado.',
39862:'O x entre semanas e meses sugere transformação de unidades; calculadora é a intenção inequívoca, sem informação de gravidez.',
44430:'Calcular juros da fatura exige saldo, período, modalidade, taxa e eventuais encargos; não inventar taxa de cartão.',
47574:'O verbo calcular designa transformação de semanas em meses, ainda sem valor inicial; trata-se de pedido genérico de operação contextual.',
47583:'O verbo calcular com origem semanas e destino meses sinaliza operação a executar, sem parâmetros ou referência de calendário.',
52269:'A expressão cálculo de horas semanais não informa marcações de ponto nem quantidade de dias; manter intenção de cálculo condicionado a dados.',
72324:'Três meses não equivalem a número universal exato de semanas sem definição de mês e marco temporal.',
72327:'Cinco meses não são sempre vinte semanas: meses têm durações variáveis e a interpretação gestacional não está explicitada.',
74391:'Como calcular pede procedimento para jornada de 25 horas, mas distribuição diária depende de escala e dias úteis.',
76247:'O enunciado solicita método de converter semanas em meses; não contém números e não indica gestação.',
83462:'Como calcular semanas para meses é consulta de procedimento; exigir aproximação ou calendário para evitar falsa exatidão.',
98272:'A pergunta é sobre juros em compra parcelada; contrato define encargos, não há saldo, taxa nem simulação completa.',
98419:'A expressão tem juros é pergunta de incidência, e a resposta depende de oferta, contrato e emissor.',
148231:'O usuário quer instruções de arredondamento para cima dentro do Excel; preservar especificidade de planilha em vez de calculadora web.',
155122:'O termo ferramenta indica busca por conversor salário bruto–líquido; deduções variam com regime e competência.',
157569:'Financiamento de fatura é produto de crédito, não financiamento imobiliário; busca ainda não define taxa ou valor.',
159146:'A palavra fórmula indica explicação do método da moda, não cálculo sem uma série de observações.',
159229:'Fórmula para calcular moda pede procedimento; em séries multimodais pode haver mais de uma moda.',
165270:'Gestação de seis meses é expressão aproximada; conversão para semanas depende de convenção gestacional e datas.',
167314:'Horas semanal é categoria vaga de jornada; não atribuir dias ou carga horária normativa sem contexto.',
167320:'A expressão horas semanais trabalhadas se refere a apuração de jornada, porém sem registros de ponto ou horários.',
167391:'Horas trabalho semanal descreve jornada de trabalho, não intervalo cronológico entre datas.',
174320:'Juros associados a compra parcelada no cartão são custos financeiros, não rentabilidade ou retorno de investimento.',
174617:'A inversão de ordem das palavras preserva consulta informativa sobre taxas e parcelamento, sem valores fornecidos.',
175314:'Consulta genérica a juros do parcelamento do cartão, não é uma tabela universal de taxas.',
175918:'A referência ao Banco do Brasil indica condições específicas da instituição; não usar taxa genérica ou datada como atual.',
175919:'A referência ao Bradesco exige condições específicas e período de vigência; não inventar taxa vigente.',
175920:'A menção à Caixa indica informação bancária; não presumir que financiamento ou rotativo tenham a mesma taxa.',
175923:'A menção ao Santander indica comparação de condições do emissor; sem valores não cabe simulação automática.',
182412:'Média aritmética e mediana são estatísticas distintas; sem amostra a intenção é explicativa.',
186977:'A palavra ponderada torna relevante explicar pesos; não colapsar média ponderada em simples nem calcular sem dados.',
186979:'Moda, média e mediana são três conceitos, embora a enumeração apareça sem pedido específico de cálculo.',
189381:'Média aritmética e mediana sem lista de valores é pesquisa conceitual, não resultado numérico.',
189389:'A ausência de conectivo não muda a intenção informativa ao comparar média e mediana.',
189391:'Lista de média, mediana e moda aponta comparação de medidas de tendência central, sem amostra numérica.',
189393:'Média e moda podem diferir e dependem da amostra; classificar como informação conceitual.',
189396:'Mesmo com ordem moda–mediana, os três termos não apresentam entradas para cálculo.',
194610:'O que é solicita definições de moda, mediana e média, não busca de ferramenta.',
194617:'A pergunta conceitual sobre média, moda e mediana não deve ser interpretada como cálculo parametrizado.',
195785:'A abreviação oq significa é pedido de definição de salário bruto, distinto de calcular salário líquido.',
202524:'Planilha controle cartão busca modelo de organização financeira, e não fórmula de retorno de investimento.',
202797:'Planilha de controle indica busca por modelo/template; não pressupor fórmula de juros.',
204061:'Para controlar cartão reforça interesse em planilha de gestão, não cálculo automático de uma compra.',
206329:'7.500 BTU/h do ar-condicionado é potência térmica nominal; potência elétrica consumida depende de eficiência e modelo.',
207405:'A consulta inclui 12.000 BTU em watts, mas sem especificar watts térmicos ou elétricos; evitar resultado único.',
207408:'A potência de 18.000 BTU/h não implica o mesmo valor numérico em watts elétricos; consulta permanece ambígua.',
207413:'24.000 BTU/h podem ser expressos em watts térmicos; consumo real exige informações técnicas do aparelho.',
207417:'36.000 BTU/h como capacidade térmica não determina potência elétrica; não misturar grandezas.',
239158:'Consumo em watts de ar de 12.000 BTU/h depende de modelo e eficiência, além de condições de operação.',
254125:'O usuário compara salário-base e salário bruto; são conceitos que podem diferir conforme adicionais e composição salarial.',
254149:'A pergunta sobre descontos no salário-base é conceitual e depende da definição adotada no contracheque.',
254160:'Descontos no salário bruto são componentes de cálculo de líquido, mas sem valores é apenas tema informativo.',
254173:'Salário bruto mínimo aproxima salário mínimo e remuneração bruta, não a comparação geral entre salário-base e salário líquido.',
255409:'Salário bruto 2022 remete a referência histórica; não substituir parâmetros de 2022 por normas atuais.',
267849:'Simulação de parcelamento do cartão pede ferramenta; cálculo real exige valor, prazo e taxas aplicáveis.',
270768:'BTU isolado é energia, enquanto W mede potência; converter exige unidade temporal (BTU/h), que a consulta não explicita.'
}
PATCHES={
 '4473':{'tipo_intencao':'cálculo contextual'},
 '47574':{'tipo_intencao':'cálculo contextual'},
 '47583':{'tipo_intencao':'cálculo contextual'},
 '148231':{'subcluster':'Arredondamento para cima no Excel','dominio_ou_grandeza':'Arredondamento para cima no Excel'},
 '254173':{'subcluster':'Salário mínimo e remuneração bruta','dominio_ou_grandeza':'Salário mínimo e remuneração bruta'},
 '270768':{'subcluster':'BTU (energia), BTU/h (potência) e watts','dominio_ou_grandeza':'BTU (energia), BTU/h (potência) e watts'}
}
EDITABLE={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_3','parecer_p3_v5_3','justificativa_p3_v5_3','area_final_p3_v5_3','cluster_final_p3_v5_3','subcluster_final_p3_v5_3','tipo_intencao_final_p3_v5_3','classificacao_alterada_p3_v5_3']
PREFIX={'informacional':'Consultar ou entender: ','busca de ferramenta':'Encontrar ferramenta: ','cálculo contextual':'Calcular com parâmetros: '}

def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:
  d=csv.DictReader(f,delimiter=';');return list(d),list(d.fieldnames)
def save(path,rows,fields=None):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
def patch_line(old,rid):
 new=old.copy();note=REASONS[int(rid)];details=PATCHES.get(rid)
 if not details:return new
 new.update(details)
 sub=new['subcluster']; typ=new['tipo_intencao'];new['intencao_principal']=PREFIX.get(typ,'Consultar ou entender: ')+sub
 new['justificativa_curta']=note+' Evidência: «'+old['Keyword']+'». (P3 v5.3: revisão técnica, homologação editorial pendente.)'
 return new

def revise_zip(infile,outfile,ids):
 seen=set();changed=set();stats=[];bases=ctrls=0
 with zipfile.ZipFile(infile) as zin,zipfile.ZipFile(outfile,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  assert zin.testzip() is None and len(zin.namelist())==30
  for fn in zin.namelist():
   d=csv.DictReader(io.StringIO(zin.read(fn).decode('utf-8-sig')),delimiter=';');fields=list(d.fieldnames)
   sink=io.StringIO(newline='');w=csv.DictWriter(sink,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader()
   lc=lb=lp=0
   for old in d:
    rid=old['id_global']; lb+=old['tipo_registro']=='base';lc+=old['tipo_registro']!='base'
    if rid in ids:
     assert rid not in seen and old['tipo_registro']=='base';seen.add(rid)
     new=patch_line(old,rid)
     diffs={k for k in fields if old[k]!=new[k]}
     assert diffs<=EDITABLE,(rid,diffs)
     if diffs:changed.add(rid);lp+=1
    else:new=old
    w.writerow(new)
   newname=fn.replace('v5.2','v5.3')
   zout.writestr(newname,('\ufeff'+sink.getvalue()).encode('utf-8'))
   stats.append({'lote':newname,'bases':lb,'controles':lc,'refinamentos':lp,'status':'PASSOU'})
   bases+=lb;ctrls+=lc
 assert seen==ids and changed==set(PATCHES) and sum(int(x['refinamentos']) for x in stats)==len(PATCHES)
 return {'bases':bases,'controles':ctrls,'stats':stats}

def mark_queue(src,dst,ids,expected):
 seen=set();orig_head=None
 with src.open(encoding='utf-8-sig',newline='') as fin,dst.open('w',encoding='utf-8-sig',newline='') as fout:
  d=csv.DictReader(fin,delimiter=';');orig_head=list(d.fieldnames)
  assert len(orig_head)==398 and not set(TRACE)&set(orig_head)
  w=csv.DictWriter(fout,fieldnames=orig_head+TRACE,delimiter=';',lineterminator='\n');w.writeheader();n=0
  for old in d:
   rid=old['id_global'];n+=1;new=old.copy();ext={k:'' for k in TRACE}
   if rid in ids:
    assert rid not in seen;seen.add(rid)
    p=patch_line({'Keyword':old['Keyword'],'area_principal':old['area_final_p3_v5_2'],'cluster':old['cluster_final_p3_v5_2'], 'subcluster':old['subcluster_final_p3_v5_2'],'tipo_intencao':old['tipo_intencao_final_p3_v5_2']},rid)
    typ=p['tipo_intencao']
    ext.update({'status_p3_v5_3':'REVISADO','parecer_p3_v5_3':'REFINADO' if rid in PATCHES else 'MANTIDO_COM_RESSALVA',
     'justificativa_p3_v5_3':REASONS[int(rid)],'area_final_p3_v5_3':p['area_principal'],
     'cluster_final_p3_v5_3':p['cluster'],'subcluster_final_p3_v5_3':p['subcluster'],
     'tipo_intencao_final_p3_v5_3':typ,'classificacao_alterada_p3_v5_3':'sim' if rid in PATCHES else 'não'})
   new.update(ext);w.writerow(new)
 assert seen==ids and n==expected,(len(seen),n,expected)
 return {'linhas':n,'colunas_historicas':len(orig_head),'novas_colunas':len(TRACE)}

def main():
 dec,_=read(SRC/'p3-v5.2-decisoes-75.csv');ids={x['id_global'] for x in dec}
 assert len(ids)==len(dec)==75 and ids=={str(i) for i in REASONS}
 assert set(PATCHES)<=ids
 gold,_=read(OURO/'ids-ouro-excluir-3609.csv');exclude={x['id_global'] for x in gold}
 assert ids.isdisjoint(exclude)
 oldfull=SRC/'lotes-001-a-030-p3-v5.2.zip';oldfilter=OURO/'lotes-30-trabalho-sem-ouro.zip'
 rf=revise_zip(oldfull,OUT/'lotes-001-a-030-p3-v5.3.zip',ids)
 rg=revise_zip(oldfilter,OUT/'lotes-001-a-030-p3-v5.3-sem-ouro.zip',ids)
 assert (rf['bases'],rf['controles'])==(294905,2190)
 assert (rg['bases'],rg['controles'])==(291296,2190)
 pairs=[(SRC/'p3-v5.2-fila-23965.csv',OUT/'p3-v5.3-fila-23965.csv',23965),
 (SRC/'fila-geral-p0-p1-p2-p3-v5.2.csv',OUT/'fila-geral-p0-p1-p2-p3-v5.3.csv',52046),
 (OURO/'fila-p3-v5.2-sem-ouro-23865.csv',OUT/'p3-v5.3-fila-23865-sem-ouro.csv',23865),
 (OURO/'fila-geral-v5.2-sem-ouro-51884.csv',OUT/'fila-geral-v5.3-sem-ouro-51884.csv',51884)]
 queues={dst.name:mark_queue(src,dst,ids,n) for src,dst,n in pairs}
 # Patch artifacts exactly match diff of lotes; the before and after dictionaries cover only changed fields
 original={x['id_global']:x for x in dec}; revised=[];patchlog=[]
 with zipfile.ZipFile(oldfull) as z:
  beforemap={}
  for name in z.namelist():
   for r in csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig')),delimiter=';'):
    if r['id_global'] in ids:beforemap[r['id_global']]=r
 assert len(beforemap)==75
 for rid in sorted(ids,key=int):
  row=beforemap[rid]; now=patch_line(row,rid);diff={k:(row[k],now[k]) for k in row if row[k]!=now[k]}
  assert bool(diff)==(rid in PATCHES)
  v=original[rid]
  revised.append({'id_global':rid,'lote_id':v['lote_id'],'familia_id':v['familia_id'],'Keyword':v['Keyword'],
   'regra_v5_2':v['regra'],'parecer_v5_3':'REFINADO' if diff else 'MANTIDO_COM_RESSALVA',
   'justificativa_individual':REASONS[int(rid)],'area_v5_2':row['area_principal'],'area_v5_3':now['area_principal'],
   'cluster_v5_2':row['cluster'],'cluster_v5_3':now['cluster'],
   'subcluster_v5_2':row['subcluster'],'subcluster_v5_3':now['subcluster'],
   'tipo_v5_2':row['tipo_intencao'],'tipo_v5_3':now['tipo_intencao'],
   'confianca_v5_3':now['confianca'],'campos_modificados':','.join(sorted(diff)),
   'homologacao_editorial':'PENDENTE'})
  if diff:
   patchlog.append({'id_global':rid,'lote_id':v['lote_id'],'Keyword':v['Keyword'],
    'campos_modificados':','.join(sorted(diff)), 'antes_json':json.dumps({k:v[0] for k,v in diff.items()},ensure_ascii=False,sort_keys=True),
    'depois_json':json.dumps({k:v[1] for k,v in diff.items()},ensure_ascii=False,sort_keys=True),
    'justificativa':REASONS[int(rid)]})
 save(OUT/'p3-v5.3-pareceres-75.csv',revised)
 save(OUT/'p3-v5.3-patches-6.csv',patchlog)
 save(OUT/'p3-v5.3-regressao-inicial-canonica.csv',rf['stats'])
 save(OUT/'p3-v5.3-regressao-inicial-sem-ouro.csv',rg['stats'])
 shutil.copyfile(SRC/'backlog-global-98-com-parecer-v27.csv',OUT/'backlog-global-98-com-parecer-v27.csv')
 counts=Counter(x['regra_v5_2'] for x in revised)
 save(OUT/'p3-v5.3-qa-por-grupo.csv',[{'grupo':k,'registros':v,'refinados':sum(x['regra_v5_2']==k and x['parecer_v5_3']=='REFINADO' for x in revised),
 'mantidos':sum(x['regra_v5_2']==k and x['parecer_v5_3']!='REFINADO' for x in revised),'homologacao_editorial':'PENDENTE'} for k,v in sorted(counts.items())])
 summary={'versao':'P3 v5.3','revisados':75,'refinamentos':len(patchlog),'mantidos_com_ressalva':75-len(patchlog),'familias':len({x['familia_id'] for x in revised}),
 'grupos':len(counts),'distribuicao':dict(counts),'lotes':30,'base_canonica':rf['bases'],'base_filtrada_ouro':rg['bases'],'controles_preservados':2190,
 'ids_ouro_reversiveis':3609,'ids_v52_revisados_excluidos_ouro':0,'fila_p3_canonica':23965,'fila_p3_ouro':23865,
 'fila_geral_canonica':52046,'fila_geral_ouro':51884,'colunas_historicas_filas':398,'colunas_novas':8,
 'p3_elegiveis_canonico':19562,'p3_elegiveis_apos_ouro':19462,'backlog_global':98,'p2_pendentes':4660,
 'homologacao_editorial':'PENDENTE','status':'AUDITORIA_TECNICA_A_VALIDAR_REGRESSAO'}
 (OUT/'p3-v5.3-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()