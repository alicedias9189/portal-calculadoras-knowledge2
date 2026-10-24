# Auditoria P3 v2.9 — Revisão integral da expansão P3 v2.8

**Data:** 23/10/2026  
**Escopo:** revisar cada um dos 66 patches da P3 v2.8 e corrigir falsos positivos ou generalizações de intenção, sem expansão desta vez.

## Resultado

- Registros revisados: **66**, incluindo **45** de taxas de financiamento de veículos.
- Patches efetivos por ID: **2** (ambos de intenção/subcluster no tema financiamento de veículos).
- Mantidos com ressalvas: **64**.
- Famílias novas incluídas: **0**.
- P3 ainda fora dos pilotos após conciliação histórica v2.8: **20.308** (permanece invariável na v2.9).
- P2 pendentes: **4.660** (não alteradas).
- Propostas globais em quarentena: **98** (arquivo idêntico byte a byte).

### Duas correções

| ID | Palavra-chave | Refinamento |
|---|---|---|
| 47729 | calcular taxa financiamento veiculo | Calcular a **taxa implícita** do financiamento a partir de condições financeiras, não apenas consultar taxas publicadas. Continua exigindo parâmetros. |
| 78698 | como calcular juros de financiamento carro | **Explicação do método** de cálculo de juros: não é simulação de parcelas e não é consulta de taxa anunciada. |

Nenhum percentual real de juros, banco vencedor, alíquota INSS, distância, direção de conversão ou período de consumo foi presumido.

### Revisão das demais 64

A manutenção exige ressalvas específicas. Consultas sobre taxa atual, histórica ou comparação entre bancos não contêm condições para simulação; documentos/tabelas solicitam referência externa e data; Celsius × Fahrenheit não fixa direção; kWh (energia) e W (potência) exigem tempo; INSS de obra exige contexto de regime/regularização; bases numéricas dependem do valor a converter.

A frequência de correção por regra está em `p3-v2.9-auditoria-por-regra.csv`. **Não extrapolar a frequência das 66 decisões da v2.8 para toda a base**, pois este universo é um conjunto pré-selecionado e não uma amostra probabilística.

### Controles e testes

- **30/30** lotes aprovados por comparação independente linha a linha entre v2.8 e v2.9.
- **294.905** registros-base e **2.190** controles mantidos.
- Somente os IDs **47729** e **78698** mudaram, e somente em campos analíticos permitidos.
- Valores de 34 colunas nos registros foram comparados; campos protegidos idênticos.
- Ambas as filas (23.965 P3 e 52.046 gerais) preservam cada valor das colunas históricas e acrescentam oito colunas de rastreabilidade da v2.9.
- 98 propostas globais não alteradas (comparação binária).
- Validação e reprodução executáveis pelos scripts Python e fontes presentes no pacote.

### Divergência histórica preservada

O total de P3 fora dos pilotos divulgado na v2.7 (**20.383**) difere em nove unidades da contagem reconstituída por status (**20.374**). Após 66 alterações elegíveis da v2.8, o valor auditável é **20.308**. A v2.9 é uma revisão, sem nova expansão; esse total se mantém. A divergência não foi resolvida artificialmente nem apagada dos históricos.

**Status:** proposta técnica revisada. Homologação editorial humana pendente.
