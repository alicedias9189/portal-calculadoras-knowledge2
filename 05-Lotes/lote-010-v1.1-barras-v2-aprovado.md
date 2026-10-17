# Lote 010 — v1.1 + barras v2 — APROVADO

## Resultado

- Keywords base: **9.831**
- Controles: **73**
- IDs base únicos: **9.831**
- Golden Set v1.1: **107/107**
- Controles incorporados preservados: **73/73**
- Reconstruções de `/`: **60**
- Área/cluster/subcluster vazios: **0**
- Conversões diretas sem origem/destino/direção: **0**
- Flags finais: **0**
- Confiança alta: **7.003**
- Confiança média: **1.463**
- Confiança baixa: **1.365**
- Revisão manual: **1.462**

## Auditoria contextual

A primeira passagem encontrou **1** caso R21 em que uma consulta de direito/licença havia caído em Datas:

- `licença maternidade sao quantos dias`

A camada v1.2, já incorporada à cadeia do finalizador v1.4, corrigiu a keyword para `Trabalho > Afastamentos > Licenças e afastamentos`. Depois da correção, a auditoria ficou com **0 flags**.

## Classificador v1.1

O classificador v1 original emitiu `ConvergenceWarning` do `LinearSVC` no lote 010. Foi criada a versão reutilizável `classificar_lote_semantico_v1_1.py`, que mantém a mesma lógica e aumenta `max_iter` de 1.000 para **10.000** nos dois modelos.

A reexecução convergiu sem warning. As classificações de área/cluster/subcluster/intenção permaneceram iguais; apenas uma keyword (`calcular gasto tinta parede`) passou de confiança baixa/revisão para confiança média sem revisão, coerente com `Construção > Pintura > Tinta e pintura`.

Não houve necessidade de alterar a Taxonomia v1.1 nem criar uma nova versão do finalizador.

## Planilha

O workbook de QA foi regenerado após a reexecução e verificado com todas as células usadas centralizadas horizontal e verticalmente, conforme a regra do projeto.

## Decisão

O lote 010 está aprovado sob **Taxonomia v1.1 + R01–R26 + barras v2 + classificador v1.1 + finalizador v1.4**. O lote 011 está liberado.
