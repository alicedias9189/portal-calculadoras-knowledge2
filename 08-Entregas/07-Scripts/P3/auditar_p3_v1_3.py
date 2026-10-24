#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 v1.3 - revisão de 5 falsos negativos e expansão controlada P3.
Reexecutável: python auditar_p3_v1_3.py --fonte DIR --saida DIR
Fonte: diretório com '08-Entregas/P3-v1.2/{lotes-001-a-030-p3-v1.2.zip,p3-v1.2-fila-23965.csv,fila-geral-p0-p1-p2-p3-v1.2.csv}'
       e '08-Entregas/P3-v1.1/p3-v1.1-qa-amostra-210.csv'.
Requer somente biblioteca padrão. Não sobrescreve arquivos-fonte.
"""
import argparse,csv,io,json,re,unicodedata,zipfile,hashlib,collections,random
from pathlib import Path

CAN_CHANGE=['area_principal','cluster','subcluster','intencao_principal','tipo_intencao','confianca','revisao_manual','justificativa_curta']
TRACK=['status_p3_v1_3','regra_p3_v1_3','justificativa_p3_v1_3','area_final_p3_v1_3','cluster_final_p3_v1_3','subcluster_final_p3_v1_3','tipo_intencao_final_p3_v1_3','classificacao_alterada_p3_v1_3']
FALSE={'33161':('algebra_fracoes','A consulta pede calculadora de equação com frações, não apenas operações elementares.',True),
       '42656':('dissidio_2022','Pedido de cálculo de dissídio/reajuste em período histórico: exige índice e instrumento coletivo aplicáveis.',True),
       '50735':('materiais_reboco','Cálculo de consumo de areia no reboco depende da área, espessura, traço e perdas.',True),
       '78915':('km_l','Intenção já coerente com consumo km/L; leitura como tutorial versus cálculo é ambígua.',False),
       '43465':('gasolina_online','Calculadora de gasolina pode referir-se a custo da viagem ou consumo; falta contexto.',False)}

def norm(t):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',t.casefold()) if not unicodedata.combining(c)).split())
def has(p,t):return re.search(p,t) is not None

def arquivo_csv(rows, cols):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=cols,delimiter=';',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows);return ('\ufeff'+s.getvalue()).encode('utf-8')
def ler_csv(data):return list(csv.DictReader(io.StringIO(data.decode('utf-8-sig')),delimiter=';'))
def grava(path, rows, cols):path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(arquivo_csv(rows,cols))

def decision(row,allowed_unreviewed):
 id_=row['id_global'];t=norm(row['Keyword']);q=row['Keyword'];cal=has(r'\b(calculadora|calcular|calculo|calculadora online|simulador)\b',t);como=has(r'\b(como|formula|passo a passo|exemplo|o que|oq|significado|lei|direitos|modelo|quem|pode|prazo|quando|tabela)\b',t)
 d={};r='';note='';s='';
 if id_ in FALSE:
  r,note,change=FALSE[id_];s='FALSO_NEGATIVO_REVISADO';
  if change and id_=='33161':d=dict(area_principal='Matemática',cluster='Álgebra',subcluster='Equações com frações',tipo_intencao='cálculo direto',intencao_principal='Resolver equações com frações',confianca='média',revisao_manual='sim')
  if change and id_=='42656':d=dict(area_principal='Trabalho',cluster='Remuneração',subcluster='Dissídio e reajuste salarial',tipo_intencao='cálculo contextual',intencao_principal='Calcular reajuste ou dissídio conforme período e convenção coletiva',confianca='média',revisao_manual='sim')
  if change and id_=='50735':d=dict(area_principal='Construção',cluster='Argamassa e revestimento',subcluster='Consumo de areia e reboco',tipo_intencao='dimensionamento',intencao_principal='Estimar areia para execução de reboco',confianca='média',revisao_manual='sim')
  if d:d['justificativa_curta']='P3 v1.3: '+note
  return (r,s,note,d)
 if not allowed_unreviewed:return None
 # Regras escolhidas com contexto explícito; ordem importa, nunca propagar por familia_id.
 if has(r'\b(?:ir|imposto de renda)\b',t) and has(r'\b(?:acoes|acao|bolsa de valores|bolsa)\b',t) and has(r'\b(?:calculadora|calcular|calculo|melhor|ferramenta)\b',t):
  r='tributacao_acoes';s='CLASSIFICADO_COM_RESSALVA'
  tipo='informacional/comercial' if has(r'\b(melhor|gratis|gratuita|xp|rico|receita federal)\b',t) else ('informacional' if como else 'cálculo contextual')
  note='IR sobre operações em ações/bolsa; requer tipo de operação, datas, operações e regras tributárias aplicáveis. Não confundir com IRRF salarial.'
  d=dict(area_principal='Finanças',cluster='Tributação de investimentos',subcluster='Imposto de renda sobre ações e bolsa',tipo_intencao=tipo,intencao_principal='Consultar ou calcular IR de investimentos em ações',confianca='média',revisao_manual='sim')
 elif has(r'\b(?:imposto de renda|irrf)\b',t) and has(r'\b(?:salario|folha de pagamento|folha|mensal)\b',t) and not has(r'\b(?:declarar|declaracao|obrigado a declarar|salario minimo para declarar)\b',t):
  r='irrf_folha';s='CLASSIFICADO_COM_RESSALVA';tipo='informacional' if como or has(r'\b(aliquota|base|tabela)\b',t) else 'cálculo contextual'
  note='IRRF sobre remuneração/folha; tabela e deduções dependem do período, rendimentos e regras aplicáveis. Não usar alíquota fixa.'
  d=dict(area_principal='Trabalho',cluster='Folha e encargos',subcluster='IRRF sobre salário e folha',tipo_intencao=tipo,intencao_principal='Consultar ou calcular IRRF na remuneração',confianca='média',revisao_manual='sim')
 elif has(r'\bfgts\b',t) and has(r'\b(?:atraso|atrasado|atrasada|juros|atualizacao monetaria)\b',t) and has(r'\b(?:calculo|calcular|calculadora|como calcular)\b',t) and not has(r'\b(?:emprestimo|saque aniversario|transferir)\b',t):
  r='fgts_encargos_atraso';s='CLASSIFICADO_COM_RESSALVA';tipo='informacional' if como else 'cálculo contextual'
  note='FGTS/encargos em atraso: índices, datas e regras podem variar. Não misturar com crédito FGTS ou saque-aniversário.'
  d=dict(area_principal='Trabalho',cluster='FGTS',subcluster='Atualização, juros e multa do FGTS',tipo_intencao=tipo,intencao_principal='Calcular/consultar FGTS em atraso',confianca='média',revisao_manual='sim')
 elif has(r'\bdsr\b',t) and has(r'\bhoras? extras?\b|\bhora extra\b',t) and not has(r'\b(?:sem hora extra|sem horas extras|comissoes|significado de dsr)\b',t):
  r='dsr_horas_extras';s='CLASSIFICADO_COM_RESSALVA';tipo='informacional' if como else 'cálculo contextual'
  note='Reflexos/DSR sobre horas extras. Exige dias úteis, descanso e contexto de jornada; sem fórmula universal indiscriminada.'
  d=dict(area_principal='Trabalho',cluster='Jornada e horas extras',subcluster='DSR sobre horas extras',tipo_intencao=tipo,intencao_principal='Calcular ou explicar reflexos de horas extras no DSR',confianca='média',revisao_manual='sim')
 elif has(r'\babono pecuniari[oa]\b',t) and not has(r'\beventual\b',t):
  r='abono_pecuniario_ferias';s='CLASSIFICADO_COM_RESSALVA';tipo='cálculo contextual' if cal and not como else 'informacional'
  note='Abono pecuniário associado a férias; considerar período aquisitivo, dias, remuneração e convenção aplicável. Consulta pode ser jurídica/informativa.'
  d=dict(area_principal='Trabalho',cluster='Férias',subcluster='Abono pecuniário de férias',tipo_intencao=tipo,intencao_principal='Consultar ou calcular abono pecuniário de férias',confianca='média',revisao_manual='sim')
 elif has(r'\bpedido de demissao\b',t) and not has(r'\b(?:gravidez|gravida|gestante|estabilidade|fgts retido|sacar fgts|sumula|tst|carta|modelo de|lei trabalhista|acordo)\b',t):
  r='pedido_demissao';s='CLASSIFICADO_COM_RESSALVA';tipo='cálculo contextual' if cal and not como else 'informacional'
  note='Pedido de demissão: cálculo das verbas ou consulta sobre direitos e aviso prévio conforme condições. Não equiparar a dispensa sem justa causa.'
  d=dict(area_principal='Trabalho',cluster='Rescisão',subcluster='Pedido de demissão e verbas',tipo_intencao=tipo,intencao_principal='Consultar ou calcular verbas de pedido de demissão',confianca='média',revisao_manual='sim')
 elif has(r'\b(?:calculadora|calcular|calculo|simplificar|somar|potenciacao)\b',t) and has(r'\b(?:fracao|fracoes)\b',t) and not has(r'\b(?:probabilidade|log|raiz|horas?|mmc|alg[eé]brica|geratriz|dizima)\b',t):
  r='operacoes_fracoes';s='CLASSIFICADO_CONTEXTO_EXPLICITO';tipo='informacional' if como else 'cálculo direto'
  note='Operações aritméticas sobre frações; a operação específica deve ser inferida somente quando explicitada.'
  d=dict(area_principal='Matemática',cluster='Números e operações',subcluster='Frações e operações',tipo_intencao=tipo,intencao_principal='Calcular ou explicar operações com frações',confianca='média',revisao_manual='sim')
 elif has(r'\b(?:calculadora|calcular|calculo|quantidade|metragem)\b',t) and has(r'\b(?:ceramica|porcelanato|piso|azulejo)\b',t) and not has(r'\b(?:preco|valor|custo|secagem|tempo|rodape|argamassa|cimento|rejunte)\b',t):
  r='quantidade_pisos';s='CLASSIFICADO_COM_RESSALVA';tipo='informacional' if como else 'dimensionamento'
  note='Dimensionamento de piso/cerâmica/porcelanato por área, tamanho e perdas. Sem estimar material sem os parâmetros.'
  d=dict(area_principal='Construção',cluster='Pisos e revestimentos',subcluster='Dimensionamento de pisos e cerâmicas',tipo_intencao=tipo,intencao_principal='Estimar quantidade de pisos e revestimentos',confianca='média',revisao_manual='sim')
 elif has(r'\bgps\b',t) and has(r'\b(?:inss|previdencia|autonomo|atrasado|atraso)\b',t) and has(r'\b(?:calcular|calculo)\b',t):
  r='gps_previdencia';s='CLASSIFICADO_COM_RESSALVA'
  note='Guia da Previdência Social do contribuinte/autônomo, não localização por satélite; taxa e recolhimento dependem de competência/regra.'
  d=dict(area_principal='Trabalho',cluster='Previdência e contribuições',subcluster='GPS e contribuições em atraso',tipo_intencao='cálculo contextual',intencao_principal='Calcular GPS/INSS do contribuinte',confianca='média',revisao_manual='sim')
 elif has(r'\bhp\s*12\s*c\b',t) and has(r'\b(?:juros|taxa|financiamento|emprestimo)\b',t) and row['area_principal']!='Finanças' and not has(r'\b(?:exercicios?|resolvidos?|apostila|pdf|material|curso|aula)\b',t):
  r='hp12c_financeira';s='CLASSIFICADO_COM_RESSALVA';tipo='informacional' if como else 'cálculo contextual'
  note='HP12C financeira em consulta de juros/taxas; tutorial de instrumento não equivale à operação autônoma da calculadora.'
  d=dict(area_principal='Finanças',cluster='Ferramentas financeiras',subcluster='Calculadora financeira e HP12C',tipo_intencao=tipo,intencao_principal='Consultar cálculo financeiro na HP12C',confianca='média',revisao_manual='sim')
 elif has(r'\bgasolina\b',t) and has(r'\b(?:km|quilometro|quilometros)\b',t) and row['area_principal'] not in ('Energia',) and not has(r'\b(?:carro|modelo|ford|fiat|honda|peugeot|gol|preco|custo)\b',t):
  r='litros_km';s='CLASSIFICADO_COM_RESSALVA'
  note='Relação distância e consumo de combustível; km/L não é conversão dimensional independente de rendimento do veículo.'
  d=dict(area_principal='Energia',cluster='Combustíveis',subcluster='Consumo e autonomia',tipo_intencao='cálculo contextual',intencao_principal='Calcular consumo por km/L com rendimento informado',confianca='média',revisao_manual='sim')
 else:return None
 d['justificativa_curta']='P3 v1.3: '+note
 return (r,s,note,d)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fonte',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args();f=args.fonte;out=args.saida;out.mkdir(exist_ok=True,parents=True)
 src=f/'08-Entregas/P3-v1.2';zold=src/'lotes-001-a-030-p3-v1.2.zip'
 fila=ler_csv((src/'p3-v1.2-fila-23965.csv').read_bytes());meta={r['id_global']:r for r in fila};assert len(meta)==23965
 qa=ler_csv((f/'08-Entregas/P3-v1.1/p3-v1.1-qa-amostra-210.csv').read_bytes());true_false={x['id_global'] for x in qa if x['veredito_QA']=='INVESTIGAR_FALSO_NEGATIVO'};assert set(FALSE)==true_false
 # Somente registros de fato fora do piloto (21.875), sem revisitar decisões v1.1 ou v1.2.
 allowed={i for i,x in meta.items() if x['status_p3_v1']=='FORA_DO_PILOTO'}
 assert len(allowed)==21875,len(allowed)
 patches=[]; decisions=[];a_false=[];update={};counter=collections.Counter();base=ctrl=0;allids=set()
 zout=out/'lotes-001-a-030-p3-v1.3.zip';lotreg=[]
 with zipfile.ZipFile(zold) as za,zipfile.ZipFile(zout,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zb:
  assert len(za.namelist())==30
  for name in za.namelist():
   rows=ler_csv(za.read(name));cols=list(rows[0]);l_changed=0;baseline=[]
   for row in rows:
    if row['tipo_registro']!='base':ctrl+=1;continue
    base+=1;id_=row['id_global']
    if id_ not in allowed and id_ not in FALSE:continue
    d=decision(row,id_ in allowed)
    if not d:continue
    rule,status,note,revised=d;old=dict(row);row.update(revised)
    diff=[k for k in CAN_CHANGE if row[k]!=old[k]]
    if diff:
     l_changed+=1;counter[rule]+=1
     patches.append({'id_global':id_,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'regra':rule,'status':status,'campos_alterados':','.join(diff),'antes_json':json.dumps({k:old[k] for k in diff},ensure_ascii=False),'depois_json':json.dumps({k:row[k] for k in diff},ensure_ascii=False)})
    update[id_]=(rule,status,note,dict(row),bool(diff))
    decisions.append({'id_global':id_,'lote':row['lote_id'],'familia_id':row['familia_id'],'Keyword':row['Keyword'],'origem':'AMOSTRA_FALSO_NEGATIVO' if id_ in FALSE else 'EXPANSAO_P3_NOVA_FAMILIA','regra':rule,'status':status,'alterado':'sim' if diff else 'não','area_antes':old['area_principal'],'area_depois':row['area_principal'],'cluster_antes':old['cluster'],'cluster_depois':row['cluster'],'subcluster_antes':old['subcluster'],'subcluster_depois':row['subcluster'],'intencao_antes':old['tipo_intencao'],'intencao_depois':row['tipo_intencao'],'justificativa':note})
    if id_ in FALSE:a_false.append(decisions[-1])
   zb.writestr(name.replace('v1.2.csv','v1.3.csv'),arquivo_csv(rows,cols))
   lotreg.append({'lote':name,'bases':sum(x['tipo_registro']=='base' for x in rows),'controles':sum(x['tipo_registro']!='base' for x in rows),'modificados':l_changed,'status':'AGUARDANDO_REGRESSAO_INDEPENDENTE'})
 assert base==294905 and ctrl==2190,(base,ctrl)
 assert len(a_false)==5
 assert len(patches)==sum(c['modificados'] for c in lotreg)
 for name in ('fila-geral-p0-p1-p2-p3-v1.2.csv','p3-v1.2-fila-23965.csv'):
  rows=ler_csv((src/name).read_bytes()); cols=list(rows[0]);assert not set(TRACK)&set(cols)
  for x in rows:
   u=update.get(x['id_global'])
   if not u: x.update(dict.fromkeys(TRACK,''));continue
   rule,status,note,row,changed=u
   x.update(dict(zip(TRACK,[status,rule,note,row['area_principal'],row['cluster'],row['subcluster'],row['tipo_intencao'],'sim' if changed else 'não'])))
  grava(out/name.replace('v1.2','v1.3'),rows,cols+TRACK)
 for name,rs in [('p3-v1.3-decisoes-por-id.csv',decisions),('p3-v1.3-patches.csv',patches),('p3-v1.3-cinco-falsos-negativos.csv',a_false),('p3-v1.3-regressao-30-lotes.csv',lotreg)]:
  grava(out/name,rs,list(rs[0]))
 pending=21875-len({x['id_global'] for x in decisions if x['origem']=='EXPANSAO_P3_NOVA_FAMILIA'})
 summary={'versao':'P3 v1.3','p3_total':23965,'p3_piloto_anterior':2090,'p3_fora_piloto_antes':21875,'falsos_negativos_revistos':len(a_false),'falsos_negativos_alterados':sum(x['alterado']=='sim' for x in a_false),'novos_casos_examinados':sum(x['origem']=='EXPANSAO_P3_NOVA_FAMILIA' for x in decisions),'novos_casos_alterados':sum(x['origem']=='EXPANSAO_P3_NOVA_FAMILIA' and x['alterado']=='sim' for x in decisions),'p3_fora_piloto_restante':pending,'novas_familias_distintas':len({x['familia_id'] for x in decisions if x['origem']=='EXPANSAO_P3_NOVA_FAMILIA'}),'total_patches':len(patches),'regra_patches':dict(counter),'registros_base':base,'controles':ctrl,'lotes':30,'limite':'Classificação por regras específicas e amostra QA, NÃO revisão humana integral nem aprovação SEO/taxonomia. Saúde P3 v1.2 ainda exige validação editorial.'}
 (out/'resumo-p3-v1.3.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
