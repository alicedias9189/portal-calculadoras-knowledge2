# Importação da auditoria P2 v4 no vault/GitHub

**Este ZIP ainda não está no GitHub**. Contém os arquivos no formato de pastas da raiz do repositório `alicedias9189/portal-calculadoras-knowledge2` para importação pelo usuário.

## Ubuntu — importar sem perder alterações

1. Baixe este ZIP único da conversa e abra um terminal na pasta do projeto `portal-calculadoras-knowledge2`.
2. Execute `git status --short` e confirme que não há mudanças locais a preservar. Se houver, faça commit ou reconcilie antes de extrair.
3. Descompacte o ZIP **na raiz da pasta do repositório**. Exemplos:

   ```bash
   cd ~/Área\ de\ trabalho/portal-calculadoras-knowledge2
   unzip -o ~/Downloads/portal-calculadoras-auditoria-P2-v4-unico.zip
   ```

   Se o arquivo ZIP baixado tiver outro nome, adapte o comando. O `-o` substitui os arquivos de mesmo nome no diretório: examine primeiro arquivos locais modificados, especialmente `08-Continuidade/ESTADO-ATUAL.md`. Uma opção mais segura é extrair em pasta temporária e copiar os novos arquivos após comparar.
4. Confira integridade a partir da raiz do repositório:

   ```bash
   sha256sum -c 08-Entregas/P2-v4/SHA256SUMS-P2-V4.txt
   git status --short
   git diff --stat
   ```

5. Se tudo estiver certo, envie manualmente:

   ```bash
   git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade LEIA-ME-IMPORTAR-P2-V4.md
   git commit -m "Auditoria contextual por familias P2 v4"
   git push
   ```

## Reexecução

O pacote traz as duas fontes v3 necessárias. Execute, a partir da raiz do repositório:

```bash
python3 07-Scripts/revisar_p2_v4.py --preview
python3 07-Scripts/revisar_p2_v4.py
python3 07-Scripts/auditar_regressao_p2_v4.py
python3 07-Scripts/gerar_qa_p2_v4.py
```

A primeira execução completa grava `saida-p2-v4/` fora da área versionada da entrega, por segurança. Para auditoria da entrega existente, execute `python3 07-Scripts/auditar_regressao_p2_v4.py --saida 08-Entregas/P2-v4`. A criação de XLSX depende do pacote Python `artifact_tool`; a classificação e regressão usam apenas a biblioteca padrão.

## Resumo
P2 v4: 384 reclassificações, 5.562 pendências. 30 lotes com 294.905 registros-base e 2.190 controles preservados. Os CSVs completos estão dentro do ZIP de auditoria, enquanto a planilha Excel é uma vista amostral e QA.
