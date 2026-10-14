# Golden Set

Conjunto de controle usado para detectar drift entre lotes e regressões da taxonomia.

## Estado

**v1 ativa: 73 casos.**

- 61 casos reais da amostra estratificada global.
- 12 regressões sintéticas baseadas em falhas já observadas.

O arquivo tabular completo está no artefato `taxonomia-mestra-v1.xlsx`, aba `Golden_Set`.

## Casos reais representativos

### Matemática
- `achar porcentagem` → Matemática / Porcentagem e variação percentual.
- `proporção e regra de tres` → Matemática / Regra de três e proporções.
- `calculadora de fração` → Matemática / Frações e decimais.
- `calcular a raiz quadrada` → Matemática / Potências, raízes e logaritmos.
- `calculadora de equação de 1 grau` → Matemática / Equações e expressões.

### Datas
- `calculadora de dias entre datas` → Datas / Diferença entre datas.
- `acrescentar dias úteis` → Datas / Somar/subtrair datas e prazos.
- `calculadora de idade` → Datas / Idade e data de nascimento.
- `descobrir dia da semana de aniversário` → Datas / Dia da semana e calendário.

### Conversores
- `1 milhas em km` → Comprimento e distância.
- `acre para m2` → Área e superfície.
- `fahrenheit em celsius` → Temperatura.
- `arroba em quilogramas` → Massa e peso.
- `conversão de pdf para word` → Documentos e PDF.
- `150mbps mb s` → Taxa de transferência e rede, preservando bit/byte.
- `1 dólar em real` → Conversão entre moedas.

### Construção
- `calculadora metro quadrado parede` → Área aplicada à construção.
- `1 saco de cimento faz quantos m3 de concreto` → Concreto.
- `calculadora de piso` → Pisos e revestimentos.
- `1 litro de tinta pinta quantos metros quadrados` → Tinta e pintura.
- `calcular quantidade de telhas` → Telhados e coberturas.
- `calculadora inss obra` → INSS e regularização de obra.

### Trabalho
- `calculadora salario liquido` → Salário líquido e bruto.
- `calculadora de inss` → INSS e IRRF.
- `calculadora de decimo terceiro` → Décimo terceiro salário.
- `calculadora de férias` → Férias.
- `calculadora de fgts rescisão` → FGTS e multa rescisória.
- `calculadora de rescisão` → Rescisão trabalhista.
- `calculador hora extra` → Hora extra.
- `adicional noturno calculo` → Adicional noturno.
- `banco de horas calculadora online` → Banco de horas.
- `calculadora de seguro desemprego` → Seguro-desemprego.

### Energia
- `1 kwh em reais` → Custo de consumo elétrico; cálculo contextual por tarifa.
- `ar condicionado 12000 btus consumo` → Ar-condicionado e BTU.
- `1 litro de gasolina faz quantos km` → Consumo e autonomia.
- `cálculo solar` → Dimensionamento solar.

### Finanças
- `calculadora juros simples` → Juros simples.
- `calculadora de juros compostos` → Juros compostos.
- `calculadora de juros emprestimo` → Empréstimos.
- `amortização price` → Amortização SAC e Price.
- `100 mil na poupança rende quanto` → Poupança.
- `1000 reais no cdi rende quanto` → CDB, CDI e renda fixa.
- `calculadora tesouro direto` → Tesouro Direto.
- `calculadora de dividendos por ação` → Ações e dividendos.
- `atualização valor ipca` → Inflação e índices.
- `cotacao do dolar hoje` → Cotação atual.

## Casos de fronteira reais

- `apk whatsapp gb` → fora de escopo; `GB` não é armazenamento.
- `preço da arroba do boi gordo hoje no mercado` → consulta de preço/mercado, fora da conversão de massa.
- `cotação da libra hoje` → Finanças / cotação atual.
- `1 libra em real` → Conversores / conversão entre moedas, com atenção à ambiguidade lexical.
- `a mulher v em pdf` → busca por conteúdo, não conversão de PDF.
- `dimensionamento energia solar fotovoltaica pdf` → Energia / informacional sobre dimensionamento, não conversão de arquivo.

## Regressões sintéticas obrigatórias

- `converter centimetros em metros` → Comprimento e distância / conversão direta.
- `tabela de conversao de unidades peso` → Massa e peso / tabela-referência.
- `converter hectares em alqueires paulista` → Área e superfície.
- `tabela de conversao de pressao psi para bar` → Pressão e grandezas mecânicas.
- `converter metros cubicos em metros quadrados` → cálculo contextual, confiança baixa, revisão.
- `converter centimetros em metros quadrados` → cálculo contextual, confiança baixa, revisão.
- `converter gramas em ml` → medidas culinárias/contextuais; depende de densidade.
- `como transformar newton em joule` → relação mecânica contextual; não conversão direta universal.
- `mb s` → taxa de transferência; ambígua/revisão, não fundir com Mbps.
- `whatsapp gb` → fora de escopo.
- `preço da arroba do boi` → preço de commodity, não massa.
- `libras hoje valor` → Finanças / cotação atual, confiança média se o contexto não remover totalmente a ambiguidade.

## Uso nos lotes

1. Inserir subconjuntos do Golden Set como controles repetidos em lotes distintos.
2. Comparar a saída com o rótulo esperado.
3. Divergência deve ser tratada antes da consolidação daquele lote.
4. Alteração intencional da taxonomia exige atualizar este Golden Set e registrar decisão.

Ver [[../00-Mapa-Global/Taxonomia Mestre v1]] e [[../02-Regras/Regras Globais]].
