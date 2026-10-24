#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Empacota entrega P2 v5 para importação manual no GitHub; preserva fontes v4."""
import json,hashlib,shutil,zipfile,csv,io
from pathlib import Path
from collections import Counter

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 base=Path(__file__).resolve().parent; prior=base/'input'; out=base/'out';stage=base/'pacote'; stage.mkdir(parents=True,exist_ok=True)
 meta=json.loads((out/'resumo-p2-v5.json').read_text());qa=json.loads((out/'regressao-independente-p2-v5.json').read_text())
 assert qa['status']=='PASSOU' and meta['reclassificadas']==414
 files={
 '08-Entregas/P2-v4/auditoria-p2-v4-csv-integral.zip':prior/'08-Entregas/P2-v4/auditoria-p2-v4-csv-integral.zip',
 '08-Entregas/P2-v4/lotes-001-a-030-p0-p1-p2-v4.zip':prior/'08-Entregas/P2-v4/lotes-001-a-030-p0-p1-p2-v4.zip',
 '08-Entregas/P2-v5/auditoria-p2-v5-csv-integral.zip':out/'auditoria-p2-v5-csv-integral.zip',
 '08-Entregas/P2-v5/lotes-001-a-030-p0-p1-p2-v5.zip':out/'lotes-001-a-030-p0-p1-p2-v5.zip',
 '08-Entregas/P2-v5/resumo-p2-v5.json':out/'resumo-p2-v5.json',
 '08-Entregas/P2-v5/regressao-independente-p2-v5.json':out/'regressao-independente-p2-v5.json',
 '08-Entregas/P2-v5/qa-validacao-p2-v5-centralizada.xlsx':out/'qa-validacao-p2-v5-centralizada.xlsx',
 '07-Scripts/revisar_p2_v5.py':base/'revisar_p2_v5.py',
 '07-Scripts/auditar_regressao_p2_v5.py':base/'auditar_regressao_p2_v5.py',
 '07-Scripts/gerar_qa_p2_v5.py':base/'gerar_qa_p2_v5.py',
 '07-Scripts/empacotar_p2_v5.py':base/'empacotar_p2_v5.py',
 }
 for name,source in files.items():
  dest=stage/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
 ra=Counter(meta['regras']);top='\n'.join(f'| {k.replace("_"," ")} | {v} |' for k,v in ra.most_common())
 report=f'''# P2 v5 — revisão contextual das pendências

Data: **2026-10-20**. Base: P2 v4 auditada, decisão DEC-042 preservada. Nova decisão: DEC-043.

## Escopo e resultados finais

| Métrica | Quantidade |
|---|---:|
| P2 total (sem mudança de escopo) | 25.050 |
| Pendências recebidas da P2 v4 | 5.562 |
| Reclassificações realizadas | **414** |
| Sem ressalva operacional | 181 |
| Com ressalva | 233 |
| Famílias com alterações | 185 |
| Pendências restantes | **5.148** |
| IDs-base originais preservados | 294.905 |
| Controles preservados | 2.190 |
| Lotes com regressão independente aprovada | 30/30 |

## Regras de reclassificação

| Regra | Registros |
|---|---:|
{top}

**As decisões sem ressalva significam confiança da regra, NÃO revisão editorial humana individual.** As decisões com ressalva dependem de dados adicionais (ex.: prazo, taxa, referência de pressão, OCR, localidade ou moeda histórica).

## Famílias que não autorizam conversões assumidas

- 157 variantes numéricas «N semanas e D dias»: não presumir gravidez, calendário de meses nem operação desejada. Permaneceram pendentes.
- Família com 69 consultas Fahrenheit anteriormente pendentes: uma variante «fahrenheit para k» contém destino explícito e foi tratada; 68 casos da família continuam ambíguos (temperaturas isoladas ou expressões sem destino).
- «milhas em km h» não informa inequivocamente uma velocidade na origem; não tratar distância como velocidade.
- «libra» em pressão ou cotação pode indicar grandezas distintas; classificar apenas intenção com ressalvas.
- Transformadores de 110/220 V são equipamentos, não conversores de unidade numérica.
- Pesquisas por teorias, tutoriais e PDFs de exercícios não são automaticamente calculadoras ou conversões de arquivo.

## Regressão independente

O auditor `07-Scripts/auditar_regressao_p2_v5.py` comparou os **30 arquivos v4/v5 linha por linha**. Conferiu:

- 294.905 IDs-base únicos e invariáveis, 73 controles por lote (2.190 no total);
- diferenças somente nos 11 campos analíticos autorizados, e apenas nos 414 IDs selecionados;
- nenhum outro ID modificado, nenhum controle alterado e nenhuma mudança em P0, P1 ou P3;
- valores antes/depois dos patches coincidem com os **CSVs reais** de origem e destino (não apenas com a fila analítica);
- conversões diretas novas com origem e destino preenchidos;
- integridade CRC dos ZIPs e contagem dos CSVs da P2.

Detalhes: `regressao-independente-p2-v5.json`, `p2-v5-qa-regressao-30-lotes.csv` e manifestos SHA256.

## Limitações e próximos passos

A revisão é contextual **baseada em regras específicas por keyword e inspeção de candidatos**, não uma checagem editorial independente de todas as 5.562 consultas. A amostra de pendências na planilha não substitui os CSVs integrais. Não criar volume Ads somando variantes ou preencher taxas, unidades e direções sem evidência.

**Próxima prioridade:** revisar as 5.148 pendências em famílias de tensão/corrente genéricas, modelos comerciais, números isolados, moedas de país indeterminado e consultas administrativas, por relevância/volume e risco. Documentar novas decisões com regressão separada.
'''
 (stage/'08-Entregas/P2-v5/RELATORIO.md').write_text(report,encoding='utf-8')
 decision=f'''# DEC-043 — Auditoria semântica focalizada P2 v5

Data: 2026-10-20.

**Decisão:** aceitar a P2 v5 como **versão paralela auditável**, aplicando 414 reclassificações contextuais aos registros ainda pendentes da P2 v4, sem editar os arquivos históricos. Usar a mesma taxonomia e preservar dados originais/Google Ads, P0/P1/P3 e controles.

- 5.562 pendências na entrada; 414 registros alterados em 185 famílias; 181 sem ressalva de regra e 233 com ressalva; 5.148 permanecem abertos.
- Comparação independente de 30 lotes: PASSOU, 294.905 IDs-base e 2.190 controles preservados.
- Corrigida a trilha antes/depois para refletir os CSVs reais de v4/v5. Não chamar o registro anterior na fila de "antes" da base.
- Não assumir gravidez para 157 consultas só com semanas e dias; não assumir destino em 68 consultas Fahrenheit isoladas; reconhecer o caso explícito Fahrenheit → K.
- Dados completos, lote a lote, residem nos ZIPs em `08-Entregas/P2-v5/`; planilha Excel é auditoria centralizada resumida.

**Status:** revisão por regras com QA estrutural aprovada; NÃO homologação editorial da P2 nem das 5.148 pendências restantes.

Relatório: [[08-Entregas/P2-v5/RELATORIO]]. Próxima etapa: análise focalizada v6 de famílias ainda pendentes.
'''
 (stage/'06-Decisoes').mkdir(exist_ok=True)
 (stage/'06-Decisoes/DEC-043 - Auditoria contextual P2 v5.md').write_text(decision,encoding='utf-8')
 state=f'''# ESTADO ATUAL — Portal de Calculadoras

Atualizado: **2026-10-20**, auditoria P2 v5. Importação ao GitHub ainda é uma **ação do usuário**, não foi feita pelo ChatGPT.

## Referência
Vault Obsidian no repositório `alicedias9189/portal-calculadoras-knowledge2`, branch `main`. O vault Git NÃO é a Biblioteca de arquivos do ChatGPT. Antes de avançar, ler o último registro em `08-Continuidade/Registros/` e as DEC-037 a DEC-043.

## Escopo, regras e preservação
Portal de calculadoras/conversores de matemática, datas, áreas trabalhistas, elétrica, construção e outras. Keyword e Ads são dados de origem. Há 30 lotes, **294.905 registros-base** e **2.190 controles**, 73 em cada lote.
Conservar IDs, volumes e 16 colunas originais; não somar volume Ads de variantes; reconstruir caracteres removidos (como barras) somente por contexto; não supor direção de câmbio, densidade ou equivalência entre dimensões incompatíveis.

## Etapas
- 30 lotes iniciais e Golden Set histórico encerrados. DEC-036 (saneamento lote 001) e DEC-037 (P0): P0 de 474 keywords, 462 patches, 109 incertezas contextuais.
- P1 v1/v2: 2.557 entradas, 32 ambiguidades finais ainda sem contexto; preservar decisões.
- P2 v1: 25.050 keywords; v2: 8.813 pendências examinadas, restaram 6.138.
- P2 v3: 192 novas reclassificações, 5 alertas corrigidos, restaram 5.946.
- P2 v4: 384 reclassificações (109 sem ressalva, 275 com ressalva), restaram 5.562. DEC-042.
- **P2 v5: 414 reclassificações (181 sem ressalva, 233 com ressalva); 5.148 pendências.** 30/30 lotes aprovados na regressão independente. DEC-043.
- P3 ainda não iniciada neste fluxo.

## Arquivos da versão atual
- `08-Entregas/P2-v5/lotes-001-a-030-p0-p1-p2-v5.zip`: 30 lotes CSV.
- `08-Entregas/P2-v5/auditoria-p2-v5-csv-integral.zip`: decisões 25.050, pendências 5.148, 414 patches, fila geral e QA.
- `08-Entregas/P2-v5/qa-validacao-p2-v5-centralizada.xlsx`: amostras, regras, resumo e patches, células centralizadas.
- `07-Scripts/revisar_p2_v5.py`, `auditar_regressao_p2_v5.py`, `gerar_qa_p2_v5.py` e `empacotar_p2_v5.py`.
- ZIP inclui as duas fontes P2 v4 requeridas para reprodução. **Não sobrescrever versões históricas homologadas.**

## Regra de operação / continuidade
1. Ao ouvir "Faça", executar a ação mais recentemente sugerida, especificada ou decidida pelo assistente, sem pedir novamente se a intenção estiver clara.
2. Entregar **um único ZIP** para o usuário importar no GitHub; não afirmar commit ou push automático.
3. Salvar cada resposta substantiva como `.md` em `08-Continuidade/Registros/`, preservando contagens, limitações, arquivos, decisão e próximo passo; atualizar este arquivo.
4. Na nova conversa, ler este estado e os dois registros mais recentes antes de trabalhar.

## Próximo passo
Revisar por famílias as **5.148 pendências P2** ainda abertas e as ambiguidades que dependem de contexto, evitando falso positivo. Manter regressão independente e ZIP único ao final. Revisão das 32 P1 pendentes quando novos dados surgirem, depois P3.
'''
 (stage/'08-Continuidade').mkdir(exist_ok=True)
 (stage/'08-Continuidade/ESTADO-ATUAL.md').write_text(state,encoding='utf-8')
 register=f'''# Registro 2026-10-20-01 — Auditoria P2 v5

## Solicitação e decisão de trabalho
Usuário escreveu «faça» após a sugestão de auditar as 5.562 pendências P2 restantes da v4. Executou-se essa próxima etapa, com entrega consolidada em um único ZIP destinado à importação MANUAL pelo usuário ao GitHub.

## Execução
- Lida a fonte real `portal-calculadoras-auditoria-P2-v4-unico.zip`, preservando as duas fontes ZIP P2-v4 dentro do pacote v5.
- 5.562 pendências analisadas por famílias e padrões contextuais; candidatas inspecionadas por regra, mantidas ambiguidades reais.
- 414 propostas aprovadas pelas regras conservadoras, em 185 famílias; 181 sem ressalva operacional, 233 com ressalva.
- 5.148 permanecem sem contexto suficiente. 157 variantes com N semanas e D dias não foram convertidas; na família Fahrenheit, apenas uma variante com destino K explícito foi resolvida e 68 continuaram abertas.
- Geradas versões paralelas dos 30 lotes, auditoria CSV 25.050, fila, pendências, patches, QA e planilha centralizada.
- Auditoria independente de regressão: **PASSOU** após detectar e corrigir a origem incorreta dos valores "antes" dos patches (a fila analítica não é a linha real do lote).
- 294.905 IDs-base, 2.190 controles e todas as colunas protegidas preservados.

## Entregáveis, decisão e próximos passos
- DEC-043: `06-Decisoes/DEC-043 - Auditoria contextual P2 v5.md`.
- Scripts de revisão, QA, planilha e empacotamento em `07-Scripts/`.
- Relatório, CSVs, XLSX, hashes e fontes v4 em `08-Entregas/P2-v5` e `08-Entregas/P2-v4`.
- O ChatGPT **não enviou ao GitHub**. O usuário extrai e faz commit/push; não misturar com a Biblioteca do ChatGPT.
- Próxima tarefa: validar famílias restantes P2 v6 (5.148), mais tarde P1 com 32 ambiguidades, e depois P3.
'''
 (stage/'08-Continuidade/Registros').mkdir(exist_ok=True)
 (stage/'08-Continuidade/Registros/2026-10-20-01-auditoria-p2-v5.md').write_text(register,encoding='utf-8')
 readme='''# Como importar P2 v5 no vault GitHub

1. **Antes de extrair:** confirme `git status` limpo ou guarde suas alterações; use `git pull` para atualizar a branch atual.
2. Extraia o ZIP **para uma pasta temporária** e examine `08-Continuidade/ESTADO-ATUAL.md`. Se o arquivo local foi alterado, **mescle manualmente**, em vez de sobrescrevê-lo sem conferir.
3. Copie as **pastas do pacote** para a raiz `portal-calculadoras-knowledge2` preservando a estrutura. Arquivos novos ficam em `08-Entregas/P2-v5`, `06-Decisoes/DEC-043 ...` e `07-Scripts/`. As duas fontes P2-v4 são as mesmas da entrega anterior: se já existem, compare hashes e não substitua.
4. Na raiz do repositório, confira a integridade dos artefatos novos com `sha256sum -c 08-Entregas/P2-v5/SHA256SUMS-P2-V5.txt`. O manifesto inclui apenas arquivos P2-v5.
5. Opcionalmente reexecute a regressão: `python3 07-Scripts/auditar_regressao_p2_v5.py --base . --novo 08-Entregas/P2-v5`.
6. Confira `git status` e publique:

```bash
git add 06-Decisoes 07-Scripts 08-Entregas 08-Continuidade
git commit -m "Auditoria P2 v5: 414 ajustes, 5148 pendencias"
git push
```

**Importante:** este pacote não altera o GitHub sozinho. A planilha XLSX centralizada é resumo/amostra; os CSVs completos estão no ZIP de auditoria. A v5 não aprova editorialmente todas as 5.148 pendências.
'''
 (stage/'LEIA-ME-IMPORTAR-P2-V5.md').write_text(readme,encoding='utf-8')
 hashes=[]
 for p in sorted((stage/'08-Entregas/P2-v5').rglob('*')):
  if p.is_file() and p.name!='SHA256SUMS-P2-V5.txt':hashes.append(f'{digest(p)}  08-Entregas/P2-v5/{p.name}')
 (stage/'08-Entregas/P2-v5/SHA256SUMS-P2-V5.txt').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
 zpath=Path('/mnt/data/portal-calculadoras-auditoria-P2-v5-unico.zip')
 with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(stage.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(stage).as_posix())
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(list(stage.rglob('*.*')))
 print(json.dumps({'zip':str(zpath),'bytes':zpath.stat().st_size,'files':len(z.namelist()),'sha256':digest(zpath),'names':z.namelist()},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
