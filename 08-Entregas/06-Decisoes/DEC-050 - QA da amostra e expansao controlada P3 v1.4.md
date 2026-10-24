# DEC-050 — Revisão crítica dos 67 registros e expansão P3 v1.4

Data: 2026-10-21. Referência anterior: DEC-049, versão P3 v1.3.

## Decisão
Manter P3 v1.3 intacta e registrar P3 v1.4 como **versão paralela provisória** de auditoria semântica, com correções dos falsos positivos da amostra estratificada e expansão seletiva por regras específicas, condicionada à revisão editorial antes de homologação.

## Auditoria da amostra (67 registros)
- 2 falsos positivos corrigidos:
  - ID 160013, `fração na calculadora do celular`: busca de instrução/uso de ferramenta, não execução de operação matemática.
  - ID 76549, `como calcular concreto para piso de garagem`: estimativa de concreto em piso, não revestimento cerâmico.
- 3 entradas mantidas com **ressalva editorial explícita**: IDs 56082 (GPS/DAE-eSocial de empregado doméstico depende da competência), 12838 (direito a dias de abono pecuniário), 199183 (aviso prévio em pedido de demissão).
- Outros 62 registros sem incoerência evidente na amostra; não significa que tenham sido aprovados editorialmente.

## Expansão
- 576 keywords fora dos pilotos anteriores receberam patches; 170 famílias distintas.
- 578 alterações totais = 576 novas + 2 da amostra.
- 21.561 P3 fora dos pilotos antes desta revisão, 20.985 depois. Universo P3: 23.965 keywords.
- Regras abordam crédito/taxas, jornada, gestante e direitos trabalhistas, amortização SAC/Price, porcentagens no Excel, aposentadoria previdenciária, antecipação do FGTS, domingos e horas extras, fundos, salário bruto/líquido, CDI e CDB, combustível, contas digitais, demanda elétrica e IR de CDB.

## Regra de integridade
- 30/30 lotes passaram na regressão independente, com 294.905 bases e 2.190 controles preservados.
- Apenas campos analíticos permitidos receberam alterações; IDs, keywords, colunas originais do Ads e rastreamento não mudaram.
- Os valores antes/depois de cada patch foram conferidos contra os arquivos CSV reais.
- Não multiplicar nem somar volumes do Google Ads por variações normalizadas.

## Limitações
- Não houve homologação editorial humana independente da totalidade das propostas.
- Taxonomia de Saúde v1.2 continua carecendo de validação editorial formal.
- As 4.660 pendências da P2 são uma fila separada e não foram alteradas nesta etapa.

## Próximo passo
Realizar auditoria estratificada da expansão P3 v1.4 (amostra de 98 decisões incluída no Excel), resolver os alertas da amostra e calibrar regras antes da próxima rodada de expansão.
