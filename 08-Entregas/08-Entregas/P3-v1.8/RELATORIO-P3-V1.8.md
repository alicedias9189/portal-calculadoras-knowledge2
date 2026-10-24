# Relatório — P3 v1.8

## Base e escopo
A partir do pacote P3 v1.7, quantificou-se a revisão por regra da amostra P3 v1.7 e foi aplicada uma expansão conservadora em casos novos da fila P3.
- Universo P3: 23.965; candidatos fora dos pilotos antes: 20.755.
- **83 alterações** em 40 famílias; fora dos pilotos depois: **20.672**.
- Por regra: {"media_ponderada": 20, "irrf_tributario_contextual": 27, "ferias_medias": 5, "dias_uteis_calendario": 3, "dias_uteis_contagem": 4, "conversao_energia_dimensional": 6, "regra_tres": 4, "poupanca_taxa_informacao": 14}.
- Os campos numéricos de Ads não foram editados nem recomputados; não se somaram volumes de variantes.

## Como interpretar a taxa de erro
A amostra anterior de 103 registros incluiu deliberadamente todas as 17 exceções conhecidas. Seus percentuais são um **indicador de risco de regra dentro dessa revisão dirigida**, não a taxa de falsos positivos de toda a regra nem intervalo de confiança estatístico. Em particular, n=1 ou n=5 tem alta incerteza.

## Proteções
Regressão independente dos lotes P3 v1.7 × v1.8: 30/30 passaram, 294.905 bases, 2.190 controles, 83 patches sem mudanças em campos protegidos. Filas completas de 23.965 e 52.046 linhas preservam as colunas anteriores (acréscimo apenas de rastreamento P3 v1.8).

## Limitações de julgamento semântico
Classificação por regras conservadoras com revisão de exemplos; não é homologação editorial individual. O campo `revisao_manual=sim` solicita auditoria, não declara aprovação humana. IRRF depende de ano/regime, poupança depende de período e regras; conversões dimensionais só aceitas para grandezas homogêneas e origem/destino escritos. Não inferir taxas financeiras correntes.

## Entregáveis
- `lotes-001-a-030-p3-v1.8.zip` — 30 CSVs integrais, todas as colunas originais.
- `p3-v1.8-fila-23965.csv`, `fila-geral-p0-p1-p2-p3-v1.8.csv` — filas com rastreamento.
- `p3-v1.8-patches.csv`, `p3-v1.8-decisoes.csv` — trilha por ID; `p3-v1.8-qa-taxas-por-regra.csv` — riscos observados na amostra.
- `p3-v1.8-regressao-independente-30-lotes.csv` e resumo JSON — prova estrutural independente.
- `qa-P3-v1.8-centralizada.xlsx` — síntese centralizada e amostras; os CSVs detêm o universo completo.
- Scripts reproduzíveis em `07-Scripts/P3/` e fontes P3 v1.7 em `FONTES-REPRODUCAO/`.
