# TAX v1.2 — Inclusão controlada de Saúde e gestação

**Data:** 2026-10-21. **Natureza:** proposta técnica aplicada na P3 v1.2 em versão paralela; depende de validação editorial antes de se tornar taxonomia geral obrigatória.

## Decisão de escopo
O portal já contempla calculadoras de Saúde. Menções explícitas a gestação **não são automaticamente fora de escopo**. Definir nova área `Saúde`, sem substituir ou renomear as áreas aprovadas da taxonomia v1.1.

Hierarquia para palavras-chave com gestação explícita:
- `area_principal`: `Saúde`.
- `cluster`: `Saúde reprodutiva e gestação`.
- `subcluster`: `Idade gestacional em semanas e dias` ou `Equivalência de semanas e meses gestacionais`.
- `tipo_intencao`: `cálculo contextual` quando houver cálculo/quantos/calculadora; de outro modo `informacional`.
- `revisao_manual`: `sim` até validação editorial de escopo e parâmetros.

## Regras de precisão e segurança
- Semanas/dias são a representação prioritária; meses gestacionais não equivalem sempre a meses civis nem admitem fator único universal. Quando o usuário pedir meses, explicitar convenção e limitações.
- Uma ferramenta educacional de gestação **não é diagnóstico médico**. Não presumir data da última menstruação, data de concepção, ciclo, prazo de parto ou condição clínica ausentes.
- A expressão `gestante/funcionária grávida` em **direitos trabalhistas** permanece em `Trabalho`; não realocar automaticamente por conter gravidez.
- Consultas genéricas sobre `semanas/dias` **sem contexto gestacional** não mudam de área.
- Termos de saúde fora dessas classes aguardam revisão separada, não se deve extrapolar a regra a toda a área.

## Aplicação controlada
184 registros que haviam sido suspensos na P3 v1.1 mais 3 falsos negativos explícitos da amostra de 210: **187 patches** apenas em campos analíticos. A P3 v1.1 e P2 v7 ficam preservadas. A classificação não está homologada para publicação de aconselhamento clínico.

## Revisão editorial futura
Confirmar nomes finais da área, interface, terminologia médica e escopo dos recursos oferecidos antes de escalar a regras globais sobre todos os lotes.
