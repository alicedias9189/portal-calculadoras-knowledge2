# Relatório — Auditoria P3 v1.7

## Método
Revisão crítica das **152** decisões novas da expansão P3 v1.6, com amostra estratificada determinística de **103**, cobrindo as sete regras. Priorização de INSS (32/59 na amostra) e financiamento imobiliário (32/54). Parecer rastreável para os 152 IDs, decisões técnicas e ressalvas editoriais preservadas.

## Resultado
- **17 correções** por ID e 135 propostas mantidas; uma decisão bancária passou a `ambígua/revisão`.
- Nenhuma nova família P3 analisada nem expansão da P3: **20.755** P3 ainda fora dos pilotos.
- **4.660** pendências P2 preservadas.

## Controle de qualidade
Verificação independente linha a linha dos 30 lotes P3 v1.6 x v1.7; comparação dos 17 patches JSON, preservação de todos os campos não modificáveis e IDs não selecionados. **30/30 PASSOU**, 294.905 bases, 2.190 controles. Filas P3 (23.965) e de revisão geral (52.046) só tiveram 8 campos de rastreamento P3 v1.7 acrescentados, sem modificar campos históricos.

## Limitações
Amostragem e regras contextuais não provam acurácia de 100% nem equivalem a validação editorial humana independente. No domínio bancário, regras e taxas dependem de instituição e data; nenhum número foi fixado. A categoria Saúde continua sujeita a homologação editorial.

## Referências
`p3-v1.7-revisao-152.csv`, `p3-v1.7-amostra-estratificada.csv`, `p3-v1.7-patches.csv`, `p3-v1.7-regressao-independente-resumo.json`, planilha QA. Script reexecutável e fontes v1.6 incluídos.
