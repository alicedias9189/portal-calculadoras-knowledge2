#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regras focalizadas da P3 v1.5. Não altera keywords nem colunas Google Ads."""
import re,unicodedata

def norm(t):return ' '.join(''.join(ch for ch in unicodedata.normalize('NFKD',str(t).casefold()) if not unicodedata.combining(ch)).split())
def has(p,t):return re.search(p,t) is not None

def revisar_p3_v14(row):
    t=norm(row['Keyword']);o=row['tipo_intencao'];sub=row['subcluster']
    if row['area_principal']=='Finanças' and sub=='Taxas de juros de crédito bancário' and o=='navegacional/transacional' and has(r'\b(juros|taxa|taxas)\b',t) and has(r'\b(credito|emprestimo|financiamento|cdc)\b',t) and not has(r'\b(site|portal|aplicativo|app|login|entrar|agencia|telefone|contratar|acesse|abrir conta)\b',t):
        return 'qa_taxa_bancaria_informativa',{'tipo_intencao':'informacional','intencao_principal':'Consultar taxa e condições de crédito de instituição financeira','confianca':'média','revisao_manual':'sim','justificativa_curta':'P3 v1.5: nome do banco não basta para indicar navegação; pedido explícito de taxa/juros é informativo e requer fonte oficial atual.'},'Consulta a taxa bancária, sem ação ou endereço do portal.'
    if row['area_principal']=='Trabalho' and sub=='Simulação de aposentadoria' and o=='cálculo contextual' and has(r'^como (fazer (?:a )?simulacao|simular|calcular)\b',t):
        return 'qa_tutorial_aposentadoria',{'tipo_intencao':'informacional','intencao_principal':'Aprender como calcular ou utilizar uma simulação de aposentadoria','revisao_manual':'sim','justificativa_curta':'P3 v1.5: a consulta começa com “como”, solicitando procedimento; não é necessariamente execução da simulação.'},'Busca por instruções, não pedido inequívoco de cálculo automático.'
    if row['area_principal']=='Trabalho' and sub=='Carga horária semanal' and o=='cálculo contextual' and has(r'^como calcular horas? de trabalho semanal\b',t):
        return 'qa_tutorial_jornada',{'tipo_intencao':'informacional','intencao_principal':'Aprender o procedimento para calcular a jornada semanal de trabalho','revisao_manual':'sim','justificativa_curta':'P3 v1.5: “como calcular” aponta a explicação do procedimento, não necessariamente à execução.'},'Consulta educacional sobre método de cálculo.'
    return None

