# P3 v3.2 — Expansão seletiva e auditoria

## Escopo e resultados

Foram identificados, avaliados e classificados **68 registros** de **36 famílias** da fila **P3**, todos previamente `FORA_DO_PILOTO` e sem status posterior. Não houve alterações em P0, P1, P2 ou na quarentena global.

A seleção foi cruzada por `id_global`, palavra-chave, família, lote, status e prioridade tanto na fila P3 (23.965 registros) quanto na fila geral (52.046 registros) e nos 30 CSVs de lotes. Há assertivas no script principal para bloquear os desvios.

| Regra | Decisões |
|---|---:|
| Horas extras — correção de domínio trabalhista | 32 |
| Payback — investimentos e retorno | 18 |
| Diferença entre datas no Excel | 9 |
| IPVA — tributo de veículos | 7 |
| Juros de cartão de crédito — instrução | 1 |
| Preço de kWh — tarifa de eletricidade | 1 |
| **Total** | **68** |

A classificação trata `como calcular` como pedido de orientação, enquanto palavras como `calculadora` sem operandos indicam cálculo contextual; planilhas/modelos são recursos e não operações concluídas. IPVA depende do estado, ano e características do veículo. Payback descontado depende de fluxos de caixa e taxa de desconto, sem valores presumidos.

## Diagnóstico de qualidade das regras anteriores

Foi compilado `p3-v3.2-qa-regras-anteriores.csv` com o histórico de refinamentos da revisão v3.1 sobre as 36 decisões da v3.0. A frequência de refinamentos **não** mede uma taxa populacional de falsos positivos: várias mudanças apenas tornaram a intenção mais específica.

## Integridade e continuidade

- 30/30 lotes aprovados por **regressão independente**.
- 294.905 bases e 2.190 controles preservados.
- 68 patches estritos e auditáveis com `antes_json`/`depois_json`.
- Filas preservam todas as colunas e valores antigos, com 9 novas colunas v3.2.
- Quarentena global de 98 propostas idêntica à anterior (verificada por bytes).
- P3 fora de piloto: **20.272 → 20.204**.
- P2 pendentes: **4.660** (sem mudanças).

**Limite:** classificações técnicas com ressalvas contextuais; homologação editorial final continua pendente. Não houve coleta de taxas atuais nem cálculos sem parâmetros.

## Reexecução

Na raiz extraída deste pacote, executar:

```bash
python 07-Scripts/P3/auditar_p3_v32.py
python 07-Scripts/P3/regressao_independente_p3_v32.py
python 07-Scripts/P3/gerar_qa_p3_v32.py
```

Os scripts usam as fontes incluídas em `08-Entregas/P3-v3.2/FONTES-REPRODUCAO`. O gerador da planilha depende de `artifact_tool`, os demais usam apenas a biblioteca padrão Python.
