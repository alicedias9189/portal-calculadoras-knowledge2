# Relatório P3 v2.3 — revisão crítica e saneamento de escopo

## Resultado principal

A P3 v2.2 apresentou um desvio de escopo: 108 patches foram aplicados aos 30 lotes, mas somente **10 IDs pertencem à fila priorizada P3 (23.965 registros)**. Os demais 98 IDs não constam sequer da fila geral priorizada de 52.046.

A amostra original de QA continha 72 entradas, das quais **68 estavam fora da P3**. Assim, os 72 casos não podem ser usados para estimar a taxa de erro das classificações P3.

A P3 v2.3 implementa **100 patches verificáveis**: **98 restaurações** dos registros fora da fila aos valores P3 v2.1 e **2 refinamentos legítimos** da intenção de calcular CET. As propostas sem escopo P3 não foram descartadas: encontram-se no CSV `p3-v2.3-quarentena-98-propostas.csv`, com informações históricas, propostas v2.2 e justificativas.

## Revisão individual das decisões

- **108** propostas v2.2 rastreadas e relatadas em `p3-v2.3-pareceres-108.csv`.
- **72** pareceres correspondentes à amostra original em `p3-v2.3-revisao-amostra-72.csv`.
- **10** registros realmente P3 revisados em `p3-v2.3-QA-10-P3-elegiveis.csv`.
- Os dois ajustes dentro da P3 são `41627` (“calcular cet mensal”) e `69676` (“cet custo efetivo total cálculo”). Foram alterados para intenção de cálculo contextual, pois dependem de dados do financiamento, e não apenas de consulta informativa.
- Os outros oito rótulos P3 foram preservados com ressalvas. Os 98 casos fora da P3 voltaram ao estado v2.1.

## Integridade independente

Os 30 lotes foram comparados linha a linha contra P3 v2.2, e as restaurações foram verificadas contra P3 v2.1. Verificação concluída com **294.905 registros-base, 2.190 controles**, somente os 100 IDs autorizados alterados, SHA-256 dos campos protegidos idêntico e filas P3/geral com todas as colunas históricas preservadas. Campos novos na fila armazenam apenas o parecer para os dez registros legitimamente P3.

## Cobertura e limites

A versão anterior reportava 20.292 casos P3 fora dos pilotos após subtrair erroneamente os 108 patches. Como somente dez eram P3, e um deles já havia sido revisado em etapas anteriores, o indicador corrigido estimado a partir da base histórica de 20.400 é **20.391**. Não equivale a uma recontagem editorial integral da P3.

As **4.660 pendências P2** seguem preservadas. As correções desta entrega são validações técnicas por registro, não homologação humana da taxonomia completa. Propostas para os 98 casos retirados devem ser encaminhadas ao planejamento de cobertura global e não readmitidas por regras P3 sem verificar prioridade/área.

## Entregáveis

- `lotes-001-a-030-p3-v2.3.zip`: os 30 CSVs atualizados.
- `p3-v2.3-fila-23965.csv`, `fila-geral-p0-p1-p2-p3-v2.3.csv`: filas completas com oito campos de histórico adicionais.
- `p3-v2.3-patches.csv`: 100 patches com antes/depois JSON exatos.
- `p3-v2.3-quarentena-98-propostas.csv`: propostas fora de escopo preservadas.
- `p3-v2.3-pareceres-108.csv`, `p3-v2.3-revisao-amostra-72.csv`, `p3-v2.3-QA-10-P3-elegiveis.csv`.
- `p3-v2.3-regressao-independente.csv/.json`, planilha centralizada e scripts Python.
