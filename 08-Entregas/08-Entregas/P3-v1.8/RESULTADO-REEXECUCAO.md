# Reprodução independente confirmada

A execução `auditar_p3_v18.py` e `regressao_independente_p3_v18.py` com as quatro fontes P3 v1.7 incluídas neste pacote gerou:
- 30/30 CSVs de lotes idênticos em conteúdo SHA-256 aos lotes entregues.
- `p3-v1.8-patches.csv`, `p3-v1.8-decisoes.csv`, `p3-v1.8-qa-taxas-por-regra.csv`, as duas filas e o resumo da regressão idênticos em bytes.
- 294.905 registros-base e 2.190 controles preservados; 83 patches corretos.

O ZIP binário recompactado pode diferir nos metadados de timestamps, embora o conteúdo de cada CSV reproduza o original.
