# Relatório técnico — P3 v1.5

Data: 2026-10-21.

## Objetivo
Revisão crítica das **98 decisões** da amostra de expansão P3 v1.4, propagação *somente* de correções com evidência semanticamente equivalente e expansão conservadora de novas famílias P3.

## Resultados confirmados
- Amostra: **98 IDs únicos**. **5 correções diretas**, **12 decisões mantidas com ressalvas** e **81 mantidas sem erro evidente na análise contextual**.
- Correções de regras prévias: **41 IDs**, incluindo os 5 da amostra (31 taxas bancárias sem navegação explícita; 9 tutoriais de aposentadoria; 1 tutorial de jornada semanal).
- Expansão de P3 ainda fora dos pilotos: **78 registros, 35 famílias**; 78 passam a ter proposta contextual, **não aprovação editorial final**.
- **119 alterações totais** nos CSVs dos lotes, documentadas em `p3-v1.5-patches.csv`.
- **5 consultas** de salário mínimo envolvendo simultaneamente `hoje` e 2021/2022/2023 **não foram corrigidas automaticamente**, para evitar a criação de uma referência temporal falsa.
- P3 ainda fora dos pilotos: **20.985 → 20.907**; universo total P3 **23.965**.
- Regressão independente: **30/30 lotes PASSOU, 294.905 bases, 2.190 controles**, hashes SHA-256 de campos protegidos idênticos na origem e na saída: `a330038a4cc65cc89d02555d903e400167b2f4d168a2603edf0bb5d72250147f`.

## Tipos de correção
- Banco mencionado na keyword, sem `site`, `portal`, `login`, contratação explícita etc., NÃO estabelece intenção navegacional quando o texto procura taxa de juros. A intenção foi corrigida de `navegacional/transacional` para `informacional` nesses 31 casos.
- `como simular` / `como calcular aposentadoria` são pedidos de procedimento. Corrigidos 9 casos para informacional, sem negar a existência de ferramenta de cálculo como intenção secundária.
- `como calcular horas de trabalho semanal` foi igualmente tratado como tutorial informacional.
- Expansões restritas a domínios evidentes: títulos públicos, antecipação FGTS, crédito consignado, salário mínimo histórico, inflação acumulada, PA/PG e equação matemática indevidamente classificada fora de matemática.

## Arquivos essenciais
- `lotes-001-a-030-p3-v1.5.zip`: os 30 lotes completos atualizados; preserva todos os campos e controles.
- `p3-v1.5-fila-23965.csv` e `fila-geral-p0-p1-p2-p3-v1.5.csv`: filas completas com trilha P3 v1.5 sem substituir histórico P0–P3 v1.4.
- `p3-v1.5-amostra-98-pareceres.csv`: 98 resultados contextualizados.
- `p3-v1.5-decisoes-por-id.csv`, `p3-v1.5-patches.csv`: 119 mudanças com campos e JSON antes/depois reais.
- `p3-v1.5-exclusoes-contextuais.csv`: os 5 conflitos temporais preservados.
- `qa-auditoria-P3-v1.5-centralizada.xlsx`: resumo, amostra, decisões, patches, regras e regressão; todas as células usadas centralizadas.
- `p3-v1.5-regressao-independente-30-lotes.csv` e `p3-v1.5-regressao-resumo.json`: teste independente, separado do gerador.
- Fontes de reprodução (ZIP de lotes P3 v1.4, decisões, filas e amostra 98) incluídas em `FONTES-REPRODUCAO/`.
- Scripts e documentos em pastas próprias do vault.

## Limitações
Classificações originam-se de revisão textual assistida e regras específicas; teste PASSOU demonstra integridade estrutural e rastreabilidade, não veracidade editorial ou jurídica das 23.965 keywords. A área Saúde da taxonomia v1.2 ainda requer aprovação editorial. A P2 conserva **4.660 pendências** fora desta revisão.

## Próxima etapa
Auditar por amostragem as **78 novas classificações** (35 famílias) e ampliar P3 apenas nas classes com evidências robustas; não reduzir artificialmente as **20.907** pendências P3. Abordar separadamente as pendências da P2 e a aprovação de Saúde.
