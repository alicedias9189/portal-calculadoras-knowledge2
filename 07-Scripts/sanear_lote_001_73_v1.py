#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduz o saneamento contextual das 73 pendências do lote 001.
Uso: python3 sanear_lote_001_73_v1.py --root .
Não sobrescreve o original.
"""
import argparse,csv
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',default='.');root=Path(p.parse_args().root)
def rd(f):
 with open(f,encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h,delimiter=';'))
def wr(f,rows,cols):
 with open(f,'w',encoding='utf-8-sig',newline='') as h:
  w=csv.DictWriter(h,fieldnames=cols,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)
pairs={'28124':('BIN','HEX'),'28125':('BIN','HEX'),'28128':('BIN','HEX'),'165700':('HEX','BIN'),'165702':('HEX','BIN'),'279803':('timestamp','data/hora legível'),'114568':('PLN','COP')}
amb=set('165699 97161 154668 187800 283907 283917 28778 137825 276737 276741'.split())
tab=set('180556 271391 191859 192600 192605 192607 271875 271879 271880 271881 271882 271883 271885 271887 271888 271892 271893 271895 271896 271897 271898 272261 272263 272264 272595 272596 272597 272598 272601 272602'.split())
estimate=set('283275 283280 283286 283292 283295'.split())
nav=set('155101 268409 106333 108708 109305 106901 106910 38234 34785 36427 279791 18149 18150 18166 106045 33270'.split())
info=set('294556 183320 192379'.split())
quote={'139940','228986'}
pending={x['id_global'] for x in rd(root/'pendencias-metadados-diretos-lote-001.csv')}
mapped=set(pairs)|amb|tab|estimate|nav|info|quote
assert pending==mapped and len(pending)==73,(pending-mapped,mapped-pending)
src=rd(root/'lote-001-classificado-v1.1-barras-v2.csv');out=[dict(x) for x in src]
ads='Keyword Avg. monthly searches Competition Competition (indexed value)'.split('|')
before={x['id_global']:x for x in src if x['tipo_registro']=='base'}
edits=[]
for x in out:
 if x['tipo_registro']!='base' or x['id_global'] not in pending:continue
 i=x['id_global']; old=x['tipo_intencao'];assert old=='conversão direta'
 if i in pairs:
  orig,dest=pairs[i];typ,conf,review='conversão direta','alta','não'
  x.update(unidade_origem=orig,unidade_destino=dest,direcao_conversao=f'{orig}→{dest}')
  why='Transformação com direção explicitamente identificável.'
 elif i in amb:typ,conf,review='ambígua/revisão','baixa','sim';why='Não há direção/contexto inequívoco.'
 elif i in tab:typ,conf,review='tabela/referência','alta','não';why='Tabela ou lista informativa, não conversão direta.'
 elif i in estimate:typ,conf,review='estimativa de quantidade','alta','não';why='Traço de concreto em recipientes; dimensionamento de materiais.'
 elif i in nav:typ,conf,review='navegacional/transacional','média','não';why='Busca por aplicativo ou ferramenta, sem par direcional.'
 elif i in info:typ,conf,review='informacional','alta','não';why='Consulta conceitual ou genérica.'
 else:typ,conf,review='cotação atual','média','sim';why='Consulta de taxa corrente, não transformação numérica.'
 x.update(tipo_intencao=typ,confianca=conf,revisao_manual=review,justificativa_curta=why)
 prefix={'conversão direta':'Converter','ambígua/revisão':'Rever intenção/direção','tabela/referência':'Consultar referência','estimativa de quantidade':'Estimar quantidade','navegacional/transacional':'Acessar ferramenta/serviço','informacional':'Consultar informação','cotação atual':'Consultar cotação'}[typ]
 x['intencao_principal']=f'{prefix}: {x["subcluster"]}'
 edits.append({'id_global':i,'Keyword':x['Keyword'],'tipo_anterior':old,'tipo_corrigido':typ,'origem':x['unidade_origem'],'destino':x['unidade_destino'],'direcao':x['direcao_conversao'],'revisao_manual':review,'justificativa':why})
assert len(out)==len(src)==9904 and len(edits)==73
for b,v in zip(src,out):
 for k in ('id_global','Keyword','Avg. monthly searches','Competition','ocorrencias_origem','areas_origem'):assert b[k]==v[k]
 if b['tipo_registro']=='controle' or b['id_global'] not in pending:assert b==v
assert all(x['unidade_origem'] and x['unidade_destino'] and x['direcao_conversao'] for x in out if x['tipo_registro']=='base' and x['tipo_intencao']=='conversão direta')
dest=root/'saneamento-revisao-30-lotes';dest.mkdir(exist_ok=True)
wr(dest/'lote-001-saneado-v1.1-barras-v2.csv',out,list(out[0]))
wr(dest/'correcoes-73-lote-001-reproduzivel.csv',edits,list(edits[0]))
print('Concluído:',len(edits),'alterações; nenhuma conversão direta sem metadados.')
