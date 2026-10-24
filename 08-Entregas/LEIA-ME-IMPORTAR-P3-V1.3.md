# Importação manual — P3 v1.3

1. Faça backup do repositório antes de extrair.
2. Extraia **o ZIP completo na raiz** do repositório `portal-calculadoras-knowledge2` (não apague versões anteriores). Confira alterações locais antes de substituir `08-Continuidade/ESTADO-ATUAL.md`.
3. Confira o manifesto: `sha256sum -c SHA256SUMS-P3-V1.3.txt` a partir da raiz.
4. Consulte `08-Entregas/P3-v1.3/RELATORIO-P3-V1.3.md` e `06-Decisoes/DEC-049 - Expansao controlada P3 v1.3 e cinco falsos negativos.md`.
5. `git status`, `git add 07-Scripts/P3 08-Entregas/P3-v1.3 06-Decisoes/DEC-049* 08-Continuidade`, `git commit -m "Auditar P3 v1.3 com expansao controlada"`, `git push`.
6. Os arquivos CSV e ZIP fazem parte da entrega e podem aumentar o tamanho do repositório. Caso seu GitHub imponha limitações, avalie Git LFS ou Releases antes de subir os pacotes grandes.

## Reexecução
`python3 07-Scripts/P3/auditar_p3_v1_3.py --fonte 08-Entregas/P3-v1.3/FONTES-REPRODUCAO --saida /tmp/p3-v1.3-reexecutada`
`python3 07-Scripts/P3/regressao_independente_p3_v1_3.py --fonte 08-Entregas/P3-v1.3/FONTES-REPRODUCAO/08-Entregas/P3-v1.2 --saida /tmp/p3-v1.3-reexecutada`
`python3 07-Scripts/P3/gerar_qa_p3_v1_3.py --saida /tmp/p3-v1.3-reexecutada`

Não sobrescreva planilhas/arquivos históricos aprovados. A taxonomia Saúde v1.2 continua proposta técnica, não homologação editorial.
