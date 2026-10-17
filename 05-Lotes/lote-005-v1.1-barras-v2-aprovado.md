# Lote 005 — Taxonomia v1.1 + barras v2

## Status

**APROVADO.**

## Estrutura

- Linhas totais: **9.904**
- Keywords base: **9.831**
- Controles: **73**
- IDs base únicos: **9.831**
- Colunas originais preservadas: **sim**
- Área/cluster/subcluster vazios: **0**

## QA

- Golden Set v1.1: **107/107**
- Controles incorporados: **73/73**
- Reconstruções de `/`: **47**
- Conversões diretas sem origem/destino/direção: **0**
- Flags finais: **0**

## Confiança

- alta: **6.363**
- média: **1.586**
- baixa: **1.882**
- revisão manual: **1.962**

## Correção adicional da auditoria

A auditoria inicial encontrou falsos positivos em `PDF_CONTENT`. A revisão manual/contextual separou três comportamentos:

1. criação/conversão real de PDF, por exemplo `jpg para pdf`, `pdf escaneado para word`, `enviar foto em pdf`;
2. edição pura de PDF sem formato de destino, que fica **fora de escopo**;
3. conteúdo de referência como `conversão de medidas pdf`, que pertence a **Conversores > Conversões gerais > Conversor genérico de unidades**, com intenção de **tabela/referência**.

Após essa correção, o lote ficou com **0 flags críticas/médias**.

## Planilhas e scripts

O QA XLSX foi gerado com todas as células usadas centralizadas horizontal e verticalmente. CSV permanece sem formatação visual por limitação do formato.

O pipeline reutilizável agora usa:

- `07-Scripts/classificar_lote_semantico_v1.py`
- `07-Scripts/posprocessar_lote_semantico_v1.py`
- `07-Scripts/finalizar_auditar_lote_v1_1.py`
- `07-Scripts/gerar_planilhas_centralizadas_v2.py`

## Próximo lote

**Lote 006 liberado.**
