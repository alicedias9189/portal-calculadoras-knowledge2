# Importação do piloto P3 v1 no GitHub

O ZIP NÃO foi enviado ao GitHub. Extraia primeiro numa pasta temporária e confira o relatório e as decisões.

1. No Ubuntu, entre no repositório `portal-calculadoras-knowledge2` e execute `git status` para confirmar que não há alterações inesperadas.
2. Extraia o pacote em uma pasta temporária; confira `08-Entregas/P3-v1/RELATORIO.md` e `08-Entregas/P3-v1/SHA256SUMS-P3-V1.txt`.
3. Copie as pastas `06-Decisoes`, `07-Scripts`, `08-Entregas` e `08-Continuidade` **sem apagar arquivos anteriores**; mescle manualmente `08-Continuidade/ESTADO-ATUAL.md` caso tenha sido atualizado localmente desde a P2 v7.
4. Na raiz do repositório: `sha256sum -c 08-Entregas/P3-v1/SHA256SUMS-P3-V1.txt`.
5. Para reproduzir: `python3 07-Scripts/P3/auditar_p3_v1_piloto.py --origem 08-Entregas/P2-v7 --saida /tmp/p3-v1-repro`; `python3 07-Scripts/P3/regressao_independente_p3_v1.py --origem 08-Entregas/P2-v7 --saida /tmp/p3-v1-repro`; `python3 07-Scripts/P3/gerar_filas_p3_v1.py --origem 08-Entregas/P2-v7 --saida /tmp/p3-v1-repro`. Planilha: `python3 07-Scripts/P3/gerar_planilha_p3_v1.py --qa /tmp/p3-v1-repro --arquivo /tmp/p3-v1-repro/qa.xlsx` (necessita `artifact_tool`).
6. Confira `git diff --stat` e `git status`; depois `git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade`, `git commit -m "Auditoria piloto P3 v1 com QA e continuidade"` e `git push`.

P3 v1 é um PILOTO: 1.207 propostas de correção, não homologação editorial. Preserva P2 v7. Não somar volumes das variantes Ads.
