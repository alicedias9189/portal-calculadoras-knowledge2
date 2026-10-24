# Auditoria P3 v2.1 — Revisão crítica da P3 v2.0

**Escopo:** 165 decisões na amostra estratificada de nove regras; 272 decisões da P3 v2.0 incluídas na trilha completa.

| Resultado | Quantidade |
|---|---:|
| Casos da amostra auditados | 165 |
| Corrigidos na amostra | 12 |
| Mantidos sem novos alertas | 23 |
| Mantidos com ressalvas | 130 |
| Correção adicional fora da amostra (CET) | 1 |
| **Total de patches em lotes** | **13** |
| **Regressão independente** | **30/30** |
| P3 ainda fora dos pilotos | 20.400 |
| P2 pendente | 4.660 |

As maiores correções foram de subcategorias de INSS. Consultas de taxas e consumo de veículos mantiveram o rótulo informacional com ressalvas explícitas, pois não fornecem dados suficientes para calcular um valor específico. A taxa de correção na amostra é **7,3% (12/165)**, não extrapolável à base porque a amostra foi estratificada e dirigida.

A regressão independente conferiu 13 patches por IDs, valores reais antes/depois e 30 lotes, além de duas filas consolidadas com 23.965 e 52.046 linhas. Todas as 294.905 keywords-base e 2.190 linhas de controle foram preservadas, assim como dados originais Ads e P0/P1/P2.

**Limite:** auditoria semântica textual; não checagem humana editorial completa e não validação de taxas, regras legais ou especificações de veículos vigentes.
