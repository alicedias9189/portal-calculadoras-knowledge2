# Entrega P3 v2.0 — Importação manual no vault GitHub

**Não extrair diretamente sobre o repositório sem comparar arquivos primeiro.**

1. Extraia este ZIP em uma pasta temporária.
2. Conferir hashes: `sha256sum -c SHA256SUMS-P3-V2.0.txt` a partir da pasta extraída (nomes com acentos estão em UTF-8).
3. Compare/copiei as pastas `06-Decisoes`, `07-Scripts/P3`, `08-Entregas/P3-v2.0` e `08-Continuidade/Registros` para o repositório local `portal-calculadoras-knowledge2`. Para `08-Continuidade/ESTADO-ATUAL.md`, faça merge manual se sua cópia local for mais recente.
4. Os dados estão em versões paralelas: não remover nem sobrescrever os lotes v1.9 ou versões históricas.
5. Opcional, reproduzir a P3 v2.0 (Python padrão):

```bash
python3 07-Scripts/P3/auditar_p3_v20.py \
  --base 08-Entregas/P3-v2.0/FONTES-REPRODUCAO/08-Entregas/P3-v1.9 \
  --saida /tmp/p3-v20-reexecucao
python3 07-Scripts/P3/regressao_independente_p3_v20.py \
  --base 08-Entregas/P3-v2.0/FONTES-REPRODUCAO/08-Entregas/P3-v1.9 \
  --resultado /tmp/p3-v20-reexecucao
```

6. A planilha de QA foi gerada usando `artifact_tool`. Opcionalmente regenere:

```bash
python3 07-Scripts/P3/gerar_qa_p3_v20.py \
  --resultados /tmp/p3-v20-reexecucao \
  --saida /tmp/qa-P3-v2.0-centralizada.xlsx
```

7. Inspecione `git status`, então `git add 06-Decisoes 07-Scripts/P3 08-Entregas/P3-v2.0 08-Continuidade` e efetue `git commit` / `git push` conforme sua política local.

**Nenhum commit automático foi feito pelo ChatGPT.** Novas categorias e intenções ainda são propostas técnicas, não homologação editorial. P2 mantém 4.660 pendências.
