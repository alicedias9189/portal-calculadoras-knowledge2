# LEIA-ME — IMPORTAÇÃO MANUAL P3 v2.7

1. Extraia este ZIP **em uma pasta temporária**, nunca diretamente por cima do vault.
2. Execute `sha256sum -c SHA256SUMS-P3-V2.7.txt` na raiz extraída; todos devem retornar OK.
3. Leia `08-Entregas/P3-v2.7/RELATORIO-P3-V2.7.md` e `06-Decisoes/DEC-063 - Revisao critica P3 v2.7 e backlog global B-C.md`.
4. Copie as **pastas novas da entrega** para o vault GitHub. Revise e integre `08-Continuidade/ESTADO-ATUAL.md` por diff, sem substituir modificações feitas no vault após esta entrega.
5. Se quiser reproduzir, execute na raiz extraída: `python3 07-Scripts/P3/auditar_p3_v27.py`, depois `python3 07-Scripts/P3/validar_regressao_p3_v27.py` e `python3 07-Scripts/P3/gerar_qa_p3_v27.py` (este último requer `artifact_tool`).
6. Use `git status`, `git diff --stat`, `git add 06-Decisoes 07-Scripts/P3 08-Entregas/P3-v2.7 08-Continuidade`, `git commit -m "Revisao P3 v2.7 e backlog global B C"` e `git push`.

### Segurança de escopo

- **Não aplicar** nenhuma das 98 propostas globais nos lotes. A v2.7 alterou somente o ID P3 `190795` em campos analíticos.
- Não misture lotes v2.2 históricos (que possuíam alterações indevidas) com esta versão.
- Os 30 lotes e duas filas completas estão no diretório `08-Entregas/P3-v2.7/`.
- Todos os insumos necessários à reprodução foram incluídos em `FONTES-REPRODUCAO/`.
- A entrega não faz commit automático no GitHub.
