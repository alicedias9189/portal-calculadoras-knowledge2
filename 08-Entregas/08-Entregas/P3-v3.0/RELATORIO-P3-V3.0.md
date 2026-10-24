# Auditoria de palavras-chave — P3 v3.0

**Data de consolidação:** 2026-10-23  
**Tipo:** expansão seletiva técnica, com escopo estrito P3. Não constitui homologação editorial.

## Resultado

- **36 registros** novos classificados em **18 famílias distintas**.
- P3 fora dos pilotos: **20.308 → 20.272** pelo método reconciliado dos status individuais.
- **4.660 pendências P2** preservadas.
- **98 propostas globais** copiadas sem alteração; não foram promovidas a nenhuma prioridade.
- **30/30 lotes** aprovados pela regressão independente.
- **294.905 registros-base e 2.190 controles** preservados; Google Ads e identificadores intactos.
- Ambas as filas (23.965 registros P3 e 52.046 gerais) preservam **212 colunas históricas**, acrescentando nove colunas de rastreabilidade v3.0.

## Regras por família

- `P3V30_BASES_OCTAL_DECIMAL`: **6** registros
- `P3V30_VELOCIDADE_INTERNET`: **6** registros
- `P3V30_BASES_HEXA`: **1** registros
- `P3V30_FINANCIAMENTO_VEICULO`: **6** registros
- `P3V30_ELETRICIDADE_KWH`: **2** registros
- `P3V30_MATEMATICA_POTENCIAS`: **4** registros
- `P3V30_CAMBIO_PESOS_REAL`: **6** registros
- `P3V30_TEMPERATURA_CONVERSOR`: **4** registros
- `P3V30_BASES_GENERICA`: **1** registros

## Salvaguardas de semântica

- Conversões de bases decimal ↔ octal/hexadecimal preservam a direção **somente** quando declarada; valor ainda precisa ser fornecido.
- Peso chileno, peso colombiano e real são moedas, não unidades de massa; a cotação depende de data e não foi inventada. A simples presença de duas moedas não estabelece uma direção.
- Velocidade da internet pode exigir teste real da conexão ou dados de tempo e tamanho; não inferir números de Mbps.
- Consultas de taxas e parcelas de veículos não autorizam afirmar ofertas, taxas reais ou resultado sem condições financeiras.
- kWh expressa energia, não uma unidade de tempo nem o mesmo que kW. As expressões informais foram sinalizadas para revisão.
- "Potência" em expoentes e monômios se refere à matemática, não a aparelhos elétricos.

## Verificações executadas

1. Checagem dos IDs na interseção de filas P3 e geral, com `prioridade=P3` e mesmo `lote`, `familia_id`, `Keyword`.
2. Revisão obrigatória de `status_p3_v1=FORA_DO_PILOTO` e ausência de status em rodadas posteriores.
3. Exame dos 30 CSVs dos lotes e dos controles; os campos protegidos foram comparados de ponta a ponta.
4. Patches auditáveis por ID, com `antes_json`, `depois_json` e os campos modificados.
5. Verificação byte a byte das 98 propostas globais, mantidas separadas.

## Próxima etapa

Auditar criticamente os **36 novos registros**, priorizando os casos com `confianca=média`: velocidade da internet, algumas consultas de crédito e eletricidade. Ajustar eventuais falsos positivos antes de nova expansão. Prosseguir de forma independente com as pendências da P2.
