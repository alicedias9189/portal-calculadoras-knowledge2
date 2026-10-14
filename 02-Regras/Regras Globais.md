# Regras Globais

Estas regras valem para todos os lotes.

## Classificação

1. Classificar pela intenção dominante da consulta, não pela palavra isolada mais fácil de reconhecer.
2. `areas_origem` é contexto, não resposta.
3. Não atribuir confiança alta apenas porque uma unidade, moeda, extensão ou palavra-chave disparou uma regra lexical.
4. Relações entre grandezas diferentes devem ser validadas dimensionalmente.
5. Origem e destino de conversão devem respeitar a ordem textual da consulta.
6. Se o cálculo depende de variável adicional, marcar como contextual; não tratar como conversão universal.
7. Consultas de cotação, preço, informação e conteúdo devem ser separadas de calculadoras/conversores quando a intenção indicar isso.
8. Casos realmente ambíguos devem ir para revisão manual, não ser forçados para um cluster.

## Dados digitais

- Preservar a distinção entre bit e byte.
- Preservar a distinção entre `MB/s` e `Mbps`.
- A expressão `mb s` pode representar `MB/s` quando o contexto justificar, mas não deve ser fundida automaticamente com Mbps.

## Métricas

- Não somar `Avg. monthly searches` entre variantes como se representassem demandas independentes.
- `Competition` do Google Ads representa concorrência entre anunciantes, não dificuldade SEO orgânica.
- Métricas servem para priorização e contexto; não decidem sozinhas a taxonomia.

## Controle de drift

Toda alteração que afete mais de um lote deve ser registrada em [[../06-Decisoes/DEC-001 - Estratégia de classificação em lotes|Decisões]] e refletida no [[../04-Regressao/Golden Set|Golden Set]] quando aplicável.
