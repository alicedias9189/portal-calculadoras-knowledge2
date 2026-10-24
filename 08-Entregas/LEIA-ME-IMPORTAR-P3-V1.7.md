# Importar P3 v1.7 no vault Obsidian/GitHub

Entrega **paralela**, preserva P3 v1.6 e anteriores. **Não houve envio automático ao GitHub.**

1. No Ubuntu, abra o repositório local e rode `git status` para verificar alterações não commitadas.
2. Extraia este ZIP em **pasta temporária** fora do repositório, não diretamente em cima de versões existentes.
3. Na raiz temporária execute `sha256sum -c SHA256SUMS-P3-V1.7.txt` e confirme todas as entradas com `OK`.
4. Copie os diretórios `06-Decisoes`, `07-Scripts/P3` e `08-Entregas/P3-v1.7` para a pasta raiz do repositório. Mantenha as outras versões.
5. Copie o registro em `08-Continuidade/Registros/`; faça **merge manual** de `08-Continuidade/ESTADO-ATUAL.md` se sua cópia do vault for mais recente. Evite substituir alterações locais.
6. No repositório, rode `git status`, confira quais arquivos serão adicionados e execute:

```bash
git add 06-Decisoes 07-Scripts/P3 08-Entregas/P3-v1.7 08-Continuidade
git commit -m 'Auditar amostra estratificada P3 v1.7'
git push
```

## Reexecutar a auditoria
Da raiz do repositório, com Python 3 (stdlib):

```bash
python3 07-Scripts/P3/auditar_p3_v17.py --fonte 08-Entregas/P3-v1.7/FONTES-REPRODUCAO --saida /tmp/p3-v17-verificacao
python3 07-Scripts/P3/regressao_independente_p3_v17.py --fonte 08-Entregas/P3-v1.7/FONTES-REPRODUCAO --saida /tmp/p3-v17-verificacao
```

Para refazer planilha opcionalmente (requer `artifact_tool`):

```bash
python3 07-Scripts/P3/gerar_qa_p3_v17.py --saida /tmp/p3-v17-verificacao
```

O arquivo `p3-v1.7-regressao-independente-resumo.json` traz as contagens. Não confundir fila geral de revisão (52.046) com o universo de registros-base (294.905). Não tratar decisões técnicas como homologação editorial.
