# Lote 001 — reauditoria com mapa de barras v2

## Status

**APROVADO.**

O lote 001 foi reavaliado após a revisão contextual das barras `/` e aplicação do mapa mestre v2.

## Cobertura

- Keywords base: **9.831**
- Controles incorporados: **73**
- Golden Set v1.1: **107/107** no QA existente
- Reconstruções de alta confiança presentes no lote: **14**
- Linhas que exigiram alteração de classificação/metadados: **6**
- Reconstruções que não mudaram a taxonomia: **8**
- Pendências notacionais não bloqueantes: **3**
- Regressões críticas: **0**
- Alertas semânticos médios nas linhas afetadas: **0**

## Alterações semânticas

### Conversões Mach → km/h

IDs `901`, `181102` e `181103` passam para:

- Área: `Conversores`
- Cluster: `Unidades físicas`
- Subcluster: `Velocidade e movimento`
- Tipo de intenção: `conversão direta`
- Origem: `Mach`
- Destino: `km/h`
- Direção: `Mach→km/h`
- Confiança: `alta`
- Revisão manual: `não`

### Abono pecuniário

ID `12861` — `abono pecuniário vende 1 3` é interpretado como `abono pecuniário vende 1/3` e passa para:

- Área: `Trabalho`
- Cluster: `Férias`
- Subcluster: `Férias e férias proporcionais`
- Intenção: `informacional`
- Confiança: `alta`
- Revisão manual: `não`

### MB/s → Mbps

ID `182212` já estava em `Conversores > Dados digitais > Taxa de transferência e rede`. A reconstrução `MB/s` torna a leitura inequívoca, então a confiança passa para `alta` e a revisão manual para `não`.

### `mil km/h`

ID `186271` passa para `Conversores > Unidades físicas > Velocidade e movimento`, mas continua `ambígua/revisão` porque há apenas um valor/unidade e nenhuma operação ou unidade de destino explícita.

## Reconstruções sem mudança taxonômica

As demais 8 reconstruções de alta confiança já estavam classificadas corretamente. Incluem frações de polegada, datas/feriados e frações em equações exponenciais.

## Ambiguidades de notação preservadas

Três keywords continuam sem reconstrução de `/` por falta de evidência suficiente:

- `251623` — `resolva as equações 3 3x 1 2 3x 2`
- `251630` — `resolva as equações 3x 1 5 4`
- `251757` — `resolva as equações em r 3x 1 2 0`

A classificação ampla `Matemática > Álgebra > Equações e expressões` permanece válida, então essas ambiguidades não bloqueiam o avanço.

## Decisão

O lote 001 permanece aprovado após a reauditoria. O lote 002 está liberado para classificação usando:

- Taxonomia Mestre v1.1;
- Regras R01–R26;
- Golden Set v1.1;
- mapa mestre de barras v2;
- regra de preservação da coluna `Keyword` original.
