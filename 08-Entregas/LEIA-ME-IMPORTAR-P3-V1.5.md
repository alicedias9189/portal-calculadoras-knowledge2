# Importar P3 v1.5 no vault Obsidian/GitHub

1. Mantenha um backup do repositório local e verifique se não há mudanças pendentes (`git status`).
2. **Extraia este ZIP em uma pasta temporária**; confira seus arquivos e o `SHA256SUMS-P3-V1.5.txt` com `sha256sum -c` a partir da pasta temporária.
3. Revise os arquivos `06-Decisoes`, `07-Scripts/P3`, `08-Entregas/P3-v1.5` e `08-Continuidade`.
4. Copie as pastas da entrega para a **raiz** do vault (`portal-calculadoras-knowledge2`). Para `08-Continuidade/ESTADO-ATUAL.md`, faça merge se o local já contiver trabalho posterior.
5. No repositório, execute `git status`, `git add 06-Decisoes 07-Scripts/P3 08-Entregas/P3-v1.5 08-Continuidade`, `git commit -m 'Auditar 98 decisoes e ampliar P3 v1.5'` e `git push`.
6. Os arquivos ZIP internos e CSVs podem ser grandes. Confira limites de tamanho do repositório; não substitua fontes antigas nem apague arquivos anteriores.

## Reprodução sem a conversa
Os insumos completos estão em `08-Entregas/P3-v1.5/FONTES-REPRODUCAO`.

```bash
python3 07-Scripts/P3/auditar_p3_v1_5.py --fonte 08-Entregas/P3-v1.5/FONTES-REPRODUCAO --saida /tmp/p3_v1_5_repro
python3 07-Scripts/P3/regressao_independente_p3_v1_5.py --fonte 08-Entregas/P3-v1.5/FONTES-REPRODUCAO --saida /tmp/p3_v1_5_repro
```

Para gerar a planilha, requer `artifact_tool`:

```bash
python3 07-Scripts/P3/gerar_qa_p3_v1_5.py --saida /tmp/p3_v1_5_repro
```

A versão P3 v1.5 modifica apenas registros selecionados por regra dentro da P3; 294.905 IDs base e 2.190 controles preservados; 30 regressões PASSOU. **Esta é uma proposta de revisão assistida**, não homologação editorial. O ZIP NÃO foi enviado automaticamente ao GitHub.
