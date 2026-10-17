# Lote 011 — aprovado sob Taxonomia v1.1 + barras v2

## Status

**APROVADO.**

## Métricas finais

- Keywords base: **9.831**
- Controles incorporados: **73**
- IDs base únicos: **9.831**
- Golden Set v1.1: **107/107**
- Controles preservados: **73/73**
- Reconstruções de `/`: **51**
- Área/cluster/subcluster vazios: **0**
- Conversões diretas sem origem/destino/direção: **0**
- Flags finais: **0**
- Confiança alta: **6.321**
- Confiança média: **1.839**
- Confiança baixa: **1.671**
- Revisão manual: **1.722**

## Auditoria contextual

A primeira passagem deixou **4 flags FUEL_MARKET** em consultas como:

- `calcular valor combustivel por km`
- `calcular valor de combustivel por km`
- `calcular valor do combustivel por km`
- `valor de combustivel por km`

A revisão contextual mostrou que esses termos não pedem preço de mercado isolado; pedem custo relacionado a deslocamento. A família foi ampliada para cobrir também `calcular gasto combustivel rota` e `calcular rota e gasto de combustivel`.

Ao todo, **6 keywords** foram reclassificadas para:

`Energia > Combustíveis > Custo de viagem`

com intenção `estimativa de custo`, confiança alta e sem revisão manual.

Depois da correção, as **4 flags FUEL_MARKET** foram eliminadas e os invariantes estruturais permaneceram válidos.

## Governança

- Taxonomia v1.1 permanece ativa.
- Nenhuma Taxonomia v1.2 foi necessária.
- O novo comportamento foi encapsulado no `finalizar_auditar_lote_v1_5.py`.
- Lote 012 liberado.
