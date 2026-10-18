# P2 — Validação contextual complementar v2

## Escopo
- Universo P2: 25,050 palavras-chave; pendências anteriores: 8,813.
- Resolvidas por regras de maior confiança: 959.
- Reclassificadas com ressalvas de operação: 1,716.
- Pendências contextuais remanescentes: 6,138.
- Registros com atualização analítica: 2,675.
- Registros P2 já classificados na v1 preservados nesta rodada: 16,237.

## Integridade e auditabilidade
- Registros-base preservados: 294.905; controles preservados: 2.190.
- Todos os 30 lotes passaram na comparação fonte x saída.
- P0, P1 e campos protegidos de Ads, rastreamento e reconstrução de barras inalterados.
- SHA256 dos campos protegidos: `adf4eae920349d805d9325434b5053b7f466a3eac6608a7a5293e1b1aa9caebc`.
- Scripts reutilizáveis não dependem de bibliotecas externas para reclassificação e regressão.

## Limites do resultado
A classificação é feita por regras textuais verificáveis, com regras de exceção; não equivale a leitura humana individual de 8.813 keywords. `RESOLVIDO_ALTA` indica confiança na regra, e não aprovação editorial final. Uma ressalva pode exigir valor, país, moeda, sentido, densidade, material, data, convenção, taxa, ou outro parâmetro. Não criar parâmetros de conversão imaginados. Os casos insuficientes continuam pendentes.

## Arquivos
`p2-v2-decisoes-25050.csv`: toda P2 e rastreabilidade; `p2-v2-pendencias-reais.csv`: restante para revisão; `p2-v2-ressalvas.csv`: casos classificados com dependências; `p2-v2-patches.csv`: diffs por registro; `p2-v2-regressao-30-lotes.csv`: testes; `fila-30-lotes-p0-p1-p2-v2.csv`: fila geral; `.zip`: 30 lotes revisados; `p2-v2-amostra-auditoria.csv`: amostra estratificada das regras. A planilha `.xlsx` resume os resultados e inclui uma amostra, enquanto os CSVs preservam todas as colunas e linhas.