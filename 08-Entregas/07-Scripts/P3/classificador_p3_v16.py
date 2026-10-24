#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regras P3 v1.6; conservadoras e reproduziveis. Sao propostas tecnicas, nao homologacao humana final."""
import re,unicodedata

def norm(s):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',str(s).casefold()) if not unicodedata.combining(c)).split())
def has(p,s):return bool(re.search(p,s))

def corrige_amostra(row):
    """Revisao individual dos 78 novos registros V1.5; altera apenas casos com erro concreto."""
    rid=row['id_global']; t=norm(row['Keyword']); d={}; reg=None; motivo=''
    if rid=='161513' and has(r'\bfundos?\s+de\s+titulos?\s+publicos?\b',t):
        reg='qa_fundos_nao_titulos_diretos';motivo='Fundos que investem em titulos publicos nao sao aquisicao direta de titulos do Tesouro.'
        d={'cluster':'Fundos de investimento','subcluster':'Fundos de renda fixa com titulos publicos', 'intencao_principal':'Conhecer fundos de investimento que aplicam em titulos publicos'}
    elif rid=='280300' and 'publicos e privados' in t:
        reg='qa_titulos_publicos_privados';motivo='Consulta compara/abrange titulos publicos e privados, nao somente Tesouro Direto.'
        d={'subcluster':'Titulos de renda fixa publicos e privados','intencao_principal':'Conhecer categorias de titulos publicos e privados'}
    elif rid=='175239' and 'juros' in t and 'consignado' in t and 'caixa' in t:
        reg='qa_taxa_consignado_informativa';motivo='Consulta pede taxa de juros do consignado em banco nomeado, nao simula um contrato.'
        d={'tipo_intencao':'informacional','intencao_principal':'Consultar juros e condicoes de consignado da Caixa'}
    elif rid=='289794' and 'salario minimo' in t and 'aposentado' in t:
        reg='qa_piso_previdenciario';motivo='Salario minimo associado a aposentado refere-se a beneficios previdenciarios, nao somente remuneracao de emprego.'
        d={'cluster':'Previdencia e beneficios','subcluster':'Piso de beneficios previdenciarios','intencao_principal':'Consultar relacao entre salario minimo e beneficio de aposentadoria'}
    elif rid in {'17365','17394'} and 'antecipar' in t and ('c6 bank' in t or 'aplicativo fgts' in t):
        reg='qa_canal_antecipacao';motivo='Consulta cita explicitamente o canal/plataforma para contratar ou acessar a antecipacao.'
        d={'tipo_intencao':'navegacional/transacional','intencao_principal':'Localizar canal especifico para antecipar o saque-aniversario FGTS'}
    elif rid in {'117919','262222','266973','267102','266809'} and 'consignado' in t and has(r'\b(simula(?:cao|dor)|simular)\b',t):
        reg='qa_simulador_banco_nomeado';motivo='Simulacao de consignado com banco especifico: procurar ferramenta desse banco; parametros ainda podem ser informados.'
        d={'tipo_intencao':'navegacional/transacional','intencao_principal':'Localizar simulador de credito consignado de instituicao especifica'}
    if reg:
        d.update(confianca='média',revisao_manual='sim',justificativa_curta='P3 v1.6 QA: '+motivo)
        return reg,d,motivo
    return None

