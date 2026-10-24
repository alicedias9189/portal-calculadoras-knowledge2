#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 v5: revisão conservadora de pendências remanescentes da P2 v4.
Uso: python3 07-Scripts/revisar_p2_v5.py --raiz . [--preview]
Usa somente stdlib; não sobrescreve fontes; gera lotes v5, auditoria e QA.
"""
import argparse,csv,io,zipfile,json,re,hashlib,unicodedata
from pathlib import Path
from collections import Counter,defaultdict
BASE_FIELDS=['area_principal','cluster','subcluster','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta','unidade_origem','unidade_destino','direcao_conversao']
FIELDS_NEW=['regra_p2_v5','status_p2_v5','justificativa_p2_v5','area_final_p2_v5','cluster_final_p2_v5','subcluster_final_p2_v5','tipo_intencao_final_p2_v5','unidade_origem_final_p2_v5','unidade_destino_final_p2_v5','classificacao_alterada_p2_v5']

def norm(s):
 return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFKD',(s or '').casefold()) if not unicodedata.combining(c))).strip()
def found(t,p):return re.search(p,t) is not None
def D(rule,area,cluster,sub,intent,reason,conf='ALTA',src='',dst=''):
 return {'regra':rule,'area':area,'cluster':cluster,'sub':sub,'intent':intent,'reason':reason,'conf':conf,'src':src,'dst':dst}

BASE_MAP={'binario':'base2','hexadecimal':'base16','octal':'base8','decimal':'base10'}
BASE_PATTERN=r'(binari[oa]|hexadecimal|octal|decimal)'

def decide(keyword):
 t=norm(keyword)
 # Famílias deliberadamente inconclusivas: contexto de gravidez e destino ausente.
 if found(t,r'^\d{1,2}\s+semanas?\s+e\s+\d\s+dias?$'):return None
 if found(t,r'^\d+(?:[.,]\d+)?\s*fahrenheit$'):return None
 if found(t,r'\b(?:milhas?\s+(?:em|para)\s+km\s+h|milhas?\s+(?:em|para)\s+km\s*/\s*h)\b') and not found(t,r'milhas?\s+por\s+hora'):return None
 # Navegação e produtos bem definidos: não inferir que loja, marca ou aparelho é calculadora.
 if found(t,r'\b(?:casio\s*(?:fx|991)|(?:fx|991)\s*[- ]?\s*991|casio\s+fx|calculadoras?\s+hp\s+antigas)\b'):
  intent='informacional' if found(t,r'\b(?:funcoes|como\s+usar|qr\s*code|e\s+boa|numeros\s+complexos|manual)\b') else 'navegacional/transacional'
  return D('produto_calculadora_fisica','Fora de escopo','Comércio e produtos','Calculadoras físicas',intent,'Busca sobre modelo de calculadora física, não execução de um cálculo no portal.')
 if found(t,r'\b(?:conversor|transformador|adaptador)\s+(?:de\s+)?voltagem\b') and found(t,r'\b(?:110|127|220|bivolt|secador|1500w|comprar|preco)\b'):
  return D('equipamento_transformador','Fora de escopo','Comércio e produtos','Transformadores elétricos','navegacional/transacional','Consulta de aparelho de transformação de tensão, não conversão numérica de volts.')
 if found(t,r'\b(?:conama\s*(?:no\s*)?237|resolucao\s+(?:conama\s*)?237)\b'):
  return D('norma_ambiental','Fora de escopo','Legislação','Normas ambientais','informacional','Referência a resolução legal, sem operação numérica.')
 if found(t,r'\b(?:piso\s+salarial|o\s+que\s+e\s+demissao\s+indireta|quais\s+direitos\s+eu\s+tenho\s+se\s+pedir\s+demissao|se\s+eu\s+pedir\s+demissao\s+recebo\s+seguro)\b'):
  return D('direito_trabalhista_informativo','Trabalhista','Direitos trabalhistas','Regras e direitos','informacional','Consulta jurídica/informativa, não cálculo sem parâmetros.',conf='RESSALVA')
 if found(t,r'\b(?:simulador|simulacao|simular)\b') and found(t,r'\b(?:consorcio|credito\s+pessoal|habitacional|casa\s+propria|credito)\b'):
  if found(t,r'\b(?:bradesco|bb|banco\s+do\s+brasil|caixa|sicredi|sicoob|santander|financeira\s+omni|crefisa|w8)\b'):
   return D('simulador_instituicao','Finanças','Crédito e financiamento','Simulador institucional','navegacional/transacional','Busca por simulador de instituição, sujeito a ofertas/condições próprias; não estimar parâmetros institucionais.',conf='RESSALVA')
 # Matemática, tabelas e tutoriais: informação distinta de motor de cálculo.
 if found(t,r'\b(?:logaritm[oa]s?|logaritmic[ao]s?)\b') and found(t,r'\b(?:definicao|formulas?|propriedades?|propriedade|mudanca\s+de\s+base|base|resumo|exercicios?|wikipedia|o\s+que\s+e|mantissa|produto|natural|decimal)\b') and not found(t,r'\b(?:calcular|calculadora|online|calcule|resolv[ae])\b'):
  return D('referencia_logaritmos','Matemática','Logaritmos','Conceitos e propriedades','informacional','Busca de teoria/propriedades de logaritmos, sem operandos para cálculo.')
 if found(t,r'\b(?:regra|metodo)\s+(?:de\s+)?cramer\b') and not found(t,r'\b(?:calculadora|resolver|calcular\s+online)\b'):
  return D('metodo_cramer','Matemática','Álgebra linear','Regra de Cramer','informacional','Consulta do método, exemplos ou exercícios, sem sistema de equações fornecido.')
 if found(t,r'\b(?:razoes?\s+e\s+proporcoes?|n[uú]meros?\s+racionais?)\b') and found(t,r'\b(?:exercicios?|atividades?|exemplos?|problemas?|6\s*ano|7\s*ano|5\s*ano|4\s*ano|definicao)\b'):
  return D('conteudo_matematico_escolar','Matemática','Educação matemática','Exercícios e conceitos','informacional','Termos de ensino/exercícios, não pedido de cálculo específico.')
 # Conversões de bases numéricas com pares explícitos.
 base_m=re.search(r'\b'+BASE_PATTERN+r'\s+(?:para|em|to)\s+'+BASE_PATTERN+r'\b',t)
 if base_m and base_m.group(1)!=base_m.group(2) and not found(t,r'\b(?:como\s+fazer|exercicios?|explicacao|apostila|teoria)\b'):
  a,b=BASE_MAP.get(base_m.group(1).replace('binaria','binario')),BASE_MAP.get(base_m.group(2).replace('binaria','binario'))
  if a and b:
   return D('bases_numericas_direcao','Conversores','Números e sistemas numéricos','Conversão entre bases','conversão direta','Duas bases numéricas com direção explícita.',src=a,dst=b)
 explicit_m=re.search(r'\bbase\s+(2|8|10|16)\s+(?:para|em)\s+base\s+(2|8|10|16)\b',t)
 if explicit_m and explicit_m.group(1)!=explicit_m.group(2):
  return D('bases_numericas_numericas','Conversores','Números e sistemas numéricos','Conversão entre bases','conversão direta','Bases especificadas por números com direção.',src='base'+explicit_m.group(1),dst='base'+explicit_m.group(2))
 if found(t,r'\b(?:romano|romana|romanos)\b') and found(t,r'^\d+\s+em\s+(?:letra\s+)?roman[ao]s?$'):
  return D('decimal_para_romano','Conversores','Números e sistemas numéricos','Decimal para romano','conversão direta','Valor arábico e destino romano explícitos.',src='base10',dst='romano')
 if found(t,r'\b(?:tabela|numeros?\s+de\s+1\s+a|tabuada\s+romana|algarismo\s+romana)\b') and found(t,r'\b(?:romano|romana|romanos)\b'):
  return D('tabela_romanos','Conversores','Números e sistemas numéricos','Tabela de algarismos romanos','tabela/referência','Busca por tabela/referência romana, sem operação específica.')
 # Converter Fahrenheit isolado NÃO, mas pares com sentido e unidades inequívocos SIM.
 temp=re.search(r'\b(celsius|fahrenheit|kelvin)\s+(?:para|em)\s+(celsius|fahrenheit|kelvin|k)\b',t)
 if temp and temp.group(1)!=temp.group(2):
  conv={'celsius':'C','fahrenheit':'F','kelvin':'K','k':'K'}
  return D('temperatura_par_explicito','Conversores','Temperatura','Conversão de temperatura','conversão direta','Origem e destino térmicos indicados.',src=conv[temp.group(1)],dst=conv[temp.group(2)])
 if found(t,r'\b(?:milhas?\s+por\s+hora)\s+(?:em|para)\s+(?:km\s+por\s+hora|km\s*/\s*h)\b'):
  return D('velocidade_mph_kmh','Conversores','Velocidade','Milhas/h para km/h','conversão direta','As duas unidades de velocidade estão explícitas.',src='mi/h',dst='km/h')
 if found(t,r'\b(?:oncas?\s+fluidas?)\s+(?:para|em)\s+ml\b'):
  return D('volume_oncas_fluidas','Conversores','Volume','Onça fluida para mililitro','conversão contextual','Onça fluida é volume, mas padrão EUA/imperial requer seleção.',conf='RESSALVA')
 if found(t,r'\b(?:libras?\s+(?:em|para)\s+(?:psi|bar)|(?:psi|bar)\s+(?:em|para)\s+libras?)\b'):
  return D('libra_pressao_ambigua','Conversores','Pressão','Conversão de pressão','conversão contextual','Libra pode significar lbf/in², unidade de força ou massa; confirmar sentido técnico e escala.',conf='RESSALVA')
 if found(t,r'\b(?:n\s*m|newton\s*metro)\s+(?:em|para)\s+(?:lb\s*ft|ft\s*lb)\b'):
  return D('torque_nm_lbft','Conversores','Torque','Torque newton-metro para libra-pé','conversão direta','Ambas as unidades de torque identificadas, sem confundir comprimento.',src='N·m',dst='lbf·ft')
 if found(t,r'\b(?:converter\s+)?(?:psig)\s+(?:para|em)\s+bar\b'):
  return D('pressao_psig_bar','Conversores','Pressão','Pressão manométrica','conversão contextual','PSIG é manométrico; bar pode ser absoluto ou manométrico. Exigir referência.',conf='RESSALVA')
 if found(t,r'\b(?:\d+(?:[.,]\d+)?\s*)?a\s+(?:para|em)\s+ma\b') and not found(t,r'\b(?:telefone|celular|galaxy|samsung|iphone|serie|modelo)\b'):
  return D('ampere_miliampere','Conversores','Eletricidade e eletrônica','Corrente elétrica','conversão direta','Notação A para mA com preposição, mesma dimensão.',src='A',dst='mA')
 if found(t,r'\b(?:\d+(?:[.,]\d+)?\s*)?g\s+(?:para|em)\s+mg\b'):
  return D('grama_miligrama','Conversores','Massa e peso','Gramas para miligramas','conversão direta','Massa, origem e destino explícitos.',src='g',dst='mg')
 # Financeiro: discriminar institucional, cálculo e informação.
 if found(t,r'\b(?:quanto\s+rende|rende\s+quanto|rendimento\s+(?:do|da)\s+(?:mercado\s+pago|banco\s+inter)|qual\s+o\s+rendimento\s+do\s+mercado\s+pago)\b') and found(t,r'\b(?:mercado\s+pago|banco\s+inter)\b'):
  return D('rendimento_conta_digital','Finanças','Investimentos','Rendimento de conta digital','cálculo contextual','Estimativa de rendimento depende de taxa atual, valor, prazo, regras da conta e tributos.',conf='RESSALVA')
 if found(t,r'\b(?:calcular\s+valor\s+futuro|valor\s+futuro\s+calculadora)\b'):
  return D('valor_futuro_financeiro','Finanças','Matemática financeira','Valor futuro','cálculo contextual','Valor futuro exige capital, taxa, período e convenção de capitalização.',conf='RESSALVA')
 if found(t,r'\b(?:calculadora\s+(?:de\s+)?poupanca|simulador\s+(?:de\s+)?aplicacao\s+financeira)\b'):
  return D('simulador_aplicacao','Finanças','Investimentos','Simulação de aplicação','cálculo contextual','Valor aportado, prazo, rentabilidade e impostos devem ser definidos.',conf='RESSALVA')
 if found(t,r'\b(?:preco\s+de\s+custo\s+e\s+preco\s+de\s+venda|preco\s+de\s+venda\s+e\s+preco\s+de\s+custo|calcular\s+(?:o\s+)?preco\s+de\s+venda|preco\s+de\s+venda\s+calculadora)\b'):
  return D('preco_venda_custo','Finanças','Gestão comercial','Preço de venda e margem','cálculo contextual','Preço de venda requer custo, margem/markup, despesas e tributos.',conf='RESSALVA')
 if found(t,r'\b(?:pedir\s+(?:a\s+)?conta|pedido\s+de\s+demissao)\b') and found(t,r'\b(?:calculadora|calcular|calculo|quanto|multa|desconto|valor)\b'):
  return D('calculo_pedido_demissao','Trabalhista','Rescisão','Pedido de demissão','cálculo contextual','Rescisão depende de salários, férias, aviso prévio, períodos e legislação.',conf='RESSALVA')
 if found(t,r'\b(?:calcular\s+desconto\s+de\s+falta|falta\s+(?:na\s+(?:segunda|sexta|sabado)|no\s+trabalho|injustificada)\s+desconta)\b'):
  return D('desconto_faltas','Trabalhista','Folha e descontos','Desconto de faltas','cálculo contextual','Desconto depende da jornada, remuneração, DSR e legislação aplicável.',conf='RESSALVA')
 # Cálculos de construção expressos sem mera pesquisa de produtos.
 if found(t,r'\b(?:calculadora\s+(?:para\s+)?telha(?:do)?|calculadora\s+de\s+obra|calculadora\s+metro\s+cubico|calculo\s+de\s+argamassa|quantidade\s+de\s+argamassa\s+para\s+assentar)\b'):
  return D('materiais_construcao_calculo','Construção','Materiais','Estimativa de materiais','cálculo contextual','Exige medidas, traço, espessura, dimensões e perdas; não assumir rendimento fixo.',conf='RESSALVA')
 if found(t,r'\b(?:blocos?\s+de\s+concreto\s+por\s+m2|quantidade\s+de\s+tijolos?\s+por\s+m2)\b'):
  return D('quantidade_blocos_m2','Construção','Alvenaria','Blocos por área','cálculo contextual','Depende das dimensões dos blocos e espessura de juntas.',conf='RESSALVA')
 # Sites, compras, fricções comerciais sem necessidade de calcular.
 if found(t,r'\b(?:moedas?\s+(?:de\s+\d+\s+real\s+)?raras?|moeda\s+invertida|moeda\s+antiga)\b') and found(t,r'\b(?:valor|preco|venda|raras?|quanto\s+vale)\b'):
  return D('numismatica','Fora de escopo','Numismática','Avaliação de moedas colecionáveis','informacional','Valor numismático não é taxa de câmbio nem conversão monetária.')
 if found(t,r'\b(?:comprar|compra|venda|trocar|troca)\s+(?:de\s+)?moedas?\s+estrangeiras?\b'):
  return D('compra_moeda_estrangeira','Finanças','Câmbio','Compra e venda de moeda','navegacional/transacional','Intenção de transação comercial, não mera conversão matemática.',conf='RESSALVA')
 if found(t,r'\b(?:como\s+poupar\s+dinheiro|como\s+(?:fazer|faco|posso|podemos)\s+para\s+poupar\s+dinheiro)\b'):
  return D('educacao_financeira','Finanças','Educação financeira','Hábitos de poupança','informacional','Busca por orientação de orçamento e economia, não operação definida.')
 if found(t,r'\b(?:quanto\s+custa|quanto\s+gasta|quanto\s+eu\s+gastaria|quanto\s+gastaria|quanto\s+gasta\s+de\s+material)\b') and found(t,r'\b(?:construir|construcao|telhado|sobrado|comodos?|alicerce|m2\s+para\s+construir)\b') and not found(t,r'\b(?:engenheiro|arquiteto|consultoria|planta)\b'):
  return D('orcamento_construcao','Construção','Orçamento de obras','Estimativa de custos','cálculo contextual','Preço depende de localidade, área, padrão construtivo, materiais e mão de obra; não supor valores.',conf='RESSALVA')
 if found(t,r'\b(?:preco|valor|cotacao|hoje)\b') and found(t,r'\b(?:arroba|vaca\s+gorda|bezerro|boi\s+(?:vivo|gordo)|nelore)\b') and not found(t,r'\b(?:leroy|brinquedo|restaurante|piada)\b'):
  return D('cotacao_agropecuaria','Fora de escopo','Mercado agropecuário','Cotações de gado','informacional','Preço agropecuário depende da praça e data; não representa conversão de unidade.',conf='RESSALVA')
 if found(t,r'\b(?:cruzados?|cruzeiros?|cruzado\s+novo)\b') and found(t,r'\b(?:reais?|conversao|converter|equivalente|calculadora)\b'):
  return D('moedas_historicas','Finanças','Histórico monetário','Conversão de moedas históricas','cálculo contextual','Reformas monetárias, ano de referência e possível correção inflacionária devem ser definidos; não aplicar cotação corrente.',conf='RESSALVA')
 if found(t,r'\b(?:somar|subtrair|calcular|calculo|calculadora)\b') and found(t,r'\b(?:horas?|minutos?|segundos?|datas?)\b') and not found(t,r'\b(?:trabalhad[oa]s?|ponto|folha|salario|professor|aula|remuneracao|reais?|r\$|desconto|km\s*por\s*hora|kilowatt|kwh|noturna|por\s*km|km\s*por|horas?\s+semanais|horas?\s+semanal|horas?\s+semanalmente|semana\s+trabalhad)\b'):
  return D('calculadora_duracao','Datas','Cálculos de tempo','Durações, somas e diferenças','cálculo contextual','Operação temporal identificável; pedir horários/datas e fuso quando necessário.',conf='RESSALVA')
 if found(t,r'\b(?:pdf\s+(?:em|para)\s+pdf\s*a|(?:converter|transformar)\s+(?:um\s+)?pdf\s+(?:em|para)\s+pdf\s*a)\b'):
  return D('conversao_pdfa','Conversores','Arquivos e documentos','PDF para PDF/A','conversão de arquivo/mídia','PDF/A é formato de preservação, diferente de PDF genérico; requer validação das características do documento.',conf='RESSALVA',src='PDF',dst='PDF/A')
 if found(t,r'\b(?:como\s+)?(?:converter|transformar)\s+(?:uma?\s+)?(?:imagem|foto)\s+(?:em|para)\s+(?:texto|word|excel)\b'):
  return D('imagem_ocr_documento','Conversores','Arquivos e documentos','Imagem para texto/documento','conversão de arquivo/mídia','Requer OCR e reconstrução opcional do layout; exatidão não garantida.',conf='RESSALVA')
 if found(t,r'\b(?:regra\s+de\s+cramer|logaritmo|funcao\s+quadratica|area\s+em\s+metros\s+quadrados?)\b') and found(t,r'\b(?:como\s+calcular|formula|f[oó]rmula)\b'):
  return D('tutorial_matematico','Matemática','Educação matemática','Métodos e fórmulas','informacional','Consulta sobre procedimento/fórmula, não operação com dados informados.')
 if found(t,r'\b(?:simulacao\s+(?:de\s+)?credito|simulador\s+(?:de\s+)?credito\s+pessoal)\b') and not found(t,r'\b(?:cartao\s+presente|video|tutorial)\b'):
  return D('simulacao_credito','Finanças','Crédito e financiamento','Simulação de empréstimo','cálculo contextual','Parcelas e CET requerem valor, prazo, encargos e taxa real da oferta.',conf='RESSALVA')
 if found(t,r'\b(?:qual\s+valor|valor|cotacao|preco)\b') and found(t,r'\bpesos?\b') and found(t,r'\breais?\b') and not found(t,r'\b(?:peso\s+corporal|peso\s+crian[ct]a|quilos|gramas|massa)\b'):
  return D('peso_real_indeterminado','Finanças','Câmbio','Cotação peso–real','conversão contextual','Moeda peso sem país pode corresponder a múltiplas moedas; exigir país e direção.',conf='RESSALVA')
 if found(t,r'\b(?:conversor|converter)\s+(?:de\s+)?(?:rpm\s+(?:para|em)\s+hz|hz\s+(?:para|em)\s+rpm)\b') or found(t,r'\b(?:hz\s+(?:para|em)\s+rpm|frequencia\s+em\s+hz\s+para\s+rpm)\b'):
  return D('frequencia_rpm_condicional','Conversores','Frequência e rotação','Hz e RPM','conversão contextual','Hz pode ser ciclo elétrico, não rotação; requer número de eventos/ciclos por volta.',conf='RESSALVA')
 if found(t,r'\b(?:numero|numeral)\s+romano\s+[xivlcdm]+\b') or found(t,r'^(?:[xivlcdm])\s+(?:letra\s+)?romano(?:\s+numero)?$'):
  return D('romanos_caracteres','Conversores','Números e sistemas numéricos','Algarismos romanos','tabela/referência','Consulta pelo significado de algarismo romano, sem quantidade adicional.')
 return None

def readcsv(z,n):
 return list(csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig',newline=''),delimiter=';'))
def writecsv(z,name,rows,fields):
 with z.open(name,'w',force_zip64=True) as b:
  f=io.TextIOWrapper(b,encoding='utf-8-sig',newline='')
  w=csv.DictWriter(f,delimiter=';',fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows);f.flush();f.detach()
def shaf(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('--raiz',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--saida',type=Path);p.add_argument('--preview',action='store_true');args=p.parse_args()
 root=args.raiz; out=args.saida or root/'saida-p2-v5'
 az=zipfile.ZipFile(root/'08-Entregas/P2-v4/auditoria-p2-v4-csv-integral.zip')
 bz=zipfile.ZipFile(root/'08-Entregas/P2-v4/lotes-001-a-030-p0-p1-p2-v4.zip')
 pending=readcsv(az,'p2-v4-pendencias-restantes.csv');assert len(pending)==5562
 chosen={};rules=Counter();example=defaultdict(list);families=defaultdict(list)
 for r in pending:
  d=decide(r['Keyword']); families[r['familia_id']].append(r)
  if d:
   chosen[r['id_global']]=d;rules[d['regra']]+=1
   if len(example[d['regra']])<250:example[d['regra']].append(r['Keyword'])
 print('PENDENTES',len(pending),'CANDIDATOS',len(chosen),'REGRAS',dict(rules),flush=True)
 for k,v in example.items():print('RULE',k,'COUNT',rules[k], '\n  '+' | '.join(v[:24]),flush=True)
 if args.preview:return
 out.mkdir(parents=True,exist_ok=True)
 decisions=readcsv(az,'p2-v4-decisoes-25050.csv');queue=readcsv(az,'p2-v4-fila-geral.csv')
 assert len(decisions)==25050 and len({x['id_global'] for x in decisions})==25050
 assert set(chosen).issubset({x['id_global'] for x in pending})
 pend_ids={x['id_global'] for x in pending};allmap={};patches=[];byfam=Counter();counts=Counter()
 def replace(d):
  return {'area_principal':d['area'],'cluster':d['cluster'],'subcluster':d['sub'],'tipo_intencao':d['intent'],'intencao_principal':d['intent'],'confianca':'alta' if d['conf']=='ALTA' else 'média','revisao_manual':'não' if d['conf']=='ALTA' else 'sim','justificativa_curta':f"P2-v5 {d['regra']}: {d['reason']}",'unidade_origem':d['src'],'unidade_destino':d['dst'],'direcao_conversao':d['src']+'->'+d['dst'] if d['src'] and d['dst'] else ''}
 for old in decisions:
  row=dict(old);key=row['id_global']; d=chosen.get(key)
  if d:
   before={k:row.get(k,'') for k in BASE_FIELDS};after=replace(d);patches.append({'id_global':key,'lote':row['lote'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra':d['regra'],'status':'RESOLVIDO' if d['conf']=='ALTA' else 'COM_RESSALVA','antes':json.dumps(before,ensure_ascii=False),'depois':json.dumps(after,ensure_ascii=False),'justificativa':d['reason']});byfam[row['familia_id']]+=1
  row.update({'regra_p2_v5':d['regra'] if d else '', 'status_p2_v5':('RESOLVIDO' if d['conf']=='ALTA' else 'COM_RESSALVA') if d else ('PENDENTE_CONTEXTUAL' if key in pend_ids else 'MANTIDO_P2_V4'), 'justificativa_p2_v5':d['reason'] if d else '', 'area_final_p2_v5':d['area'] if d else row.get('area_final_p2_v4',''), 'cluster_final_p2_v5':d['cluster'] if d else row.get('cluster_final_p2_v4',''), 'subcluster_final_p2_v5':d['sub'] if d else row.get('subcluster_final_p2_v4',''), 'tipo_intencao_final_p2_v5':d['intent'] if d else row.get('tipo_intencao_final_p2_v4',''), 'unidade_origem_final_p2_v5':d['src'] if d else row.get('unidade_origem_final_p2_v4',''), 'unidade_destino_final_p2_v5':d['dst'] if d else row.get('unidade_destino_final_p2_v4',''), 'classificacao_alterada_p2_v5':'sim' if d else 'não'})
  allmap[key]=row
 newdec=[allmap[x['id_global']] for x in decisions]
 remaining=[allmap[x['id_global']] for x in pending if x['id_global'] not in chosen]
 freport=[]
 for fam,l in families.items():
  ss=[x['id_global'] for x in l if x['id_global'] in chosen];rs=Counter(chosen[i]['regra'] for i in ss)
  untouched=[x['Keyword'] for x in l if x['id_global'] not in chosen]
  freport.append({'familia_id':fam,'pendentes_v4':len(l),'classificados_v5':len(ss),'ainda_abertos':len(l)-len(ss),'regras':'; '.join(f'{k}:{n}' for k,n in rs.most_common()),'amostras_abertas':' | '.join(untouched[:7]),'metodo':'cada consulta avaliada individualmente, sem herdar decisão de família'})
 freport.sort(key=lambda x:(-int(x['ainda_abertos']),x['familia_id']))
 cntbase=cntctl=cntmod=0;seen=set();qa=[];patch_map={x['id_global']:x for x in patches};zpath=out/'lotes-001-a-030-p0-p1-p2-v5.zip'
 with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zo:
  for name in sorted(n for n in bz.namelist() if n.endswith('.csv')):
   rows=readcsv(bz,name);cols=list(rows[0]);b=c=m=0
   for r in rows:
    before=dict(r);kind=r['tipo_registro'];id=r['id_global'];
    if kind=='base':
     b+=1;assert id not in seen;seen.add(id)
     if id in chosen:
      patch_map[id]['antes']=json.dumps({k:before.get(k,'') for k in BASE_FIELDS},ensure_ascii=False)
      r.update(replace(chosen[id]));m+=1
    elif kind=='controle':c+=1
    assert all(r[x]==before[x] for x in cols if x not in BASE_FIELDS)
    if kind!='base' or id not in chosen: assert r==before
   cntbase+=b;cntctl+=c;cntmod+=m
   qa.append({'lote':name.split('/')[-1][:8],'base':b,'controles':c,'alteracoes':m,'integridade':'PASSOU'})
   writecsv(zo,name.replace('-v4.csv','-v5.csv'),rows,cols)
 assert len(qa)==30 and cntbase==294905 and cntctl==2190 and cntmod==len(chosen)
 # Queue is analytics review queue, preserve all rows incl P0/P1/P3; only add v5 fields.
 newqueue=[]
 for x in queue:
  y=dict(x);d=chosen.get(y['id_global']);
  if d:y.update({k:v for k,v in replace(d).items() if k in y})
  y.update({k:allmap.get(y['id_global'],{}).get(k,'') for k in FIELDS_NEW});newqueue.append(y)
 audit=out/'auditoria-p2-v5-csv-integral.zip'
 with zipfile.ZipFile(audit,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zo:
  for name,rs,cols in [
   ('p2-v5-decisoes-25050.csv',newdec,list(newdec[0])),
   ('p2-v5-pendencias-restantes.csv',remaining,list(newdec[0])),
   ('p2-v5-patches.csv',patches,list(patches[0]) if patches else ['id_global']),
   ('p2-v5-fila-geral.csv',newqueue,list(newqueue[0])),
   ('p2-v5-qa-regressao-30-lotes.csv',qa,list(qa[0])),
   ('p2-v5-familias-analisadas.csv',freport,list(freport[0]))]:writecsv(zo,name,rs,cols)
 sm={'versao':'P2-v5','universo_p2':len(newdec),'pendencias_entrada_v4':len(pending),'reclassificadas':len(chosen),'sem_ressalva':sum(v['conf']=='ALTA' for v in chosen.values()),'com_ressalva':sum(v['conf']=='RESSALVA' for v in chosen.values()),'pendencias_restantes':len(remaining),'familias_com_patches':len(byfam),'familias_com_pendencias':len(families),'base':cntbase,'controles':cntctl,'lotes':len(qa),'regras':dict(rules),'exemplos':{k:v[:7] for k,v in example.items()},'sha256_lotes':shaf(zpath),'sha256_auditoria':shaf(audit)}
 (out/'resumo-p2-v5.json').write_text(json.dumps(sm,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('FINAL',json.dumps({k:v for k,v in sm.items() if k not in ('exemplos','regras')},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
