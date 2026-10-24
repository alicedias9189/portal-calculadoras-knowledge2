#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera Excel centralizado de QA do piloto P3 v1 com artifact_tool.
Uso: python3 gerar_planilha_p3_v1.py --qa /caminho/saida --arquivo /caminho/qa-p3-v1.xlsx
"""
import argparse, csv, json, collections, random
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

def csvrows(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def main(qa,arquivo):
    stats=json.loads((qa/'p3-v1-resumo.json').read_text(encoding='utf-8'))
    regression=json.loads((qa/'p3-v1-regressao-independente.json').read_text(encoding='utf-8'))
    decisions=csvrows(qa/'p3-v1-piloto-2090-decisoes.csv');patches=csvrows(qa/'p3-v1-patches.csv')
    fam=collections.defaultdict(list)
    for r in decisions:fam[r['familia_id']].append(r)
    families=[]
    for fid,rr in sorted(fam.items(),key=lambda x:(-len(x[1]),x[0])):
        families.append([fid,len(rr),rr[0]['area_atual'],sum(q['houve_patch']=='sim' for q in rr),sum(q['status']=='SEM_EVIDENCIA_PILOTO' for q in rr),rr[0]['Keyword'][:115]])
    rule_count=collections.Counter(p['regra'] for p in patches)
    random.seed(207)
    per_rule=collections.defaultdict(list)
    for p in patches:per_rule[p['regra']].append(p)
    samples=[]
    for rule,items in sorted(per_rule.items()):
        for p in random.sample(items,min(6,len(items))):samples.append(p)
    for p in random.sample([r for r in decisions if r['status']=='SEM_EVIDENCIA_PILOTO'],min(80,stats['sem_evidencia'])):
        samples.append({'id_global':p['id_global'],'lote':p['lote'],'familia_id':p['familia_id'],'Keyword':p['Keyword'],'regra':'sem_evidencia','status':'SEM_EVIDENCIA_PILOTO','justificativa':p['justificativa'],'antes_json':'','depois_json':''})
    wb=Workbook.create()
    def add(name,headers,rows,widths=None):
        sh=wb.worksheets.add(name)
        matrix=[headers]+[[str(v)[:30000] if isinstance(v,str) else v for v in row] for row in rows]
        sh.get_range_by_indexes(0,0,len(matrix),len(headers)).values=matrix
        allr=sh.get_range_by_indexes(0,0,len(matrix),len(headers))
        allr.format.horizontal_alignment='center';allr.format.vertical_alignment='center';allr.format.row_height=21
        sh.get_range_by_indexes(0,0,1,len(headers)).format={'fill':'#17324D','font':{'color':'#FFFFFF','bold':True},'horizontal_alignment':'center','vertical_alignment':'center','row_height':32,'wrap_text':True}
        sh.freeze_panes.freeze_rows(1)
        for ci,h in enumerate(headers):
            w=widths[ci] if widths and ci<len(widths) else (35 if h in ('Keyword','justificativa','antes_json','depois_json','Exemplo') else 19)
            sh.get_range_by_indexes(0,ci,len(matrix),1).format.column_width=w
        return sh
    summary=[['Universo P3',stats['P3_universo']],['Famílias P3 no universo',stats['familias_P3']],['Famílias no piloto',stats['familias_piloto']],['Entradas piloto',stats['keywords_piloto']],['Propostas por regras',stats['regras_detectadas']],['Patches aplicados',stats['reclassificadas_com_patch']],['Com ressalvas',stats['status'].get('PROPOSTA_COM_RESSALVA',0)],['Sem ressalvas',stats['status'].get('PROPOSTA_SEM_RESSALVA',0)],['Sem evidência no piloto',stats['sem_evidencia']],['P3 fora do piloto',stats['P3_nao_selecionadas']],['Famílias com patches',stats['familias_com_patches']],['Mudanças de área',regression['alteracao_area']],['Mudanças de intenção',regression['alteracao_tipo_intencao']],['Lotes aprovados',regression['lotes']],['Registros-base preservados',regression['registros_base']],['Controles preservados',regression['controles']],['Limite metodológico','Rótulos automáticos são propostas de QA; não homologação editorial'],['Prioridade seguinte','Auditoria amostral de precisão antes da expansão P3']]
    add('Resumo',['Indicador','Resultado'],summary,[42,78])
    selectedcols=['id_global','lote','familia_id','Keyword','area_atual','cluster_atual','tipo_intencao_atual','Avg. monthly searches','regra','status','houve_patch','justificativa']
    add('Todas 2090 decisões',selectedcols,[[r.get(c,'') for c in selectedcols] for r in decisions],[13,10,22,55,19,24,26,19,24,28,15,55])
    pcols=['id_global','lote','familia_id','Keyword','regra','status','campos_alterados','antes_json','depois_json','justificativa']
    add('1129 patches',pcols,[[p.get(c,'') for c in pcols] for p in patches],[13,10,22,52,25,26,32,57,57,62])
    add('66 familias',['ID familia','No piloto','Area de entrada','Com patch','Sem evidencia','Exemplo'],families,[26,16,24,15,20,70])
    add('Regras',['Regra','Quantidade'],sorted([[k,v] for k,v in rule_count.items()],key=lambda x:-x[1]),[40,22])
    sampcols=['id_global','lote','familia_id','Keyword','regra','status','antes_json','depois_json','justificativa']
    add('Amostra para QA',sampcols,[[x.get(c,'') for c in sampcols] for x in samples],[14,10,26,56,30,30,60,60,58])
    add('Regressao 30 lotes',['Lote','Linhas','Controles','Patches','Resultado'],[[r['lote'],r['linhas'],r['controle'],r['patches'],r['resultado']] for r in regression['por_lote']],[20,20,20,20,20])
    arquivo.parent.mkdir(parents=True,exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(arquivo))
    print(json.dumps({'output':str(arquivo),'sheets':7,'decisions':len(decisions),'patches':len(patches),'samples':len(samples)},ensure_ascii=False))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--qa',type=Path,required=True);p.add_argument('--arquivo',type=Path,required=True);a=p.parse_args();main(a.qa,a.arquivo)
