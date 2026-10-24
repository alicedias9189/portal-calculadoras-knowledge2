# Importação manual da auditoria P3 v1.8 para o GitHub

1. Salve o ZIP recebido e extraia em **pasta temporária**, não diretamente sobre o vault.
2. Verifique os hashes dos arquivos extraídos: `sha256sum -c SHA256SUMS-P3-V1.8.txt` a partir da raiz extraída. O manifesto lista os arquivos da entrega, exceto o próprio manifesto.
3. Compare `08-Continuidade/ESTADO-ATUAL.md` e outros arquivos existentes no vault antes de copiar. Em caso de alteração local posterior, faça merge manual em vez de sobrescrever.
4. Copie as novas subpastas e arquivos para a raiz do vault Obsidian `portal-calculadoras-knowledge2`. As fontes de reprodução ficam em `08-Entregas/P3-v1.8/FONTES-REPRODUCAO`.
5. Depois de revisar `git status`, execute `git add 06-Decisoes 07-Scripts/P3 08-Entregas/P3-v1.8 08-Continuidade` e `git commit -m "Auditoria P3 v1.8 com regressao"`, então `git push`.
6. O ZIP não foi enviado automaticamente ao GitHub; o comando `git pull` isolado não o traz antes do seu commit/push.

## Reprodução com Python
Da raiz do repositório, usando os arquivos-fontes do pacote:

```bash
python3 07-Scripts/P3/auditar_p3_v18.py --fonte 08-Entregas/P3-v1.8/FONTES-REPRODUCAO --saida /tmp/p3-v18-reexec
python3 07-Scripts/P3/regressao_independente_p3_v18.py --fonte 08-Entregas/P3-v1.8/FONTES-REPRODUCAO --saida /tmp/p3-v18-reexec
```

Para recriar o Excel, instale `artifact_tool` e execute:

```bash
python3 07-Scripts/P3/gerar_qa_p3_v18.py --saida /tmp/p3-v18-reexec
```

Os scripts não editam os arquivos da pasta de origem; usam a pasta de saída indicada. Os CSVs completos ficam em `08-Entregas/P3-v1.8/`, não apenas na planilha QA.
