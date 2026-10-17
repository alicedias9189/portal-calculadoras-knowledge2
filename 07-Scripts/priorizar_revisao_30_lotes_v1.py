#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cria fila de prioridade e agrupamento por família para a revisão dos 30 lotes.
Uso: python3 priorizar_revisao_30_lotes_v1.py --root .
Requer L001 saneado em saneamento-revisao-30-lotes/.
"""
import argparse,csv,re,unicodedata,zipfile
from pathlib import Path
from collections import Counter,defaultdict
p=argparse.ArgumentParser();p.add_argument('--root',default='.');root=Path(p.parse_args().root)
out=root/'saneamento-revisao-30-lotes';out.mkdir(exist_ok=True)
def rd(f):
 with open(f,encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h,delimiter=';'))
def wr(f,rows):
 with open(f,'w',encoding='utf-8-sig',newline='') as h:
  w=csv.DictWriter(h,delimiter=';',fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def norm(s):
 return ''.join(x for x in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(x))
def vol(s):
 try:return int(s.replace('.',''))
 except (ValueError,AttributeError):return -1
review=[];bases=0
for lot in range(1,31):
 if lot==1:r=rd(out/'lote-001-saneado-v1.1-barras-v2.csv')
 elif lot==3:
  with zipfile.ZipFile(root/'lote-003-v1.1-barras-v2-aprovado.zip') as z:
   names=[x for x in z.namelist() if x.endswith('lote-003-classificado-v1.1-barras-v2.csv')]
   assert len(names)==1
   r=list(csv.DictReader(z.read(names[0]).decode('utf-8-sig').splitlines(),delimiter=';'))
 else:r=rd(root/f'lote-{lot:03d}-classificado-v1.1-barras-v2.csv')
 for row in r:
  if row['tipo_registro']!='base':continue
  bases+=1
  if row['revisao_manual']=='sim':review.append((lot,row))
assert bases==294905,bases
size=Counter(row['familia_id'] for lot,row in review)
queue=[]
for lot,r in review:
 k=norm(r['Keyword']);area=r['area_principal'];typ=r['tipo_intencao'];v=vol(r['Avg. monthly searches'])
 risks=[]
 if typ=='ambígua/revisão':risks.append('intenção/direção ambígua')
 if area=='Conversores' and r['cluster']=='Moedas e câmbio' and ('peso' in k or 'libra' in k):risks.append('ambiguidade monetária')
 if area=='Conversores' and re.search(r'\b(?:mbps|mb/s|gbps|gb/s)\b',k):risks.append('bits versus bytes')
 if area=='Conversores' and re.search(r'\b(?:pdf|docx?|dwg|tiff|mobi)\b',k):risks.append('documento/conversão')
 if area=='Trabalho' and re.search(r'\b(?:vale a pena|vale comprar|vale investir)\b',k):risks.append('possível falso positivo: vale')
 if area in ('Datas','Trabalho') and re.search(r'\b(?:licenca|ferias|folga|rescisao|clt|irrf|inss)\b',k):risks.append('direitos trabalhistas')
 if area=='Matemática' and re.search(r'\b(?:[4-9]\s*ano|ensino fundamental|exercicios?|atividade|prova)\b',k):risks.append('conteúdo escolar')
 if r['confianca']=='baixa':risks.append('confiança baixa')
 pr='P0' if v>=50000 else 'P1' if v>=5000 or 'possível falso positivo: vale' in risks else 'P2' if typ=='ambígua/revisão' or v>=500 or len(risks)>=2 else 'P3'
 family=r['familia_id']
 score={'P0':4,'P1':3,'P2':2,'P3':1}[pr]*10**9+max(v,0)*1000+min(size[family],999)
 queue.append({'prioridade':pr,'score_ordenacao':score,'lote':f'{lot:03d}','id_global':r['id_global'],
 'familia_id':family,'qtd_itens_familia_marcados':size[family],'Keyword':r['Keyword'],
 'area':area,'cluster':r['cluster'],'subcluster':r['subcluster'],'tipo_intencao_atual':typ,
 'confianca_atual':r['confianca'],'Avg. monthly searches':r['Avg. monthly searches'],
 'riscos_detectados':' | '.join(risks),'status_revisao':'PENDENTE',
 'decisao_sugerida':'Revisar intenção e relevância; confirmar exceções da família',
 'decisao_final':'','observacao_revisor':''})
queue.sort(key=lambda r:(-r['score_ordenacao'],int(r['id_global'])))
wr(out/'fila-revisao-priorizada-30-lotes.csv',queue)
wr(out/'primeiras-500-revisoes.csv',queue[:500])
group=defaultdict(list)
for r in queue:group[r['familia_id']].append(r)
families=[]
for fam,items in group.items():
 a=items[0]
 families.append({'familia_id':fam,'qtd_keywords':len(items),'prioridade_max':min(x['prioridade'] for x in items),
 'area_predominante':Counter(x['area'] for x in items).most_common(1)[0][0],
 'cluster_predominante':Counter(x['cluster'] for x in items).most_common(1)[0][0],
 'exemplo_keyword':a['Keyword'],'exemplo_id':a['id_global'],
 'lotes':','.join(sorted(set(x['lote'] for x in items))),'decisao_familia':'',
 'nota':'Verificar amostras e exceções antes de corrigir em massa'})
families.sort(key=lambda x:({'P0':0,'P1':1,'P2':2,'P3':3}[x['prioridade_max']],-x['qtd_keywords']))
wr(out/'familias-agrupadas-revisao.csv',families)
print('Fila',len(queue),'Famílias',len(families),'Prioridades',dict(Counter(x['prioridade'] for x in queue)))
