# Como importar P3 v2.3 no seu vault GitHub

Esta entrega corrige a P3 v2.2; NÃO expande a fila indiscriminadamente.

1. Coloque o ZIP em uma pasta temporária e extraia seu conteúdo preservando os diretórios.
2. Revise `08-Entregas/P3-v2.3/RELATORIO-P3-V2.3.md` e `06-Decisoes/DEC-059 - Corrigir escopo P3 v2.3.md`.
3. Confira hashes usando `sha256sum -c SHA256SUMS-P3-V2.3.txt` a partir da pasta extraída.
4. Copie os arquivos para a raiz do repositório Git de modo controlado. **Confira o diff de `08-Continuidade/ESTADO-ATUAL.md` antes de substituir**, pois pode haver edições mais recentes em seu vault.
5. `git status`, `git add`, `git commit -m "Auditoria P3 v2.3: corrigir escopo e revisar amostra"` e `git push`.

Reprodução após extração:

```bash
python3 07-Scripts/P3/auditar_p3_v23.py
python3 07-Scripts/P3/regressao_independente_p3_v23.py
python3 07-Scripts/P3/gerar_qa_p3_v23.py  # requer artifact_tool
```

Os scripts usam Python padrão, exceto o gerador Excel que requer `artifact_tool`. Recomenda-se reexecutar numa cópia do ZIP extraído, pois o script de auditoria regenera as saídas v2.3.

Os 98 registros restaurados permanecem como propostas na quarentena para análise futura. Todos os CSVs completos e colunas históricas foram preservados. Não foi feito upload automático ao GitHub.
