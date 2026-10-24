# DEC-053 — P3 v1.7: calibração das 152 classificações novas da P3 v1.6

Data: 2026-10-21. Versão paralela, sem sobrescrever decisões anteriores.

## Escopo
Revisar criticamente a expansão P3 v1.6, priorizando INSS e taxas de financiamento imobiliário, antes de ampliar outras famílias. Total P3 v1.6 objeto da revisão: **152 decisões**, 7 regras semânticas; amostra estratificada determinística: **103 casos**. O CSV `p3-v1.7-revisao-152.csv` contém avaliação rastreável do universo; não representa homologação editorial independente de cada registro.

## Resultado
- **17 ajustes** por ID, incluindo **uma reabertura de ambiguidade** (`abrir conta pelo site`, ID 13149). **135 propostas mantidas**, parte com ressalvas.
- 59 decisões INSS; 54 financiamentos imobiliários; 15 variância/desvio padrão; 13 contas digitais; 5 arranjos/combinações; 5 numeração romana; 1 raiz cúbica. Amostra estratificada por regra de 32, 32, 15, 13, 5, 5 e 1, respectivamente.
- Distinguir **CET** (não equivale a taxa nominal de juros), Selic (não é taxa contratual), buscas comparativas de oferta, ensino de métodos de cálculo e consultas de taxa de financiamento.
- Desconto de **INSS e IRRF** envolve dois descontos; 13º tem incidência própria; tetos/anos devem ser contextualizados.
- "Calcular variância e desvio padrão" sem amostra/valores precisa de dados: tipo `cálculo contextual`, não `cálculo direto`.
- "Calculadora de numeração romana" descreve conversor de sentido selecionável, não cálculo aritmético direto.
- Consulta "abrir conta pelo site" não nomeia instituição nem serviço; classificar como `ambígua/revisão`, sem presumir banco.

## Integridade e qualidade
Regressão **independente** por coluna e por ID: **30/30 lotes PASSOU**; **294.905 registros-base e 2.190 controles**; **17 patches exatos**, todos nos campos semânticos autorizados. Nenhum ID fora das 17 alterações, nenhuma coluna protegida alterada. Filas de revisão preservadas: 23.965 P3 e 52.046 geral, apenas com nova trilha v1.7.

## Limites
Esta etapa **não fez nova expansão da P3**: permanecem 20.755 entradas P3 fora dos pilotos; **4.660 pendências P2** preservadas. Não se presumem taxas de bancos, Selic, CET, tabelas INSS ou alíquotas atualizadas. A amostra e as propostas **não são aprovação editorial definitiva**. Saúde v1.2 permanece sujeita à decisão editorial.

## Entrega e reprodução
`08-Entregas/P3-v1.7` inclui CSVs completos, ZIP dos 30 lotes, planilha centralizada, amostra e pareceres, diffs e regressão, além das fontes v1.6 necessárias. Scripts Python em `07-Scripts/P3/auditar_p3_v17.py` e `regressao_independente_p3_v17.py`; planilha requer `artifact_tool`.

## Próxima decisão
Antes de outra expansão, medir risco semântico por regra, revisar termos novos com amostragem, só prosseguir em famílias com ganho acima dos falsos positivos. Restrições P2 mantidas. Importação ao GitHub é **manual** pelo usuário, não automática.
