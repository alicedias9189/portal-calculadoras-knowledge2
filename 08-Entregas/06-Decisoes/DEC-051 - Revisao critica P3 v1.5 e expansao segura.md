# DEC-051 — P3 v1.5: revisão da amostra 98 e expansão por evidência

Data: 2026-10-21. Aprovação: **versão paralela para auditoria, não homologação editorial**.

## Decisão
Aceitar 119 propostas de alteração pontual em P3 v1.5 após teste independente, sendo 41 correções da revisão das regras P3 v1.4 (5 encontradas diretamente nos 98 exemplos) e 78 novas classificações em 35 famílias. **Não** alterar P0, P1, P2, outras P3 nem registros de controle ou dados Ads.

## Regras revisadas
1. Busca de **taxa de juros** de banco sem site/ação explícita é **informacional**, mesmo que o nome do banco apareça na consulta (31 ajustes, intenção navegacional anterior incorreta).
2. **“Como calcular/simular”** aposentadoria é busca pelo método de cálculo, não prova de querer executar uma simulação naquela interface (9 correções).
3. **“Como calcular horas de trabalho semanal”** orienta método, não execução inequívoca (1 correção).
4. Reclassificar por regras fortes para áreas mal atribuídas (crédito, títulos públicos, FGTS antecipado, inflação, salários históricos, matemática); confiar no texto individual, não na família como um todo.
5. Expressões como **“salário mínimo 2022 hoje”** mantidas ambíguas, sem substituir ano pelo presente.

## Evidências
- Relatório: `08-Entregas/P3-v1.5/RELATORIO-P3-V1.5.md`.
- QA integral: `08-Entregas/P3-v1.5/qa-auditoria-P3-v1.5-centralizada.xlsx`.
- Trilha: `08-Entregas/P3-v1.5/p3-v1.5-patches.csv`.
- Teste independente PASSOU em **30 lotes, 294.905 IDs base, 2.190 controles**, SHA de campos protegidos `a330038a4cc65cc89d02555d903e400167b2f4d168a2603edf0bb5d72250147f`.

## Pendências
**20.907 P3** ainda fora dos pilotos; **4.660 P2** pendentes em trilha paralela; escopo de Saúde da P3 v1.2 ainda sujeito a homologação. Próximo passo: auditar amostra das 78 novas decisões e considerar expansão adicional sem forçar classificação.
