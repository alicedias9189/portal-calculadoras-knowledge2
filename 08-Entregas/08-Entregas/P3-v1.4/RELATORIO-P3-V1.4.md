# Relatório técnico — Auditoria P3 v1.4

## Resultados
- Amostra crítica herdada de P3 v1.3: **67 IDs**, com **2 correções** e **3 ressalvas editoriais** documentadas; **62 sem incoerência evidente**.
- Expansão controlada: **576 keywords**, distribuídas em **170 famílias**.
- Patches totais aplicados: **578**.
- P3 fora dos pilotos: **21.561 → 20.985**. Universo P3: **23.965**.
- Integridade estrutural: **294.905 bases**, **2.190 controles**, **30/30 lotes** com regressão independente PASSOU.
- Os valores antes/depois de cada alteração correspondem aos CSVs; os dados históricos e Google Ads ficaram inalterados.

## Regras — quantidade de ajustes
- `consulta_taxa_credito_instituicao`: 86 registros
- `jornada_trabalho_semanal`: 34 registros
- `direitos_trabalhistas_gestante`: 116 registros
- `sac_price_comparacao`: 7 registros
- `percentual_excel_educacional`: 26 registros
- `simulacao_aposentadoria_previdencia`: 38 registros
- `saque_aniversario_antecipacao`: 24 registros
- `horas_extras_domingo`: 23 registros
- `fundos_consulta_rentabilidade`: 29 registros
- `salario_liquido_descontos`: 57 registros
- `comparacao_cdi_cdb`: 33 registros
- `custo_combustivel_viagem`: 20 registros
- `rendimento_conta_digital`: 43 registros
- `fracao_calculadora_celular`: 1 registros
- `cdi_historico`: 18 registros
- `concreto_piso_garagem`: 1 registros
- `demanda_eletrica`: 15 registros
- `tributacao_cdb_consulta`: 7 registros

## Arquivos essenciais
- `lotes-001-a-030-p3-v1.4.zip`: todos os 30 CSVs de lotes (versão paralela).
- `p3-v1.4-fila-23965.csv` e `fila-geral-p0-p1-p2-p3-v1.4.csv`: filas atualizadas com campos de rastreamento adicionais.
- `p3-v1.4-patches.csv`: campos antes/depois reais por ID; `p3-v1.4-decisoes-por-id.csv`: justificativas.
- `p3-v1.4-amostra-67-pareceres.csv`: registros revisados individualmente.
- `qa-auditoria-P3-v1.4-centralizada.xlsx`: resumo, amostra, propostas, testes, amostra da nova expansão; todas as células utilizadas centralizadas.
- `regressao-independente-30-lotes-p3-v1.4.csv`: testes por lote; `regressao-independente-resumo-v1.4.json`: conclusão.
- Quatro scripts Python e fontes da P3 v1.3 necessários à reprodução incluídos neste ZIP.

## Ressalva
As propostas foram geradas por regras e revisões textuais orientadas por contexto. `PASSOU` refere-se a integridade do processamento e dos campos protegidos; não é certificação da precisão editorial de cada rótulo.
