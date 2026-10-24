#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 v6: triagem contextual conservadora. Python 3 stdlib, sem sobrescrever arquivos base.
Uso: python3 07-Scripts/revisar_p2_v6.py --raiz . --saida saida-p2-v6 [--preview]
Fontes: 08-Entregas/P2-v5/{lotes-001-a-030-p0-p1-p2-v5.zip,auditoria-p2-v5-csv-integral.zip}
"""
import argparse,csv,io,zipfile,json,re,hashlib,unicodedata
from pathlib import Path
from collections import Counter,defaultdict
BASE_FIELDS=['area_principal','cluster','subcluster','tipo_intencao','intencao_principal','confianca','revisao_manual','justificativa_curta','unidade_origem','unidade_destino','direcao_conversao']
FIELDS_NEW=['regra_p2_v6','status_p2_v6','justificativa_p2_v6','area_final_p2_v6','cluster_final_p2_v6','subcluster_final_p2_v6','tipo_intencao_final_p2_v6','unidade_origem_final_p2_v6','unidade_destino_final_p2_v6','classificacao_alterada_p2_v6']

def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',(s or '').casefold()) if not unicodedata.combining(c))
    return re.sub(r'\s+',' ',s).strip()

def hit(s,p):return bool(re.search(p,s))

def D(rule,area,cluster,sub,intent,reason,conf='ALTA',src='',dst=''):
    return dict(regra=rule,area=area,cluster=cluster,sub=sub,intent=intent,reason=reason,conf=conf,src=src,dst=dst)

def decide(keyword):
    t=norm(keyword)
    # Sempre manter consultas subespecificadas, ainda que semanticamente próximas de uma calculadora.
    if hit(t,r'^\d{1,2}\s+semanas?\s+e\s+\d\s+dias?$'):return None
    if hit(t,r'^\d+(?:[.,]\d+)?\s*fahrenheit$'):return None
    if hit(t,r'\bmilhas?\s+(?:em|para)\s+km\s+h\b'):return None
    if hit(t,r'^\d{4,}$'):return None
    if hit(t,r'^\w{1,3}\s+\d+[a-z]?\s*(?:vs|x)\s*\w{1,4}\d+'):return None
    # Produtos específicos de calculadora física e marcas; a palavra 'online' isolada pode ser um emulador, exigir ressalva.
    if hit(t,r'\bcasio\b|\bclasswiz\b|\bfx\s*[- ]?\s*(?:82|991)\w*\b|\bcalculadora\s+(?:cientifica\s+)?hp\s*(?:12\s*c|48\w*)\b'):
        return D('modelo_calculadora_fisica','Fora de escopo','Comércio e produtos','Calculadoras físicas','navegacional/transacional','Referência a modelo/marca de calculadora física; não implica execução online de operação.', 'RESSALVA' if hit(t,r'\bonline\b') else 'ALTA')
    # Exercícios escolares: não confundir com conversor de arquivo ou solucionador online.
    if hit(t,r'\b(?:exercicios?|atividades?|6\s*ano|7\s*ano|9\s*ano|5\s*ano)\b') and hit(t,r'\b(?:mmc|multiplo\s+comum|heron|sistema\s+de\s+numeracao|razao|proporcao|discriminante|delta|combinatori|principio\s+multiplicativo|tendencia\s+central|polinom|equacoes?|equacao|permutacao|anagrama|grandezas?|proporcionalidade|superficie|decimal|incognitas?|probabilidad|ap[oó]tema|biquadradas?|radicais?|raizes?)\b'):
        return D('exercicios_matematica_escolar','Matemática','Educação matemática','Exercícios e material didático','informacional','Consulta por exercícios ou material pedagógico; não transformação de PDF nem cálculo parametrizado.')
    # Comparações de bancos são consultas de mercado, não simulações de rendimento.
    if hit(t,r'^(?:melhores?\s+bancos?|qual\s+o\s+melhor\s+banco)\b') and hit(t,r'\b(?:rende|rendimento|render|dinheiro)\b'):
        return D('comparacao_bancos_rendimento','Finanças','Investimentos','Comparação de contas e bancos','informacional','Busca por comparação de ofertas e taxas de bancos, não simulador individual; taxas podem mudar.', 'RESSALVA')
    # Datas de eleição: informacionais, não calculadoras.
    if hit(t,r'\b(?:qual\s+.*data|data\s+do)\b') and hit(t,r'\b(?:turno\s+da\s+eleicao|eleicoes?|eleicao)\b'):
        return D('datas_eleitorais_informativas','Fora de escopo','Informações públicas','Calendário eleitoral','informacional','Procura data de eleição, não diferença aritmética entre datas.')
    # Marcas comerciais, quando o objetivo é produto/serviço e não matemática.
    if hit(t,r'\b(?:preco\s+(?:de\s+)?tv|tv\s+.*casas?\s+bahia|preco\s+de\s+inversores?\s+solares?)\b'):
        return D('preco_produto_comercial','Fora de escopo','Comércio e produtos','Consulta de preços de produto','navegacional/transacional','Busca preço de produto comercial, sem operação de cálculo.', 'RESSALVA')
    # Rotas: ainda exige meio de transporte e critérios antes de produzir ETA.
    if hit(t,r'^(?:de\s+)?(?:acailandia|bacabal|peritoro|imperatriz|balsas|santa\s+ines|buriticupu|caxias|codo|estreito|grajau|porto\s+franco|timon|tutoia|vitoria\s+do\s+mearim|barra\s+do\s+corda)\s+a\s+sao\s+luis$'):
        return D('rota_cidades_maranhao','Fora de escopo','Mapas e deslocamento','Rotas entre cidades','navegacional/transacional','Trajeto entre cidades explícito, sem distância numérica ou meio de transporte; oferecer rota/cartografia.', 'RESSALVA')
    # Placas/fontes elétricas com V e A informam características, não conversões entre grandezas.
    if hit(t,r'^\d+(?:[.,]\d+)?\s*(?:v|volts?)\s+\d+(?:[.,]\d+)?\s*(?:a|amperes?)$|^\d+(?:[.,]\d+)?\s*a\s+\d+(?:[.,]\d+)?\s*v$'):
        return D('especificacoes_volts_amperes','Eletricidade e eletrônica','Instalações elétricas','Tensão e corrente nominais','informacional','Valores de tensão e corrente informam características nominais; potência depende de tipo de corrente/fator de potência.', 'RESSALVA')
    # Troca de notas, moedas e câmbio em balcão são intenções comerciais; não taxa de conversão.
    if hit(t,r'\b(?:banco\s+troca\s+moedas|trocar\s+(?:moeda\s+no\s+banco|moeda\s+por\s+(?:dinheiro|nota)|notas\s+por\s+moedas|moedas\s+banco)|troca\s+de\s+cedulas)\b'):
        return D('troca_especie_bancaria','Finanças','Serviços bancários','Troca de dinheiro e cédulas','navegacional/transacional','Busca serviço de troca de dinheiro ou cédulas; verificar disponibilidade, valor facial e condições.', 'RESSALVA')
    # Massa de sacas agrícolas depende da cultura/padrão da saca.
    if hit(t,r'\b(?:sacas?|sacos?)\b') and hit(t,r'\b(?:kg|quilogramas?|quilos?|toneladas?)\b') and not hit(t,r'\b(?:hectare|plantar|colheita|produz|quantos\s+sacos\s+de\s+)\b'):
        return D('sacas_para_quilos_contextual','Conversores','Massa e peso','Sacas agrícolas para peso','conversão contextual','O peso da saca depende do produto e do padrão regional; não assumir sempre 60 kg.', 'RESSALVA')
    # Conversões de arquivos com tipos explícitos. Não confundir aula em PDF com converter PDF.
    m=re.fullmatch(r'(?:converter\s+|transformar\s+|de\s+)?(jpg|png|webp|docx|doc|odt|ods|pptx|powerpoint|word|excel|pdf|ogg)\s+(?:para|em|to|a)?\s*(jpg|png|webp|docx|doc|odt|ods|pptx|powerpoint|word|excel|pdf|mp3)',t)
    if m and m.group(1)!=m.group(2) and not (m.group(1)=='docx' and m.group(2)=='word'):
        explicit=bool(re.search(r'\b(?:para|em|to|a)\b',t))
        if (m.group(1),m.group(2)) in [('docx','doc'),('doc','docx'),('odt','docx'),('ods','excel'),('docx','word')]:
            why='Formato de entrada e saída explícitos; a preservação de edição e layout deve ser verificada.'
        else:why='Formato de origem e destino explícitos; processamento deve preservar legibilidade e qualidade.'
        return D('formatos_documentos_explicitos' if explicit else 'formatos_sem_direcao','Conversores','Arquivos e documentos','Conversão de formato digital','conversão de arquivo/mídia' if explicit else 'conversão contextual',why if explicit else 'Dois formatos presentes sem preposição inequívoca; pedir qual é origem e destino.','RESSALVA',m.group(1).upper() if explicit else '',m.group(2).upper() if explicit else '')
    # Unidades explícitas: o símbolo isolado com número não fornece direção, mas pares com preposição podem.
    g= r'(?:miligramas?|miligrama|mg|gramas?|grama|g)' 
    if hit(t,r'^(?:\d+(?:[.,]\d+)?\s*)?(?:g|gramas?|mg|miligramas?)\s+(?:(?:para|em|a)\s+)?(?:mg|g|cg|gramas?|miligramas?)$') or hit(t,r'^g\s+cg\s+mg$'):
        return D('massa_mg_g_pares','Conversores','Massa e peso','Gramas, centigramas e miligramas','conversão contextual','Unidades de massa mencionadas; direção não é explícita em todos os termos. Exigir seleção da direção se ausente.', 'RESSALVA')
    if hit(t,r'\b(?:transferir\s+libras?\s+a\s+kilos|libras?\s+(?:para|em)\s+(?:kg|kilos?|quilogramas?|quilos?))\b') and not hit(t,r'\b(?:preco|valor|libra\s+esterlina|cotacao)\b'):
        return D('libra_massa_para_kg','Conversores','Massa e peso','Libra-massa para quilograma','conversão direta','Origem lb como massa e destino kg inequívocos.',src='lb',dst='kg')
    # Cozinha: conversões entre massa e volume dependem de densidade; colheres precisam padrão.
    if hit(t,r'\b(?:margarina|farinha|acucar|ingredientes?|colheres?|xicaras?|culinaria|cozinha)\b') and hit(t,r'\b(?:equivale|equivalencia|medidas?|gramas?|\d+\s*g\b|litros?|ml\b|quantos?|tabela|peso\s+|converter|passar)\b'):
        return D('medidas_culinarias_contextuais','Conversores','Culinária e medidas contextuais','Equivalência culinária','conversão contextual','Padrão de colher/xícara e ingrediente/densidade variam; não usar fator genérico massa→volume.', 'RESSALVA')
    # Equivalência agrícola por hectare depende da cultura, solo e região; NÃO assumir rendimento.
    if hit(t,r'\b(?:hectare|alqueire)\b') and hit(t,r'\b(?:produz|sacas?|kg\s+de|kg\s+por|quilos?|quantos?|produtividade)\b') and not hit(t,r'\b(?:preco\s+de\s+um\s+alqueire|comprar|vender)\b'):
        return D('produtividade_agricola','Agropecuária','Produção agrícola','Cultivo e produtividade por área','cálculo contextual','Quantidade de plantio, adubação ou colheita por área depende da cultura, finalidade, manejo e localidade; não fixar taxas.', 'RESSALVA')
    # Consultas de inclinação mínima são busca por orientação e especificação de material.
    if hit(t,r'\b(?:inclinacao|caida|queda|declividade)\b') and hit(t,r'\b(?:minima|fibrocimento|vidro)\b') and hit(t,r'\b(?:telha|telhado|fibrocimento|cobertura)\b') and not hit(t,r'\b(?:calcular|calculo|calculadora|como\s+calcular)\b'):
        return D('inclincacao_cobertura_normas','Construção','Telhados e coberturas','Inclinação mínima e especificações','informacional','Consulta de orientação construtiva; mínima depende do fabricante, material, clima e projeto.', 'RESSALVA')
    # Consultas explícitas sobre inclinação em coberturas, cálculo exige dimensões e padrão de projeto.
    if hit(t,r'\b(?:caida|queda|inclinacao|declividade)\b') and hit(t,r'\b(?:telhad|telha|fibrocimento|cobertura)\w*\b'):
        return D('inclinacao_telhado','Construção','Telhados e coberturas','Inclinação de telhado','cálculo contextual','Inclinação/queda identificadas; pedir vão, desnível e recomendações do fabricante.', 'RESSALVA')
    if hit(t,r'\b(?:calculadora\s+(?:para\s+)?forro\s+(?:de\s+)?pvc|calcular\s+caibro\s+para\s+telhado|calcul(?:o|ar)\s+(?:para\s+)?telhado\s+colonial)\b'):
        return D('quantidade_materiais_cobertura','Construção','Materiais','Estimativa de cobertura/forro','cálculo contextual','Cálculo de materiais requer área, inclinação, perdas e dimensões das peças.', 'RESSALVA')
    # Investimentos: taxas atuais, impostos e modalidade nunca inferidos.
    if hit(t,r'\b(?:quanto\s+rende|rendimento\s+(?:de|da|do|dos)|rendimento\s+\d|simulador\s+de\s+rendimento|calculadora\s+(?:de\s+)?rendimento|render\s+dinheiro|rendimento\s+aplicacao|rendimento\s+poupanca)\b') and hit(t,r'\b(?:reais?|dinheiro|banco|conta|poupanca|aplicad[oa]|mil|milhao|bilhao|nubank|mercado\s+pago|pagbank|99pay|petrobras|itau|santander|bradesco|bb\b|aplicac(?:ao|oes)|rendimento|rende\s+facil|acoes?)\b'):
        return D('rendimento_investimentos_contextual','Finanças','Investimentos','Projeção de rendimento','cálculo contextual','Estimativa depende de ativo, valor aplicado, horizonte, rendimentos efetivos e impostos; não prometer taxa/retorno.', 'RESSALVA')
    if hit(t,r'\b(?:tabela\s+price\s+amortizacao|amortizacao\s+(?:pela|na)\s+tabela\s+price|calculadora\s+de\s+amortizacao|calculo\s+tabela\s+price)\b'):
        return D('amortizacao_tabela_price','Finanças','Crédito e financiamento','Tabela Price','cálculo contextual','Amortização Price exige principal, taxa, prazo, prestações e eventuais carências.', 'RESSALVA')
    # Sistemas numéricos: direção clara ou tabela conceitual.
    m=re.search(r'\b(?:numero\s+)?(\d{1,6})\s+(?:em|para)\s+(?:numeros?\s+)?roman[oa]s?\b',t)
    if m:
        return D('inteiro_para_romano','Conversores','Números e sistemas numéricos','Número para romano','conversão direta','Valor inteiro e destino romano explícitos.',src='inteiro',dst='romano')
    if hit(t,r'\b(?:romano|romanos|numeral\s+romano)\b') and hit(t,r'\b(?:tradutor\s+(?:de\s+)?romano\s+para\s+decimal|roman[os]*\s+para\s+decimal)\b'):
        return D('romano_para_decimal','Conversores','Números e sistemas numéricos','Romano para decimal','conversão direta','Origem romana e destino decimal explícitos.',src='romano',dst='base10')
    if hit(t,r'\b(?:por\s+extenso\s+para\s+algarismo|numero\s+por\s+extenso\s+para\s+algarismo|algarismo\s+para\s+numero\s+por\s+extenso|decimal\s+para\s+numero\s+por\s+extenso)\b'):
        source='extenso' if 'extenso para' in t else 'base10'
        return D('numero_extenso','Conversores','Números e sistemas numéricos','Algarismos e escrita por extenso','conversão direta','Sentido entre numeral decimal e expressão escrita indicado.',src=source,dst='base10' if source=='extenso' else 'extenso')
    if hit(t,r'\b(?:calculadora\s+(?:base\s+\d+|decimal\s+(?:e|para)\s+binario|em\s+hexadecimal|de\s+numero\s+binario)|calculadora\s+em\s+hexadecimal)\b'):
        return D('calculadora_base_numerica','Conversores','Números e sistemas numéricos','Calculadora de bases','conversão contextual','Ferramenta de base numérica clara; exigir base inicial e final quando ausentes.', 'RESSALVA')
    # Funções aritméticas de computador são referência de uso, não conversor.
    if hit(t,r'\b(?:arredondar|arredonda|arredondamento)\b') and hit(t,r'\b(?:excel|javascript|python|formula|funcao|ceil|floor|casas?\s+decimais?|para\s+cima|para\s+baixo)\b') and not hit(t,r'^arredonda\s+para\s+(?:cima|baixo)$'):
        return D('arredondamento_metodo','Matemática','Números e operações','Arredondamento','informacional','Referência a regra/função ou procedimento de arredondamento; não há valor específico a processar.', 'RESSALVA' if hit(t,r'\b(?:excel|python|javascript)\b') else 'ALTA')
    # Conteúdo matemático escolar informacional e ferramentas operacionais explícitas.
    if hit(t,r'\b(?:logaritmo\s+(?:python|em\s+python|na\s+medicina|na\s+biologia|ferretto|professor|khan\s+academy)|ferretto\s+logaritmo|python\s+logaritmo)\b'):
        return D('referencia_logaritmo_externa','Matemática','Logaritmos','Material e implementação de logaritmos','informacional','Consulta de aula, linguagem de programação ou aplicação conceitual.', 'ALTA')
    if hit(t,r'\b(?:divisao|multiplicacao)\s+de\s+polinomios?\s+online\b'):
        return D('operacoes_polinomios_online','Matemática','Álgebra','Operações com polinômios','cálculo contextual','Operação entre polinômios identificada; exigir expressões/coeficientes.', 'RESSALVA')
    # Tributação/folha planilha, sem supor legislação.
    if hit(t,r'\b(?:folha\s+de\s+ponto\s+excel\s+calcul|como\s+calcular\s+.*(?:horas\s+extras|salario\s+liquido|fgts))\b'):
        return D('planilha_trabalhista','Trabalhista','Jornada e adicionais','Controle de horas e remuneração','cálculo contextual','Cálculo depende de jornada, contrato, base salarial e regras legais.', 'RESSALVA')
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
 root=args.raiz; out=args.saida or root/'saida-p2-v6'
 az=zipfile.ZipFile(root/'08-Entregas/P2-v5/auditoria-p2-v5-csv-integral.zip')
 bz=zipfile.ZipFile(root/'08-Entregas/P2-v5/lotes-001-a-030-p0-p1-p2-v5.zip')
 pending=readcsv(az,'p2-v5-pendencias-restantes.csv');assert len(pending)==5148
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
 decisions=readcsv(az,'p2-v5-decisoes-25050.csv');queue=readcsv(az,'p2-v5-fila-geral.csv')
 assert len(decisions)==25050 and len({x['id_global'] for x in decisions})==25050
 assert set(chosen).issubset({x['id_global'] for x in pending})
 pend_ids={x['id_global'] for x in pending};allmap={};patches=[];byfam=Counter();counts=Counter()
 def replace(d):
  return {'area_principal':d['area'],'cluster':d['cluster'],'subcluster':d['sub'],'tipo_intencao':d['intent'],'intencao_principal':d['intent'],'confianca':'alta' if d['conf']=='ALTA' else 'média','revisao_manual':'não' if d['conf']=='ALTA' else 'sim','justificativa_curta':f"P2-v6 {d['regra']}: {d['reason']}",'unidade_origem':d['src'],'unidade_destino':d['dst'],'direcao_conversao':d['src']+'->'+d['dst'] if d['src'] and d['dst'] else ''}
 for old in decisions:
  row=dict(old);key=row['id_global']; d=chosen.get(key)
  if d:
   before={k:row.get(k,'') for k in BASE_FIELDS};after=replace(d);patches.append({'id_global':key,'lote':row['lote'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra':d['regra'],'status':'RESOLVIDO' if d['conf']=='ALTA' else 'COM_RESSALVA','antes':json.dumps(before,ensure_ascii=False),'depois':json.dumps(after,ensure_ascii=False),'justificativa':d['reason']});byfam[row['familia_id']]+=1
  row.update({'regra_p2_v6':d['regra'] if d else '', 'status_p2_v6':('RESOLVIDO' if d['conf']=='ALTA' else 'COM_RESSALVA') if d else ('PENDENTE_CONTEXTUAL' if key in pend_ids else 'MANTIDO_P2_V5'), 'justificativa_p2_v6':d['reason'] if d else '', 'area_final_p2_v6':d['area'] if d else row.get('area_final_p2_v5',''), 'cluster_final_p2_v6':d['cluster'] if d else row.get('cluster_final_p2_v5',''), 'subcluster_final_p2_v6':d['sub'] if d else row.get('subcluster_final_p2_v5',''), 'tipo_intencao_final_p2_v6':d['intent'] if d else row.get('tipo_intencao_final_p2_v5',''), 'unidade_origem_final_p2_v6':d['src'] if d else row.get('unidade_origem_final_p2_v5',''), 'unidade_destino_final_p2_v6':d['dst'] if d else row.get('unidade_destino_final_p2_v5',''), 'classificacao_alterada_p2_v6':'sim' if d else 'não'})
  allmap[key]=row
 newdec=[allmap[x['id_global']] for x in decisions]
 remaining=[allmap[x['id_global']] for x in pending if x['id_global'] not in chosen]
 freport=[]
 for fam,l in families.items():
  ss=[x['id_global'] for x in l if x['id_global'] in chosen];rs=Counter(chosen[i]['regra'] for i in ss)
  untouched=[x['Keyword'] for x in l if x['id_global'] not in chosen]
  freport.append({'familia_id':fam,'pendentes_v5':len(l),'classificados_v6':len(ss),'ainda_abertos':len(l)-len(ss),'regras':'; '.join(f'{k}:{n}' for k,n in rs.most_common()),'amostras_abertas':' | '.join(untouched[:7]),'metodo':'cada consulta avaliada individualmente, sem herdar decisão de família'})
 freport.sort(key=lambda x:(-int(x['ainda_abertos']),x['familia_id']))
 cntbase=cntctl=cntmod=0;seen=set();qa=[];patch_map={x['id_global']:x for x in patches};zpath=out/'lotes-001-a-030-p0-p1-p2-v6.zip'
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
   writecsv(zo,name.replace('-v5.csv','-v6.csv'),rows,cols)
 assert len(qa)==30 and cntbase==294905 and cntctl==2190 and cntmod==len(chosen)
 # Queue is analytics review queue, preserve all rows incl P0/P1/P3; only add v6 fields.
 newqueue=[]
 for x in queue:
  y=dict(x);d=chosen.get(y['id_global']);
  if d:y.update({k:v for k,v in replace(d).items() if k in y})
  y.update({k:allmap.get(y['id_global'],{}).get(k,'') for k in FIELDS_NEW});newqueue.append(y)
 audit=out/'auditoria-p2-v6-csv-integral.zip'
 with zipfile.ZipFile(audit,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zo:
  for name,rs,cols in [
   ('p2-v6-decisoes-25050.csv',newdec,list(newdec[0])),
   ('p2-v6-pendencias-restantes.csv',remaining,list(newdec[0])),
   ('p2-v6-patches.csv',patches,list(patches[0]) if patches else ['id_global']),
   ('p2-v6-fila-geral.csv',newqueue,list(newqueue[0])),
   ('p2-v6-qa-regressao-30-lotes.csv',qa,list(qa[0])),
   ('p2-v6-familias-analisadas.csv',freport,list(freport[0]))]:writecsv(zo,name,rs,cols)
 sm={'versao':'P2-v6','universo_p2':len(newdec),'pendencias_entrada_v5':len(pending),'reclassificadas':len(chosen),'sem_ressalva':sum(v['conf']=='ALTA' for v in chosen.values()),'com_ressalva':sum(v['conf']=='RESSALVA' for v in chosen.values()),'pendencias_restantes':len(remaining),'familias_com_patches':len(byfam),'familias_com_pendencias':len(families),'base':cntbase,'controles':cntctl,'lotes':len(qa),'regras':dict(rules),'exemplos':{k:v[:7] for k,v in example.items()},'sha256_lotes':shaf(zpath),'sha256_auditoria':shaf(audit)}
 (out/'resumo-p2-v6.json').write_text(json.dumps(sm,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('FINAL',json.dumps({k:v for k,v in sm.items() if k not in ('exemplos','regras')},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
