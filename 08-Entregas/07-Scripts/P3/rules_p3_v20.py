#!/usr/bin/env python3
"""Conservative semantic P3 v2.0 proposals. Standard library only; require traceable per-ID patch."""
import re, unicodedata

def norm(s):
    return re.sub(r'\s+', ' ', ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))).strip()

def match(row):
    """Return rule, area, cluster, subcluster, intent, confidence, reason; or None.
    Follow priority order. Never invent missing numeric conversion parameters.
    """
    t=norm(row['Keyword']); area=row['area']
    P=lambda exp: bool(re.search(exp,t))
    # Restrictive cross-domain repairs.
    if P(r'\b(?:salario maternidade|salario materno|licenca maternidade)\b') and not P(r'\b(?:emprestimo|consignado|credito|cesaria|exame|tabela de natalidade)\b'):
        if area not in ('Trabalho',) and (P(r'\b(?:calcul|valor|estabilidade|direito|licenca|contribuicao|meses|salario)\b') or 'salario maternidade' in t):
            return ('P3V20_SALARIO_MATERNIDADE','Trabalho',('Legislação e direitos' if P(r'\bestabilidade\b') else 'Previdência e benefícios'),('Estabilidade após licença-maternidade' if P(r'\bestabilidade\b') else 'Salário-maternidade'),('cálculo contextual' if P(r'\b(?:calculadora|calcular|calculo)\b') else 'informacional'),'com ressalva','Consulta de benefício trabalhista/previdenciário; não é câmbio, energia ou produto. Não pressupor elegibilidade.')
    if P(r'\b(?:imposto de renda retido na fonte|irrf)\b') and area not in ('Finanças','Trabalho') and not P(r'\b(?:arquivo|pdf|manual)\b'):
        return ('P3V20_IRRF_DOMINIO','Finanças','Tributos','IRRF',('cálculo contextual' if P(r'\b(?:calculadora|calcular|calculo)\b') else 'informacional'),'com ressalva','IRRF é matéria tributária, não consumo elétrico/matemática genérica. Aplicação depende do fato gerador e exercício.')
    if P(r'\b(?:inss|previdencia social)\b') and area in ('Energia','Matemática','Conversores','Construção') and not P(r'\b(?:obra|construc|civil|edific|empresa|simples nacional|patronal|consignado|emprestimo|credito|retencao de obra)\b'):
        return ('P3V20_INSS_DOMINIO','Trabalho','Previdência e benefícios','Contribuições ao INSS',('cálculo contextual' if P(r'\b(?:calculadora|calcular|calculo|formula)\b') else ('navegacional/transacional' if P(r'\b(?:consultar processo|acessar processo|site do inss)\b') else 'informacional')),'com ressalva','INSS/previdência sem contexto de obra, empresa ou crédito não é o domínio atribuído; exigir categoria de contribuinte.')
    if P(r'\b(?:variancia|desvio padrao)\b') and area not in ('Matemática',) and not P(r'\b(?:salario|ferias|trabalh|consumo|energia|eletric|salarial|bolsa)\b'):
        return ('P3V20_ESTATISTICA_DOMINIO','Matemática','Estatística e probabilidade','Dispersão estatística',('cálculo contextual' if P(r'\b(?:calculadora|calcular|calculo)\b') else 'informacional'),'com ressalva','Desvio-padrão/variância são estatística; sem conjunto numérico não há cálculo direto.')
    if P(r'\b(?:raiz quadrada|equac(?:ao|oes)|logaritmo)\b') and area not in ('Matemática',) and not P(r'\b(?:salario|ferias|energia|eletric|financeir|credito|juros|invest|planilha de|excel)\b'):
        return ('P3V20_ALGEBRA_DOMINIO','Matemática','Álgebra','Equações e radiciação',('cálculo direto' if P(r'\b(?:calcule|resolver|resolva|calculadora)\b') and not P(r'\b(?:como|explicacao|tutorial|exemplos|pdf|exercicios?)\b') else 'informacional'),'com ressalva','Tema matemático explícito, não domínio atual. Operação depende da expressão e do contexto.')
    # Informational retail specifications are not user-supplied fuel calculators.
    if area=='Energia' and P(r'\b(?:km por litro|km/l|consumo medio|faz quantos km)\b') and P(r'\b(?:faz|consumo|rendimento|gasta|quantos|media)\b') and P(r'\b(?:onix|palio|gol|uno|hb20|civic|corolla|fiat|honda|toyota|chevrolet|ford|fiesta|sandero|logan|renault|peugeot|cobalt|kwid|etios|ka |fox |celta|march|prisma|ecosport|compass|hilux|saveiro|spin|jetta|up |mobi|toro|tucson|fit |cruze|voyage|duster|clio|fusca|astra|vectra|siena|polo|argo|tracker|sw4|correia|208|308|208|206|nissan|citroen|volkswagen|hyundai)\b'):
        if not P(r'\b(?:calcular|calculadora|formula|conta|converter|conversor|como faz conta|planilha)\b'):
            return ('P3V20_CONSUMO_VEICULO','Energia','Combustíveis','Consumo por modelo de veículo','informacional','com ressalva','Consulta de especificação de consumo de veículo, não cálculo com dados do próprio usuário; depende da versão e condução.')
    # Didactic resources, not executed calculations.
    if P(r'\b(?:pdf|apostila|exercicios? resolvidos?|gabarito)\b') and P(r'\b(?:calculo|matematica|geometria|algebra|integral|derivada|estatistica|raiz|equac(?:ao|oes)|mmc|mdc|matriz|trigonometria|fracao|fatoracao)\b') and not P(r'\b(?:converter|conversor|pdf para|transformar pdf|gerar pdf|calcular em pdf)\b'):
        if (row['tipo_intencao_atual'] in ('cálculo direto','conversão de arquivo/mídia','simulação/projeção') or area in ('Energia','Finanças','Construção','Datas','Conversores')) and not P(r'\b(?:calculo de area pdf|curso de calculo de area)\b'):
            return ('P3V20_MATERIAL_DIDATICO','Matemática', ('Álgebra' if P(r'\b(?:sistema de equac|equacao|matriz)\b') else ('Geometria' if P(r'\bgeometria\b') else 'Números e operações')), 'Materiais didáticos', 'informacional','com ressalva','Material didático/arquivo sobre matemática não significa solicitar cálculo ou converter o PDF.')
    # Published market rate or bank tariff is not itself a loan simulation.
    if area=='Finanças' and P(r'\b(?:taxa(?:s)? de juros|juros do|juros para|cet)\b') and P(r'\b(?:qual|quanto|valor|tabela|hoje|202[0-9]|20[0-1][0-9]|atual|medio|media|banco|caixa|itau|santander|bradesco|nubank)\b') and row['tipo_intencao_atual'] in ('simulação/projeção','cálculo direto','navegacional/transacional'):
        if not P(r'\b(?:simulador|simulacao|simular|calcular|calculadora|financiar|como calcular|formula|converter)\b'):
            return ('P3V20_TAXA_JUROS_INFORME','Finanças',('Investimentos' if P(r'\b(?:poupanca|cdb)\b') else 'Crédito'),('Taxas e rendimentos informados' if P(r'\b(?:poupanca|cdb)\b') else 'Taxas e condições de crédito'),'informacional','com ressalva','Consulta sobre taxa ou CET informado, sem dados para simular empréstimo. Valor e data dependem da instituição.')
    # Physical directional pairs misfiled under energy consumption; never a number without destination.
    if P(r'\b(?:joules?|kj|megajoules?|kwh|wh)\s+(?:para|em)\s+(?:joules?|kj|megajoules?|kwh|wh)\b') and area=='Energia' and not P(r'\b(?:preco|custo|reais|r\$|tarifa|formula|passagem|como|tutorial)\b'):
        return ('P3V20_CONVERSAO_ENERGIA','Conversores','Energia, potência e calor','Conversão entre unidades de energia','conversão direta','sem ressalva','Origem e destino de energia explícitos; regra muda a classificação, não aplica fator numérico.')
    return None
