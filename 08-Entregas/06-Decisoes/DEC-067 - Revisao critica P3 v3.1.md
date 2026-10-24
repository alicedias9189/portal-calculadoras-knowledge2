# DEC-067 — Revisão crítica P3 v3.1

## Decisão

Após conferir individualmente as 36 novas classificações da P3 v3.0, restringir refinamentos a oito registros já elegíveis à P3 e já classificados na etapa anterior. Não ampliar automaticamente outras famílias, não mover registros entre prioridades e não aplicar as 98 propostas globais.

## Regras de correção

1. **Velocidade da internet (6 IDs):** substituir subcluster que pressuponha medição efetiva por uma taxonomia neutra de teste ou cálculo, com método não informado.
2. **Juros compostos no financiamento de veículo (1 ID):** distinguir explicação de encargos compostos de uma busca por taxas anunciadas; não assumir sistema de amortização.
3. **Melhor banco para financiamento (1 ID):** classificar como comparação de instituições, sem ordenar bancos nem inferir taxas, CET ou critérios.

## Escopo técnico

- Universo de revisão: somente 36 IDs registrados em `p3-v3.0-decisoes.csv`.
- Modificações: somente os oito IDs citados em `p3-v3.1-patches.csv`.
- Segurança: exigir interseção exata entre os dois CSVs de filas P3 v3.0, decisão v3.0 e metadados dos lotes.
- Fonte de verdade: conteúdo efetivo de `lotes-001-a-030-p3-v3.0.zip`, não supor dados de versões anteriores.
- 98 globais e 4.660 pendências P2 permanecem isoladas.

## Resultado

8 refinamentos; 28 decisões mantidas com ressalvas; regressão independente de 30 lotes concluída sem divergência. Homologação editorial final continua pendente.
