# DEC-050 — P3 v1.4: revisão crítica de 67 decisões e expansão controlada

**Data:** 2026-10-21. **Predecessora:** DEC-049/P3 v1.3. Versão paralela; não substituir históricos.

## Decisão e alcance
- Auditar criticamente a amostra estratificada de **67 decisões** do piloto P3 v1.3, preservando a seleção reprodutível por semente 1303 e seis exemplos por regra.
- Corrigir **2 falsos positivos**: ID 76549 (“como calcular concreto para piso de garagem”) passa de quantidade de cerâmica para dimensionamento de concreto; ID 160013 (“fração na calculadora do celular”) passa de cálculo aritmético direto para instrução de uso da ferramenta.
- Os outros **65** casos da amostra não revelaram incoerência óbvia na leitura contextual; isso **não** representa homologação editorial por um revisor externo.
- Expandir de modo conservador a P3 para **576 keywords**, em **170 famílias** ainda fora do piloto, com regras específicas por consulta. São **578 patches** nesta versão.
- A P3 ainda fora dos pilotos passou de 21.561 para **20.985** keywords. Universo P3: **23.965**.

## Principais famílias novas abordadas
Direitos de gestantes no trabalho (diferentes de calculadoras gestacionais), jornada semanal, remuneração e salário líquido, consulta de taxas bancárias, comparação de CDI/CDB, rentabilidade informativa de fundos, saque-aniversário como produto de crédito, tributação de CDB, aposentadoria, financiamento SAC/Price, consumo de combustível de viagem, demanda elétrica e porcentagens no Excel.

## Limitações editoriais importantes
- Consultas sobre **PIS, FGTS e 13º** foram excluídas da regra de salário líquido quando o contexto não permitiu usar uma lógica comum. FGTS do empregador não deve virar automaticamente desconto em salário líquido.
- Não inventar taxas de juros, benefícios, parâmetros de cálculo, datas de vigência, destino de conversão, volume do Google Ads ou regras legais atemporais.
- Taxonomia Saúde v1.2 e as propostas sobre gestação permanecem sujeitas à validação editorial; os termos sobre **estabilidade gestante trabalhista** foram separados por contexto de emprego.
- Os 4.660 casos P2 sem evidência continuam separados. Nenhuma P0/P1/P2 anterior foi modificada.
- O trabalho é uma revisão por regras e auditoria textual, **não revisão humana independente linha por linha** nem aprovação SEO.

## Integridade verificada
Regressão independente de CSVs v1.3 versus v1.4: **30/30 lotes passaram**; **294.905** registros-base, **2.190** controles intactos, **578** alterações exclusivamente nos campos semânticos autorizados. SHA-256 das colunas protegidas: `c615847e8393889bc085b05d19ee66139111f1a6a9a2374fc52040a7d9ab560b`. Patches contêm JSON real antes/depois, conferido contra os lotes.

## Entregáveis e reprodução
- `08-Entregas/P3-v1.4/`: ZIP dos 30 lotes, CSVs completos de decisões/patches/filas, QA e resultados por lote.
- `08-Entregas/P3-v1.4/FONTES-REPRODUCAO/08-Entregas/P3-v1.3/`: fontes completas para reexecutar.
- `07-Scripts/P3/`: classificador, auditor, regressão independente, geração de QA e empacotamento.
- `SHA256SUMS-P3-V1.4.txt`: todos os hashes; relatório de continuidade em `08-Continuidade/`.

## Próxima etapa
Validar criticamente os **98 casos da amostra de expansão** incluídos na planilha; depois ampliar famílias P3 restantes ou corrigir regras conforme os falsos positivos encontrados. Manter pendências P2 e aprovação de Saúde separadas.


## Checagem adicional de reexecução
Foram extraídos do ZIP os scripts e as quatro fontes v1.3; a reexecução P3 v1.4 gerou os mesmos arquivos de patches, decisões, amostra, filas e resumo (SHA-256 idêntico), além dos **30 CSVs dos lotes com conteúdo idêntico byte a byte após descompactação**. O arquivo `.zip` interno possui SHA físico diferente por metadados do contêiner, sem diferença de conteúdo. Uma tentativa de repetir a regressão independente também sobre o diretório reexecutado excedeu o tempo de execução; a regressão independente sobre a entrega original já havia PASSADO 30/30.
