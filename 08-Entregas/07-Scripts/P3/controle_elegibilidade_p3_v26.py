#!/usr/bin/env python3
# coding: utf-8
"""Bloqueio de escopo P3: exige simultaneamente fila P3, fila geral P3 e lote-base.
Execucao padrão é auditoria dry-run; nunca grava lotes. Biblioteca Python padrão.
Exemplo: python controle_elegibilidade_p3.py --fila-p3 <csv> --fila-geral <csv> --lotes <zip> --candidatos <csv> --saida <pasta>
"""
import argparse, csv, io, json, zipfile, pathlib, collections, re

def read_csv(path):
    with open(path,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f,delimiter=';'))

def index_rows(rows,name):
    dic={}
    for r in rows:
        id=r.get('id_global')
        if not id: raise ValueError(f'{name}: ID vazio')
        if id in dic: raise ValueError(f'{name}: ID duplicado: {id}')
        dic[id]=r
    return dic

def normalize_lote(v):
    text=(v or '').strip()
    match=re.search(r'(?:^|[/_-])lote[-_ ]?(\d{1,3})(?:\D|$)',text,re.I)
    if not match:match=re.fullmatch(r'[Ll]?(\d{1,3})',text)
    return match.group(1).zfill(3) if match else ''

def load_indexes(fila_p3,fila_geral,lotes):
    a=index_rows(read_csv(fila_p3),'fila P3'); b=index_rows(read_csv(fila_geral),'fila geral')
    if len(a)!=23965 or len(b)!=52046: raise ValueError('Tamanho esperado da fila P3/geral divergente')
    if any(r.get('prioridade')!='P3' for r in a.values()):raise ValueError('Fila P3 contém outra prioridade')
    for id,r in a.items():
        if id not in b or b[id].get('prioridade')!='P3':raise ValueError('Fila geral não confirma P3: '+id)
        for f in ('Keyword','familia_id'):
            if r.get(f)!=b[id].get(f):raise ValueError('Conflito entre filas '+id+' em '+f)
        if normalize_lote(r.get('lote'))!=normalize_lote(b[id].get('lote')):raise ValueError('Conflito entre lotes das filas '+id)
    lots={}; cnt=collections.Counter()
    with zipfile.ZipFile(lotes) as z:
        names=z.namelist()
        if len(names)!=30:raise ValueError('ZIP de lotes não contém exatamente 30 arquivos')
        for filename in names:
            with z.open(filename) as f:
                it=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''),delimiter=';')
                for r in it:
                    typ=r.get('tipo_registro')
                    cnt[typ]+=1
                    if typ!='base':continue
                    id=r.get('id_global')
                    if not id or id in lots:raise ValueError('Duplicidade/ausência ID em lotes: '+str(id))
                    lots[id]=(r.get('Keyword'),r.get('familia_id'),normalize_lote(r.get('lote_id')))
    if cnt['base']!=294905 or cnt['controle']!=2190:raise ValueError('Contagens de base/controles divergentes '+str(cnt))
    for id,r in a.items():
        lot=lots.get(id)
        if not lot or lot!=(r.get('Keyword'),r.get('familia_id'),normalize_lote(r.get('lote'))):
            raise ValueError('ID na fila P3 diverge do lote real: '+id)
    return a,b,lots,cnt

def validate(candidates,p3,general,lots):
    allowed=[];blocked=[];seen=set()
    for r in candidates:
        id=r.get('id_global','')
        reason=''
        if not id:reason='ID_VAZIO'
        elif id in seen:reason='ID_CANDIDATO_DUPLICADO'
        elif id not in lots:reason='ID_NAO_EXISTE_BASE'
        elif id not in p3:reason='FORA_FILA_P3' if id in general else 'FORA_DA_FILA_GERAL_E_P3'
        elif id not in general or general[id].get('prioridade')!='P3':reason='PRIORIDADE_GERAL_DIVERGENTE'
        else:
            for f in ('Keyword','familia_id'):
                if r.get(f) and r[f]!=p3[id].get(f):reason='DIVERGENCIA_'+f.upper()
            if r.get('lote') and normalize_lote(r['lote'])!=normalize_lote(p3[id].get('lote')):reason='DIVERGENCIA_LOTE'
        seen.add(id)
        a={**r,'controle_p3':'BLOQUEADO' if reason else 'ELEGIVEL','motivo_bloqueio':reason}
        (blocked if reason else allowed).append(a)
    return allowed,blocked

def write_csv(path,rs):
    pathlib.Path(path).parent.mkdir(parents=True,exist_ok=True)
    cols=list(rs[0]) if rs else ['id_global','controle_p3','motivo_bloqueio']
    with open(path,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,delimiter=';',fieldnames=cols,lineterminator='\n'); w.writeheader();w.writerows(rs)

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    for field in ('fila-p3','fila-geral','lotes','candidatos','saida'):pa.add_argument('--'+field,required=True)
    args=pa.parse_args();p3,general,lots,cnt=load_indexes(args.fila_p3,args.fila_geral,args.lotes)
    candidates=read_csv(args.candidatos);allow,blocked=validate(candidates,p3,general,lots)
    dest=pathlib.Path(args.saida);dest.mkdir(parents=True,exist_ok=True)
    write_csv(dest/'p3-elegiveis.csv',allow);write_csv(dest/'p3-bloqueados.csv',blocked)
    report={'total_candidatos':len(candidates),'elegiveis':len(allow),'bloqueados':len(blocked),'motivos':dict(collections.Counter(r['motivo_bloqueio'] for r in blocked)),'modo':'SOMENTE_AUDITORIA','base':cnt['base'],'controles':cnt['controle']}
    (dest/'p3-controle-resumo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
    # explicit nonzero exit code if ineligible applicants are detected
    return 2 if blocked else 0
if __name__=='__main__':raise SystemExit(main())
