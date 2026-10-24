# Portal de Calculadoras — auditoria de cores Ouro/Ouro escuro 1

**Data:** 2026-10-24 | **Base:** auditoria P3 v5.2 | **Natureza:** filtro **não destrutivo** de variantes automáticas.

## Evidências nas 7 planilhas ODS originais

- `SementesEnergia.ods`, aba `Codex`: **3.368** células preenchidas em cor de fonte **Ouro `#FFBF00`** e **348** em **Ouro escuro 1 `#E8A202`**.
- Nas outras seis planilhas analisadas não há células de palavras-chave com essas duas cores.
- As **3.716** células resultam em **3.610** textos distintos após normalização técnica conservadora (minúsculas, diacríticos, pontuação simples e espaços).
- **3.601** desses textos foram encontrados na base; **9** não foram localizados. Alguns aparecem em mais de um registro-base, originando **3.621 IDs** correspondentes.
- **12** desses IDs também apresentam a mesma expressão em uma origem sem a cor dourada. Eles ficam pendentes de revisão, sem exclusão automática.
- **3.609 IDs** foram retirados **somente das visões derivadas de trabalho**.

## Efeito na auditoria

| Arquivo de trabalho | Antes | Depois | Diferença |
|---|---:|---:|---:|
| 30 lotes — registros-base | 294.905 | 291.296 | −3.609 |
| 30 lotes — controles | 2.190 | 2.190 | 0 |
| Fila geral P0–P3 | 52.046 | 51.884 | −162 |
| Fila P3 (incluindo tratados) | 23.965 | 23.865 | −100 |
| P3 estritamente elegíveis | 19.562 | **19.462** | **−100** |

Dos 162 IDs dourados na fila geral, 100 pertencem à P3 ainda elegível, 29 à P3 previamente tratada e 33 à P2. **A fila P3 filtrada preserva os 29 já tratados**, para não apagar a trilha histórica daquela revisão. A visão geral filtrada exclui os 162, sem alterar o arquivo canônico; os 33 P2 também permanecem documentados no relatório por IDs.

## Conteúdo e como reutilizar

- `ids-ouro-cruzados-3621.csv`: todos os registros encontrados, incluindo os 12 de origem dupla.
- `ids-ouro-excluir-3609.csv`: exclusões confirmadas, com evidência, local exato na semente e justificativa.
- `ids-ouro-revisar-12.csv`: conflitos de origem colorida e não colorida.
- `ids-p3-ouro-removidos-100.csv`: exclusões aplicadas na fila estritamente elegível P3.
- `fila-p3-v5.2-sem-ouro-23865.csv`: fila P3 de trabalho preservando os pareceres anteriores.
- `pendentes-p3-sem-ouro-19462.csv`: somente os elegíveis restantes, para a próxima expansão após v5.3.
- `fila-geral-v5.2-sem-ouro-51884.csv`: visão geral filtrada, nunca substitui o original.
- `lotes-30-trabalho-sem-ouro.zip`: os 30 lotes filtrados para uso derivado. **Não substitui os lotes canônicos** usados nos testes históricos.
- `qa-cores-ouro-p3-v5.2-centralizada.xlsx`: resumo e conferência com todas as células centralizadas.
- `estatistica-planilhas-ods.csv`, `sementes-douradas-sem-match-na-base-9.csv`, `regressao-30-lotes.csv`: evidências complementares.
- `auditar_e_filtrar_ouro.py`: script reproduzível (requer `lxml`); recebe ZIP das 7 ODS e ZIP P3 v5.2 como entrada.
- `verificar_independente.py`: regressão independente comparando **cada registro retido** contra o arquivo-fonte completo.
- `gerar_qa_ouro.py`: reconstrução da planilha QA (`artifact_tool`).
- `resumo.json`, `manifesto-fontes.json`, `SHA256SUMS.txt`: contagens e integridade.

**Reexecução:**

```bash
python auditar_e_filtrar_ouro.py \
  --ods-zip /caminho/todas_originais_ods.zip \
  --p3-zip /caminho/portal-calculadoras-auditoria-P3-v5.2-unico.zip \
  --saida /caminho/saida
```

## Limites e próximos passos

A marca de cor sinaliza a origem/variante gerada, **não demonstra por si só ausência de busca real no Google Ads**. Por isso as palavras foram retiradas da fila operacional, mas dados de volume Ads e palavras-chave originais foram preservados no arquivo canônico. Não se devem somar volumes de palavras geradas artificialmente nem presumir que uma frase plausível é gerada sem evidência da origem.

A identificação em mais de uma célula pode gerar múltiplos registros coincidentes; a exclusão foi feita exclusivamente por **ID**, sem apagar famílias inteiras. Não há exclusão por aproximação fuzzy ou semelhança parcial. Palavras semelhantes não pintadas continuam na base, pois a cor é a evidência rastreável.

**Homologação editorial: PENDENTE.** A P3 v5.3 deve revisar os 75 pareceres anteriores da v5.2, consultando o filtro de 100 exclusões na seleção das próximas expansões. Revisar os 12 casos de origem dupla e as 9 sementes não localizadas se houver necessidade de interpretação adicional.