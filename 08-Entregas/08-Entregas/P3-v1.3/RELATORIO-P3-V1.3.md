# P3 v1.3 — revisão dos cinco falsos negativos e expansão controlada

Data: 2026-10-21. Etapa seguinte à P3 v1.2/DEC-048.

## Resultados auditados
- Universo P3: **23.965** keywords; piloto P3 anterior: 2.090; ainda fora do piloto anterior: 21.875.
- Cinco falsos negativos da amostra P3 v1.1 examinados; **3 tiveram correção de rótulo** e **2 foram preservados por ambiguidade**.
- Expansão para **314 keywords de 111 famílias novas** com evidência textual específica.
- **317 patches reais** aplicados, restritos a campos analíticos.
- Restam **21.561 P3 fora dos pilotos**. Não confundir com 4.660 pendências P2, que permanecem documentadas.
- Auditoria independente: **30/30 lotes PASSOU**, 294.905 registros-base, 2.190 controles, todos os IDs e campos protegidos intactos. A fila consolidada anterior mantém todas as colunas e valores históricos, com oito campos extras de rastreamento.

## Cinco falsos negativos analisados
- `33161` — "calculadora de equação com fração": corrigir para Matemática > Álgebra > Equações com frações.
- `42656` — "calcular dissídio 2022": corrigir para Trabalho > Remuneração > Dissídio e reajuste salarial; depende da convenção/índice aplicável ao período.
- `50735` — "calculo de areia para reboco": corrigir para Construção > Argamassa e revestimento > Consumo de areia e reboco; exigir metragem/traço/espessura.
- `78915` — "como calcular km l": classificado coerentemente como consumo e autonomia; mantido, pois tutorial x cálculo requer contexto.
- `43465` — "calcular gasolina online": mantido como cálculo contextual de combustível, sem adivinhar se é custo ou consumo.

## Famílias novas priorizadas
IR sobre operações em ações (não IRRF salarial); IRRF em folha; FGTS em atraso; DSR sobre horas extras; abono pecuniário de férias; pedido de demissão; operações com frações; quantidade de pisos; GPS previdenciária; uso financeiro da HP12C; distância/consumo de gasolina (sem misturar especificações de veículos). Regras aplicadas a **cada keyword elegível**, e não a todas as entradas da família por herança.

## Exceções removidas após conferência
- Modelos de veículos e rendimento GNV não são conversão genérica de gasolina.
- Exercícios/tutorial de HP12C não são necessariamente simulação financeira.
- Pedido de demissão "com acordo" exige regra própria e não recebeu classificação automática genérica.
- Declaração de IR por salário mínimo não foi confundida com IRRF descontado em folha.

## Limitações e não aprovação editorial
As 314 novas classificações e três correções são propostas técnicas automáticas contextualizadas, não leitura humana de todos os termos nem homologação SEO. Taxonomia Saúde v1.2 continua como proposta a validar editorialmente. Regras fiscais e trabalhistas dependem de contexto, ano e parâmetros; não criar valores monetários ou fórmulas fixas. Colunas Google Ads e reconstruções de barras permanecem preservadas.

## Entregáveis
- `p3-v1.3-decisoes-por-id.csv`: 319 decisões, inclusive 2 revisões sem patch.
- `p3-v1.3-patches.csv`: 317 alterações, com valores reais antes/depois.
- `p3-v1.3-cinco-falsos-negativos.csv`: parecer por ID.
- `qa-auditoria-P3-v1.3-centralizada.xlsx`: sete abas centralizadas, com amostra estratificada de 67 decisões.
- `p3-v1.3-fila-23965.csv` e `fila-geral-p0-p1-p2-p3-v1.3.csv`: colunas históricas + rastreio v1.3.
- `lotes-001-a-030-p3-v1.3.zip`: 30 lotes CSV completos.
- `regressao-independente-30-lotes-p3-v1.3.csv`: comparação byte-interpretada das colunas protegidas e verificação por ID.
- `FONTES-REPRODUCAO`: quatro arquivos completos da P3 v1.2/v1.1, sem sobrescrever dados antigos.

## Próxima ação
Validar amostra e rótulos propostos (sobretudo regimes tributários, trabalhistas e peculiaridades do FGTS), e então ampliar a P3 com seleção de novas famílias distintas, mantendo os 21.561 casos fora dos pilotos identificados. Não voltar a aplicar automaticamente padrões que produziram falsos positivos.
