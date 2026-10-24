# IMPORTAR P3 v3.1 NO GITHUB

1. Extraia este ZIP em uma pasta temporária.
2. Leia `08-Entregas/P3-v3.1/RELATORIO-P3-V3.1.md` e a decisão `06-Decisoes/DEC-067 - Revisao critica P3 v3.1.md`.
3. Copie as pastas fornecidas ao seu repositório preservando a estrutura. **Não sobrescreva versões anteriores nem exclua o histórico.**
4. Confirme as somas SHA-256 em `SHA256SUMS-P3-V3.1.txt` (linhas relativas à raiz do ZIP).
5. Revise o diff e faça o commit no seu ambiente. Nenhuma mudança foi enviada automaticamente ao repositório.

## Arquivos principais

- `08-Entregas/P3-v3.1/lotes-001-a-030-p3-v3.1.zip`: todos os 30 lotes atualizados.
- `08-Entregas/P3-v3.1/p3-v3.1-fila-23965.csv`: fila P3 completa.
- `08-Entregas/P3-v3.1/fila-geral-p0-p1-p2-p3-v3.1.csv`: fila geral completa.
- `08-Entregas/P3-v3.1/p3-v3.1-pareceres-36.csv`: justificativas individualizadas.
- `08-Entregas/P3-v3.1/p3-v3.1-patches.csv`: campos anteriores/posteriores por ID.
- `08-Entregas/P3-v3.1/qa-auditoria-P3-v3.1-centralizada.xlsx`: seis abas, células centralizadas.
- `08-Entregas/P3-v3.1/FONTES-REPRODUCAO/`: dados de entrada incluídos no pacote.
- `07-Scripts/P3/`: três scripts executáveis sem alterar as fontes.

## Reexecutar

Instale `artifact_tool` no ambiente apenas se desejar reconstruir a planilha Excel; os scripts de auditoria e regressão utilizam exclusivamente a biblioteca padrão do Python.

Da raiz do pacote:

```bash
python 07-Scripts/P3/auditar_p3_v31.py
python 07-Scripts/P3/regressao_independente_p3_v31.py
python 07-Scripts/P3/gerar_qa_p3_v31.py
```

Todos os pareceres continuam provisórios, sujeitos a homologação editorial. A revisão v3.1 não expandiu a fila P3; revisou 36 decisões v3.0.
