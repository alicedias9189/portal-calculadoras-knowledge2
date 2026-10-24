#!/usr/bin/env python3
# coding: utf-8
"""Gera planilha centralizada a partir dos CSVs P3 v2.4, usando artifact_tool.
Execução: python gerar_qa_p3_v24.py --dados <08-Entregas/P3-v2.4> --saida <xlsx>
"""
import argparse,csv,json,pathlib,collections
from artifact_tool import Workbook,SpreadsheetFile

def rows(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def add_sheet(wb,title,records,fields=None):
    s=wb.worksheets.add(title)
    if fields is None:fields=list(records[0])
    allrows=[fields]+[[r.get(f,'') for f in fields] for r in records]
    n=len(allrows);m=len(fields)
    s.get_range_by_indexes(0,0,n,m).values=allrows
    rg=s.get_range_by_indexes(0,0,n,m)
    rg.format.horizontal_alignment='center';rg.format.vertical_alignment='center'
    rg.format.row_height=28
    header=s.get_range_by_indexes(0,0,1,m)
    header.format={'fill':'#1C3550','font':{'bold':True,'color':'#FFFFFF'},'horizontal_alignment':'center','vertical_alignment':'center','row_height':34}
    s.get_range_by_indexes(0,0,n,m).format.wrap_text=True
    s.get_range_by_indexes(0,0,n,m).format.column_width=22
    for i,f in enumerate(fields):
        if f in ['Keyword','observacao_individual','justificativa','destino_recomendado','parecer_contextual','motivo_nao_aplicar','proxima_acao']:
            s.get_range_by_indexes(0,i,n,1).format.column_width=36
    s.freeze_panes.freeze_rows(1)
    return s

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dados',required=True);ap.add_argument('--saida',required=True);args=ap.parse_args()
    folder=pathlib.Path(args.dados)
    tri=rows(folder/'p3-v2.4-quarentena-98-triada.csv')
    ok=rows(folder/'p3-v2.4-elegibilidade-108.csv')
    stats=json.loads((folder/'p3-v2.4-testes-seletor.json').read_text(encoding='utf-8'))
    byreg=collections.Counter(r['regra'] for r in tri)
    byparecer=collections.Counter(r['parecer_contextual'] for r in tri)
    wb=Workbook.create()
    add_sheet(wb,'Resumo',[{'Indicador':k,'Quantidade':v} for k,v in [
        ('Total de propostas v2.2',108),('ID na P3 (elegíveis)',10),('ID fora da P3 e geral',98),
        ('Triados individualmente',98),('Modificações nos lotes',0),('Registros-base preservados',294905),
        ('Controles preservados',2190),('Lotes preservados',30)]])
    add_sheet(wb,'Por regra',[{'Regra':k,'Registros':v} for k,v in sorted(byreg.items())])
    add_sheet(wb,'Por parecer',[{'Parecer':k,'Registros':v} for k,v in sorted(byparecer.items())])
    detail=['id_global','lote','familia_id','Keyword','regra','prioridade_verificada','destino_recomendado','parecer_contextual','tipo_intencao_proposto_revisado','origem_area','origem_tipo','proposta_area','proposta_tipo','observacao_individual','aplicar_agora','motivo_nao_aplicar']
    add_sheet(wb,'Quarentena 98',tri,detail)
    elig=['id_global','Keyword','regra','controle_p3','motivo_bloqueio']
    add_sheet(wb,'Elegibilidade 108',ok,elig)
    add_sheet(wb,'Testes',[{'Verificação':k,'Resultado':str(v)} for k,v in stats.items()])
    assert len(tri)==98 and len(ok)==108
    result=wb.inspect({'kind':'table','range':'Resumo!A1:B9','include':'values','table_max_rows':10,'table_max_cols':2})
    print(result.ndjson[:900])
    SpreadsheetFile.export_xlsx(wb).save(args.saida)
    print('Excel',args.saida)
if __name__=='__main__':main()
