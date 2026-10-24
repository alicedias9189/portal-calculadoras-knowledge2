# Como importar — P3 v2.1

1. Extraia o ZIP **em uma pasta temporária** e confirme `SHA256SUMS-P3-V2.1.txt` antes de copiar arquivos.
2. Confira se as versões P3 v1.9/v2.0 já importadas no seu vault são compatíveis; esta entrega cria uma **nova pasta P3-v2.1**, não substitui P3 v2.0.
3. Copie os diretórios `06-Decisoes`, `07-Scripts` e `08-Entregas` para a raiz do vault Obsidian `portal-calculadoras-knowledge2`, sem apagar arquivos existentes. Compare `08-Continuidade/ESTADO-ATUAL.md` antes de atualizar, caso tenha mudanças locais.
4. No Ubuntu:

```bash
cd ~/portal-calculadoras-knowledge2
sha256sum -c SHA256SUMS-P3-V2.1.txt
# execute após os arquivos desta entrega estarem no diretório correto
# para não editar seu histórico sem conferência:
git status
git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade
git commit -m "P3 v2.1 - revisão crítica de 165 decisões, 13 correções"
git push
```

O manifesto foi gerado **na raiz do ZIP**; a verificação `sha256sum -c` precisa ser executada a partir da pasta extraída, antes de copiar, ou copie o manifesto também para a raiz do repositório.

### Reproduzir sem depender de arquivos externos
As fontes necessárias estão em `08-Entregas/P3-v2.1/FONTES-REPRODUCAO/08-Entregas/P3-v2.0/`. Em uma cópia de teste da pasta extraída execute, nesta ordem:

```bash
python3 07-Scripts/P3/auditar_p3_v21.py
python3 07-Scripts/P3/regressao_independente_p3_v21.py
python3 07-Scripts/P3/gerar_qa_p3_v21.py
```

A planilha usa `artifact_tool`; auditor e regressão dependem apenas de Python padrão. Use uma **cópia de teste** porque os scripts reescrevem as saídas P3-v2.1.

### Conteúdo
- 30 lotes CSV completos da P3 v2.1 em ZIP, sem sobrescrever os 30 da v2.0
- CSVs das duas filas (23.965 e 52.046 registros) com oito colunas adicionais da v2.1
- 165 pareceres da amostra e 272 pareceres totais, 13 patches, regressões e resumo
- Excel centralizada, scripts, relatório, DEC-057, estado e histórico Markdown
- fontes usadas para reproduzir a revisão sem acesso a outras conversas

**Cuidado:** versão revisada por análise textual. Não homologação editorial humana nem valores de juros, regras do INSS ou consumo de veículos em tempo real.
