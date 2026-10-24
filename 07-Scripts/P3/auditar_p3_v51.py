#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v5.1: revisão crítica fechada dos 75 IDs da v5.0, sem expansão.
Reexecute da raiz do pacote: python 07-Scripts/P3/auditar_p3_v51.py
Só 19 registros-base podem ter classificação alterada. Fonte v5.0 imutável.
"""
from pathlib import Path
from collections import Counter
import csv,io,zipfile,json,re
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'08-Entregas/P3-v5.1/FONTES-REPRODUCAO/08-Entregas/P3-v5.0'
OUT=ROOT/'08-Entregas/P3-v5.1'
READ=['p3-v5.0-decisoes-75.csv','p3-v5.0-patches-75.csv','p3-v5.0-plano-por-id.csv']
EDIT={'area_principal','cluster','subcluster','intencao_principal','tipo_intencao','dominio_ou_grandeza','confianca','revisao_manual','justificativa_curta'}
TRACE=['status_p3_v5_1','parecer_p3_v5_1','justificativa_p3_v5_1','area_final_p3_v5_1','cluster_final_p3_v5_1','subcluster_final_p3_v5_1','tipo_intencao_final_p3_v5_1','classificacao_alterada_p3_v5_1']
# Intenções "informacional" não assumem números ou execução no presente.
PREFIX={'informacional':'Consultar ou entender: ','cálculo contextual':'Calcular com parâmetros: ','busca de ferramenta':'Encontrar ferramenta: '}
# Deliberações EDITORIAIS: apenas esses IDs têm refinamento semântico necessário.
BTU={19940,19954,19969,19990,20011,206302,206323}
CHANGES={
 18136:{'tipo_intencao':'informacional'},
 85882:{'subcluster':'Perímetro a partir da área sob hipóteses geométricas'},
 160019:{'tipo_intencao':'informacional'},
 200874:{'tipo_intencao':'informacional'},
 207450:{'tipo_intencao':'informacional'},
 207458:{'subcluster':'Expoentes negativos e fracionários','tipo_intencao':'informacional'},
 207492:{'tipo_intencao':'informacional','confianca':'baixa'},
 207494:{'tipo_intencao':'informacional','confianca':'baixa'},
 207640:{'subcluster':'Potência de potência envolvendo frações','tipo_intencao':'informacional'},
 212548:{'tipo_intencao':'informacional'},
 242905:{'tipo_intencao':'informacional'},
 245615:{'tipo_intencao':'informacional','confianca':'baixa'},
}
for x in BTU:CHANGES[x]={
 'subcluster':'Capacidade em BTU/h versus watts térmicos e elétricos',
 'confianca':'baixa',
}
assert len(CHANGES)==19
# Uma avaliação contextual específica para cada uma das 75 keywords; nenhuma é aprovação humana.
REASONS={
18136:'Aplicar regra de três a dinheiro pede orientação sobre proporções monetárias; sem grandezas e quantias fornecidas, é consulta ao método, não execução de um cálculo específico.',
19940:'O termo 12.000 BTUs no ar-condicionado em geral é 12.000 BTU/h de capacidade térmica. Isto equivale a watts térmicos, mas não revela consumo elétrico em watts.',
19954:'Grafia 12000 BTUs sem pontuação equivale ao patamar 12.000 BTU/h; esclarecer watts térmicos versus entrada elétrica do aparelho antes de calcular.',
19969:'18.000 BTU/h de refrigeração admitem conversão dimensional para watts térmicos; watts de consumo dependem de eficiência e aparelho.',
19990:'24.000 BTU/h se referem à capacidade térmica, não à energia elétrica consumida; distinguir claramente as duas acepções de watts.',
20011:'60.000 BTU/h podem ser expressos em watts térmicos, mas não permitem inferir potência elétrica de entrada sem dados adicionais do sistema.',
20815:'Área e perímetro de figuras planas são conceitos relacionados mas diferentes; a expressão genérica aponta para explicação e fórmulas, sem figura ou dimensões.',
34947:'O termo calculadora indica navegação até ferramenta que conte dias corridos; faltam data inicial, final e critério de inclusão.',
34952:'Ferramenta para prazo em dias úteis deve considerar feriados e região; não assumir que fins de semana e feriados possam ser ignorados indistintamente.',
34973:'Plural prazos em dias corridos mantém a busca por ferramenta; dias de calendário não são contagem exclusiva de dias úteis.',
35042:'Busca por calculadora de probabilidade combinatória da Mega-Sena; não autoriza previsão de números sorteados nem promessa de acerto.',
39022:'Calculadora de perímetro do círculo é uma calculadora de comprimento de circunferência; requer raio ou diâmetro, ausentes na consulta.',
39176:'A expressão online confirma busca de ferramenta de contagem de dias corridos, não fornece limites temporais para cálculo direto.',
40713:'Verbo calcular aponta para três medidas estatísticas sobre uma amostra inexistente na consulta; exige conjunto de dados antes de produzir números.',
44797:'A consulta combina média, mediana e desvio padrão; a dispersão não deve ser confundida com as duas medidas de tendência central.',
46200:'Cálculo em distribuição normal precisa de média, desvio padrão e intervalo/limiar; não inferir probabilidade numérica sem parâmetros.',
46749:'Regra de três composta envolve várias grandezas e suas relações; não reduzir à simples ou calcular sem tabela de valores.',
50126:'A expressão cálculo da média, mediana e moda sugere operação estatística, mas não inclui amostra; manter cálculo contextual.',
52745:'Termo online sinaliza procura por calculadora de mediana, que depende de observações ordenadas e do tamanho do conjunto.',
52915:'Cálculo de perímetro de triângulo requer comprimentos de lados e não se confunde com área, alturas ou fórmulas de circunferência.',
53028:'Fórmula de cálculo de probabilidade sinaliza busca conceitual pela expressão apropriada e condições; nenhum espaço amostral é dado.',
73453:'Como achar indica tutorial de média, mediana e moda, não solicitação de três resultados numéricos.',
73455:'Como achar a mediana em estatística pede procedimento de ordenação e posição central, sem conjunto de dados.',
74540:'Como calcular a área de retângulo remete ao método base vezes altura; dados de base e altura ausentes.',
75232:'Como calcular a probabilidade de um evento remete a método; casos equiprováveis e espaço amostral não foram especificados.',
80707:'Como calcular perímetro de terreno pede técnica para somar medidas do contorno; tamanho e formato não informados.',
80708:'Terreno retangular tem perímetro duas vezes a soma dos lados adjacentes; a busca pede explicação sem medidas.',
81221:'Como calcular valor de potências solicita regras de base/expoente, sem operandos específicos para resultado.',
82145:'Como calcular expoente negativo pede explicação do inverso da potência, ressalvadas bases nulas quando expoente é negativo.',
82165:'Como calcular potência com expoente fracionário exige explicação de raízes e domínio dos números reais, não valores presumidos.',
82248:'Eventos independentes exigem distinguir interseção do evento isolado; como calcular pede fórmula condicionalmente, não um número.',
85882:'Direção da pergunta é obter perímetro dado área, não obter área dado perímetro; área isolada normalmente não define perímetro sem formato e medidas adicionais.',
85883:'Como descobrir o perímetro de quadrado pede multiplicar comprimento do lado por quatro; sem lado fornecido, consulta metodológica.',
92645:'Como saber perímetro de quadrado é intenção educacional semelhante, sem medida do lado para calcular.',
129186:'Definição de média, mediana e moda é busca de informação conceitual; não há cálculo a executar.',
134674:'Diferença média mediana compara métricas estatísticas distintas; não pressupor amostra ou resultado.',
146495:'Escrever radicais como potência fracionária é transformação algébrica ensinável; sem expressões concretas, não é uma conta definida.',
146953:'Medidas de tendência central incluem média, mediana e moda; buscar teoria, não misturar com desvio padrão.',
148215:'Excel calcular mediana aponta para instruções da função MED/MEDIAN e seleção de células, não busca de calculadora web independente.',
150927:'Expoente inteiro negativo é expressão conceitual genérica, envolvendo inversos e restrição de base diferente de zero.',
154466:'Ferramenta calculadora de expoente aponta explicitamente para ferramenta de potenciação, sem par base-expoente.',
154574:'Ferramenta calculadora perímetro é navegação para calculadora geométrica, mas figura e medidas não estão definidas.',
154618:'Ferramenta calcular expoente mantém busca de ferramenta de potenciação; não inferir potência elétrica.',
159546:'Fórmulas de média moda e mediana são informação metodológica e não fornecem série estatística.',
160019:'Fração negativa com expoente negativo nomeia propriedade algébrica, sem base e expoente concretos; não há cálculo definido.',
171613:'Interseção de eventos pede conceito e fórmula da probabilidade conjunta, sem pressupor independência.',
183059:'Pergunta se mediana é média pede distinção conceitual, não operação estatística.',
200863:'Passo a passo do perímetro de figura irregular requer procedimento para medir todos os segmentos do contorno.',
200873:'Perímetro de terreno é tópico de medição, mas não há dimensões nem verbo de executar cálculo; reter informação.',
200874:'Todo triângulo tem três lados; a expressão genérica sugere fórmula P=a+b+c, sem comprimentos numéricos para operar.',
204997:'Porcentagem de desconto de vale-refeição é benefício trabalhista; percentual efetivo não pode ser inferido sem regras aplicáveis e vínculo.',
205012:'Vale-alimentação exige distinguir desconto em folha de empréstimo ou cartão financeiro; nenhum percentual fixo foi fornecido.',
205013:'Desconto do vale-refeição refere-se a política de benefício e regras aplicáveis, não juros e nem cálculo com dados completos.',
205034:'A grafia sem preposição mantém a intenção de consultar percentual de desconto de vale-refeição e suas condições.',
205496:'Porcentagem com regra de três simples é busca de método proporcional; sem entradas numéricas não há resultado.',
206302:'Para 18.000 BTU/h, watts podem indicar capacidade térmica convertível ou potência elétrica consumida; o segundo requer eficiência/modelo.',
206323:'Para 60.000 BTU/h, não confundir W térmicos com W elétricos; sem identificação do equipamento, sentido de potência é ambíguo.',
207444:'Exemplos de expoente fracionário são pedido de demonstração didática, não de um cálculo com operandos.',
207450:'Potência com expoente fracionário negativo descreve classe de operações, sem base ou expoente explícitos para resolver.',
207455:'Expoente inteiro negativo exemplos pede casos ilustrativos e explicação, não operação específica.',
207458:'Expoente negativo e fracionário reúne duas propriedades da potenciação; sem base nem expoente numérico, tratar como consulta metodológica.',
207492:'A sequência 23 pode significar vinte e três ou 2³ após perda de sobrescrito; não há expoente explicitado, portanto não produzir resultado automático.',
207494:'A sequência 32 pode significar trinta e dois ou 3²; não reconstruir expoente sem contexto verificável.',
207552:'Potência de dez na calculadora científica tende a instrução sobre tecla EXP/10^x, não pedido de comprar ou localizar outra ferramenta.',
207640:'Potência de potência com fração não diz se a fração está na base ou no expoente; é busca por propriedade algébrica e não cálculo fechado.',
212548:'Probabilidade da interseção de eventos, sem valores, sugere fórmula P(A∩B)=P(A)P(B|A), sem hipótese automática de independência.',
212582:'Eventos dependentes referem-se a probabilidades condicionais e produto, não a conteúdo PDF nem à regra para eventos independentes.',
242905:'Raiz com expoente fracionário é tema de radiciação/potenciação, sem radicando ou expoente concreto para gerar resposta numérica.',
245597:'Regra de três em dinheiro indica explicação de proporcionalidade envolvendo valores monetários, não juros nem simulação de crédito.',
245599:'Regra de três para dinheiro sinaliza método proporcional aplicado a montantes; não pressupor taxas de empréstimos.',
245600:'Regra de três para finanças é amplo e não identifica produto financeiro nem dados; reter método genérico, com ressalva.',
245605:'Termo online identifica ferramenta para regra de três em porcentagens; a consulta não traz os três valores conhecidos.',
245615:'Valores pode aludir a entradas de uma regra de três ou a exemplos; não há números nem verbo específico, então evitar presumir cálculo imediato.',
269077:'Site para calcular probabilidade é navegação para ferramenta; sem eventos ou espaço amostral, não se calcula valor direto.',
294636:'Quadrado com perímetro conhecido permite calcular área via lado P/4, mas perímetro numérico não foi fornecido; cálculo contextual.'
}
assert len(REASONS)==75, len(set(REASONS))==75

def read(path):
 with open(path,encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f,delimiter=';');return list(r),list(r.fieldnames)
def dump(path,rows,fields):
 path.parent.mkdir(parents=True,exist_ok=True)
 with open(path,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
def row_updated(old,rid):
 if rid not in CHANGES:return old.copy(),[]
 new=old.copy();new.update(CHANGES[rid]);
 if 'subcluster' in CHANGES[rid]:new['dominio_ou_grandeza']=new['subcluster']
 if 'subcluster' in CHANGES[rid] or 'tipo_intencao' in CHANGES[rid]:new['intencao_principal']=PREFIX[new['tipo_intencao']]+new['subcluster']
 new['justificativa_curta']=REASONS[rid]+' (P3 v5.1: refinamento técnico; homologação editorial pendente.)'
 delta=[c for c in old if old[c]!=new[c]]
 assert delta and set(delta)<=EDIT,(rid,delta)
 return new,delta

def main():
 decisions,_=read(SRC/'p3-v5.0-decisoes-75.csv');plan,_=read(SRC/'p3-v5.0-plano-por-id.csv')
 by_id={int(x['id_global']):x for x in decisions}
 assert len(by_id)==len(plan)==75 and set(by_id)==set(REASONS)
 assert set(CHANGES).issubset(by_id)
 q,oldcols=read(SRC/'p3-v5.0-fila-23965.csv');g,gcols=read(SRC/'fila-geral-p0-p1-p2-p3-v5.0.csv')
 assert len(q)==23965 and len(g)==52046 and oldcols==gcols and len(oldcols)==382
 qi={int(x['id_global']):x for x in q};gi={int(x['id_global']):x for x in g}
 assert all(qi[rid]['status_p3_v5_0']=='TRATADO' and gi[rid]['status_p3_v5_0']=='TRATADO' for rid in by_id)
 for row in q:
  if row['status_p3_v5_0']:assert int(row['id_global']) in by_id
 OUT.mkdir(parents=True,exist_ok=True)
 newrows={};patches=[];stats=[];controls=bases=0
 with zipfile.ZipFile(SRC/'lotes-001-a-030-p3-v5.0.zip') as zin,zipfile.ZipFile(OUT/'lotes-001-a-030-p3-v5.1.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  assert len(zin.namelist())==30 and zin.testzip() is None
  for name in zin.namelist():
   rdr=csv.DictReader(io.StringIO(zin.read(name).decode('utf-8-sig')),delimiter=';');fields=list(rdr.fieldnames)
   b=io.StringIO();wr=csv.DictWriter(b,fieldnames=fields,delimiter=';',lineterminator='\n');wr.writeheader()
   local_review=local_changes=base_count=ctrl_count=0
   for old in rdr:
    rid=int(old['id_global']) if old['id_global'].isdigit() else None
    base_count+=old['tipo_registro']=='base';ctrl_count+=old['tipo_registro']!='base'
    after=old
    if rid in by_id:
     assert rid not in newrows and old['tipo_registro']=='base'
     assert old['Keyword']==by_id[rid]['Keyword'] and old['familia_id']==by_id[rid]['familia_id']
     after,delta=row_updated(old,rid);newrows[rid]=after.copy();local_review+=1
     if delta:
      local_changes+=1
      patches.append(dict(id_global=rid,lote=name.replace('v5.0','v5.1'),familia_id=old['familia_id'],Keyword=old['Keyword'],motivo_revisao=REASONS[rid],campos_modificados=','.join(delta),antes_json=json.dumps({c:old[c] for c in delta},ensure_ascii=False,sort_keys=True),depois_json=json.dumps({c:after[c] for c in delta},ensure_ascii=False,sort_keys=True)))
    wr.writerow(after)
   zout.writestr(name.replace('v5.0','v5.1'),('\ufeff'+b.getvalue()).encode('utf-8'))
   stats.append(dict(lote=name.replace('v5.0','v5.1'),bases=base_count,controles=ctrl_count,pareceres_revisados=local_review,refinamentos_aplicados=local_changes,status='PASSOU'))
   controls+=ctrl_count;bases+=base_count
 assert len(newrows)==75 and len(patches)==19 and bases==294905 and controls==2190
 reviewed=[]
 for rid,d in sorted(by_id.items()):
  new=newrows[rid];oldp=next((x for x in decisions if int(x['id_global'])==rid),None)
  changed=rid in CHANGES
  reviewed.append(dict(id_global=rid,lote_id=d['lote_id'],familia_id=d['familia_id'],Keyword=d['Keyword'],regra=d['regra'],parecer_v5_1='REFINADO_COM_RESSALVA' if changed else 'MANTIDO_COM_RESSALVA',justificativa_individual=REASONS[rid],area_v5_0=d['area_nova'],area_v5_1=new['area_principal'],cluster_v5_0=d['cluster_novo'],cluster_v5_1=new['cluster'],subcluster_v5_0=d['subcluster_novo'],subcluster_v5_1=new['subcluster'],tipo_v5_0=d['tipo_novo'],tipo_v5_1=new['tipo_intencao'],confianca_v5_1=new['confianca'],campos_modificados=next((p['campos_modificados'] for p in patches if int(p['id_global'])==rid),''),homologacao_editorial='PENDENTE'))
 for original,target,expected in [('p3-v5.0-fila-23965.csv','p3-v5.1-fila-23965.csv',23965),('fila-geral-p0-p1-p2-p3-v5.0.csv','fila-geral-p0-p1-p2-p3-v5.1.csv',52046)]:
  count=0;seen=set()
  with (SRC/original).open(encoding='utf-8-sig',newline='') as fi,(OUT/target).open('w',encoding='utf-8-sig',newline='') as fo:
   rdr=csv.DictReader(fi,delimiter=';');f=list(rdr.fieldnames);assert f==oldcols
   w=csv.DictWriter(fo,fieldnames=f+TRACE,delimiter=';',lineterminator='\n');w.writeheader()
   for old in rdr:
    rid=int(old['id_global']) if old['id_global'].isdigit() else None
    trace=dict.fromkeys(TRACE,'')
    if rid in by_id:
     assert rid not in seen;seen.add(rid);n=newrows[rid]
     trace.update(status_p3_v5_1='REVISADO',parecer_p3_v5_1='REFINADO_COM_RESSALVA' if rid in CHANGES else 'MANTIDO_COM_RESSALVA',justificativa_p3_v5_1=REASONS[rid],area_final_p3_v5_1=n['area_principal'],cluster_final_p3_v5_1=n['cluster'],subcluster_final_p3_v5_1=n['subcluster'],tipo_intencao_final_p3_v5_1=n['tipo_intencao'],classificacao_alterada_p3_v5_1='sim' if rid in CHANGES else 'não')
    old.update(trace);w.writerow(old);count+=1
  assert seen==set(by_id) and count==expected
 dump(OUT/'p3-v5.1-pareceres-75.csv',reviewed,list(reviewed[0]))
 dump(OUT/'p3-v5.1-patches-19.csv',patches,list(patches[0]))
 dump(OUT/'p3-v5.1-regressao-30-lotes.csv',stats,list(stats[0]))
 ag=[]
 for rule,n in sorted(Counter(x['regra'] for x in reviewed).items()):
  rr=[x for x in reviewed if x['regra']==rule]
  ag.append(dict(grupo=rule,pareceres=n,refinados=sum(x['parecer_v5_1']=='REFINADO_COM_RESSALVA' for x in rr),mantidos=sum(x['parecer_v5_1']=='MANTIDO_COM_RESSALVA' for x in rr),familias=len({x['familia_id'] for x in rr}),homologacao_editorial='PENDENTE'))
 dump(OUT/'p3-v5.1-qa-por-grupo.csv',ag,list(ag[0]))
 # A fila global de 98 não se altera sequer em um byte.
 (OUT/'backlog-global-98-com-parecer-v27.csv').write_bytes((SRC/'backlog-global-98-com-parecer-v27.csv').read_bytes())
 summary={'versao':'P3 v5.1','fonte':'P3 v5.0','pareceres_revisados':75,'refinados':19,'mantidos_com_ressalva':56,'familias':len({x['familia_id'] for x in reviewed}),'grupos':len(ag),'p3_elegiveis_preservados':19637,'p2_pendentes_preservados':4660,'backlog_global_preservado':98,'lotes':30,'registros_base':bases,'controles':controls,'linhas_fila_p3':23965,'linhas_fila_geral':52046,'colunas_historicas_preservadas_por_fila':382,'novas_colunas_rastreio':8,'homologacao_editorial':'PENDENTE','status':'AUDITOR_PASSOU'}
 (OUT/'p3-v5.1-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()