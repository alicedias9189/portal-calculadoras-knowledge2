# Lote 021 — aprovado sob Taxonomia v1.1 + barras v2

## Status
**APROVADO**

## Métricas finais
- Keywords base: **9.830**
- Controles: **73**
- IDs base únicos: **9.830**
- Golden Set v1.1: **107/107**
- Controles incorporados preservados: **73/73**
- Reconstruções de `/`: **26**
- Conversões diretas sem metadados: **0**
- Flags finais: **0**
- Confiança alta: **6.643**
- Confiança média: **1.572**
- Confiança baixa: **1.615**
- Revisão manual: **1.728**

## Correção nova
Foi criada a camada **finalizar_auditar_lote_v1_12.py** para reconhecer verbos de conversão em inglês (`convert`/`conversion`) e formatos CAD como DWG/DXF em pares com PDF. O falso positivo `convert pdf dwg` deixou de ser tratado como conteúdo PDF e passou a conversão de arquivo. A regra também normaliza outros pares PDF↔CAD inequívocos encontrados no lote.

## Integridade
- Colunas originais preservadas: **sim**
- Área/cluster/subcluster vazios: **0**
- Taxonomia: **v1.1 congelada**
- XLSX de QA: células usadas centralizadas horizontal e verticalmente

## Observação estrutural
Este lote possui **9.830** keywords base, uma a menos que a maioria dos lotes anteriores; o total é coerente com o arquivo de entrada e os IDs base permanecem únicos, portanto não há perda de linha no processamento.

## Propagação
O **lote 022 está liberado** e deve usar o lote 021 aprovado como treino/controle anterior, com finalizador v1.12.
