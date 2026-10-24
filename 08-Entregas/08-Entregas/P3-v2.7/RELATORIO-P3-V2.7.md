# P3 v2.7 — Revisão crítica P3 e fila global B/C

**Data de execução:** 22/10/2026 (horário local). **Natureza:** auditoria técnica/contextual; não equivale a homologação editorial independente.

## Escopo e resultados

- 17 alterações P3 originadas na v2.6 revistas individualmente; **1 refinamento semântico** no ID `190795`, expressão `novo piso do inss`.
- O subgrupo anterior `Piso e reajuste de benefícios do INSS` pressupunha benefícios. A expressão não especifica se se trata de piso de benefício, contribuição ou outra referência; na v2.7 o subgrupo passa a `Piso previdenciário (natureza a confirmar)`, reduzindo a confiança e registrando revisão necessária.
- 16 decisões P3 preservadas com ressalvas operacionais/previdenciárias e sem alteração dos lotes.
- 48 propostas globais fora de P0–P3 examinadas (30 média, 18 baixa/complexa). **5 propostas refinadas nos pareceres**; **43 mantidas com ressalvas**. **Zero propostas globais aplicadas**.
- As 50 propostas globais de alta prioridade, já revisadas na v2.6, foram mantidas no backlog com todas as colunas históricas intactas.
- Não houve promoção automática de prioridade nem aplicação de taxas/benefícios previdenciários reais.

## Critérios da revisão global

- **CET:** diferenciar consulta informacional, explicação de como calcular e busca por calculadora; CET inclui custos e encargos, não é igual a juros nominais. Banco citado não define intenção navegacional por si só.
- **IRRF:** consultas sobre tabela e base são informacionais; cálculo depende da base, ano e regime. Para históricos, não inferir que tabelas atuais se aplicam.
- **Financiamento imobiliário:** perguntas sobre taxas são informacionais ou comparativas; taxa atual depende da instituição, produto, período e condições. Não classificá-las como simulação sem entradas.
- **INSS:** distinguir consulta sobre desconto de salário de serviço de consulta e da ferramenta conjunta INSS+IRPF.

## Integridade

- 30/30 lotes aprovados por regressão independente.
- **294.905 registros-base e 2.190 controles preservados.**
- **1 único ID alterado nos campos analíticos autorizados**; patches antes/depois conferidos contra ZIPs reais.
- P3 v2.6 e seus arquivos-fonte incluídos como base de reprodução separada, sem sobrescrita.
- Fila P3 com 23.965 linhas e fila geral com 52.046 linhas: todas as colunas e valores históricos preservados, novas colunas de parecer v2.7 acrescentadas.
- As 98 propostas do backlog global mantêm as colunas anteriores; somente foram adicionadas colunas de parecer para os 48 casos B/C.
- P3 ainda fora dos pilotos: **20.383**; pendências P2: **4.660** — não alteradas.

## Limitações e próximo passo

A avaliação é contextual por regras com inspeção individual das keywords e exceções registradas; não garante precisão de decisões sem homologação editorial. Antes de expandir, priorizar nova seleção com checagem obrigatória de elegibilidade P3; manter as 98 propostas fora das filas até definição formal do fluxo global.
