#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cria uma planilha Excel de QA centralizada a partir da auditoria P2 v6.
Uso: python3 07-Scripts/gerar_qa_p2_v6.py --entrada saida-p2-v6 --saida 08-Entregas/P2-v6/qa-revisao-p2-v6-centralizada.xlsx
CSV completos continuam no ZIP de auditoria, não truncar registros nem colunas.
Requer `artifact_tool` (apenas para construir XLSX).
"""
import argparse,csv,io,zipfile,json,collections,random
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile

def read(z,name):
    return list(csv.DictReader(io.TextIOWrapper(z.open(name),encoding='utf-8-sig',newline=''),delimiter=';'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--entrada',type=Path,required=True);p.add_argument('--saida',type=Path,required=True);a=p.parse_args()
    base=a.entrada;sm=json.loads((base/'resumo-p2-v6.json').read_text())
    qa=json.loads((base/'regressao-independente-p2-v6.json').read_text())
    with zipfile.ZipFile(base/'auditoria-p2-v6-csv-integral.zip') as z:
        patch=read(z,'p2-v6-patches.csv');pending=read(z,'p2-v6-pendencias-restantes.csv');family=read(z,'p2-v6-familias-analisadas.csv')
    wb=Workbook.create()
    def sheet(name,headers,rows,widths=None):
        sh=wb.worksheets.add(name)
        data=[headers]+rows
        # split writes to avoid large intermediate operations
        for offset in range(0,len(data),200):
            chunk=data[offset:offset+200]
            sh.get_range_by_indexes(offset,0,len(chunk),len(headers)).values=chunk
        sh.get_range_by_indexes(0,0,len(data),len(headers)).format.horizontal_alignment='center'
        sh.get_range_by_indexes(0,0,len(data),len(headers)).format.vertical_alignment='center'
        sh.get_range_by_indexes(0,0,len(data),len(headers)).format.row_height=22
        hd=sh.get_range_by_indexes(0,0,1,len(headers));hd.format={'fill':'#153148','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':30}
        for j,w in enumerate(widths or [24]*len(headers)):
            sh.get_range_by_indexes(0,j,len(data),1).format.column_width=w
        sh.freeze_panes.freeze_rows(1)
        return sh
    summary=[
        ['Versão','P2 v6'],['Data','2026-10-20'],['Universo P2',sm['universo_p2']],
        ['Pendências recebidas da P2 v5',sm['pendencias_entrada_v5']],
        ['Reclassificações',sm['reclassificadas']],['Sem ressalvas',sm['sem_ressalva']],
        ['Com ressalvas',sm['com_ressalva']],['Pendências restantes',sm['pendencias_restantes']],
        ['Famílias afetadas',sm['familias_com_patches']],['Regressão independente',qa['status']],
        ['Lotes conferidos',qa['lotes']],['Registros-base',qa['id_base_unicos']],['Controles preservados',qa['controles_intactos']],
        ['Limitação','Decisões por regras textuais; não equivalem a homologação editorial individual'],
        ['Dados completos','Dentro do ZIP auditoria-p2-v6-csv-integral.zip']]
    sheet('Resumo',['Indicador','Resultado'],summary,[42,76])
    rules=sorted(sm['regras'].items(),key=lambda x:-x[1])
    sheet('Regras',['Regra','Registros','Amostras'],[[k,v,' | '.join(sm['exemplos'].get(k,[])[:3])] for k,v in rules],[43,14,100])
    sheet('Patches',['ID','Lote','Família','Keyword','Regra','Status','Justificativa'],
          [[x['id_global'],x['lote'],x['familia_id'],x['Keyword'],x['regra'],x['status'],x['justificativa']] for x in patch],
          [15,12,23,57,39,20,95])
    sheet('Regressao 30 lotes',['Lote','Base','Controles','Modificações','Resultado'],
          [[x['lote'],x['base'],x['controles'],x['alteracoes'],x['status']] for x in qa['alteracoes_por_lote']],[35,16,16,22,19])
    sheet('Familias mais pendentes',['Família','Abertos antes','Reclassificados','Pendentes','Exemplos pendentes'],
          [[x['familia_id'],int(x['pendentes_v5']),int(x['classificados_v6']),int(x['ainda_abertos']),x['amostras_abertas']] for x in family[:160]],[24,18,19,18,100])
    # Make deterministic stratified sample of remaining, not full corpus; full data in CSV.
    byfam=collections.defaultdict(list)
    for x in pending:byfam[x['familia_id']].append(x)
    random.seed(20261020)
    samp=[]
    for fam in sorted(byfam,key=lambda f:-len(byfam[f])):
        val=byfam[fam]
        take=12 if len(val)>70 else 5 if len(val)>15 else 2 if len(val)>3 else 1
        samp.extend(random.sample(val,min(take,len(val))))
        if len(samp)>=1050:break
    samp=samp[:1050]
    sheet('Amostra pendencias',['ID','Família','Keyword','Área P2 v6','Intenção','Buscas médias'],
          [[x['id_global'],x['familia_id'],x['Keyword'],x['area_final_p2_v6'],x['tipo_intencao_final_p2_v6'],x['Avg. monthly searches']] for x in samp],
          [15,23,68,28,30,20])
    a.saida.parent.mkdir(parents=True,exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(a.saida))
    print('XLSX',a.saida,a.saida.stat().st_size,'sheets',6,'patches',len(patch),'sample',len(samp))
if __name__=='__main__':main()