def expandir_p3(row):
    t=norm(row['Keyword']);a=row['area_principal'];orig=row['tipo_intencao'];d={};rule=None;note=''
    if has(r'\b(titulos? publicos?|tesouro direto)\b',t) and a!='Finanças' and has(r'\b(o que e|como funciona|rendimento|investir|investimento|comprar|compra|venda|rentabilidade|taxa|juros|resgate|tesouro direto|titulos? publicos?)\b',t):
        rule='titulos_publicos_dominio';note='Títulos públicos e Tesouro Direto são instrumentos financeiros; como e quanto rendem depende do título e de suas regras.'
        kind='informacional' if has(r'^como |\bo que e\b|\btipos?\b|\bquais?\b',t) else ('cálculo contextual' if has(r'\bcalculadora|calcular|projecao\b',t) else 'informacional')
        d=dict(area_principal='Finanças',cluster='Investimentos',subcluster='Tesouro Direto e títulos públicos',tipo_intencao=kind,intencao_principal='Consultar ou calcular características de títulos públicos')
    elif has(r'\b(pa e pg|progressao aritmetica|progressao geometrica)\b',t) and a!='Matemática' and not has(r'\b(pa\s+[0-9]{2,4}|previdencia|santa|professor|paulo|planilha)\b',t):
        rule='progressao_pa_pg_dominio';note='PA/PG significa progressões aritmética e geométrica; não intervalo de datas.'
        d=dict(area_principal='Matemática',cluster='Sequências e progressões',subcluster='Progressões PA e PG',tipo_intencao='informacional' if has(r'^como\b',t) else 'cálculo contextual',intencao_principal='Aprender ou calcular progressões aritméticas e geométricas')
    elif has(r'\b(inflacao acumulada|ipca acumulado|inflacao do periodo|inflacao entre)\b',t) and a!='Finanças' and not has(r'\b(obra|construcao|planta|beneficio|fgts)\b',t):
        rule='inflacao_indicador_dominio';note='Inflação acumulada é indicador econômico ou cálculo de variação de índice em período definido, não tema trabalhista/energia.'
        kind='informacional' if has(r'^como\b|\b20\d\d\b|\btaxa\b',t) else 'cálculo contextual'
        d=dict(area_principal='Finanças',cluster='Indicadores econômicos',subcluster='Inflação e IPCA acumulado',tipo_intencao=kind,intencao_principal='Consultar ou calcular inflação acumulada num período')
    elif has(r'\bsalario minimo\b',t) and a!='Trabalho' and has(r'\b(20\d\d|ano|atual|valor|hoje|vigente|historico|brasileiro|brasil)\b',t) and not has(r'\b(desconto|descontos|poder de compra|aumento do salario minimo|comercial)\b',t):
        rule='salario_minimo_valor';note='Consulta histórica ou regional ao salário mínimo legal; pesquisar período e jurisdição e não apresentar como cotação de mercado.'
        d=dict(area_principal='Trabalho',cluster='Remuneração e pisos',subcluster='Salário mínimo por período e localidade',tipo_intencao='informacional',intencao_principal='Consultar salário mínimo legal por ano/região')
    elif has(r'\b(emprestimo consignado|credito consignado)\b',t) and a!='Finanças' and has(r'\b(calculadora|simular|simulador|simulacao|calculo|calcular|parcelas?|taxas?|juros|valor|banco)\b',t):
        rule='credito_consignado_dominio';note='Consignado é crédito financeiro; margem, parcelas e taxas dependem de regime, instituição e período.'
        kind=('informacional' if has(r'^como calcular|\btaxa de juros\b|\bporcentagem de juros\b',t) else 'simulação/projeção')
        d=dict(area_principal='Finanças',cluster='Crédito e financiamentos',subcluster='Empréstimo e crédito consignado',tipo_intencao=kind,intencao_principal='Consultar ou simular empréstimo consignado')
    elif has(r'\b(antecipar|antecipacao|adiantar|adiantamento)\b',t) and has(r'\b(saque aniversario|saque-aniversario)\b',t) and a!='Finanças' and not has(r'\b(como antecipar|como adiantar|como solicitar|consultar|extrato)\b',t):
        rule='antecipacao_fgts_dominio';note='Antecipação do saque-aniversário é operação de crédito vinculada ao FGTS; distinguir dúvida operacional de simulação.'
        kind=('simulação/projeção' if has(r'\bsimular|simulacao|simulador\b',t) else 'informacional')
        d=dict(area_principal='Finanças',cluster='Crédito e financiamentos',subcluster='Antecipação do saque-aniversário FGTS',tipo_intencao=kind,intencao_principal='Consultar ou simular antecipação do saque-aniversário')
    elif has(r'\b(equacao\s+(?:irracional|linear|quadratica|do segundo grau)|equacao diferencial|equacoes? de primeiro grau)\b',t) and a!='Matemática' and not has(r'\b(financiamento|investimento|preditiva|taxa|emprestimo)\b',t):
        rule='equacao_dominio';note='Equação matemática não corresponde ao domínio de energia ou de juros.'
        d=dict(area_principal='Matemática',cluster='Álgebra e equações',subcluster='Equações algébricas e resolução',tipo_intencao='informacional' if has(r'^como\b',t) else 'cálculo direto',intencao_principal='Resolver ou aprender a resolver equação')
    if rule:
        d.update(confianca='média',revisao_manual='sim',justificativa_curta='P3 v1.5: '+note)
        return rule,d,note
    return None
