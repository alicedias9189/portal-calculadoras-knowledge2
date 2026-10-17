# Lote 008 — Taxonomia v1.1 + barras v2 — APROVADO

## Resumo

- Linhas totais: **9.904**
- Keywords base: **9.831**
- Controles: **73**
- IDs base únicos: **9.831**
- Colunas originais preservadas: **sim**
- Área/cluster/subcluster vazios: **0**
- Golden Set v1.1: **107/107**
- Controles incorporados: **73/73**
- Reconstruções de `/`: **90**
- Conversões diretas sem origem/destino/direção: **0**
- Flags finais: **0**

## Confiança

- alta: **6.426**
- média: **1.735**
- baixa: **1.670**
- revisão manual: **1.800**

## Ajuste validado no lote 008

A auditoria encontrou dois falsos positivos `PDF_CONTENT` em consultas que eram conversões inequívocas mesmo sem verbo:

- `pdf em imagem`
- `pdf em xml`

Foi criado o `finalizar_auditar_lote_v1_4.py`, que reconhece pares explícitos de formato com direção por `em/para/to` e mantém esses casos em `Conversores > Arquivos e documentos > Documentos e PDF`, com intenção `conversão de arquivo/mídia`.

## Planilhas

O workbook de QA foi gerado com todas as células usadas centralizadas horizontal e verticalmente, conforme regra do projeto.

## Decisão

**Lote 008 aprovado. Lote 009 liberado.**
