# Lote 019 — aprovado sob Taxonomia v1.1 + barras v2

## Status
**APROVADO**

## Métricas finais
- Keywords base: **9.831**
- Controles: **73**
- IDs base únicos: **9.831**
- Golden Set v1.1: **107/107**
- Controles incorporados preservados: **73/73**
- Reconstruções de `/`: **9**
- Conversões diretas sem metadados: **0**
- Flags finais: **0**
- Confiança alta: **6.104**
- Confiança média: **1.690**
- Confiança baixa: **2.037**
- Revisão manual: **2.162**

## Correções novas
Foi criada a camada **finalizar_auditar_lote_v1_10.py**. Ela:
- trata PDF/A como formato documental válido;
- reconhece variantes compactas como `pdf de word`, `pdf no word`, `pdf for excel` e `pdf for jpg` como conversão;
- mantém pares nus como `pdf e word` e `pdf x word` em `ambígua/revisão`;
- reclassifica buscas por livros identificados em PDF, como `leithold vol 1 pdf`, como conteúdo/documento.

No lote 019 foram corrigidos **2** casos de conteúdo/livro, **9** pares documentais/direcionais e **2** pares nus mantidos para revisão. As **10** flags PDF_CONTENT residuais foram resolvidas.

## Integridade
- Colunas originais preservadas: **sim**
- Área/cluster/subcluster vazios: **0**
- Taxonomia: **v1.1 congelada**
- XLSX de QA: células usadas centralizadas horizontal e verticalmente

## Propagação
O **lote 020 está liberado** e deve usar o lote 019 aprovado como treino/controle anterior, com finalizador v1.10.
