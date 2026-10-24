# Importar P2 v7 no vault Portal de Calculadoras

Pacote ZIP único para `alicedias9189/portal-calculadoras-knowledge2` (não enviado automaticamente).

1. Extraia este ZIP em uma pasta temporária.
2. Confira `08-Entregas/P2-v7/RELATORIO.md` e `06-Decisoes/DEC-045 - Fechamento conservador P2 v7 e prioridade P3.md`.
3. Copie os arquivos e pastas da extração para a raiz do seu repositório Git local **sem apagar arquivos anteriores**. A versão v6 fica em subpasta própria e pode coexistir com v7.
4. Antes de substituir `08-Continuidade/ESTADO-ATUAL.md`, compare o arquivo local com a versão do ZIP e **mescle eventuais anotações/commits posteriores**. A base do ZIP é a continuidade conhecida na entrega P2 v6.
5. Para conferir integridade depois da extração, execute na raiz do repositório: `sha256sum -c 08-Entregas/P2-v7/SHA256SUMS-P2-V7.txt`.
6. Para reproduzir a revisão: `python3 07-Scripts/revisar_p2_v7.py --raiz . --saida /tmp/saida-p2-v7`; `python3 07-Scripts/auditar_independente_p2_v7.py --raiz . --saida /tmp/saida-p2-v7`. Para regenerar a planilha, instale `artifact_tool` e execute `python3 07-Scripts/gerar_qa_p2_v7.py` (com arquivos v7 sob `08-Entregas/P2-v7`).
7. Após verificar, `git status`, `git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade`, `git commit -m "Auditar P2 v7 e priorizar P3"`, `git push`. Faça isso no seu GitHub; não houve push remoto do ChatGPT.

**Escopo:** 101 correções de P2; 4.660 pendências restantes; P3 não alterada. CSVs completos dentro dos ZIPs; Excel é amostra de QA. Fonte P2 v6 original incluída para reprodução. Não importar bases duplicadas como novas keywords nem somar volumes do Ads por variante.
