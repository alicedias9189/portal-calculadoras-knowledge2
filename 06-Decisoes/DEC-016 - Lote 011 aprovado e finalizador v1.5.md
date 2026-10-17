# DEC-016 — Lote 011 aprovado e finalizador v1.5

## Contexto

Durante a auditoria do lote 011, quatro consultas sobre `valor de combustível por km` foram sinalizadas como `FUEL_MARKET`, embora o contexto indicasse custo de deslocamento e não preço de mercado isolado.

## Decisão

Quando uma keyword contiver combustível + linguagem de custo/gasto/valor + vínculo explícito com deslocamento (`por km`, `km rodado`, `rota`, `trajeto`, `viagem`, `distância` ou `percurso`), classificar como:

`Energia > Combustíveis > Custo de viagem`

com intenção `estimativa de custo`.

Essa regra não se aplica a consultas de preço atual de gasolina, etanol, diesel ou combustível sem relação com distância/rota, que continuam sendo preço/mercado conforme R22.

## Implementação

Criado `07-Scripts/finalizar_auditar_lote_v1_5.py`, executado após a cadeia v1.4.

No lote 011, a regra corrigiu **6 keywords** e removeu **4 flags FUEL_MARKET** residuais. O lote terminou com:

- Golden Set: **107/107**
- controles incorporados: **73/73**
- conversões diretas sem metadados: **0**
- flags finais: **0**
- status: **APROVADO**

## Impacto

A Taxonomia v1.1 permanece suficiente; não foi criada v1.2. O lote 012 deve usar o finalizador v1.5.
