# Taxonomia Mestre v1.1

Status: **ativa para os próximos lotes**.

A v1.1 foi fechada após a classificação completa do lote 001, auditoria pós-classificação, correção das regressões encontradas e nova auditoria aprovada.

## Escala

- Base global de referência: 294.905 keywords.
- Taxonomia v1: 92 subclusters.
- Novos subclusters v1.1: 24.
- Total v1.1: 116 subclusters.
- Tipos de intenção: 17.
- Regras globais: R01–R26.
- Golden Set v1.1: 107 casos.

## Novos subclusters da v1.1

### Matemática

- Ferramentas matemáticas
  - Calculadora científica
  - Calculadora geral
- Álgebra
  - Progressões e sequências
  - Otimização e programação linear
- Trigonometria
  - Trigonometria e geometria angular
- Geometria
  - Relações métricas, semelhança e circunferência

### Datas

- Representação temporal
  - Timestamp e formatos de data

### Conversores

- Conversões gerais
  - Conversor genérico de unidades
- Eletricidade e eletrônica
  - Frequência
- Tamanhos e numeração
  - Roupas e calçados
- Grandezas físico-químicas
  - Densidade e concentração

### Construção

- Impermeabilização
  - Impermeabilização e vedação

### Trabalho

- Previdência e benefícios
  - Previdência e benefícios do INSS
- Legislação e direitos
  - Direitos trabalhistas e CLT
- Benefícios e desligamento
  - PIS/PASEP
- Ferramentas trabalhistas
  - Calculadora trabalhista geral

### Finanças

- Ferramentas financeiras
  - Calculadora financeira e HP12C
- Custos e precificação
  - Precificação de produtos
- Tributos
  - Impostos e Simples Nacional
- Criptoativos
  - Conversão e cotação de criptomoedas

### Energia

- Tarifas e regulação
  - Regulação, bandeiras e tarifas
- Medição e demanda
  - Medição de energia
  - Demanda elétrica
- Mercado e geração
  - Geração própria e mercado livre

## Regras aprendidas com o lote 001

A v1.1 incorpora explicitamente os seguintes limites:

- potência de aparelho elétrico não é potenciação matemática;
- `quantos anos` não implica Datas quando a pergunta é sobre curso, pessoa, produto ou regra de serviço;
- dias de licença/luto/paternidade regidos por CLT pertencem a Trabalho;
- preço/notícia de gasolina ou Petrobras não é cálculo de consumo energético;
- cotação/variação/gráfico cambial não é conversão de quantia;
- `dólar australiano` e `dólar canadense` são unidades monetárias compostas e devem ser extraídas como AUD/CAD;
- `peso` monetário sem país/código é ambíguo;
- conversão direta deve preencher origem, destino e direção quando identificáveis;
- `remuneração da poupança` pertence a Finanças, não Trabalho;
- `valor` de rescisão/férias/13º não é preço de mercado.

## Governança

1. Esta versão substitui a v1 como contrato operacional.
2. Não criar novos subclusters silenciosamente durante os lotes.
3. Novo conceito recorrente deve ser registrado em `06-Decisoes` antes de entrar em produção.
4. Todo lote deve passar pelo Golden Set v1.1 e por auditoria pós-classificação.
5. Regressão crítica bloqueia o lote seguinte.
6. Casos genuinamente ambíguos podem permanecer em confiança média/baixa, mas não devem ficar sem área/cluster/subcluster.

Ver [[MOC - Taxonomia]], [[../02-Regras/Regras Globais]], [[../04-Regressao/Golden Set]] e [[../06-Decisoes/DEC-004 - Taxonomia Mestre v1.1]].
