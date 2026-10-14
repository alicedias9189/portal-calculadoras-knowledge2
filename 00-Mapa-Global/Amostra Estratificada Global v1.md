# Amostra Estratificada Global v1

## Objetivo

Criar uma amostra global suficientemente diversa para construir a [[MOC - Taxonomia|taxonomia-mestra v1]] sem depender de uma seleção aleatória simples e sem classificar semanticamente as 294.905 palavras-chave de uma vez.

A amostra foi refeita do zero em High.

## Base

- Base válida considerada: **294.905 palavras-chave únicas**.
- Registros de metadados do Google Ads excluídos: 2.
- Tamanho da amostra: **10.000 palavras-chave**.
- Combinações exatas de `areas_origem` existentes na base: **44**.
- Combinações representadas na amostra: **44 de 44**.
- Seleção determinística para permitir reprodução e comparação entre versões.

## Estratégia de amostragem

A amostra não é puramente proporcional. Ela combina representatividade com superamostragem intencional de casos importantes para a taxonomia.

### 1. Núcleo estratificado

Estratificação por:

- combinação exata de `areas_origem`;
- faixa de volume mensal;
- faixa de `ocorrencias_origem`.

Isso evita que áreas muito grandes eliminem da amostra combinações pequenas ou raras.

### 2. Sobreposição entre áreas

Consultas presentes em várias áreas foram deliberadamente superamostradas, pois são as mais úteis para definir fronteiras da taxonomia.

Distribuição final por `qtd_areas`:

- 1 área: **4.970**
- 2 áreas: **3.712**
- 3 áreas: **1.137**
- 4 áreas: **175**
- 5 áreas: **6**

Todos os registros existentes com 4 ou 5 áreas ficaram representados na amostra.

### 3. Volume e recorrência

A amostra inclui reforço para:

- termos de alto volume;
- volume zero;
- volume ausente;
- alta recorrência entre sementes/exportações.

Distribuição por faixa de volume:

- 0: **1.156**
- 1–100: **3.546**
- 101–1.000: **1.807**
- 1.001–10.000: **1.225**
- >10.000: **1.417**
- ausente: **849**

Distribuição por `ocorrencias_origem`:

- 1: **557**
- 2–3: **2.486**
- 4–10: **3.926**
- 11–30: **2.377**
- >30: **654**

### 4. Riscos lexicais e técnicos

Foram superamostrados padrões que historicamente geram falsos positivos ou ambiguidades:

- conversão e conversores;
- cálculo/calculadora;
- moedas e cotação;
- arquivos, documentos e mídia;
- dados digitais e taxas de transferência;
- unidades físicas e conversões dimensionais;
- trabalho e cálculos legais;
- datas e tempo;
- energia e construção;
- ambiguidades conhecidas como libra, arroba, segundo e MB/s × Mbps.

Esses padrões servem para testar regras, não para pré-classificar a consulta.

## Representação das áreas exclusivas

Entre as palavras-chave que aparecem em apenas uma área, a amostra contém:

- Finanças: **1.077**
- Conversores: **917**
- Datas: **678**
- Trabalho: **659**
- Matemática: **632**
- Construção: **514**
- Energia: **493**

## Diversidade adicional

A amostra também inclui deliberadamente:

- long-tails;
- consultas curtas e genéricas;
- consultas com números;
- consultas contendo símbolos/unidades;
- uma amostra aleatória global determinística.

## Regra de uso

A amostra serve para descobrir e validar a taxonomia inicial. Ela **não deve ser usada para estimar percentuais reais de cada intenção na base**, porque alguns estratos foram propositalmente superamostrados.

A área de origem continua sendo somente evidência de procedência, não a classificação final.

## Próximo passo

Usar esta amostra em High para:

1. descobrir famílias de intenção recorrentes;
2. construir a taxonomia-mestra v1;
3. definir critérios de inclusão/exclusão por cluster;
4. identificar ambiguidades que precisam de regras globais;
5. selecionar os primeiros itens do [[../04-Regressao/Golden Set|Golden Set]];
6. só depois definir o particionamento semântico dos lotes.
