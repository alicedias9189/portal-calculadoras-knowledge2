# Relatório da auditoria P3 v1.6

## Escopo
- Amostra inteira da P3 v1.5: **78 novas classificações** revistas individualmente, 11 correções.
- Expansão: **152 alterações em 56 famílias**; 163 patches totais.
- P3 fora dos pilotos: **20.755** de um universo de **23.965**.
- P2: **4.660 pendências** preservadas separadamente.

## Regras aplicadas (quantidades)
- inss_desconto_folha: 59
- taxa_financiamento_imobiliario: 54
- variancia_desvio_padrao: 15
- abertura_conta_bancaria: 13
- referencia_numerais_romanos: 5
- arranjo_combinacao: 5
- qa_simulador_banco_nomeado: 5
- qa_canal_antecipacao: 2
- qa_fundos_nao_titulos_diretos: 1
- qa_titulos_publicos_privados: 1
- qa_piso_previdenciario: 1
- raiz_cubica_valor_explicito: 1
- qa_taxa_consignado_informativa: 1

## Auditoria
Regressão independente passou nos 30 lotes. Linhas-base: 294.905; controles: 2.190; alterações somente nos oito campos analíticos autorizados. Os 163 patches foram validados por IDs, colunas e JSON de antes/depois, comparando cada linha v1.5 e v1.6. A fila histórica foi preservada e somente oito colunas de auditoria foram acrescentadas.

## Critérios e cautelas
- Classificação por texto, domínio e intenção, sem simular legislação ou câmbio em vigor.
- Busca informativa de taxa de banco não equivale a simulação; site nomeado pode caracterizar busca navegacional.
- Tabela de desconto do INSS requer ano/regime pertinentes; não inferir percentuais.
- Metadados e dados Google Ads originais não foram reescritos, volumes não foram somados.
- 78 pareceres podem ser auditados na planilha, mas todos são propostas assistidas e não revisão editorial humana independente.

## Arquivos
- `lotes-001-a-030-p3-v1.6.zip`: 30 CSVs integrais com todas as colunas dos lotes.
- `fila-geral-p0-p1-p2-p3-v1.6.csv` e `p3-v1.6-fila-23965.csv`: filas completas e auditáveis.
- `p3-v1.6-amostra-78-pareceres.csv`, `p3-v1.6-patches.csv`, `p3-v1.6-decisoes-por-id.csv`: decisões e alterações pontuais.
- `p3-v1.6-regressao-independente-30-lotes.csv`, `p3-v1.6-regressao-independente-resumo.json`: integridade independente.
- `qa-auditoria-P3-v1.6-centralizada.xlsx`: planilha com todas as células utilizadas centralizadas, incluindo 78 pareceres, decisões, regras, patches, regressão e amostra de pendências. Dados completos disponíveis nos CSVs.
- 4 scripts e 4 fontes v1.5 para reexecução fora do ChatGPT.
