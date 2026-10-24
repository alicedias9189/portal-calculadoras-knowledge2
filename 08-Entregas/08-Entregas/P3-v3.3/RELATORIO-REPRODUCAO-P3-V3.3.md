# Prova de reprodução — P3 v3.3

Reexecução realizada usando somente os arquivos da pasta `FONTES-REPRODUCAO` presentes no ZIP final.

## Resultados

- Script de auditoria: passou; **68 pareceres e 10 patches**.
- Script de regressão independente: passou nos **30 lotes**, com **294.905** registros-base e **2.190** controles.
- Dados de saída: os **30 CSVs internos dos lotes** foram reproduzidos byte a byte, assim como os **dez arquivos CSV/JSON** comparados.
- Excel: a nova exportação reproduziu exatamente o XML das **seis abas** e os estilos. O arquivo `.xlsx` completo apresentou diferenças apenas nos componentes de metadados/relacionamentos (`xl/workbook.xml`, `_rels/.rels` e `xl/_rels/workbook.xml.rels`). Portanto, **não se declara identidade binária do XLSX inteiro**.

Todos os registros globais permanecem fora da P3, com o arquivo de 98 propostas preservado em bytes. O pacote não foi enviado ao GitHub automaticamente.
