# DEC-015 - Lote 010 aprovado sob v1.1 e barras v2

## Decisão

O lote 010 foi aprovado sem alteração da Taxonomia v1.1.

A classificação continua usando:

- Taxonomia v1.1;
- regras R01–R26;
- Golden Set v1.1;
- mapa mestre de barras v2;
- classificador semântico v1;
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

Uma keyword de licença-maternidade em dias caiu inicialmente em Datas, mas a regra R21 já existente na cadeia v1.2 a corrigiu para `Trabalho > Afastamentos > Licenças e afastamentos`. Como a regra existente resolveu o padrão, não foi criada uma nova versão do finalizador.

## Continuidade

O lote 011 está liberado para usar o lote 010 como treino e controle anterior. O `07-Scripts/README.md` foi atualizado com o comando correspondente.
