# IMPORTAÇÃO MANUAL — P3 v2.6 (50 casos globais + 17 P3)

1. Extraia o ZIP numa pasta temporária, **não diretamente sobre o vault**.
2. Confira `SHA256SUMS-P3-V2.6.txt` com `sha256sum -c SHA256SUMS-P3-V2.6.txt` na raiz da extração.
3. Leia a DEC-062 e `08-Entregas/P3-v2.6/RELATORIO-P3-V2.6.md`.
4. Revise `08-Continuidade/ESTADO-ATUAL.md` e incorpore seu conteúdo ao estado local, sem substituir cegamente alterações posteriores no GitHub.
5. Copie os arquivos novos preservando os diretórios. A nova versão não sobrescreve os lotes v2.3 nem o backlog v2.5.
6. Opcionalmente reexecute `python3 07-Scripts/P3/auditar_global_e_p3_v26.py` e `python3 07-Scripts/P3/testar_escopo_v26.py`; gere a planilha com `python3 07-Scripts/P3/gerar_qa_global_p3_v26.py` (requer `artifact_tool`).
7. Após revisar o diff, execute `git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade SHA256SUMS-P3-V2.6.txt` e `git commit -m "Auditoria global A50 e microexpansao P3 v2.6"` e `git push`.

## Segurança

- O backlog global de 98 **não pertence à fila P3** e permanece sem alterações nos 30 lotes.
- Apenas 17 IDs P3 elegíveis foram alterados, em campos analíticos permitidos. Não há promoção automática de prioridades.
- P0/P1/P2, 294.905 IDs originais, 2.190 controles e campos originais Ads preservados.
- Parecer técnico contextual **não significa homologação editorial humana**.
- Esta entrega é um ZIP único com os dados e scripts, sem envio automático para o GitHub.
