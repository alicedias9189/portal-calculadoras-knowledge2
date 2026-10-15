# DEC-004 - Taxonomia Mestre v1.1

## Contexto

A Taxonomia v1 foi testada no lote 001 completo. A auditoria pós-classificação encontrou regressões sistemáticas fora dos 73 controles originais, incluindo potência elétrica confundida com potenciação matemática, direitos trabalhistas em Datas, cotação cambial como conversão, consultas de combustível como consumo e erros de extração monetária.

Além disso, 1.241 keywords estavam com área atribuída mas sem cluster/subcluster da v1.

## Decisão

A Taxonomia v1 é substituída operacionalmente pela **Taxonomia Mestre v1.1**.

A v1.1:

- adiciona 24 subclusters;
- amplia as regras globais para R01–R26;
- amplia o Golden Set de 73 para 107 casos;
- resolve os 1.241 registros sem cluster/subcluster do lote 001;
- mantém revisão manual para ambiguidades reais, mas não permite campos taxonômicos vazios;
- exige auditoria pós-classificação antes de liberar o lote seguinte.

## Critério de aceitação

O lote 001 reclassificado deve atender simultaneamente a:

1. 9.831 IDs base únicos e íntegros;
2. nenhuma alteração indevida das colunas originais;
3. nenhum campo área/cluster/subcluster vazio;
4. Golden Set v1.1 em 107/107;
5. zero regressões críticas nas famílias de erro descobertas na primeira auditoria.

## Resultado

O lote 001 reclassificado foi **APROVADO** segundo esses critérios.

## Consequência

O lote 002 pode ser iniciado usando:

- [[../00-Mapa-Global/Taxonomia Mestre v1.1]];
- [[../02-Regras/Regras v1.1 - R19-R26]] em conjunto com as regras anteriores;
- [[../04-Regressao/Golden Set v1.1]].

Qualquer nova regressão crítica interrompe a sequência e exige nova decisão versionada antes de continuar.
