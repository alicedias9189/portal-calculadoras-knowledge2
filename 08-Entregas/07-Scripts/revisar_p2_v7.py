#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoria P2 v7 conservadora sobre pendências v6, sem alterar arquivos originais.
Uso: python3 revisar_p2_v7.py --raiz <diretorio-com-08-Entregas/P2-v6> --saida <pasta> [--preview]
Somente stdlib; cria lotes ZIP, trilhas CSV e SHA256. NUNCA replica decisões por família.
"""
import argparse,csv,io,json,re,hashlib,zipfile,unicodedata
from pathlib import Path
from collections import Counter,defaultdict
FIELDS=['area_principal','cluster','subcluster','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta','unidade_origem','unidade_destino','direcao_conversao']
NEW=['regra_p2_v7','status_p2_v7','justificativa_p2_v7','area_final_p2_v7','cluster_final_p2_v7','subcluster_final_p2_v7','tipo_intencao_final_p2_v7','unidade_origem_final_p2_v7','unidade_destino_final_p2_v7','classificacao_alterada_p2_v7']
def norm(s):return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFKD',(s or '').casefold()) if not unicodedata.combining(c))).strip()
def hit(t,p):return bool(re.search(p,t))
def D(rule,area,cluster,sub,intent,reason,conf='ALTA',src='',dst=''):
 return dict(rule=rule,area=area,cluster=cluster,sub=sub,intent=intent,reason=reason,conf=conf,src=src,dst=dst)

def decide(keyword):
 t=norm(keyword)
 # Explicit exclusions: high ambiguity, not resolved merely by neighboring family.
 if hit(t,r'^\d{1,2}\s+semanas?\s+e\s+\d\s+dias?$|^\d+(?:[.,]\d+)?\s*fahrenheit$|^fahrenheit\s+\d+(?:[.,]\d+)?$'):return None
 if hit(t,r'\bmilhas?\s+(?:em|para)\s+km\s+h\b|^\d{4,}$'):return None
 # CONVERTERS, strong exact patterns (domain-homogeneous)
 units=[
 (r'^(?:converter\s+|transformar\s+)?(?:mili\s*ohms?|mohms?)\s+(?:para|em|a)\s+ohms?$', 'resistencia_miliohm_ohm','Eletricidade e eletrônica','Resistência elétrica','mΩ','Ω'),
 (r'^kilovolts?\s+(?:para|em|a)\s+volts?$', 'tensao_kv_v','Eletricidade e eletrônica','Tensão elétrica','kV','V'),
 (r'^(?:converter\s+)?joules?\s+(?:para|em|a)\s+(?:electron\s+volts?|eletron\s+volts?|ev)$', 'energia_j_ev','Energia, potência e calor','Energia','J','eV'),
 (r'^(?:converter\s+)?kgfm\s+(?:para|em|a)\s+nm$', 'torque_kgfm_nm','Pressão e grandezas mecânicas','Torque','kgf·m','N·m'),
 (r'^(?:transformar\s+|converter\s+)?km3\s+(?:para|em|a)\s+m3$', 'volume_km3_m3','Volume e capacidade','Volume cúbico','km³','m³'),
 (r'^(?:converter\s+|transformar\s+)?gal[aã]o\s+ingl[eê]s\s+(?:para|em|a)\s+litros?$', 'galao_imperial_litro','Volume e capacidade','Galão imperial e litro','gal imperial','L'),
 (r'^(?:converter\s+)?graus?\s+(?:para|em|a)\s+segundos?\s+de\s+arco$', 'grau_segundo_arco','Ângulos','Graus e segundos de arco','°','arcsec'),
 (r'^(?:converter\s+)?(?:turns?|voltas?)\s+(?:para|em|a)\s+(?:graus?|rad(?:ianos?)?)$', 'voltas_angulo','Ângulos','Voltas, graus e radianos','turn','°/rad'),
 (r'^(?:converter\s+)?c\s+(?:para|em)\s+fahrenheit$', 'celsius_fahrenheit','Temperatura','Celsius e Fahrenheit','°C','°F'),
 (r'^(?:converter\s+)?(?:bin|binario)\s+(?:para|em|a)\s+(?:base\s*)?36$', 'base2_base36','Números e sistemas numéricos','Bases 2 e 36','base 2','base 36'),
 (r'^(?:converter\s+)?(?:base\s*)?36\s+(?:para|em|a)\s+(?:bin|binario)$', 'base36_base2','Números e sistemas numéricos','Bases 36 e 2','base 36','base 2'),
 (r'^(?:converter\s+)?(?:horas?)\s+(?:para|em)\s+microsegundos?$', 'horas_microsegundos','Tempo','Hora e microssegundo','h','µs'),
 (r'^(?:converter\s+)?(?:microsegundos?)\s+(?:para|em)\s+segundos?$', 'microsegundos_segundos','Tempo','Microssegundos e segundos','µs','s'),
 (r'^(?:converter\s+)?teaspoons?\s+(?:para|em)\s+ml$', 'culinaria_colher_cha_ml','Culinária e medidas contextuais','Colher de chá e mililitros','tsp','mL'),
 ]
 for pat,rule,cluster,sub,src,dst in units:
  if re.fullmatch(pat,t):
   if rule=='voltas_angulo':dst='rad' if hit(t,r'rad') else '°'
   return D(rule,'Conversores',cluster,sub,'conversão direta',f'Grandezas compatíveis e direção textual explícitas: {src} → {dst}.', 'RESSALVA' if rule in ('culinaria_colher_cha_ml','voltas_angulo') else 'ALTA',src,dst)
 # Conversions with explicit numerator/denominator or educational intent must be contextual.
 if hit(t,r'^(?:hex\s+bin|bin\s+hex|calculadora\s+hexa|numeros?\s+em\s+bases\s+diferentes)$'):
  return D('sistemas_bases_bi_hexa','Conversores','Números e sistemas numéricos','Bases binária e hexadecimal','conversão contextual','A consulta identifica sistemas numéricos, mas a direção e o valor podem precisar de seleção.','RESSALVA')
 if hit(t,r'^(?:numeros?\s+romanos?\s+(?:xi|vi|xii|todos)|algarismo\s+[ivxlcdm]|numero\s+roma|c\s+para\s+arabico)$'):
  return D('romanos_referencia_educacional','Matemática','Sistemas numéricos','Algarismos romanos','informacional','Consulta de representação romana específica ou referência; não presumir exercício de cálculo.','RESSALVA')
 # Financial calculations, simulations versus rates/advertisements
 if hit(t,r'^(?:calcular\s+)?dividend\s+yield$|^como\s+calcular\s+(?:o\s+)?dividend\s+yield$'):
  return D('calcular_dividend_yield','Finanças','Investimentos','Indicador Dividend Yield','cálculo contextual','Rendimento de dividendos/preço da ação exige ambos valores e período; não promete taxa futura.','RESSALVA')
 if hit(t,r'^(?:calcular\s+)?renda\s+passiva$|^quanto\s+preciso\s+investir\s+para\s+ter\s+\d+\s*milh[aã]o[s]?$'):
  return D('projecao_renda_passiva','Finanças','Investimentos','Renda passiva e meta de patrimônio','simulação/projeção','Requer valor, taxas, horizonte, tributos e hipóteses de risco; não garantia de rendimento.','RESSALVA')
 if hit(t,r'^(?:nubank\s+simulador|aplica[cç][aã]o\s+financeira\s+simulador|p[oó]s\s+fixado\s+simulador|quanto\s+\d+(?:\s+\d+)?\s*(?:mil|milh[oõ]es)?\s+rende\s+(?:no\s+)?nubank)$'):
  return D('simulacao_rendimento_produto','Finanças','Investimentos','Simulação de rendimentos','simulação/projeção','Produto ou instituição citada; taxa, custos e regras atuais devem ser informados.','RESSALVA')
 if hit(t,r'^(?:qual\s+(?:o\s+)?valor\s+da\s+poupanca\s+hoje|poupanca\s+banco\s+do\s+brasil\s+rendimento|banco\s+do\s+brasil\s+fundos\s+rentabilidade|qual\s+banco\s+rende\s+mais\s+dinheiro|qual\s+banco\s+o\s+dinheiro\s+rende\s+mais)$'):
  return D('informacao_rendimento_bancario','Finanças','Investimentos','Consulta de taxas e ofertas','informacional','Taxas ou comparações atuais; sem dados suficientes para simulação personalizada.','RESSALVA')
 if hit(t,r'^(?:calculo\s+)?tabela\s+sac$|^amortiza[cç][aã]o\s+tabela\s+price$'):
  return D('amortizacao_sac_price','Finanças','Crédito','Amortização de financiamentos','cálculo contextual','Requer principal, juros, prazo e regime de amortização.','RESSALVA')
 # Construction & material quantities, avoid guessing geometry
 if hit(t,r'^1000\s+blocos\s+faz\s+quantos\s+metros\s+quadrados$|^calculadora\s+(?:espa[cç]ador|nivelador)\s+cortag$|^como\s+medir\s+para\s+colocar\s+ceramicas$'):
  return D('revestimento_blocos_pecas','Construção','Materiais','Blocos, espaçadores e revestimentos','cálculo contextual','Área/cobertura depende do tamanho das peças e juntas, perdas e layout.','RESSALVA')
 if hit(t,r'^quantos\s+sacos\s+de\s+areia\s+tem\s+um\s+metro$'):
  return D('sacos_areia_por_volume','Construção','Materiais','Areia em sacos por volume','cálculo contextual','Volume do saco e densidade da areia são necessários; metro pode significar metro cúbico.','RESSALVA')
 if hit(t,r'^formula\s+blondel$'):
  return D('formula_blondel_escadas','Construção','Escadas','Proporção de degrau e espelho','informacional','Solicita fórmula de dimensionamento de escadas; verificar norma local e dimensões.','RESSALVA')
 # Transportation, gasoline calculations
 if hit(t,r'^(?:calculadora\s+(?:de\s+)?(?:consumo\s+)?gasolina(?:\s+(?:por\s+km|km))?|calculadora\s+(?:de\s+)?gasto\s+(?:de\s+)?combustivel|calcular\s+gasolina\s+e\s+km|como\s+calcular\s+quanto\s+(?:o\s+)?carro\s+faz\s+por\s+litro|como\s+calcular\s+quantos\s+quilometros\s+por\s+litro)$'):
  return D('calculadora_consumo_veiculo','Transportes','Combustíveis','Consumo e custo por distância','cálculo contextual','Necessita distância e consumo real (e preço para custo), não taxa universal.','RESSALVA')
 if hit(t,r'^(?:calcular\s+(?:quanto\s+)?(?:vou\s+)?gastar\s+de\s+gasolina|calcular\s+pedagio\s+e\s+gasolina|quanto\s+gasta\s+de\s+gasolina\s+e\s+pedagio)$'):
  return D('custo_viagem_combustivel','Transportes','Combustíveis','Custo de viagem e pedágio','cálculo contextual','Exige rota, distância, rendimento e preços; pedágio depende do trajeto.','RESSALVA')
 if hit(t,r'^(?:combustivel\s+aumento|diesel\s+aumenta|aumento\s+(?:do\s+)?(?:preco\s+)?combustiveis?\s+(?:hoje|para\s+a\s+semana)?|preco\s+do\s+boi\s+(?:hoje\s+)?(?:em\s+sao\s+paulo)?)$'):
  return D('consulta_preco_mercado','Fora de escopo','Mercado e cotações','Notícias e preços atuais','informacional','Consulta valor/notícia atual, não cálculo parametrizado.','RESSALVA')
 # Employment information or explicit calculation, keep legal caveats
 if hit(t,r'^(?:pedido\s+demissao\s+calculo|simular\s+acerto\s+de\s+trabalho|calcular\s+13\s+com\s+comissao|calculadora\s+hora\s+trabalhada\s+valor)$'):
  return D('calculo_trabalhista_condicional','Trabalhista','Rescisão e jornada','Verbas e remuneração de trabalho','cálculo contextual','Requer salário, contrato, datas e regras legais vigentes; resultados dependem de circunstâncias.','RESSALVA')
 if hit(t,r'^(?:se\s+faltar\s+na\s+sexta\s+desconta\s+quantos\s+dias|hora\s+de\s+almoco\s+e\s+remunerada|faltas\s+justificadas\s+podem\s+ser\s+descontadas|demissao\s+indireta\s+o\s+que\s+e|escala\s+24x72\s+como\s+funciona|horario\s+12x36\s+como\s+funciona)$'):
  return D('direito_trabalhista_info','Trabalhista','Direitos do trabalhador','Dúvidas legais e jornada','informacional','Pergunta sobre regras trabalhistas; não calcular sem fatos contratuais e legislação.','RESSALVA')
 # Lists, guides, product names
 if hit(t,r'^(?:lista\s+de\s+despesas\s+mensais|dicas\s+para\s+gastar\s+menos|financas\s+pessoais\s+como\s+organizar|como\s+controlar\s+as\s+contas\s+(?:pessoais|domesticas)|objetivo\s+de\s+economia)$'):
  return D('planejamento_financeiro_info','Finanças','Orçamento pessoal','Organização de despesas e poupança','informacional','Busca orientação/organização, não cálculo com inputs definidos.','ALTA')
 if hit(t,r'^(?:como\s+faco\s+para\s+acessar\s+minha\s+conta\s+da\s+caixa|qual\s+o\s+horario\s+de\s+funcionamento\s+dos\s+bancos|qual\s+o\s+horario\s+de\s+funcionamento\s+da\s+b3|caixa\s+proposta\s+habitacional|caixa\s+simulador\s+veiculo|consorcio\s+yamaha\s+simulador)$'):
  return D('consulta_servico_instituicao','Fora de escopo','Serviços e portais','Serviços de empresas/instituições','navegacional/transacional','Busca por serviço, simulação oferecida por empresa ou funcionamento; não calculadora genérica.','RESSALVA')
 if hit(t,r'^(?:hora\s+de\s+almoco|contas?\s+para\s+pagar|contas\s+pagar)$'):
  return None # ambíguas, não inferir significado bancário ou temporal
 if hit(t,r'^(?:numeros?\s+romanos?\s+todos|o\s+que\s+sao\s+numeros\s+romanos|algarismos?\s+e\s+numerais|os\s+numeros\s+ordinais|o\s+que\s+sao\s+logaritmos|regras\s+da\s+exponenciacao|capitalizacao\s+composta\s+formula|permutacoes\s+com\s+elementos\s+repetidos|metodo\s+de\s+substituicao)$'):
  return D('referencia_conceito_matematico','Matemática','Educação matemática','Conceitos e fórmulas','informacional','Consulta por explicação/conceito, não parâmetros para solver.','ALTA')
 if hit(t,r'^(?:calc(?:ule|ular)?\s+os\s+seguintes\s+logaritmos|resolver\s+problemas\s+de\s+matematica\s+online|fatorador\s+online)$'):
  return D('ferramenta_matematica_exercicio','Matemática','Ferramentas matemáticas','Álgebra e combinatória','cálculo contextual','Exercício/operação matemático identificável; faltam argumentos concretos.','RESSALVA')
 return None

def readcsv(z,name):
 with z.open(name) as b:return list(csv.DictReader(io.TextIOWrapper(b,encoding='utf-8-sig',newline=''),delimiter=';'))
def writecsv(z,name,rows,fields):
 with z.open(name,'w',force_zip64=True) as b:
  f=io.TextIOWrapper(b,encoding='utf-8-sig',newline='');w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows);f.flush();f.detach()
def sha(path):
 h=hashlib.sha256();
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()
def replace(d):
 return {'area_principal':d['area'],'cluster':d['cluster'],'subcluster':d['sub'],'tipo_intencao':d['intent'],'intencao_principal':d['intent'],'confianca':'alta' if d['conf']=='ALTA' else 'média','revisao_manual':'não' if d['conf']=='ALTA' else 'sim','justificativa_curta':f"P2-v7 {d['rule']}: {d['reason']}",'unidade_origem':d['src'],'unidade_destino':d['dst'],'direcao_conversao':f"{d['src']}->{d['dst']}" if d['src'] and d['dst'] else ''}
def main():
 a=argparse.ArgumentParser();a.add_argument('--raiz',type=Path,default=Path(__file__).resolve().parents[1]);a.add_argument('--saida',type=Path);a.add_argument('--preview',action='store_true');args=a.parse_args()
 root=args.raiz;out=args.saida or root/'out'; az=zipfile.ZipFile(root/'08-Entregas/P2-v6/auditoria-p2-v6-csv-integral.zip'); bz=zipfile.ZipFile(root/'08-Entregas/P2-v6/lotes-001-a-030-p0-p1-p2-v6.zip')
 pending=readcsv(az,'p2-v6-pendencias-restantes.csv'); assert len(pending)==4761
 chosen={};rules=Counter();byfam=Counter();examples=defaultdict(list)
 for r in pending:
  d=decide(r['Keyword'])
  if d:
   k=r['id_global']; assert k not in chosen;chosen[k]=d;rules[d['rule']]+=1;byfam[r['familia_id']]+=1
   if len(examples[d['rule']])<500:examples[d['rule']].append(r['Keyword'])
 print('PENDENTES',len(pending),'CANDIDATOS',len(chosen),'REGRAS',dict(rules),flush=True)
 for name,cnt in rules.most_common(): print('RULE',name,cnt,' | '.join(examples[name][:80]),flush=True)
 if args.preview:return
 out.mkdir(parents=True,exist_ok=True)
 decisions=readcsv(az,'p2-v6-decisoes-25050.csv');queue=readcsv(az,'p2-v6-fila-geral.csv');assert len(decisions)==25050 and len(set(x['id_global'] for x in decisions))==25050
 pendids={r['id_global'] for r in pending};assert set(chosen).issubset(pendids)
 patchlist=[];mapped={};families=defaultdict(list)
 for r in pending:families[r['familia_id']].append(r)
 for orig in decisions:
  r=dict(orig);k=r['id_global'];d=chosen.get(k)
  if d:
   patchlist.append({'id_global':k,'lote':r['lote'],'familia_id':r['familia_id'],'Keyword':r['Keyword'],'regra':d['rule'],'status':'RESOLVIDO' if d['conf']=='ALTA' else 'COM_RESSALVA','antes':'','depois':json.dumps(replace(d),ensure_ascii=False),'justificativa':d['reason']})
  r.update({'regra_p2_v7':d['rule'] if d else '', 'status_p2_v7':('RESOLVIDO' if d['conf']=='ALTA' else 'COM_RESSALVA') if d else ('PENDENTE_CONTEXTUAL' if k in pendids else 'MANTIDO_P2_V6'), 'justificativa_p2_v7':d['reason'] if d else '', 'area_final_p2_v7':d['area'] if d else r.get('area_final_p2_v6',''),'cluster_final_p2_v7':d['cluster'] if d else r.get('cluster_final_p2_v6',''),'subcluster_final_p2_v7':d['sub'] if d else r.get('subcluster_final_p2_v6',''),'tipo_intencao_final_p2_v7':d['intent'] if d else r.get('tipo_intencao_final_p2_v6',''),'unidade_origem_final_p2_v7':d['src'] if d else r.get('unidade_origem_final_p2_v6',''),'unidade_destino_final_p2_v7':d['dst'] if d else r.get('unidade_destino_final_p2_v6',''),'classificacao_alterada_p2_v7':'sim' if d else 'não'})
  mapped[k]=r
 dec=[mapped[x['id_global']] for x in decisions];rem=[mapped[x['id_global']] for x in pending if x['id_global'] not in chosen]
 famreport=[]
 for fid,ll in families.items():
  chosen_f=[x['id_global'] for x in ll if x['id_global'] in chosen];rem_f=[x['Keyword'] for x in ll if x['id_global'] not in chosen];rs=Counter(chosen[x]['rule'] for x in chosen_f)
  famreport.append({'familia_id':fid,'pendentes_v6':len(ll),'reclassificadas_v7':len(chosen_f),'ainda_pendentes':len(rem_f),'regras':' ; '.join(f'{k}:{v}' for k,v in rs.most_common()),'exemplos_pendentes':' | '.join(rem_f[:6]),'metodo':'Avaliação individual, sem propagar por ID de família'})
 famreport.sort(key=lambda x:(-x['ainda_pendentes'],x['familia_id']))
 patchbyid={x['id_global']:x for x in patchlist};qa=[];seen=set();base=control=modified=0
 loteszip=out/'lotes-001-a-030-p0-p1-p2-v7.zip'
 with zipfile.ZipFile(loteszip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  for name in sorted(n for n in bz.namelist() if n.endswith('.csv')):
   rows=readcsv(bz,name); cols=list(rows[0]);b=c=m=0
   for r in rows:
    before=dict(r);k=r['id_global'];kind=r['tipo_registro']
    if kind=='base':
     b+=1;assert k not in seen;seen.add(k)
     if k in chosen:
      patchbyid[k]['antes']=json.dumps({f:before.get(f,'') for f in FIELDS},ensure_ascii=False)
      r.update(replace(chosen[k]));m+=1
    elif kind=='controle':c+=1
    assert all(r[f]==before[f] for f in cols if f not in FIELDS)
    if kind!='base' or k not in chosen:assert r==before
   base+=b;control+=c;modified+=m;qa.append({'lote':name.split('/')[-1][:8],'base':b,'controles':c,'alteracoes':m,'integridade':'PASSOU'})
   writecsv(zout,name.replace('-v6.csv','-v7.csv'),rows,cols)
 assert len(qa)==30 and base==294905 and control==2190 and modified==len(chosen)
 updatedqueue=[]
 for row in queue:
  x=dict(row);k=x['id_global'];d=chosen.get(k)
  if d:
   for field,value in replace(d).items():
    if field in x:x[field]=value
  for field in NEW:x[field]=mapped.get(k,{}).get(field,'')
  updatedqueue.append(x)
 audit=out/'auditoria-p2-v7-csv-integral.zip'
 with zipfile.ZipFile(audit,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,rows in [('p2-v7-decisoes-25050.csv',dec),('p2-v7-pendencias-restantes.csv',rem),('p2-v7-patches.csv',patchlist),('p2-v7-fila-geral.csv',updatedqueue),('p2-v7-qa-regressao-30-lotes.csv',qa),('p2-v7-familias-analisadas.csv',famreport)]:
   if rows:writecsv(z,name,rows,list(rows[0]))
 sm={'versao':'P2-v7','universo_p2':len(dec),'pendencias_entrada_v6':len(pending),'reclassificadas':len(chosen),'sem_ressalva':sum(d['conf']=='ALTA' for d in chosen.values()),'com_ressalva':sum(d['conf']=='RESSALVA' for d in chosen.values()),'pendencias_restantes':len(rem),'familias_com_patches':len(byfam),'familias_com_pendencias':len(families),'registros_base':base,'controles':control,'lotes':len(qa),'regras':dict(rules),'exemplos':{k:v[:20] for k,v in examples.items()},'sha256_lotes':sha(loteszip),'sha256_auditoria':sha(audit)}
 (out/'resumo-p2-v7.json').write_text(json.dumps(sm,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('RESULTADO',json.dumps({k:v for k,v in sm.items() if k not in ('exemplos','regras')},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
