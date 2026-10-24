# P2 v5 — revisão contextual das pendências

Data: **2026-10-20**. Base: P2 v4 auditada, decisão DEC-042 preservada. Nova decisão: DEC-043.

## Escopo e resultados finais

| Métrica | Quantidade |
|---|---:|
| P2 total (sem mudança de escopo) | 25.050 |
| Pendências recebidas da P2 v4 | 5.562 |
| Reclassificações realizadas | **414** |
| Sem ressalva operacional | 181 |
| Com ressalva | 233 |
| Famílias com alterações | 185 |
| Pendências restantes | **5.148** |
| IDs-base originais preservados | 294.905 |
| Controles preservados | 2.190 |
| Lotes com regressão independente aprovada | 30/30 |

## Regras de reclassificação

| Regra | Registros |
|---|---:|
| cotacao agropecuaria | 44 |
| referencia logaritmos | 39 |
| calculadora duracao | 36 |
| orcamento construcao | 33 |
| produto calculadora fisica | 31 |
| equipamento transformador | 25 |
| simulador instituicao | 15 |
| compra moeda estrangeira | 14 |
| moedas historicas | 13 |
| conteudo matematico escolar | 13 |
| bases numericas direcao | 13 |
| metodo cramer | 12 |
| rendimento conta digital | 11 |
| educacao financeira | 11 |
| materiais construcao calculo | 9 |
| norma ambiental | 9 |
| imagem ocr documento | 8 |
| libra pressao ambigua | 8 |
| direito trabalhista informativo | 6 |
| simulacao credito | 5 |
| calculo pedido demissao | 5 |
| preco venda custo | 5 |
| desconto faltas | 5 |
| numismatica | 5 |
| tutorial matematico | 4 |
| frequencia rpm condicional | 4 |
| tabela romanos | 4 |
| bases numericas numericas | 4 |
| conversao pdfa | 3 |
| simulador aplicacao | 3 |
| quantidade blocos m2 | 3 |
| romanos caracteres | 3 |
| torque nm lbft | 3 |
| temperatura par explicito | 2 |
| valor futuro financeiro | 1 |
| ampere miliampere | 1 |
| velocidade mph kmh | 1 |
| pressao psig bar | 1 |
| decimal para romano | 1 |
| volume oncas fluidas | 1 |

**As decisões sem ressalva significam confiança da regra, NÃO revisão editorial humana individual.** As decisões com ressalva dependem de dados adicionais (ex.: prazo, taxa, referência de pressão, OCR, localidade ou moeda histórica).

## Famílias que não autorizam conversões assumidas

- 157 variantes numéricas «N semanas e D dias»: não presumir gravidez, calendário de meses nem operação desejada. Permaneceram pendentes.
- Família com 69 consultas Fahrenheit anteriormente pendentes: uma variante «fahrenheit para k» contém destino explícito e foi tratada; 68 casos da família continuam ambíguos (temperaturas isoladas ou expressões sem destino).
- «milhas em km h» não informa inequivocamente uma velocidade na origem; não tratar distância como velocidade.
- «libra» em pressão ou cotação pode indicar grandezas distintas; classificar apenas intenção com ressalvas.
- Transformadores de 110/220 V são equipamentos, não conversores de unidade numérica.
- Pesquisas por teorias, tutoriais e PDFs de exercícios não são automaticamente calculadoras ou conversões de arquivo.

## Regressão independente

O auditor `07-Scripts/auditar_regressao_p2_v5.py` comparou os **30 arquivos v4/v5 linha por linha**. Conferiu:

- 294.905 IDs-base únicos e invariáveis, 73 controles por lote (2.190 no total);
- diferenças somente nos 11 campos analíticos autorizados, e apenas nos 414 IDs selecionados;
- nenhum outro ID modificado, nenhum controle alterado e nenhuma mudança em P0, P1 ou P3;
- valores antes/depois dos patches coincidem com os **CSVs reais** de origem e destino (não apenas com a fila analítica);
- conversões diretas novas com origem e destino preenchidos;
- integridade CRC dos ZIPs e contagem dos CSVs da P2.

Detalhes: `regressao-independente-p2-v5.json`, `p2-v5-qa-regressao-30-lotes.csv` e manifestos SHA256.

## Limitações e próximos passos

A revisão é contextual **baseada em regras específicas por keyword e inspeção de candidatos**, não uma checagem editorial independente de todas as 5.562 consultas. A amostra de pendências na planilha não substitui os CSVs integrais. Não criar volume Ads somando variantes ou preencher taxas, unidades e direções sem evidência.

**Próxima prioridade:** revisar as 5.148 pendências em famílias de tensão/corrente genéricas, modelos comerciais, números isolados, moedas de país indeterminado e consultas administrativas, por relevância/volume e risco. Documentar novas decisões com regressão separada.
