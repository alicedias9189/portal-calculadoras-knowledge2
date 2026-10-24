# Portal de Calculadoras — P3 v5.4

Expansão de 100 novos registros com filtro operacional reversível de variantes Ouro; referência DEC-091.

## Conteúdo

- `06-Decisoes/DEC-091 - Expansao seletiva P3 v5.4 100 IDs.md`: decisão e salvaguardas.
- `08-Entregas/P3-v5.4/`: dois ZIPs com 30 lotes cada; quatro filas CSV completas; pareceres 100, patches 100, plano por ID, QA por grupo, regressão inicial, regressão independente, resumo JSON e planilha centralizada de 7 abas.
- `07-Scripts/P3/`: quatro scripts Python reexecutáveis de auditoria, regressão, QA e empacotamento.
- `08-Continuidade/Registros/`: registro de passagem e próxima etapa.
- `SHA256SUMS-P3-V5.4.txt`: manifesto verificável dos arquivos internos (exceto o próprio manifesto).

## Reexecução

1. Extrair o pacote anterior **P3 v5.3** na mesma raiz (fornece `08-Entregas/P3-v5.3/`); ele não é duplicado dentro desta entrega.
2. Extrair este ZIP sem alterar a estrutura de pastas, mantendo os arquivos `P3-v5.3` intactos.
3. Na raiz executar:
   - `python 07-Scripts/P3/auditar_p3_v54.py`
   - `python 07-Scripts/P3/regressao_independente_p3_v54.py`
   - `python 07-Scripts/P3/gerar_qa_p3_v54.py`
   - `python 07-Scripts/P3/montar_entrega_p3_v54.py`

Somente os IDs previstos em `p3-v5.4-pareceres-100.csv` podem receber alterações de classificação. Não alterar nem descartar as fontes canônicas. A filtragem de Ouro não é apagamento e permanece reversível.

**Estado:** 60 lotes PASSOU; P3 elegíveis sem Ouro 19.362; homologação editorial PENDENTE; próxima v5.5 para revisão de 100 pareceres.