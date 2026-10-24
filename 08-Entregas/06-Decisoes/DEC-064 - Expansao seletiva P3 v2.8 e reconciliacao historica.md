# DEC-064 — Expansão seletiva P3 v2.8 com bloqueio de escopo

Data: 22/10/2026. Decisão técnica auditável, sem homologação editorial independente.

1. Operar somente sobre `prioridade=P3` nas duas filas, linha `FORA_DO_PILOTO` sem status de expansão anterior, e checar ID, Keyword, família e lote originais na fonte física.
2. Autorizar 66 alterações em 37 famílias, registradas por regra e valores antes/depois, em paralelo aos 30 lotes da P3 v2.7.
3. Preservar TODOS os campos não analíticos, todos os controles e os 98 casos do backlog global.
4. Não completar dados omitidos, como tempo na relação W–kWh, taxas de bancos, números a converter ou alíquotas previdenciárias.
5. Formalizar divergência de 9 no total histórico de P3 fora dos pilotos: contagem de status reconstruída=20.374 antes e 20.308 após 66 patches; relatório P3 v2.7 dizia 20.383.
6. Homologação editorial continua pendente; próxima fase é revisão crítica dos 66 novos ajustes, não expansão automática indiscriminada.

Verificações: 30/30 lotes, 294.905 registros-base, 2.190 controles; 105 testes do seletor; 66 patches conferidos por regressão independente.
