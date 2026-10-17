# DEC-009 - Lote 004 aprovado e scripts no cofre

## Decisões

1. O lote 004 está **APROVADO** sob Taxonomia v1.1 + regras R01–R26 + Golden Set v1.1 + mapa mestre de barras v2.
2. O lote 005 está liberado.
3. A partir desta decisão, toda planilha XLSX gerada no projeto deve manter **todas as células usadas centralizadas horizontal e verticalmente**.
4. CSV continua sendo usado para processamento/intercâmbio e não possui formatação visual.
5. Todo script usado no pipeline deve ter uma versão reutilizável salva em `07-Scripts/` no cofre.

## Scripts reutilizáveis salvos

- `07-Scripts/classificar_lote_semantico_v1.py`
- `07-Scripts/finalizar_auditar_lote_v1.py`
- `07-Scripts/posprocessar_lote_semantico_v1.py.part1`
- `07-Scripts/posprocessar_lote_semantico_v1.py.part2`
- `07-Scripts/instalar_pipeline_semantico_v1.py`
- `07-Scripts/gerar_qa_centralizado_v1.py`
- `07-Scripts/README.md`

O pós-processador é armazenado em duas partes no GitHub/Obsidian e reconstruído pelo instalador. O instalador valida o SHA-256 do script completo antes de utilizá-lo.

## Lote 004

- base: **9.831**
- controles: **73**
- Golden: **107/107**
- reconstruções de `/`: **21**
- conversões diretas sem metadados: **0**
- flags críticas/médias: **0**
- confiança alta: **6.592**
- confiança média: **1.655**
- confiança baixa: **1.584**
- revisão manual: **1.678**

## Governança

As versões reutilizáveis dos scripts devem evoluir junto com as regras de auditoria. Mudanças sistemáticas encontradas em lotes futuros devem ser incorporadas ao pipeline e registradas no cofre antes de serem propagadas automaticamente.
