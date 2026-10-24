# IMPORTAÇÃO SEGURA — P3 v1.2

Esta entrega **não foi enviada ao GitHub automaticamente**. O usuário importa manualmente o ZIP.

## Como usar no Ubuntu
1. Faça backup de alterações locais e confira que o repositório `portal-calculadoras-knowledge2` está limpo: `git status --short`.
2. Extraia o ZIP desta entrega numa **pasta temporária**. Não sobrescreva diretamente o vault antes de conferir os caminhos.
3. Verifique o manifesto: na raiz da pasta extraída, execute `sha256sum -c SHA256SUMS-P3-V1.2.txt`.
4. Copie as pastas `01-Taxonomia`, `06-Decisoes`, `07-Scripts`, `08-Entregas`, `08-Continuidade` para a raiz do vault, preservando o histórico. `08-Continuidade/ESTADO-ATUAL.md` será substituído; revise antes caso tenha evoluído desde a P3 v1.1.
5. Verifique novamente o que foi modificado: `git status --short` e `git diff --stat`.
6. `git add 01-Taxonomia 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade`
7. `git commit -m 'Auditar P3 v1.2: Saude gestacao e simuladores bancarios'`
8. `git push`.

## Reprodução local
`python3 07-Scripts/P3/auditar_p3_v1_2.py --fonte . --destino /tmp/auditoria-p3-v1-2`
`python3 07-Scripts/P3/gerar_qa_p3_v1_2.py --dados /tmp/auditoria-p3-v1-2`

Requer a instalação do `artifact_tool` apenas para gerar o Excel. A triagem é feita com bibliotecas padrão do Python.

## Observações
O ZIP contém arquivos P3 v1.1 de entrada para reexecução; não elimina versões antigas. Não altera diretamente a taxonomia v1.1 preexistente. A nova área Saúde é proposta em v1.2 e requer validação editorial antes de se tornar global. `git push` será realizado por você.
