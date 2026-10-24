# Registro 2026-10-21-01 — P3 v1.2 Saúde e navegação de crédito

## Pedido e compromisso
O usuário disse `Faça`, o que significa executar o próximo passo sugerido na resposta anterior: formalizar o tratamento de Saúde/gestação na taxonomia e revisar 43 alertas de intenção navegacional em crédito bancário. O trabalho deve ser entregue em **ZIP único para importação manual no GitHub**, não enviado diretamente.

## Fontes
ZIP P3 v1.1 crítica, DEC-047, reavaliação dos 1.207 patches P3 v1, amostra QA de 210, 30 CSVs com 34 campos, filas consolidadas. Versões anteriores preservadas.

## Procedimento
1. Identificar exatamente 184 registros suspensos de escopo com gestação explícita e três falsos negativos sobre gestação na amostra.
2. Adotar área `Saúde`, cluster `Saúde reprodutiva e gestação`, subgrupos de semanas/dias e convenção meses gestacionais, sem produzir diagnóstico.
3. Revisar 43 alertas bancários: 27 mencionam `simulador` e nome de banco e recebem tipo `navegacional/transacional`; 16 usam somente `simular` ou `simulação` e são preservados como intenção potencialmente híbrida.
4. Aplicar 214 patches no ZIP paralelo dos 30 lotes, sem tocar linhas não selecionadas; gerar fila consolidada com 8 campos novos, QA XLSX centralizado, CSVs, scripts e regressão completa.

## Resultado
187 Saúde, 27 navegação, 16 bancários preservados. **214 IDs alterados**, 294.905 base, 2.190 controles, 30/30 lotes aprovados. Sem nova verificação editorial independente da taxonomia toda ou do Golden Set.

## Arquivos
`01-Taxonomia/TAX-v1.2 - Saude e gestacao.md`, `06-Decisoes/DEC-048 - Escopo Saude e auditoria bancarios P3 v1.2.md`, `08-Entregas/P3-v1.2/*`, `07-Scripts/P3/auditar_p3_v1_2.py`, `07-Scripts/P3/gerar_qa_p3_v1_2.py`, este registro e `ESTADO-ATUAL.md`. Fontes mínimas de v1.1 incluídas em `08-Entregas/P3-v1.1/`.

## Pendências
Confirmação editorial da nova área; 16 buscas bancárias híbridas, cinco falsos negativos não gestacionais da amostra; 21.875 P3 fora do piloto e 4.660 P2 pendentes. Checar se o usuário importou o ZIP no GitHub antes de avançar.
