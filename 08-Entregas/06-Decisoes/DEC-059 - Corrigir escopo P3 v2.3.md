# DEC-059 — Correção de escopo e revisão crítica P3 v2.3

**Data:** 2026-10-22. **Situação:** decisão técnica documentada; não é aprovação editorial integral.

## Problema

P3 v2.2 alterou 108 registros, mas somente 10 IDs constavam da fila P3. A amostra QA de 72 abrangia apenas quatro registros P3. Fazer nova expansão a partir dessas classificações sem identificar o desvio propagaria uma violação de escopo.

## Decisão aplicada

1. Restaurar os 98 registros fora da P3 aos campos analíticos da versão v2.1, preservando todas as mudanças legítimas até essa versão.
2. Arquivar os 98 candidatos excluídos em quarentena auditável, em vez de apagá-los.
3. Revisar todos os dez elegíveis; refinar a intenção dos IDs 41627 e 69676; não alterar os outros oito.
4. Preservar todas as linhas, IDs, controles, colunas e métricas Ads; acrescentar às filas apenas a rastreabilidade da P3 v2.3.
5. Bloquear expansões futuras que não façam interseção do conjunto candidato com a fila de IDs priorizados da etapa.

## Evidências e verificações

`08-Entregas/P3-v2.3/RELATORIO-P3-V2.3.md`, planilha QA, CSVs e scripts. Regressão comparada com a v2.2 e restaurações com a v2.1; 30 lotes aprovados.

## Próximas etapas

Validar a priorização e o escopo das 98 propostas retiradas (P3 versus outras áreas/fora da fila). Somente após resolver o processo de triagem ampliar a P3 com filtros obrigatórios de elegibilidade.
