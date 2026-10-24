# DEC-054 — Risco por regra e expansão seletiva P3 v1.8

Data: 2026-10-21. Decisão técnica paralela, após DEC-053.

## Escopo
1. Avaliar a **amostra estratificada direcionada** de 103 registros da P3 v1.7 (referentes às 152 classificações da P3 v1.6), com 17 correções observadas.
2. Executar uma expansão pequena sobre os 20.755 registros ainda fora dos pilotos P3; sem reutilizar a aprovação editorial como pressuposto.

## Auditoria por regra (denominador: amostra direcionada, NÃO população)
- Desconto INSS: 7 correções / 32 amostrados = 21,88%.
- Taxa financiamento imobiliário: 6 / 32 = 18,75%.
- Variância/desvio padrão: 2 / 15 = 13,33%.
- Abertura de conta bancária: 1 / 13 = 7,69%.
- Referência de numerais romanos: 1 / 5 = 20%, base muito pequena.
- Arranjo/combinatória: 0 / 5. Raiz cúbica explícita: 0 / 1.
- Total: 17 / 103 = 16,50% corrigidos na amostra. **As 17 exceções foram forçadas à amostra: não extrapolar como taxa de falsos positivos na P3 inteira.** Não interpretar ausência de correção como validação humana completa.

## Expansão v1.8
- **83 registros em 40 famílias**, dos 20755 ainda fora dos pilotos.
- Taxonomia de IRRF (27), média ponderada (20), poupança e taxa/rendimento informativo (14), conversões de energia com grandezas homogêneas (6), médias trabalhistas de férias (5), regra de três (4) e dias úteis (7).
- P3 fora dos pilotos: **20672**. P2 mantém 4.660 pendências sem alteração.
- Conservar como pendentes os casos sem unidade de destino ou tempo necessário (por ex. W↔kWh), impostos sem parâmetros e termos de banco que procuram simuladores ou operações transacionais.

## Controles
- Regressão independente 30/30 lotes; 294.905 bases, 2.190 controles; 83 patches por ID e valores antes/depois; somente colunas analíticas permitidas.
- Filas P3 (23.965) e geral (52.046) com histórico preservado e campos novos P3 v1.8.
- Versões antigas P0, P1, P2 e P3 v1.7 **não sobrescritas**.
- Resultados são propostas técnicas, **não homologação editorial**, e a taxonomia Saúde ainda requer validação.

## Continuidade
A próxima etapa deve auditar criticamente os 83 ajustes da v1.8, especialmente IRRF, poupança e médias remuneratórias, antes de avançar a P3. Arquivos íntegros e fontes em `08-Entregas/P3-v1.8/`.
