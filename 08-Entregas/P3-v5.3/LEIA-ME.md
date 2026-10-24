# Entrega P3 v5.3 — como usar

**Fonte canônica:** `portal-calculadoras-auditoria-P3-v5.2-unico.zip`.
**Fonte da filtragem:** `portal-calculadoras-filtro-ouro-p3-v5.2.zip` (DEC-089).
**Não substitua as duas fontes pelos arquivos derivados.** Os dados originais devem permanecer intactos.

## Conteúdo

- `08-Entregas/P3-v5.3/lotes-001-a-030-p3-v5.3.zip`: todos os 30 lotes canônicos, 294.905 bases + 2.190 controles.
- `08-Entregas/P3-v5.3/lotes-001-a-030-p3-v5.3-sem-ouro.zip`: os 30 lotes de trabalho após filtro de 3.609 Ouro, 291.296 bases + 2.190 controles.
- Quatro filas completas, duas canônicas e duas sem Ouro, com 398 colunas anteriores e oito de rastreabilidade v5.3.
- `p3-v5.3-pareceres-75.csv`, `p3-v5.3-patches-6.csv`, planilha QA, regressão independente, resumos JSON, relatório e DEC-090.
- `07-Scripts/P3/*p3_v53.py`: execução, verificador independente e geração de QA XLSX.
- `SHA256SUMS-P3-V5.3.txt`: hashes SHA-256 dos arquivos da entrega.

## Como reproduzir

1. Extrair os dois pacotes anteriores e este pacote numa pasta de trabalho.
2. Colocar o conteúdo de `08-Entregas/P3-v5.2/` na pasta homônima e a pasta `auditoria-ouro/` da entrega Ouro ao lado. As fontes devem corresponder exatamente à versão de outubro/2026.
3. Executar `python 07-Scripts/P3/auditar_p3_v53.py` (após salvar os scripts em `07-Scripts/P3/`) para gerar os lotes, filas e pareceres derivados. O script calcula a raiz a partir de sua localização na árvore `07-Scripts/P3/`; precisa ficar nesse caminho.
4. Executar `python 07-Scripts/P3/regressao_independente_p3_v53.py` e validar o resultado `PASSOU` antes de usar as filas.
5. Executar `python 07-Scripts/P3/gerar_qa_p3_v53.py` para gerar a planilha QA centralizada (dependência `artifact_tool`).

O pacote contém **saídas reproduzidas e scripts**, mas não duplica todas as fontes históricas P3 v5.2 nem os sete ODS. Os insumos necessários permanecem nos pacotes originais já entregues.

## Fila a usar na próxima etapa

Use `08-Entregas/P3-v5.3/p3-v5.3-fila-23865-sem-ouro.csv` e a lista de **19.462 IDs estritamente elegíveis** nela. O status v5.3 dos 75 revisados consta nas oito últimas colunas; não revisitar esses IDs numa expansão de novos registros. Próxima rodada: **P3 v5.4, 100 palavras**.

**Atenção:** exclusão Ouro é reversível, os 12 casos de cores ambíguas continuam em revisão e a homologação editorial dos pareceres segue PENDENTE.