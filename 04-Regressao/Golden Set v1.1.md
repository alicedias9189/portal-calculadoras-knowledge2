# Golden Set v1.1

## Estado

**107 casos ativos.**

A v1.1 mantém os 73 casos anteriores e adiciona 34 regressões aprendidas na auditoria pós-classificação do lote 001.

## Novas regressões obrigatórias

- `potência de microondas em watts` → Energia / Aparelhos elétricos / Consumo de aparelhos / informacional.
- `remuneração da caderneta de poupança` → Finanças / Investimentos / Poupança / informacional.
- `nascimento do filho o pai tem direito a quantos dias` → Trabalho / Afastamentos / Licenças e afastamentos / informacional.
- `variação do dolar em tempo real` → Finanças / Câmbio / Cotação atual / cotação atual.
- `variação dolar real` → Finanças / Câmbio / Cotação atual / cotação atual.
- `gasolina subiu hoje de novo` → Fora de escopo / Preço de mercado / Combustíveis e petróleo / consulta de preço/mercado.
- `proporção de argamassa por metro quadrado` → Construção / Argamassa e revestimento / Argamassa, reboco e assentamento / cálculo contextual.
- `converter dolar australiano em reais` → Conversores / Moedas e câmbio / Conversão entre moedas / conversão direta, AUD→BRL.
- `convert pesos argentinos to reais` → Conversores / Moedas e câmbio / Conversão entre moedas / conversão direta, ARS→BRL.
- `conversor de dolar para peso` → Conversores / Moedas e câmbio / Conversão entre moedas / conversão direta, confiança média/revisão por `peso` genérico.
- `1 mes e 20 dias sao quantas semanas` → Conversores / Unidades temporais / Tempo / conversão direta.
- `mb s mbps` → Conversores / Dados digitais / Taxa de transferência e rede / conversão direta, preservando MB/s ≠ Mbps.
- `calculadora cientifica online` → Matemática / Ferramentas matemáticas / Calculadora científica.
- `oq e progressão aritmética` → Matemática / Álgebra / Progressões e sequências.
- `impermeabilização fachada` → Construção / Impermeabilização / Impermeabilização e vedação.
- `funções seno cosseno e tangente` → Matemática / Trigonometria / Trigonometria e geometria angular.
- `calculadora financeira hp 12c on line` → Finanças / Ferramentas financeiras / Calculadora financeira e HP12C.
- `o que é clt e pj` → Trabalho / Legislação e direitos / Direitos trabalhistas e CLT.
- `aneel bandeira vermelha` → Energia / Tarifas e regulação / Regulação, bandeiras e tarifas.
- `pis 2023 como consultar` → Trabalho / Benefícios e desligamento / PIS/PASEP.
- `calculadora on line simples` → Matemática / Ferramentas matemáticas / Calculadora geral.
- `calculadora de calculos trabalhistas` → Trabalho / Ferramentas trabalhistas / Calculadora trabalhista geral.
- `calculadora para precificar um produto` → Finanças / Custos e precificação / Precificação de produtos.
- `converter mhz para ghz` → Conversores / Eletricidade e eletrônica / Frequência / conversão direta, MHz→GHz.
- `timestamp para data humana` → Datas / Representação temporal / Timestamp e formatos de data.
- `simulação aliquota simples nacional` → Finanças / Tributos / Impostos e Simples Nacional.
- `conversor de criptomoeda` → Finanças / Criptoativos / Conversão e cotação de criptomoedas.
- `tabela de conversão de brix para densidade` → Conversores / Grandezas físico-químicas / Densidade e concentração / cálculo contextual.
- `conversor de tamanhos de roupa homem` → Conversores / Tamanhos e numeração / Roupas e calçados.
- `sistema de medição de energia` → Energia / Medição e demanda / Medição de energia.
- `calculo de demanda elektro` → Energia / Medição e demanda / Demanda elétrica.
- `geração própria no mercado livre de energia` → Energia / Mercado e geração / Geração própria e mercado livre.
- `advocacia quantos anos de faculdade` → Fora de escopo / Educação / Cursos e duração.
- `conversão de unidades energia` → Conversores / Unidades físicas / Energia, potência e calor / tabela-referência, sem direção artificial.

## Critério de bloqueio

Qualquer divergência em regressão crítica bloqueia o lote seguinte até revisão. O lote 001 reclassificado passou em **107/107** casos.

Ver [[../00-Mapa-Global/Taxonomia Mestre v1.1]] e [[../02-Regras/Regras v1.1 - R19-R26]].
