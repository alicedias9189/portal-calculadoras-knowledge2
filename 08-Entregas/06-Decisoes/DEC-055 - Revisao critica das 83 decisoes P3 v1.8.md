# DEC-055 — Revisão crítica das 83 decisões P3 v1.8 (P3 v1.9)

Data de execução: 2026-10-22. **Decisão:** não expandir a P3 antes de concluir a revisão por ID das 83 propostas da etapa v1.8. A v1.9 é uma versão paralela, sem substituir a v1.8.

## Resultado
- 83 decisões analisadas uma a uma, em oito grupos de regra.
- 10 alterações efetivas, 19 classificações mantidas sem novos alertas, 54 mantidas com ressalvas operacionais/semânticas.
- 30 lotes aprovados em regressão independente. 294.905 registros-base e 2.190 controles preservados.
- Fila P3: 23.965 registros; fila geral: 52.046; colunas históricas preservadas e 8 colunas de QA v1.9 acrescentadas. P3 ainda fora dos pilotos: 20.672, sem expansão. P2 pendências: 4.660, sem mudança.

## Correções
- Média ponderada: distinguir consulta nominal, pedido de cálculo contextual, ENEM com pesos dependentes de seleção, orientação LibreOffice/HP e material tabelado.
- IRRF: `irrf de adiantamento salarial` e `irrf sobre adiantamento salarial` são consultas informacionais sem pedido explícito de cálculo.
- Energia: `como converter kwh em wh` e `como converter wh em kwh` têm forma de tutorial; direção e metadados dimensionais foram preservados mesmo com tipo informacional.
- Outras 73 propostas permanecem como estavam, com notas por ID nos 83 pareceres.

## Interpretação e limites
Esta é uma auditoria contextual do texto das consultas, sem parecer humano externo, verificação jurídica de vigência de IRRF ou validação de intenção por SERP. Taxas e regras tributárias não foram presumidas. As 54 ressalvas não são automaticamente erros. O termo `MANTIDA` significa ausência de falso positivo identificado nesta passagem, não homologação editorial.

## Evidências
`08-Entregas/P3-v1.9/p3-v1.9-pareceres-83.csv` e `p3-v1.9-patches-10.csv`; `p3-v1.9-regressao-independente-resumo.json`; 30 lotes no arquivo `lotes-001-a-030-p3-v1.9.zip`; QA XLSX centralizada. Scripts em `07-Scripts/P3/`.

## Próximo passo
Nova expansão P3 em famílias de interpretação clara, com amostragem dirigida às regras de IRRF, poupança, férias e ENEM. Manter ressalvas e evitar classificação em massa por família. Não sobrescrever fontes/histórico sem versionar.
