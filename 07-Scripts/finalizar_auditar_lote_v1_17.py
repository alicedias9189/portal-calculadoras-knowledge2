#!/usr/bin/env python3
"""Pipeline v1.17: TIFF↔PDF e PDF/CAD sem direção; preserva CSV original.
Uso: python finalizar_auditar_lote_v1_17.py --lote 30 --controle-anterior 29 --root .
Se v1.16 já foi executado: acrescente --skip-anterior.
"""
import argparse,csv,re,subprocess,sys,unicodedata
from pathlib import Path
from collections import Counter
pa=argparse.ArgumentParser()
pa.add_argument('--lote',type=int,required=True);pa.add_argument('--controle-anterior',type=int)
pa.add_argument('--root',default='.');pa.add_argument('--skip-anterior',action='store_true')
a=pa.parse_args();N=a.lote;P=a.controle_anterior or N-1;R=Path(a.root).resolve()
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def write(p,rows,fields):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)
def norm(t):
 t=unicodedata.normalize('NFKD',(t or '').casefold());return re.sub(r'\s+',' ',''.join(x for x in t if not unicodedata.combining(x))).strip()
if not a.skip_anterior:
 subprocess.run([sys.executable,str(R/'finalizar_auditar_lote_v1_16.py'),'--lote',str(N),'--controle-anterior',str(P),'--root',str(R)],check=True)
prefix=f'lote-{N:03d}'
cp=R/f'{prefix}-classificado-v1.1-barras-v2.csv'
fp=R/f'auditoria-pos-classificacao-{prefix}-v1.1-barras-v2-final-flags.csv'
report=R/f'relatorio-classificacao-{prefix}-v1.1-barras-v2.md'
audit=R/f'auditoria-pos-classificacao-{prefix}-v1.1-barras-v2-final.md'
rows=read(cp);ti=set();bare=set()
for r in rows:
 if r.get('tipo_registro')!='base':continue
 t=norm(r['Keyword']);src=dst=None
 if re.search(r'\b(?:tif|tiff)\b',t) and re.search(r'\bpdf\b',t):
  if re.search(r'\b(?:tif|tiff)\b\s+(?:em|para|to)\s+\bpdf\b',t):src,dst='TIFF','PDF'
  elif re.search(r'\bpdf\b\s+(?:em|para|to)\s+\b(?:tif|tiff)\b',t):src,dst='PDF','TIFF'
  if src:
   r.update(area_principal='Conversores',cluster='Arquivos e documentos',subcluster='Documentos e PDF',intencao_principal='Converter arquivo TIFF/PDF',tipo_intencao='conversão de arquivo/mídia',dominio_ou_grandeza='formatos de arquivo/imagem',unidade_origem=src,unidade_destino=dst,direcao_conversao=f'{src}→{dst}',confianca='alta',revisao_manual='não',justificativa_curta='TIFF e PDF com preposição explícita indicam conversão.');ti.add(r['id_global'])
 if re.fullmatch(r'(?:pdf\s+(?:dwg|dxf)|(?:dwg|dxf)\s+pdf)',t):
  r.update(area_principal='Conversores',cluster='Arquivos e documentos',subcluster='Documentos e PDF',intencao_principal='Revisar direção de conversão PDF/CAD',tipo_intencao='ambígua/revisão',dominio_ou_grandeza='par PDF/CAD sem direção',unidade_origem='',unidade_destino='',direcao_conversao='',confianca='média',revisao_manual='sim',justificativa_curta='Par PDF/DWG ou PDF/DXF sem verbo não define origem/destino.');bare.add(r['id_global'])
write(cp,rows,list(rows[0]))
flags=read(fp);rem=[f for f in flags if not(f.get('issue_code')=='PDF_CONTENT' and f.get('id_global') in ti|bare)]
write(fp,rem,['severity','issue_code','id_global','Keyword','label','tipo_intencao','reason'])
orig=read(R/f'{prefix}.csv');fields=list(orig[0]);base=[r for r in rows if r['tipo_registro']=='base'];ctrl=[r for r in rows if r['tipo_registro']=='controle']
pres=len(orig)==len(rows) and all(all(x[k]==y[k] for k in fields) for x,y in zip(orig,rows))
prev=read(R/f'lote-{P:03d}-classificado-v1.1-barras-v2.csv');pctrl={r['controle_id']:r for r in prev if r['tipo_registro']=='controle'}
semantic=[k for k in rows[0] if k not in fields]
ce=sum(r['controle_id'] in pctrl and all(r.get(k,'')==pctrl[r['controle_id']].get(k,'') for k in semantic) for r in ctrl)
ge=sum(x['match_exato']=='sim' for x in read(R/f'{prefix}-golden-qa-v1.1.csv'))
uniq=len({r['id_global'] for r in base});bl=sum(not(r['area_principal'] and r['cluster'] and r['subcluster']) for r in base)
missing=sum(r['tipo_intencao']=='conversão direta' and not(r['unidade_origem'] and r['unidade_destino'] and r['direcao_conversao']) for r in base)
conf=Counter(r['confianca'] for r in base);review=sum(r['revisao_manual']=='sim' for r in base);bars=sum(bool(r.get('keyword_interpretada')) for r in base)
status='APROVADO' if pres and len(ctrl)==ce==73 and ge==107 and uniq==len(base) and bl==missing==len(rem)==0 else 'REVISAR'
report.write_text(f'# Lote {N:03d}: classificação v1.1 + barras v2\n\n- Status: **{status}**\n- Base: **{len(base)}**; controles **{ce}/73**; Golden **{ge}/107**\n- Reconstruções de barras: **{bars}**; flags: **{len(rem)}**; conversões incompletas: **{missing}**\n- Confiança: alta **{conf["alta"]}**, média **{conf["média"]}**, baixa **{conf["baixa"]}**; revisão manual **{review}**\n- v1.17: TIFF↔PDF direcionais **{len(ti)}**; pares nus CAD/PDF ambíguos **{len(bare)}**.\n',encoding='utf-8')
audit.write_text(f'# Auditoria lote {N:03d}\n\n**{status}**\n\n- Keywords base **{len(base)}**, IDs únicos **{uniq}**, controles **{ce}/73**, Golden **{ge}/107**\n- Originais preservados: **{pres}**; campos taxonômicos vazios: **{bl}**; conversões diretas sem metadados: **{missing}**; flags finais: **{len(rem)}**\n- TIFF/PDF explícito **{len(ti)}**; pares PDF/CAD ambíguos **{len(bare)}**; reconstruções barras **{bars}**.\n',encoding='utf-8')
print(dict(status=status,base=len(base),gold=ge,controls=ce,flags=len(rem),tiff_pdf=len(ti),cad_ambiguos=len(bare),confianca=dict(conf),manual=review,barras=bars))
if status!='APROVADO':sys.exit(2)
