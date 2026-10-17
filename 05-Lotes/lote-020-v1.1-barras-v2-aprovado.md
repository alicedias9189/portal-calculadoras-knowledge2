# Lote 020 — aprovado sob Taxonomia v1.1 + barras v2

## Status
**APROVADO**

## Métricas finais
- Keywords base: **9.831**
- Controles: **73**
- IDs base únicos: **9.831**
- Golden Set v1.1: **107/107**
- Controles incorporados preservados: **73/73**
- Reconstruções de `/`: **28**
- Conversões diretas sem metadados: **0**
- Flags finais: **0**
- Confiança alta: **6.966**
- Confiança média: **1.456**
- Confiança baixa: **1.409**
- Revisão manual: **1.500**

## Correção nova
Foi criada a camada **finalizar_auditar_lote_v1_11.py** para reconhecer `transformador` como substantivo de ferramenta de transformação/conversão quando aplicado a PDF. No lote 020, **21** keywords foram normalizadas sob essa regra e as **4** flags PDF_CONTENT residuais foram removidas.

## Integridade
- Colunas originais preservadas: **sim**
- Área/cluster/subcluster vazios: **0**
- Taxonomia: **v1.1 congelada**
- XLSX de QA: células usadas centralizadas horizontal e verticalmente

## Propagação
O **lote 021 está liberado** e deve usar o lote 020 aprovado como treino/controle anterior, com finalizador v1.11.
