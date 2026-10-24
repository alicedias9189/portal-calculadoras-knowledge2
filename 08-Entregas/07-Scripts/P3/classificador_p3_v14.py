#!/usr/bin/env python3
"""P3 v1.4: regras de expansão conservadora, sem extrapolar famílias."""
import re,unicodedata

def norm(t):
 return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',str(t).casefold()) if not unicodedata.combining(c)).split())
def h(pattern,t):return re.search(pattern,t) is not None

def rule(row):
 t=norm(row['Keyword']);cal=h(r'\b(calculadora|calcular|calculo|simulador|simular|simulacao)\b',t)
 expl=h(r'\b(como|passo a passo|formula|o que|quem|direito|tabela|lei|porque|por que|quando|preco|cotacao)\b',t)
 rule='';status='COM_RESSALVA';notes='';d={};
 if h(r'\b(?:jornada|carga horaria|horas? de trabalho|horas? semanais?|horas? semanal|horas? por semana)\b',t) and h(r'\bsemanal\b|\bsemana\b',t) and not h(r'\b(?:extra|extras|mensais?|mensal|ferias|hora atividade|curso|estagio|cristao)\b',t) and (h(r'\b(?:trabalho|trabalhar|trabalhada|trabalhador|jornada|carga horaria|domestica|lei)\b',t) ):
  rule='jornada_trabalho_semanal'; notes='Jornada semanal de trabalho ou regime de horas; duração contratual/legislação não é conversão genérica de tempo.'
  d=dict(area_principal='Trabalho',cluster='Jornada e horas extras',subcluster='Carga horária semanal',intencao_principal='Consultar ou calcular jornada semanal de trabalho',tipo_intencao='cálculo contextual' if cal else 'informacional')
 elif h(r'\b(?:emprestimo|credito pessoal|financiamento|cdc)\b',t) and h(r'\b(?:bradesco|itau|caixa economica|santander|banco do brasil|bb|nubank|sicredi)\b',t) and h(r'\b(?:juros|taxa|taxas)\b',t) and not cal and not h(r'\b(?:construcao|solar|saque aniversario|fgts|investimento)\b',t):
  rule='consulta_taxa_credito_instituicao';notes='Consulta à taxa/condições de crédito de uma instituição; valor atual deve ser consultado na fonte, não calculado por fator fixo.'
  d=dict(area_principal='Finanças',cluster='Crédito e financiamentos',subcluster='Taxas de juros de crédito bancário',intencao_principal='Consultar taxa e condições de crédito de instituição financeira',tipo_intencao='informacional/comercial' if h(r'\b(?:menor|melhor|barato|vale a pena)\b',t) else 'informacional')
 elif h(r'\b(?:cdb|cdi)\b',t) and h(r'\b(?:vale a pena|melhor que|ou poupanca|x poupanca|versus poupanca|comparar)\b',t) and not cal:
  rule='comparacao_cdi_cdb';notes='Comparação de alternativas/rentabilidades, não conversão ou pagamento garantido; contexto de produto e tributação pode variar.'
  d=dict(area_principal='Finanças',cluster='Investimentos',subcluster='Avaliação e comparação de renda fixa',intencao_principal='Avaliar rendimento de CDB/CDI ou comparar alternativas',tipo_intencao='informacional/comparativo')
 elif h(r'\bcdi\b',t) and h(r'\bacumulad[oa]\b|\bhistoric[oa]\b',t) and not h(r'\b(?:calcular|calculadora|simular|simulador|projecao|entre datas|periodo de|em datas|calculo do)\b',t):
  rule='cdi_historico';notes='Busca por série/taxa acumulada histórica do CDI; não projetar rendimento futuro como fato.'
  d=dict(area_principal='Finanças',cluster='Indicadores econômicos',subcluster='CDI histórico e acumulado',intencao_principal='Consultar valor ou histórico acumulado do CDI',tipo_intencao='informacional')
 elif h(r'\b(?:rentabilidade|rendimento)\b',t) and h(r'\bfundos?\b',t) and h(r'\b(?:banco do brasil|bb|caixa|bradesco|itau)\b',t) and not cal and not h(r'\b(?:quanto rende|se eu investir|simular|projecao)\b',t):
  rule='fundos_consulta_rentabilidade';notes='Consulta de desempenho ou rentabilidade publicada do fundo de investimento; rendimento passado não é simulação garantida.'
  d=dict(area_principal='Finanças',cluster='Investimentos',subcluster='Rentabilidade de fundos bancários',intencao_principal='Consultar rentabilidade divulgada de fundos',tipo_intencao='informacional')
 elif h(r'\b(?:saque aniversario|saque-aniversario)\b',t) and h(r'\b(?:emprestimo|antecipar|antecipacao|adiantar|bancos?|instituicoes?)\b',t) and not cal and h(r'\b(?:quais bancos|bancos que|melhor banco|como funciona|vale a pena|regras? da|onde contratar|quais instituicoes)\b',t):
  rule='saque_aniversario_antecipacao';notes='Produto financeiro de antecipação FGTS: distinguir elegibilidade/contratação do cálculo de valor.'
  d=dict(area_principal='Finanças',cluster='Crédito e financiamentos',subcluster='Antecipação do saque-aniversário FGTS',intencao_principal='Consultar condições ou instituições de antecipação do FGTS',tipo_intencao='informacional/comercial' if h(r'\b(?:quais|bancos?|onde|melhor)\b',t) else 'informacional')
 elif h(r'\b(?:salario|salarial|folha)\b',t) and h(r'\b(?:bruto|liquido|desconto|descontos)\b',t) and cal and not h(r'\b(?:cdb|financiamento|emprestimo|planilha|excel|pis|pasep|fgts|decimo terceiro|13o|13º)\b',t):
  rule='salario_liquido_descontos';notes='Cálculo de bruto/líquido e descontos na folha, que depende de competência, vínculos, deduções e incidências.'
  d=dict(area_principal='Trabalho',cluster='Folha e remuneração',subcluster='Salário bruto, líquido e descontos',intencao_principal='Calcular salário líquido e descontos',tipo_intencao='cálculo contextual')
 elif h(r'\b(?:aposentadoria)\b',t) and h(r'\b(?:simulador|simular|simulacao|calculadora|calcular|calculo)\b',t) and not h(r'\b(?:investimento|previdencia privada|poupanca|banco|cdb)\b',t):
  rule='simulacao_aposentadoria_previdencia';notes='Simulação previdenciária: depende de vínculos, contribuições e regras da competência/entidade.'
  d=dict(area_principal='Trabalho',cluster='Previdência e benefícios',subcluster='Simulação de aposentadoria',intencao_principal='Estimar direito ou valor de aposentadoria',tipo_intencao='navegacional/informacional' if h(r'\b(?:meu inss|gov br|site|portal|camprev)\b',t) else 'cálculo contextual')
 elif h(r'\b(?:calcular|calculadora|calculo)\b',t) and h(r'\b(?:gasolina|combustivel)\b',t) and h(r'\b(?:viagem|trajeto|percurso)\b',t) and not h(r'\b(?:veiculo|ford|fiat|gol|onix|toyota|preco|aumento|alcool|etanol)\b',t):
  rule='custo_combustivel_viagem';notes='Estimativa de gasto/consumo de combustível em trajeto; requer distância, km/L e preço.'
  d=dict(area_principal='Energia',cluster='Combustíveis e transporte',subcluster='Gasto de combustível em viagem',intencao_principal='Calcular custo ou consumo de combustível de viagem',tipo_intencao='cálculo contextual')
 elif h(r'\b(?:tabela|sistema|calculadora|simulador)\b',t) and h(r'\bprice\b',t) and h(r'\bsac\b',t) and not h(r'\b(?:apostila|exercicio|exercicios|pdf|o que e|diferenca)\b',t):
  rule='sac_price_comparacao';notes='Comparação de sistemas de amortização Price/SAC; exige valor, taxa, prazo e encargos, sem assumir equivalência.'
  d=dict(area_principal='Finanças',cluster='Crédito e financiamentos',subcluster='Sistemas de amortização SAC e Price',intencao_principal='Comparar parcelas e juros de SAC e Price',tipo_intencao='simulação/projeção' if cal else 'informacional')
 elif h(r'\b(?:domingo|domingos)\b',t) and h(r'\b(?:hora extra|horas extras|adicional)\b',t) and not h(r'\b(?:lei|feriado|tabela|convenio)\b',t):
  rule='horas_extras_domingo';notes='Remuneração adicional em domingo depende da escala, descanso, legislação, convenção e compensação.'
  d=dict(area_principal='Trabalho',cluster='Jornada e horas extras',subcluster='Horas extras aos domingos',intencao_principal='Consultar ou calcular adicional de domingo',tipo_intencao='cálculo contextual' if cal else 'informacional')
 elif h(r'\b(?:porcentagem|percentual|variacao percentual)\b',t) and h(r'\bexcel\b',t) and h(r'\b(?:como|formula|planilha|calcular)\b',t) and not h(r'\b(?:importar|converter|arquivo)\b',t):
  rule='percentual_excel_educacional';notes='Tutorial ou fórmula de percentual em planilha, não conversor de arquivos.'
  d=dict(area_principal='Matemática',cluster='Porcentagem',subcluster='Fórmulas de porcentagem no Excel',intencao_principal='Aprender fórmula de percentual em planilha',tipo_intencao='informacional')
 elif h(r'\b(?:demanda eletrica|demanda de energia|demanda contratada)\b',t) and h(r'\b(?:calcular|calculo|calculadora)\b',t) and not h(r'\b(?:mercado|energia solar|instalacao de painel)\b',t):
  rule='demanda_eletrica';notes='Dimensionamento/cálculo de demanda elétrica de cargas e/ou contrato, requer simultaneidade e perfil; sem conversão fixa.'
  d=dict(area_principal='Energia',cluster='Eletricidade',subcluster='Demanda elétrica e dimensionamento',intencao_principal='Calcular demanda elétrica',tipo_intencao='cálculo contextual')
 elif h(r'\b(?:quanto rende|quanto renderia|rendimento de)\b',t) and h(r'\b(?:pagbank|picpay)\b',t) and not h(r'\b(?:taxa atual|juros hoje|consulta|extrato|sacar|saque)\b',t):
  rule='rendimento_conta_digital';notes='Estimativa financeira por saldo e prazo; taxa ofertada, limites, impostos e regras variam. Não prometer rentabilidade.'
  d=dict(area_principal='Finanças',cluster='Investimentos',subcluster='Simulador de rendimento em conta digital',intencao_principal='Simular rendimento hipotético em conta digital',tipo_intencao='simulação/projeção')
 elif h(r'\bcdb\b',t) and h(r'\bimposto de renda\b',t) and h(r'\b(?:liquidez diaria|tem|paga|quanto)\b',t) and not h(r'\b(?:calculadora|calcular|calculo|simulador)\b',t):
  rule='tributacao_cdb_consulta';notes='Dúvida informacional sobre tributação CDB, com regras dependentes de data, tipo e prazo.'
  d=dict(area_principal='Finanças',cluster='Tributação de investimentos',subcluster='Imposto de renda em CDB',intencao_principal='Consultar incidência de IR sobre CDB',tipo_intencao='informacional')
 elif h(r'\b(?:gravida|gestante|gravidez)\b',t) and h(r'\b(?:empregada|domestica|contrato|empresa|direito|estabilidade)\b',t) and not h(r'\b(?:semanas|meses|parto|ultrassom|feto|conversao)\b',t) and h(r'\b(?:trabalho|trabalhista|emprego|empresa|contrato|domestica|empregada|estabilidade|direitos?)\b',t):
  rule='direitos_trabalhistas_gestante';notes='Direitos e estabilidade de gestante no trabalho; questão trabalhista, não calculadora gestacional.'
  d=dict(area_principal='Trabalho',cluster='Direitos e estabilidade',subcluster='Estabilidade e direitos da gestante',intencao_principal='Consultar direitos trabalhistas de gestantes',tipo_intencao='informacional')
 else:return None
 
 # Preserva intenção navegacional em buscas por bancos/aplicativos específicos.
 if h(r'\b(?:bradesco|itau|caixa|santander|banco do brasil|bb|nubank|app|aplicativo|portal|site)\b',t) and row['tipo_intencao']=='navegacional/transacional':
  d['tipo_intencao']='navegacional/transacional'
 d['confianca']='média';d['revisao_manual']='sim';d['justificativa_curta']='P3 v1.4: '+notes
 return rule,status,notes,d
