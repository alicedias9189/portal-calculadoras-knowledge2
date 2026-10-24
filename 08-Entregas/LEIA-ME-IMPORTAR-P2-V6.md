# Importar P2 v6 no Knowledge Vault — GitHub

1. Na pasta local `portal-calculadoras-knowledge2` execute `git status` e `git pull` antes de importar. Guarde alterações locais que ainda não foram commitadas.
2. Extraia este ZIP **em uma pasta temporária**, NÃO diretamente sobre arquivos locais modificados. Confira `08-Continuidade/ESTADO-ATUAL.md` e faça merge de possíveis mudanças pessoais.
3. Copie as pastas `06-Decisoes`, `07-Scripts`, `08-Entregas`, `08-Continuidade` para a raiz, preservando a estrutura. Não sobrescreva versões antigas diferentes; os dois ZIPs-fonte da P2 v5 podem já estar presentes.
4. No diretório raiz, execute `sha256sum -c 08-Entregas/P2-v6/SHA256SUMS-P2-V6.txt`.
5. Opcional: reexecute a regressão `python3 07-Scripts/auditar_regressao_p2_v6.py --base . --novo 08-Entregas/P2-v6`.
6. `git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade && git commit -m "Auditoria P2 v6: 387 ajustes e 4761 pendencias" && git push`

Este pacote **não foi enviado ao GitHub pelo assistente**. A planilha é amostra/QA, os CSVs integrais com todas as colunas estão nos ZIPs.