def expandir(row):
    t=norm(row['Keyword']);a=row['area_principal'];orig=row['tipo_intencao'];d={}; rule=None;note=''
    if ('inss' in t.split()) and (has(r'\b(descont\w*|aliquot\w*|holerite|teto)\b',t) or (has(r'\btabela\b',t) and has(r'\b(?:inss|contribuicao)\b',t)) or has(r'\bcalculadora\s+inss\s+salario\b',t)) and not has(r'\b(empregador|empresa|simples nacional|mei|autonomo|prolabore|pro-labore|contribuinte individual|facultativo|servidor publico|obra|construcao civil)\b',t):
        rule='inss_desconto_folha';note='Desconto, aliquota ou tabela do INSS sobre remuneracao e/ou holerite; valor depende de ano e situacao.'
        kind=('informacional' if has(r'\b(tabela|aliquota|teto|quanto|qual|202\d|201\d|o que|novo desconto|como (?:calcular|e calculado)|porcentagem|percentual|vai para onde|faixa salarial)\b',t) and not has(r'\bcalculadora\b',t) else 'cálculo contextual')
        d=dict(area_principal='Trabalho',cluster='Remuneração e descontos',subcluster='Desconto de INSS em folha',tipo_intencao=kind,intencao_principal=('Consultar regras/tabelas de desconto INSS' if kind=='informacional' else 'Calcular desconto INSS sobre salario com parametros de competencia'))
    elif 'variancia' in t and has(r'\bdesvio(?:s)?\s+(?:de\s+)?padra\w*\b',t):
        rule='variancia_desvio_padrao';note='Termos explicitos de estatistica descritiva; distinguir material explicativo de calculo sobre amostra.'
        kind=('informacional' if has(r'\b(como|questoes|enem|significa|relacao|diferenc|exemplos|excel)\b',t) else 'cálculo direto' if has(r'\bcalcular\b',t) else 'informacional')
        d=dict(area_principal='Matemática',cluster='Estatística descritiva',subcluster='Variância e desvio padrão',tipo_intencao=kind,intencao_principal=('Estudar variancia e desvio padrao' if kind=='informacional' else 'Calcular variancia e desvio padrao'))
    elif has(r'\barranjos?\b',t) and has(r'\bcombinac(?:ao|oes)\b',t):
        rule='arranjo_combinacao';note='Consulta explicita de analise combinatoria e nao de trabalho ou construcao.'
        d=dict(area_principal='Matemática',cluster='Análise combinatória',subcluster='Arranjos e combinações',tipo_intencao='informacional',intencao_principal='Estudar e comparar arranjos e combinacoes')
    elif has(r'\b(?:numeracao\s+romana|numeros?\s+romanos?|algarismos?\s+romanos?)\b',t) and (a not in ('Conversores','Matemática') or orig in ('estimativa de quantidade','estimativa de custo','consulta de preço/mercado','fora de escopo')):
        rule='referencia_numerais_romanos';note='Consulta sobre representacao em algarismos romanos, nao quantidades de obra ou custos.'
        d=dict(area_principal='Conversores',cluster='Sistemas numéricos',subcluster='Algarismos romanos e bases',tipo_intencao='cálculo contextual' if has(r'\bcalculadora\b',t) else 'tabela/referência',intencao_principal='Utilizar calculadora de numerais romanos' if has(r'\bcalculadora\b',t) else 'Consultar tabela e representacao de algarismos romanos')
    elif has(r'\braiz\s+cubica\s+(?:de|do|da)\s+\d+\b',t) and a!='Matemática':
        rule='raiz_cubica_valor_explicito';note='Operando numerico presente; raiz cubica e calculo de matematica.'
        d=dict(area_principal='Matemática',cluster='Potências e raízes',subcluster='Raiz cúbica',tipo_intencao='cálculo direto',intencao_principal='Calcular raiz cubica de numero explicito')
    elif has(r'\bfinanciamento\b',t) and has(r'\b(?:imovel|imoveis|imobiliari\w*|casa|apartamento)\b',t) and has(r'\b(?:taxas?|juros|menor|melhor)\b',t) and not has(r'\b(?:calculadora|simulador|simulacao|simular|simule|parcelas?|valor da prestacao|calculo das?|pro rata)\b',t):
        # Taxas/condicoes solicitadas, sem pedido de simulacao numerica.
        rule='taxa_financiamento_imobiliario';note='Busca comparativa de juros/taxas de financiamento; nao ha pedido inequivoco de simular parcelas.'
        d=dict(area_principal='Finanças',cluster='Crédito e financiamentos',subcluster='Taxas de financiamento imobiliário',tipo_intencao='informacional',intencao_principal='Consultar ou comparar taxas de financiamento imobiliario')
    elif has(r'\babrir\s+conta\b',t) and has(r'\b(?:site|online|aplicativo|app)\b',t) and a in ('Conversores','Trabalho','Fora de escopo','Matemática'):
        rule='abertura_conta_bancaria';note='Abertura de conta por site ou aplicativo e intencao de servico financeiro, nao conversao.'
        kind='informacional' if has(r'\b(como|posso|tem como)\b',t) else 'navegacional/transacional'
        d=dict(area_principal='Finanças',cluster='Contas e serviços bancários',subcluster='Abertura de conta digital',tipo_intencao=kind,intencao_principal='Abrir conta bancaria por meio digital' if kind=='navegacional/transacional' else 'Informar-se sobre abertura digital de conta')
    if rule:
        meaningful=('area_principal','cluster','subcluster','tipo_intencao','intencao_principal')
        if not any(row.get(k)!=v for k,v in d.items() if k in meaningful):return None
        d.update(confianca='média',revisao_manual='sim',justificativa_curta='P3 v1.6: '+note)
        return rule,d,note
    return None
