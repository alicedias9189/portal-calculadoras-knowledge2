# P2 v4 — Auditoria contextual por famílias

Data: 2026-10-18. Fonte: P2 v3, sem alterar originais. Relacionada à DEC-042.

## Resultado auditado

| Indicador | Valor |
|---|---:|
| P2 total | 25.050 |
| Pendências analisadas (v3) | 5.946 |
| Reclassificadas nesta rodada | **384** |
| Regras sem ressalvas operacionais | 109 |
| Classificadas com ressalva | 275 |
| Pendências restantes | **5.562** |
| Famílias presentes na fila v3 | 2.983 |
| Famílias com pelo menos um patch | 143 |
| Base total preservada | 294.905 |
| Controles preservados | 2.190 |
| Lotes com QA independente aprovado | 30 |

**Não confundir com a triagem preliminar de 388 registros.** A checagem contextual identificou quatro falsos positivos potenciais (torque versus comprimento, tabela e padrões de volume ambíguos). Foram excluídos antes da reexecução final.

## Regras aplicadas na v4

| Regra | Reclassificadas |
|---|---:|
| Simulação de rendimento | 184 |
| Unidades mesma dimensão, direção explícita | 98 |
| Tijolos por área | 19 |
| Intervalos de tempo | 13 |
| Fatoração | 12 |
| Cálculo de área/volume | 12 |
| Consumo de combustível | 11 |
| Arredondamento | 11 |
| Moedas com par explícito | 10 |
| Conversão de formatos | 10 |
| Ano bissexto | 3 |
| Cotação monetária sem par | 1 |

## Controle de qualidade

A verificação independente `auditar_regressao_p2_v4.py` comparou os **30 pares de CSV v3/v4** linha por linha. Verificou unicidade dos 294.905 IDs-base, 73 controles em cada lote, estabilidade de todas as colunas não analíticas, estabilidade de todos os IDs não selecionados e ausência de mudanças em controle, P0/P1/P3. As 384 mudanças só atingem onze campos analíticos conhecidos. Os 25.050 registros P2 permanecem representados na fila de decisões. Conversões diretas aprovadas por regra têm origem e destino não vazios.

Algumas classificações receberam a marca **COM_RESSALVA** porque faltam prazo, taxa, material, densidade, unidade de referência ou outros parâmetros; não converter isso em uma fórmula com dados inventados.

## Fontes e artefatos

- `lotes-001-a-030-p0-p1-p2-v4.zip`: 30 CSVs atualizados, versão paralela.
- `auditoria-p2-v4-csv-integral.zip`: decisões 25.050; patches 384; fila geral; pendências 5.562; QA 30 lotes; resumo das 2.983 famílias.
- `qa-validacao-p2-v4-centralizada.xlsx`: planilha centralizada com resumo, 12 regras, 384 patches e amostras prioritárias. **Os dados completos estão nos CSVs**, não apenas na planilha.
- `resumo-p2-v4.json`, `regressao-independente-p2-v4.json`: métricas e checks de qualidade.
- Scripts `.py` em `07-Scripts/`: reproduzem revisão, regressão e QA Excel.
- Para reexecutar: os dois ZIPs da P2 v3 estão incluídos em `08-Entregas/P2-v3/` neste pacote.

## Limites

A revisão foi feita por regras verificáveis e leitura focalizada de amostras, e **não** por conferência editorial individual de todas as 5.946 queries. Os termos restantes continuam pendentes. Não somar volume Google Ads entre variantes como se fossem buscas adicionais. Não alterar a taxonomia antiga ou versões homologadas silenciosamente.

## Próximo passo

Aprofundar análise editorial das famílias com maior número de pendências, especialmente 157 variantes «N semanas e D dias» e 69 valores isolados em Fahrenheit, sem deduzir automaticamente gravidez ou unidade de destino. Depois revisar classes comerciais e financeiras ainda não resolvidas e os casos de ambiguidades na reconstrução de barras.
