# DEC-015 - Lote 010 aprovado sob v1.1 e barras v2

## Decisão

O lote 010 foi aprovado sem alteração da Taxonomia v1.1.

A classificação passa a usar:

- Taxonomia v1.1;
- regras R01–R26;
- Golden Set v1.1;
- mapa mestre de barras v2;
- **classificador semântico v1.1**;
- pós-processador semântico v1;
- finalizador/auditor v1.4;
- gerador de planilhas centralizadas v2.

## Auditoria

A auditoria final confirmou:

- **107/107** no Golden Set;
- **73/73** controles preservados;
- **60** reconstruções de `/` aplicadas;
- **0** conversões diretas sem metadados;
- **0** flags finais;
- colunas originais preservadas;
- nenhuma necessidade de Taxonomia v1.2.

Uma keyword de licença-maternidade em dias caiu inicialmente em Datas, mas a regra R21 já existente na cadeia v1.2 a corrigiu para `Trabalho > Afastamentos > Licenças e afastamentos`.

## Classificador v1.1

Durante a primeira execução do lote 010, o `LinearSVC` do classificador v1 emitiu `ConvergenceWarning`. A versão `classificar_lote_semantico_v1_1.py` aumenta `max_iter` para **10.000** nos dois classificadores e convergiu sem warning.

A reexecução manteve as classificações semânticas e alterou apenas a camada de confiança de uma keyword (`calcular gasto tinta parede`), de baixa/revisão para média/sem revisão. A nova distribuição final é:

- confiança alta: **7.003**;
- confiança média: **1.463**;
- confiança baixa: **1.365**;
- revisão manual: **1.462**.

## Continuidade

O lote 011 está liberado para usar o lote 010 como treino e controle anterior. O `07-Scripts/README.md` foi atualizado para usar o classificador v1.1.
