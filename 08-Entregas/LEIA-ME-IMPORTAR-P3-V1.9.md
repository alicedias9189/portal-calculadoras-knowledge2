# Importação manual P3 v1.9 para o vault GitHub

1. Extraia este ZIP **num diretório temporário** (não sobrescreva diretamente o seu vault).
2. Compare os caminhos `06-Decisoes/`, `07-Scripts/P3/`, `08-Entregas/P3-v1.9/` e `08-Continuidade/` com o seu `portal-calculadoras-knowledge2`.
3. Copie os arquivos novos para as pastas equivalentes. Se seu `08-Continuidade/ESTADO-ATUAL.md` já recebeu mudanças posteriores, **faça merge manual** em vez de substituí-lo.
4. Da raiz do vault, execute, se quiser reproduzir esta auditoria (Python 3):

```bash
python3 07-Scripts/P3/auditar_p3_v19.py \
  --fonte 08-Entregas/P3-v1.9/FONTES-REPRODUCAO \
  --saida /tmp/reproducao-p3-v19
python3 07-Scripts/P3/regressao_independente_p3_v19.py \
  --fonte 08-Entregas/P3-v1.9/FONTES-REPRODUCAO \
  --saida /tmp/reproducao-p3-v19
```

5. Para gerar QA Excel no seu Ubuntu, use `gerar_qa_p3_v19.py` (necessita `artifact_tool`). A auditoria e regressão CSV dependem só da biblioteca padrão.
6. Verifique os hashes de `SHA256SUMS-P3-V1.9.txt` antes da importação ou do commit.
7. Por fim, faça `git status`, `git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade`, `git commit -m "Auditoria critica P3 v1.9"` e `git push`.

**Atenção:** estes arquivos não foram enviados ao GitHub pelo ChatGPT. A v1.8 e quaisquer decisões anteriores não devem ser apagadas. Os ZIPs contém versões paralelas. A decisão DEC-055 contém os limites editoriais da revisão.
