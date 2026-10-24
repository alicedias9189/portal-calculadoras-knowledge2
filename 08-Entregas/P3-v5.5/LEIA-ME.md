# Entrega P3 v5.5 — instruções de importação e reprodução

Esta entrega **revisa os 100 pareceres P3 v5.4** (DEC-091) e não abre novos IDs. Resultado: **23 refinamentos + 77 mantidos com ressalvas**, descritos em DEC-092.

## Conteúdo

- `08-Entregas/P3-v5.5/`: lotes canônicos (30), sem Ouro (30), filas completas (4), 100 pareceres, 23 patches com antes/depois, regressão independente, resumo JSON, relatório Markdown e Excel de QA de **oito abas com alinhamento central**.
- `07-Scripts/P3/`: quatro scripts Python reutilizáveis (`auditar`, `regressao_independente`, `gerar_qa`, `montar_entrega`).
- `06-Decisoes/DEC-092 - Revisao critica individual P3 v5.5.md` e `08-Continuidade/Registros/2026-10-24-11-P3-v5.5-revisao-100.md`.
- `SHA256SUMS-P3-V5.5.txt` com hashes por arquivo interno.

## Como reproduzir no vault

1. Extraia o **pacote P3 v5.4** na raiz local, mantendo `08-Entregas/P3-v5.4` com os arquivos de entrada.
2. Extraia este ZIP na **mesma raiz**, preservando a estrutura de pastas.
3. Execute na raiz: `python 07-Scripts/P3/auditar_p3_v55.py`.
4. Execute `python 07-Scripts/P3/regressao_independente_p3_v55.py` e confirme `PASSOU`/60 lotes.
5. Execute `python 07-Scripts/P3/gerar_qa_p3_v55.py` para atualizar a planilha. Execute `python 07-Scripts/P3/montar_entrega_p3_v55.py` se desejar refazer o ZIP de entrega.

Atenção: os nomes anteriores e as colunas de histórico devem ser preservados exatamente; não usar o filtro Ouro para apagar registros da fonte canônica.

**Pendências P3 sem Ouro: 19.362. Homologação editorial pendente.**