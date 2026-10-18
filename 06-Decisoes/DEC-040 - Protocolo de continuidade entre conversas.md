# DEC-040 — Protocolo de continuidade entre conversas

Data: 2026-10-17. Solicitado pelo usuário após o limite da conversa anterior.

## Fonte de verdade
"Cofre", no contexto do projeto, significa o vault Obsidian versionado no GitHub `alicedias9189/portal-calculadoras-knowledge2`, sincronizado no Ubuntu com `git pull`. A Biblioteca/Cofre de arquivos do ChatGPT É OUTRO sistema. Salvar apenas na Biblioteca não alimenta o Git.

## Registro obrigatório daqui em diante
1. Antes de continuar, ler `08-Continuidade/ESTADO-ATUAL.md`, os registros mais recentes em `08-Continuidade/Registros/` e as últimas DEC.
2. Ao concluir cada resposta substantiva, criar um arquivo Markdown em `08-Continuidade/Registros/` contendo: data, solicitação, o que foi executado, fatos, contagens, decisões, arquivos, Git commit, riscos, pendências e próxima ação. Se houver várias respostas numa mesma sessão, usar nomes únicos sequenciais.
3. Atualizar `08-Continuidade/ESTADO-ATUAL.md` com o resumo cumulativo, o último commit e próximo passo. Preferir arquivos nomeados e imutáveis; nunca sobrescrever entregáveis aprovados silenciosamente.
4. Salvar scripts reutilizáveis em `07-Scripts/`, decisões em `06-Decisoes/` e entregas em `08-Entregas/` com manifesto de origem e integridade. Planilhas com células centralizadas e dados completos preservados.
5. Distinguir "executado", "revisado por regras", "aprovado editorialmente", "salvo na Biblioteca", "objeto Git preparado" e "commit visível no GitHub". Nunca declarar sincronização sem conferir branch e arquivos.
6. Se uma ferramenta futura não tiver autorização para escrever no GitHub, registrar a limitação com clareza; não assumir persistência automática apenas pela conversa.

## Limitação estrutural
Um modelo numa nova conversa pode não ler o GitHub espontaneamente. A orientação é abrir `08-Continuidade/ESTADO-ATUAL.md` no início e referenciar os registros; quando necessário, o usuário pode pedir "leia o estado atual do vault".