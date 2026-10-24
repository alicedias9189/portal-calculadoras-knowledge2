# Como importar P2 v5 no vault GitHub

1. **Antes de extrair:** confirme `git status` limpo ou guarde suas alterações; use `git pull` para atualizar a branch atual.
2. Extraia o ZIP **para uma pasta temporária** e examine `08-Continuidade/ESTADO-ATUAL.md`. Se o arquivo local foi alterado, **mescle manualmente**, em vez de sobrescrevê-lo sem conferir.
3. Copie as **pastas do pacote** para a raiz `portal-calculadoras-knowledge2` preservando a estrutura. Arquivos novos ficam em `08-Entregas/P2-v5`, `06-Decisoes/DEC-043 ...` e `07-Scripts/`. As duas fontes P2-v4 são as mesmas da entrega anterior: se já existem, compare hashes e não substitua.
4. Na raiz do repositório, confira a integridade dos artefatos novos com `sha256sum -c 08-Entregas/P2-v5/SHA256SUMS-P2-V5.txt`. O manifesto inclui apenas arquivos P2-v5.
5. Opcionalmente reexecute a regressão: `python3 07-Scripts/auditar_regressao_p2_v5.py --base . --novo 08-Entregas/P2-v5`.
6. Confira `git status` e publique:

```bash
git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade
git commit -m "Auditoria P2 v5: 414 ajustes, 5148 pendencias"
git push
```

**Importante:** este pacote não altera o GitHub sozinho. A planilha XLSX centralizada é resumo/amostra; os CSVs completos estão no ZIP de auditoria. A v5 não aprova editorialmente todas as 5.148 pendências.
