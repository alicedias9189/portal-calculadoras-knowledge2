# DEC-057 — Revisão crítica P3 v2.1 da amostra P3 v2.0

Data: 2026-10-22. Proveniência: ZIP P3 v2.0, DEC-056. Nova versão paralela, sem substituir a anterior.

## Escopo
- 165 decisões da amostra estratificada P3 v2.0 foram avaliadas individualmente.
- As 272 decisões da expansão P3 v2.0 foram registradas no arquivo de pareceres, incluindo 107 não pertencentes à amostra original. Não se deve confundir isso com uma auditoria editorial independente de todas as keywords.
- Foram corrigidos 12 registros da amostra e 1 CET fora dela, total 13 patches nos campos analíticos autorizados. Amostra: 12 corrigidos, 23 mantidos sem novos alertas, 130 mantidos com ressalvas.

## Decisões principais
- Benefícios por incapacidade, informe de rendimentos, consulta de processo, revisão previdenciária e tempo de contribuição não são equivalentes a recolhimento de contribuição ao INSS.
- `calculadora da previdência social` não identifica o tipo de cálculo; subtema permanece genérico e com ressalva.
- `cálculo de atrasados do INSS` pode ser benefício retroativo ou recolhimento atrasado: não supor natureza específica.
- `fórmula para calcular INSS Excel 2021` é busca por instrução/fórmula, não cálculo de contracheque com parâmetros conhecidos.
- `resolva o sistema de equações a seguir` sem a expressão apresentada exige dados; trocar `cálculo direto` por `cálculo contextual`.
- `taxa anual CET caixa` exige distinguir custo efetivo total de taxa nominal; não inventar taxa/ano.
- Consultas por rendimento de veículos e por taxas bancárias são predominantemente informacionais, não cálculos com parâmetros fornecidos. Valores reais não foram inventados.

## Integridade
- 294.905 IDs base, 2.190 controles e 30 lotes preservados.
- Comparação independente de campos antigos/novos: **13 alterações autorizadas; zero indevidas**.
- As duas filas, de 23.965 e 52.046 linhas, conservaram seus campos anteriores; oito colunas P3-v2.1 novas registram pareceres.
- P2: 4.660 pendências preservadas; P3 fora dos pilotos: 20.400 registros, sem alteração nessa etapa.
- Regra de não propagação automática para famílias inteiras; todo patch é individual e com justificativa.

## Limitações e próximo passo
Os pareceres são revisão contextual baseada no texto, não validação editorial humana de toda a base nem checagem do conteúdo atual de instituições financeiras. A amostra é estratificada por regra e não fornece estimativa estatística de erro da população.

**Próxima etapa:** priorizar famílias P3 ainda não examinadas, mantendo exceções identificadas nesta revisão; realizar expansão pequena e auditar falsos positivos por regra. Conservar P2 como fila de ambiguidades sem especulação.

## Evidências
- `08-Entregas/P3-v2.1/p3-v2.1-revisao-amostra-165.csv`
- `08-Entregas/P3-v2.1/p3-v2.1-pareceres-272.csv`
- `08-Entregas/P3-v2.1/p3-v2.1-patches.csv`
- `08-Entregas/P3-v2.1/p3-v2.1-regressao-independente.json`
- `07-Scripts/P3/auditar_p3_v21.py`, `regressao_independente_p3_v21.py` e `gerar_qa_p3_v21.py`
