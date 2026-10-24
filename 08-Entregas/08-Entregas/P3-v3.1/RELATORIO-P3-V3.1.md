# P3 v3.1 — Revisão crítica das 36 decisões da v3.0

**Data:** 23/10/2026  
**Natureza:** revisão conservadora por ID; não amplia o universo P3 nem representa homologação editorial humana.

## Resumo quantitativo

- **36** decisões P3 v3.0 examinadas individualmente.
- **8** refinamentos com alterações efetivas e patches auditáveis.
- **28** mantidas com ressalvas específicas, sem mudança nos lotes.
- **6** ajustes de velocidade da internet: o texto não permite concluir se o usuário quer medição ativa da conexão ou cálculo com tamanho de arquivo e tempo de transferência.
- **1** ajuste em `juros compostos financiamento veiculo`: discrimina informação sobre juros compostos de consulta a taxas divulgadas.
- **1** ajuste em `melhor banco para financiamento veiculo`: a busca compara instituições, não apenas uma taxa nominal.

## Avaliação por regra

| Regra da P3 v3.0 | Revistos | Correções v3.1 |
|---|---:|---:|
| P3V30_BASES_GENERICA | 1 | 0 |
| P3V30_BASES_HEXA | 1 | 0 |
| P3V30_BASES_OCTAL_DECIMAL | 6 | 0 |
| P3V30_CAMBIO_PESOS_REAL | 6 | 0 |
| P3V30_ELETRICIDADE_KWH | 2 | 0 |
| P3V30_FINANCIAMENTO_VEICULO | 6 | 2 |
| P3V30_MATEMATICA_POTENCIAS | 4 | 0 |
| P3V30_TEMPERATURA_CONVERSOR | 4 | 0 |
| P3V30_VELOCIDADE_INTERNET | 6 | 6 |

## Integridade de dados

- **30/30** lotes verificados por regressão independente.
- **294.905 registros-base** e **2.190 controles** preservados.
- Campos protegidos, incluindo os dados originais do Google Ads, idênticos linha a linha.
- Apenas oito IDs da revisão receberam mudanças nos campos analíticos autorizados.
- Filas com 23.965 e 52.046 registros, todas as colunas históricas conservadas e oito colunas novas para a P3 v3.1.
- As **98 propostas da fila global** permanecem em quarentena, byte a byte inalteradas.
- As **4.660 pendências P2** não foram alteradas.
- P3 fora dos pilotos permanece em **20.272 registros**, porque esta é somente uma revisão de decisões já classificadas.

## Interpretação e limites

O agrupamento semântico a partir da palavra-chave isolada exige ressalvas em busca de ferramenta, falta de unidade/operando, ausência de cotação e termos financeiros sujeitos a comparação contextual. Não se inferiram taxas, rendimentos, prazos, tarifas ou resultados numéricos. As ressalvas são proposições técnicas que ainda dependem de homologação editorial.

## Referências internas

- `p3-v3.1-pareceres-36.csv`: parecer por ID e notas de risco.
- `p3-v3.1-patches.csv`: alterações efetivas, valores antes/depois.
- `p3-v3.1-regressao-independente-30-lotes.csv`: validação em cada um dos 30 lotes.
- `qa-auditoria-P3-v3.1-centralizada.xlsx`: planilha integralmente centralizada.
- `07-Scripts/P3/`: código Python reproduzível; a fonte necessária está embutida em `FONTES-REPRODUCAO`.
