# DEC-045 — P2 v7 conservadora e prioridade da próxima auditoria

Data: 2026-10-20. Continuidade de DEC-044 (P2 v6).

**Decisão:** registrar 101 revisões contextuais de P2, com 28 sem ressalva e 73 com ressalva, distribuídas por 81 famílias. Manter abertas **4.660 keywords** da P2, sem atribuir uma intenção apenas porque termos compartilham família. Preservar P0/P1 e classificações P2 anteriores.

**Evidência estrutural:** regressão independente PASSOU 30/30, com 294.905 registros-base, 2.190 controles, patches antes/depois confrontados com CSVs reais, nenhuma mudança fora dos IDs-alvo e dos campos autorizados. Não equivale à aprovação editorial humana nem à reexecução do Golden Set.

**Análise de retorno:** a P2 v7 resolveu 101/4.761 (2,12%) nesta passagem, com 4.660 restantes. A fila P3 contém 23.965 keywords e 9.278 famílias ainda não auditadas neste fluxo.

**Prioridade aprovada para proposição:** começar P3 v1 com piloto de alto impacto, auditoria por famílias e testes de regressão, mantendo a P2 v7 como versão paralela preservada e as 4.660 pendências abertas para revisão dirigida. Não abrir P3 como classificada sem executar o processo.

**Evidência:** `08-Entregas/P2-v7/RELATORIO.md`, ZIP de auditoria, patches CSV, QA Excel e scripts.
