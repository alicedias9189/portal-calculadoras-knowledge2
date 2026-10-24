# Portal de Calculadoras — Entrega P3 v1.4

Este ZIP é preparado para **importação MANUAL** ao vault Obsidian/GitHub `alicedias9189/portal-calculadoras-knowledge2`. Não houve push automático.

## Conteúdo
- `08-Entregas/P3-v1.4/`: planilha, CSVs completos, lotes completos e regressões.
- `08-Entregas/P3-v1.4/FONTES-REPRODUCAO/08-Entregas/P3-v1.3/`: as quatro fontes necessárias à reexecução.
- `07-Scripts/P3/`: classificador, auditor, QA da planilha e regressão independente.
- `06-Decisoes/DEC-050 ...md`: decisão técnica e ressalvas.
- `08-Continuidade/ESTADO-ATUAL.md` e registro datado: descrição precisa do andamento.
- `SHA256SUMS-P3-V1.4.txt`: hashes SHA-256 para verificar o conteúdo.

## Importação segura (Ubuntu)
1. Faça backup e confirme `git status` limpo, ou separe seu trabalho local com commit/stash conforme preferir.
2. Extraia este ZIP para uma pasta temporária, **não diretamente no repositório**.
3. Compare os documentos existentes, especialmente `08-Continuidade/ESTADO-ATUAL.md`, com versões que você tenha modificado e faça merge quando necessário.
4. Copie as subpastas novas e arquivos da entrega para a raiz do repositório preservando nomes e estrutura.
5. Confira os arquivos importados e rode `git status`; depois `git add`, `git commit -m "Auditoria P3 v1.4"` e `git push`.

## Reproduzir a auditoria localmente
As quatro fontes P3 v1.3 estão em `08-Entregas/P3-v1.4/FONTES-REPRODUCAO/`.

```bash
python3 07-Scripts/P3/auditar_p3_v1_4.py \
  --fonte 08-Entregas/P3-v1.4/FONTES-REPRODUCAO \
  --saida /tmp/repro-p3-v1.4
python3 07-Scripts/P3/regressao_independente_p3_v1_4.py \
  --antes 08-Entregas/P3-v1.4/FONTES-REPRODUCAO/08-Entregas/P3-v1.3/lotes-001-a-030-p3-v1.3.zip \
  --depois /tmp/repro-p3-v1.4
```

Para planilha Excel, `gerar_qa_p3_v1_4.py` usa `artifact_tool`; os scripts de classificação/regressão usam apenas biblioteca padrão Python.

**Atenção:** regressão PASSOU certifica isolamento das alterações e integridade dos arquivos, não qualidade editorial definitiva de todas as 576 propostas.
