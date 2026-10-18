# DEC-038 — Revisão P1 e validação semântica v2

Data: 2026-10-17. Registro retrospectivo das entregas efetuadas após DEC-037.

## Escopo e resultados
- P1: 2.557 keywords em 1.173 famílias nos 30 lotes.
- Triagem inicial: 1.464 classificadas por regras fortes, 1.093 mantidas pendentes; 1.719 registros com campos analíticos alterados (412 mudanças de área e 1.195 de intenção).
- Segunda validação dessas 1.093: 700 validadas, 361 com ressalva de operação e 32 pendentes por contexto insuficiente. Houve 1.061 atualizações analíticas nos lotes na segunda passagem.
- 294.905 registros-base e 2.190 controles preservados; P0/P2/P3 e campos Ads protegidos mantidos.
- Regras de classificação não equivalem a revisão humana independente de cada termo. Os 32 casos permanecem explicitamente abertos.

## Regras e exemplos
- `libra x real` não define direção; `peso em reais` não especifica país.
- `gramas em ml` exige densidade/ingrediente; não converter por fator arbitrário.
- `24 semanas são quantos meses` depende de convenção de mês e às vezes contexto gestacional.
- Intenção informativa, comercial e navegacional não deve ser confundida com operação de calculadora.
- Não somar volumes Ads de variantes ou famílias como se fossem demanda independente.

## Evidências
- Relatório inicial: [[08-Entregas/P1-v1/relatorio-revisao-p1]]
- Relatório da segunda passagem: [[08-Entregas/P1-v2/relatorio-validacao-p1-v2]]
- Scripts: `07-Scripts/P1/`
- Planilhas, CSVs completos e ZIPs permanecem temporariamente na Biblioteca do ChatGPT; NÃO foram incorporados ao GitHub nesta sincronização. Ver `08-Entregas/MANIFESTO.md`.

## Próximos passos
Revisar os 32 casos P1 em aberto quando houver contexto adicional; verificar editorialmente amostras das 1.464 decisões da triagem inicial. Não declarar P1 integralmente homologada.