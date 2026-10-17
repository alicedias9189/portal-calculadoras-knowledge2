# Saneamento do L001 e triagem pós-30-lotes (v1)

Data: 2026-10-17.

## Correção delimitada

Origem: **73 keywords** do L001 com tipo `conversão direta` sem origem/destino/direção completos. O arquivo de classificação original foi preservado; o novo artefato é `saneamento-revisao-30-lotes/lote-001-saneado-v1.1-barras-v2.csv`.

- **7** conversões explícitas receberam metadados (BIN↔HEX, PLN→COP, timestamp→data legível).
- **66** keywords tiveram tipo de intenção reclassificado (30 tabelas/referências, 16 navegacionais, 10 ambíguas, 5 estimativas, 3 informacionais, 2 cotações atuais).
- **0** conversões diretas permaneceram sem metadados no L001 saneado.
- 73 controles idênticos; 9.831 IDs base e colunas originais intactos; nenhuma modificação fora dos 73 IDs.

## Revisão geral priorizada

Os 30 lotes possuem 294.905 keywords base, 52.050 marcadas originalmente. Após a atualização do L001, são **52.046 sinalizadas** em **15.117 famílias**. Triagem heurística:
- **P0:** 474 (patamar de buscas mensal 50.000+)
- **P1:** 2.557 (5.000+ ou indício de falso positivo)
- **P2:** 25.050 (intenção ambígua, 500+ ou múltiplos alertas)
- **P3:** 23.965 (prioridade posterior)

**A fila não representa revisão semântica humana concluída**. Casos exemplares de possível erro entre os P0 incluem `hoje e lua` em Finanças e `caixa simulador habitacional` em Datas. Não aplicar correção em massa sem avaliar a família e suas exceções.

Arquivos gerados para download no chat: fila total CSV, agrupamento por família CSV, 500 primeiras linhas CSV, correções detalhadas CSV, lote 001 saneado CSV e QA XLSX centralizado.

## Reprodução

Os scripts compactos `07-Scripts/sanear_lote_001_73_v1.py` e `07-Scripts/priorizar_revisao_30_lotes_v1.py` permitem reproduzir as regras-chave. O pacote entregável também inclui versões integrais da execução, inclusive o gerador XLSX via `artifact_tool`. Nunca somar mecanicamente volumes de buscas de variantes Google Ads.

## Pendência

Propor correções por famílias começando por P0 e P1; validar regressão Golden Set e propagações antes de reemitir os 30 lotes. A saída saneada do L001 não substitui automaticamente as entregas anteriores.
