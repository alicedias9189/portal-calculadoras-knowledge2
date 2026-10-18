# DEC-039 — Revisão P2 e validação contextual v2

Data: 2026-10-17. Registro retrospectivo, sem substituir DEC-037 ou DEC-038.

## Universo e primeira passagem
- P2: 25.050 keywords dos 30 lotes.
- V1: 8.946 classificações por regra sem ressalva; 7.291 com ressalva; 8.813 pendências.
- Registros alterados na V1: 16.237.

## Segunda passagem (somente os 8.813 pendentes)
- 959 resolvidos por regra de maior confiança.
- 1.716 classificados com ressalva operacional/contextual.
- 6.138 continuam pendentes.
- Total 2.675 com atualização analítica; as 16.237 classificações anteriores foram preservadas nesta passagem.
- Amostra estratificada de 438 decisões da P2 V1, com 5 sinais heurísticos para revisão editorial.
- Integridade: 294.905 registros-base e 2.190 controles preservados em 30 lotes; P0, P1, P3 e dados Ads protegidos sem mudança.

## Ressalvas
- Regras computacionais não substituem aprovação editorial individual.
- `kWh em reais` trata de custo energético, não câmbio.
- Moedas colecionáveis não são automaticamente operações de câmbio.
- `libra` pode ser moeda ou massa, a decidir pelo contexto.
- Unidade e direção só quando explícitas; conversões físicas condicionais exigem parâmetros reais.
- Priorizar revisão de 6.138 pendências e 5 alertas antes de promover rótulos a taxonomia de produção.

## Evidências
- [[08-Entregas/P2-v1/relatorio-p2-v1]]
- [[08-Entregas/P2-v2/relatorio-validacao-p2-v2]]
- Scripts em `07-Scripts/P2/`
- Binários e CSVs completos ainda em Biblioteca do ChatGPT; ver `08-Entregas/MANIFESTO.md`.