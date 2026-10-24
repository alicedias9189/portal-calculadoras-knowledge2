# Auditoria P2 v6 — revisão conservadora por intenção e risco

Data: 2026-10-20. Fonte: P2 v5 (DEC-043). Esta versão é paralela; decisões anteriores não foram sobrescritas nos arquivos históricos.

## Resultado definitivo

| Indicador | Valor |
|---|---:|
| Universo P2 | 25.050 |
| Pendências recebidas | **5.148** |
| Reclassificações | **387** |
| Decisões por regra sem ressalva | **106** |
| Decisões por regra com ressalva | **281** |
| Famílias distintas com patches | **160** |
| Pendências preservadas | **4.761** |
| Lotes verificados | **30/30** |
| IDs-base preservados | **294.905** |
| Controles preservados | **2.190** |

## Regras aplicadas

| Regra | Registros |
|---|---:|
| `medidas_culinarias_contextuais` | 47 |
| `produtividade_agricola` | 43 |
| `especificacoes_volts_amperes` | 39 |
| `exercicios_matematica_escolar` | 34 |
| `modelo_calculadora_fisica` | 32 |
| `rendimento_investimentos_contextual` | 24 |
| `rota_cidades_maranhao` | 22 |
| `inclinacao_telhado` | 17 |
| `arredondamento_metodo` | 16 |
| `massa_mg_g_pares` | 15 |
| `inclincacao_cobertura_normas` | 13 |
| `sacas_para_quilos_contextual` | 11 |
| `referencia_logaritmo_externa` | 10 |
| `datas_eleitorais_informativas` | 9 |
| `amortizacao_tabela_price` | 7 |
| `troca_especie_bancaria` | 7 |
| `formatos_sem_direcao` | 6 |
| `preco_produto_comercial` | 5 |
| `quantidade_materiais_cobertura` | 5 |
| `formatos_documentos_explicitos` | 5 |
| `inteiro_para_romano` | 4 |
| `calculadora_base_numerica` | 4 |
| `comparacao_bancos_rendimento` | 3 |
| `operacoes_polinomios_online` | 3 |
| `numero_extenso` | 3 |
| `romano_para_decimal` | 2 |
| `libra_massa_para_kg` | 1 |

## Exemplos de decisões e ressalvas

- `12 v 5 a`: especificações de tensão e corrente, **não** uma conversão numérica de V em A; potência exigiria dados do circuito.
- `quantos kg de tomate por hectare`: cálculo contextual de produção por área, sem inferir produtividade fixa.
- `medidas de farinha em xícaras`: equivalência culinária, exige tipo de ingrediente, densidade e padrão de medida.
- `casio fx991lax`: busca por calculadora física, não execução de operação no portal.
- `doc jpg`: dois formatos sem sentido inequívoco; status com ressalva, sem unidade origem/destino inventadas.
- `numero 8 em romanos`: inteiro e destino romano explícitos; classificação de conversão direta.
- `quantas sacas tem 1 tonelada`: massa por saca depende da cultura/padrão; nenhuma taxa fixa.
- `melhores bancos para render dinheiro`: consulta comparativa de ofertas, não simulador financeiro.
- `10 semanas e 2 dias`: continua aberto; não presumir gravidez nem conversão para meses.
- `39 fahrenheit`: continua aberto sem destino explícito.
- `100 milhas em km h`: não inferir velocidade se a origem foi escrita apenas como distância.

## Integridade da revisão

A regressão independente comparou os **30 CSVs v5 e v6, linha por linha**. Verificou:
- Mesmo conjunto de IDs-base e mesma quantidade de controles (73 por lote).
- Apenas os **11 campos analíticos autorizados** mudaram, e exclusivamente nos 387 IDs registrados.
- Valores `antes`/`depois` dos patches coincidem com os CSVs de fato; alterações em P0, P1, P3, Ads e campos protegidos **não ocorreram**.
- Conversões diretas com origem, destino e direção preenchidos.
- As famílias de **157 semanas/dias** e **68 temperaturas Fahrenheit isoladas** permanecem sem decisão indevida.
- CRC ZIP passou e arquivos SHA-256 estão documentados.

## Interpretação responsável

A auditoria é feita por regras semânticas e inspeção dos candidatos, **não** é revisão humana independente dos 5.148 termos. Os rótulos sem ressalva refletem força das regras, não homologação editorial completa. As 4.761 pendências não devem ser forçadas a uma área ou operação.

## Artefatos

- `lotes-001-a-030-p0-p1-p2-v6.zip`: 30 CSVs íntegros com novas decisões P2.
- `auditoria-p2-v6-csv-integral.zip`: 25.050 decisões, 4.761 pendências, patches, fila geral, QA e famílias, com todas as colunas.
- `qa-revisao-p2-v6-centralizada.xlsx`: resumo e amostras para inspeção; células centralizadas. Não é substituto dos CSVs integrais.
- `resumo-p2-v6.json`, `regressao-independente-p2-v6.json` e `SHA256SUMS-P2-V6.txt`.
- Scripts `07-Scripts/revisar_p2_v6.py`, `07-Scripts/auditar_regressao_p2_v6.py`, `07-Scripts/gerar_qa_p2_v6.py`.
- ZIP inclui os dois artefatos P2 v5 necessários à reexecução, sem depender de arquivos da conversa anterior.

## Próxima auditoria

Priorizar uma análise editorial/SEO por **relevância, demanda e risco semântico** sobre as 4.761 pendências, conservando termos subespecificados. Avaliar exceções em moeda sem país, código de produto e grandezas físicas incompletas. Sem dado suficiente, continuar pendente; considerar avançar para P3 quando a P2 não oferecer novas decisões seguras.
