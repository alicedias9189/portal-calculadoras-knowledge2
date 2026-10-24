# P3 v1 — Piloto de revisão semântica por famílias

Data: 2026-10-20. Origem: P2 v7 validada estruturalmente (DEC-045). Este pacote é **versão paralela**, e não substitui os lotes existentes.

## Escopo e resultados
| Item | Quantidade |
|---|---:|
| P3, universo total | 23,965 |
| Famílias P3, universo total | 9,278 |
| Piloto: keywords e famílias | 2,090 / 66 |
| Propostas de ajuste que geraram patches | **1,207** |
| Propostas sem ressalva da regra | 418 |
| Propostas com ressalvas | 789 |
| Keywords do piloto sem evidência para alterar | 883 |
| P3 fora do piloto (não revisadas) | 21,875 |
| P3 sem proposta de ajuste nesta rodada | **22,758** |
| Famílias com alterações | 39 |
| Mudanças na área principal | 207 |
| Mudanças no tipo de intenção | 604 |
| Testes de regressão | **30/30 PASSOU** |
| Registros-base / controles | 294,905 / 2,190 |

**Interpretação essencial:** propostas = ajustes produzidos por regras conservadoras e não aprovação humana. Muitas propostas mantêm área e/ou tipo de intenção e refinam a descrição/subcluster. São 207 mudanças de área e 604 de tipo de intenção, que se sobrepõem. Não somar essas métricas.

## Seleção do piloto
Selecionadas as 35 maiores famílias da fila P3 e até as oito maiores famílias por área predominante, removendo duplicatas: **66 famílias e 2.090 registros**. A amostra é deliberadamente concentrada em volume de família e cobertura por área; **não** é amostra aleatória representativa de toda a P3. Volumes Google Ads das variantes não foram somados.

## Revisões aplicadas
- Custos em kWh anteriormente categorizados como Trabalho → Energia/Consumo elétrico; exigem tarifa real e período.
- Livros de cálculo de James Stewart (inclusive PDF) → materiais didáticos; não conversão de arquivos nem cálculo construtivo.
- Consulta de calendário mensal e datas de Carnaval → calendário/referência, sem criar conversões numéricas.
- Gastos e controle de orçamento pessoal → planilhas/ferramentas financeiras, sem confundir com energia ou investimentos.
- Direito de gestantes separado de equivalências de idade gestacional; decisão conservadora em linha com o escopo da P2, sujeita à revisão do escopo de saúde.
- Consultas de rendimento CDI e simulação separadas de cotação de índices; anos históricos não tratados como taxa atual.
- Cálculos de combustível, crédito, dissídio e IGP-M mantêm ressalvas quanto a tarifa, taxas, calendário ou parâmetros necessários.

## Integridade
Auditoria independente por leitura das fontes v7 e dos 30 CSVs novos linha por linha: mesmo ID/keyword/ordem, os **2.190 controles idênticos**, nenhum registro fora dos 1.207 IDs alterado, e patches com valores reais antes/depois. Somente oito campos analíticos autorizados puderam mudar. SHA-256 concatenado dos campos protegidos da fonte: `928be7100acf8558102ad415d330617f052c8d8db33a73e1a8baa1a61eb09975`. Nenhum registro de P0/P1/P2 foi alterado. Golden Set histórico **não foi reexecutado**.

## Limitações e segurança editorial
Não se pode inferir intenção apenas por semelhança de família, nem determinar valores de taxas futuras/históricas ou dias do calendário sem entradas. As 883 consultas selecionadas sem evidência e 21.875 ainda fora do piloto permanecem preservadas. P2 mantém 4.660 pendências intactas.

A planilha apresenta **todas as 2.090 decisões e os 1.207 patches**, com todos os campos da planilha centralizados, 66 famílias, regras, amostra estratificada de 210 registros e regressão. CSVs integrais e todas as 34 colunas dos lotes estão nos dois ZIPs novos. A fila geral também preserva suas 69 colunas preexistentes, acrescentando somente metadados P3 v1.

## Próxima auditoria recomendada
1. Revisar editorialmente as 210 amostras, sobretudo as famílias de gestação/saúde, CDI histórico, direitos trabalhistas e buscas de ferramentas.
2. Ajustar exceções e medir precisão por regra antes de expandir a P3.
3. Só então processar lote incremental seguinte de famílias P3, preservando versões paralelas e regressão independente.
