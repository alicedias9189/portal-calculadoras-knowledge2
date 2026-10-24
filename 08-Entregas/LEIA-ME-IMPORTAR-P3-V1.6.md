# Importar P3 v1.6 no vault Obsidian/GitHub

1. Verifique que o repositório local `portal-calculadoras-knowledge2` não tenha alterações pendentes com `git status`.
2. Extraia o ZIP **em uma pasta temporária**, NÃO diretamente sobre arquivos existentes.
3. A partir da raiz dessa pasta temporária: `sha256sum -c SHA256SUMS-P3-V1.6.txt` (em Linux) e leia `06-Decisoes/DEC-052 ... .md`.
4. Copie as novas pastas `06-Decisoes`, `07-Scripts/P3` e `08-Entregas/P3-v1.6` para a raiz do repositório. Para `08-Continuidade/ESTADO-ATUAL.md`, faça merge se houver versão mais recente localmente, não sobrescreva cegamente. O registro datado em `08-Continuidade/Registros` pode ser copiado diretamente.
5. No repositório: `git status`; depois `git add 06-Decisoes 07-Scripts/P3 08-Entregas/P3-v1.6 08-Continuidade`; `git commit -m 'Auditar 78 classificacoes e ampliar P3 v1.6'`; `git push`.
6. A versão v1.6 é paralela; NÃO apague v1.5 ou anteriores. Binários grandes podem exigir verificação dos limites GitHub. Nada foi enviado automaticamente pelo ChatGPT.

## Reprodução
A fonte está em `08-Entregas/P3-v1.6/FONTES-REPRODUCAO/`.

```bash
python3 07-Scripts/P3/auditar_p3_v16.py --fonte 08-Entregas/P3-v1.6/FONTES-REPRODUCAO --saida /tmp/reproduzir_p3_v16
python3 07-Scripts/P3/regressao_independente_p3_v16.py --fonte 08-Entregas/P3-v1.6/FONTES-REPRODUCAO --saida /tmp/reproduzir_p3_v16
```

Opcional (requer `artifact_tool`):

```bash
python3 07-Scripts/P3/gerar_qa_p3_v16.py --saida /tmp/reproduzir_p3_v16
```

A auditoria preserva 294.905 IDs, 2.190 controles e todos os campos protegidos. Os 163 patches e 78 pareceres permanecem na trilha CSV. As regras são propostas técnicas, não homologação editorial.
