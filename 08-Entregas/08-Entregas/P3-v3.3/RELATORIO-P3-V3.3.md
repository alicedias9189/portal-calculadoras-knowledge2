# Relatório — P3 v3.3 — revisão crítica dos 68 registros v3.2

**Estado:** etapa concluída tecnicamente; homologação editorial humana pendente.

## Objetivo e escopo

Revisar individualmente as 68 decisões da expansão P3 v3.2. A v3.3 não amplia a P3, não promove novas famílias, não desloca as 98 propostas da fila global e não resolve as 4.660 pendências P2.

## Resultado por regra

| Regra | Analisados | Refinamentos de subcategoria/intenção | Preservados com ressalvas |
| --- | ---: | ---: | ---: |
| Horas extras e reflexos | 32 | 8 | 24 |
| Payback e investimento | 18 | 2 | 16 |
| Diferença entre datas no Excel | 9 | 0 | 9 |
| IPVA | 7 | 0 | 7 |
| Juros de cartão | 1 | 0 | 1 |
| Preço da energia | 1 | 0 | 1 |
| **Total** | **68** | **10** | **58** |

Os 10 patches são refinamentos de subtipo e de intenção em **categorias principais já coerentes**. Não devem ser descritos como 10 erros de área nem como uma taxa de falsos positivos generalizável.

### Casos aprimorados

- Supressão de horas extras foi separada de apuração genérica de jornada, sem pressupor indenização.
- Décimo terceiro envolvendo horas extras foi diferenciado de cálculos trabalhistas genéricos.
- Consultas sobre porcentagem e adicionais foram distinguidas de operações com números informados.
- Referências a cálculo no Excel foram especificadas como orientação sobre fórmulas.
- Pedidos de reflexos de horas extras não presumem que DSR seja o único reflexo.
- Payback na HP 12C foi identificado como instrução de uso da calculadora financeira, sem dados para apuração numérica.

Todos os pareceres estão detalhados, por ID, em `p3-v3.3-pareceres-68.csv`.

## Integridade comprovada

- Regressão independente: **30/30 lotes aprovados**.
- Registros-base: **294.905** preservados.
- Controles: **2.190** preservados.
- Apenas **10 IDs autorizados** alterados e somente em campos analíticos.
- 238 colunas históricas de cada fila preservadas, mais 8 novas colunas de QA da v3.3.
- Backlog global de 98 casos idêntico em bytes.
- P3 fora dos pilotos: **20.204**, inalterado.
- Pendências P2: **4.660**, separadas.

## Reprodutibilidade

Executar sequencialmente, a partir da raiz deste pacote:

```bash
python 07-Scripts/P3/auditar_p3_v33.py
python 07-Scripts/P3/regressao_independente_p3_v33.py
python 07-Scripts/P3/gerar_qa_p3_v33.py
```

Dependências: Python 3 e `artifact_tool` para Excel. Os outros scripts utilizam a biblioteca padrão. Antes de reexecutar, preservar uma cópia do pacote para manter os hashes do arquivo original; a reexecução sobre a mesma pasta reescreve os outputs intencionalmente.

**Nota:** a revisão foi conservadora, baseada no texto de cada busca. Nenhuma decisão equivale à homologação por um editor humano.

## Prova de reprodução da entrega

Consulte `RELATORIO-REPRODUCAO-P3-V3.3.md`. Os dados e estilos das seis abas Excel foram reproduzidos; não há identidade binária do contêiner XLSX devido a metadados internos não determinísticos.
