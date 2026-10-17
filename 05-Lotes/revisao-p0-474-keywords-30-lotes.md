# Revisão semântica P0 — 474 keywords dos lotes 001–030

Data: 2026-10-17. Taxonomia v1.1 + barras v2.

## Resultado confirmado
- P0 revisadas individualmente: **474**, em **285 famílias**.
- Registros com alterações: **462** (inclui confiança e status de revisão, além de mudanças de classe).
- Alterações de área: **102**; alterações de tipo de intenção: **300**.
- Marcações P0 resolvidas: **365**; P0 ainda sem contexto suficiente: **109**.
- Revisões manuais do acervo: **52.046 → 51.681** (P1–P3 inalterados).
- Keywords base: **294.905** em **30 lotes**.
- **2.190/2.190** controles incorporados comparados e preservados; **0** conversões diretas base sem metadados.
- O histórico anterior Golden 107/107 por lote não comprova individualmente as 462 correções novas. É regressão estrutural, não reavaliação de Golden.

## Política de alterações
Não alterar Keyword, IDs, dados Google Ads ou registros de controle. Preservar lotes originais e publicar CSVs paralelos para cada lote. Não extrapolar as correções para P1/P2/P3 nem para famílias inteiras sem análise contextual.

Exemplos: empréstimos da Caixa saíram de Datas, cotação do dólar saiu de unidade física, horas extras saíram de cálculos com datas, preço de ouro saiu de folha trabalhista, fórmulas de juros compostos saíram de geometria.

## Artefatos
A entrega da conversa contém ZIP separado com (i) auditoria, QA XLSX centralizado, CSV de 474 decisões, CSV de 462 patches antes/depois, 109 pendências e scripts originais; (ii) 30 lotes CSV corrigidos, com manifesto SHA-256. Arquivos grandes não são versionados neste repositório.

No GitHub, usar `07-Scripts/aplicar_correcoes_p0_de_csv_v1.py` com o CSV de correções incluído no pacote, para reproduzir alterações a partir do acervo local; o script autoral completo da triagem está no ZIP da entrega.
