# Regras Globais

Estas regras valem para todos os lotes.

## Classificação

1. Classificar pela intenção dominante da consulta, não pela palavra isolada mais fácil de reconhecer.
2. `areas_origem` é contexto, não resposta.
3. Não atribuir confiança alta apenas porque uma unidade, moeda, extensão ou palavra disparou uma regra lexical.
4. Contexto temático explícito vence matemática genérica.
5. Conversão direta entre unidades dimensionalmente compatíveis vai para Conversores.
6. Aplicação temática vence Conversores quando a fórmula depende de variáveis/regra daquele domínio.
7. Conversão explícita de valor entre moedas vai para Conversores; cotação atual/histórica vai para Finanças.
8. Relações entre grandezas diferentes devem ser validadas dimensionalmente.
9. Origem e destino de conversão devem respeitar a ordem textual da consulta.
10. Se o cálculo depende de variável adicional, marcar como contextual; não tratar como conversão universal.
11. Consultas de cotação, preço, informação e conteúdo devem ser separadas de calculadoras/conversores quando a intenção indicar isso.
12. Casos realmente ambíguos devem ir para revisão manual, não ser forçados para um cluster.
13. Metragem/material explicitamente de obra vai para Construção.
14. Jornada, salário, FGTS, rescisão, férias e benefícios vão para Trabalho quando a regra laboral é necessária.
15. Consumo/custo/dimensionamento energético vai para Energia; conversão pura de unidade energética/elétrica vai para Conversores.
16. Uma keyword recebe uma única classificação primária.
17. Confiança alta exige coerência semântica completa, não apenas match lexical.
18. Volume do Google Ads serve para priorização, nunca para decidir a intenção.

## Grandezas e dimensionalidade

- m³ → m² exige variável adicional.
- cm → m² exige variável adicional.
- g → mL depende de densidade/ingrediente.
- N → J depende de contexto físico, como deslocamento.
- Relações elétricas como kVA → kW podem depender de fator de potência.
- Casos desse tipo devem usar `cálculo contextual`, confiança baixa/média e revisão quando faltar parâmetro essencial.

## Dados digitais

- Preservar a distinção entre bit e byte.
- Preservar a distinção entre `MB/s` e `Mbps`.
- A expressão `mb s` pode representar `MB/s` quando o contexto justificar, mas não deve ser fundida automaticamente com Mbps.
- `WhatsApp GB` é nome/variante de aplicativo, não armazenamento digital.

## Arquivos e mídia

- Presença de `pdf`, `jpg`, `mp3`, `mp4` etc. não implica intenção de conversão.
- Busca por documento/conteúdo em PDF sem verbo/intenção de transformação deve ser informacional ou fora de escopo, conforme o caso.

## Métricas

- Não somar `Avg. monthly searches` entre variantes como se representassem demandas independentes.
- `Competition` do Google Ads representa concorrência entre anunciantes, não dificuldade SEO orgânica.
- Métricas servem para priorização e contexto; não decidem sozinhas a taxonomia.

## Controle de drift

Toda alteração que afete mais de um lote deve ser registrada em `06-Decisoes` e refletida no [[../04-Regressao/Golden Set|Golden Set]] quando aplicável.

Ver [[../00-Mapa-Global/Taxonomia Mestre v1]].
