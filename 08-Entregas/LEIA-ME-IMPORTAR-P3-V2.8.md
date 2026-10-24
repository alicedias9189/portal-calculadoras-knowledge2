# P3 v2.8 — Como importar ao GitHub

1. Extraia este ZIP numa pasta temporária.
2. Leia `08-Entregas/P3-v2.8/RELATORIO-P3-V2.8.md` e a `06-Decisoes/DEC-064 ...`.
3. Copie os diretórios `06-Decisoes`, `07-Scripts/P3`, `08-Continuidade` e `08-Entregas/P3-v2.8` para o repositório, preservando nomes e estrutura. **Não sobrescreva entregas antigas**.
4. Confira o manifesto `SHA256SUMS-P3-V2.8.txt`. A entrega inclui os 30 CSVs atualizados dentro de `lotes-001-a-030-p3-v2.8.zip`.
5. Para repetir a análise e a validação, a partir da raiz do pacote, execute:
   ```
   python3 07-Scripts/P3/auditar_p3_v28.py
   python3 07-Scripts/P3/validar_regressao_p3_v28.py
   python3 07-Scripts/P3/testar_seletor_p3_v28.py
   python3 07-Scripts/P3/gerar_qa_p3_v28.py
   ```
   Somente o último script precisa do pacote Python `artifact_tool`.
6. Faça o commit manual depois da revisão do diff. O GitHub não foi alterado automaticamente.

O ZIP da fonte histórica v2.7 está dentro de FONTES-REPRODUCAO. As 98 propostas globais foram copiadas sem alterações, mas não pertencem à P3. Consulte a divergência de 9 itens históricos antes de comparar totais.
