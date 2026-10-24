# DEC-043 — Auditoria semântica focalizada P2 v5

Data: 2026-10-20.

**Decisão:** aceitar a P2 v5 como **versão paralela auditável**, aplicando 414 reclassificações contextuais aos registros ainda pendentes da P2 v4, sem editar os arquivos históricos. Usar a mesma taxonomia e preservar dados originais/Google Ads, P0/P1/P3 e controles.

- 5.562 pendências na entrada; 414 registros alterados em 185 famílias; 181 sem ressalva de regra e 233 com ressalva; 5.148 permanecem abertos.
- Comparação independente de 30 lotes: PASSOU, 294.905 IDs-base e 2.190 controles preservados.
- Corrigida a trilha antes/depois para refletir os CSVs reais de v4/v5. Não chamar o registro anterior na fila de "antes" da base.
- Não assumir gravidez para 157 consultas só com semanas e dias; não assumir destino em 68 consultas Fahrenheit isoladas; reconhecer o caso explícito Fahrenheit → K.
- Dados completos, lote a lote, residem nos ZIPs em `08-Entregas/P2-v5/`; planilha Excel é auditoria centralizada resumida.

**Status:** revisão por regras com QA estrutural aprovada; NÃO homologação editorial da P2 nem das 5.148 pendências restantes.

Relatório: [[08-Entregas/P2-v5/RELATORIO]]. Próxima etapa: análise focalizada v6 de famílias ainda pendentes.
