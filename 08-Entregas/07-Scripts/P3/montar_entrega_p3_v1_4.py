#!/usr/bin/env python3
"""Monta o pacote reproduzível P3 v1.4 (sem alterar arquivos do usuário).
Uso: python montar_entrega_p3_v1_4.py --trabalho /path/p3_v14_work --fonte /path/p3_v13_work/entrega_git --zip /path/entrega.zip
"""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--trabalho',type=Path,required=True);ap.add_argument('--fonte',type=Path,required=True);ap.add_argument('--zip',type=Path,required=True);a=ap.parse_args()
 work=a.trabalho;root=work/'entrega_git';out=work/'out';src=a.fonte/'08-Entregas/P3-v1.3'
 # script preserva documentação escrita manualmente no layout Git; inclui fontes v1.3 para reprodução.
 scripts=['auditar_p3_v1_4.py','classificador_p3_v14.py','regressao_independente_p3_v1_4.py','gerar_qa_p3_v1_4.py','montar_entrega_p3_v1_4.py']
 for name in scripts:
  target=root/'07-Scripts/P3'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(work/name,target)
 files=['lotes-001-a-030-p3-v1.4.zip','fila-geral-p0-p1-p2-p3-v1.4.csv','p3-v1.4-fila-23965.csv','p3-v1.4-patches.csv','p3-v1.4-decisoes-por-id.csv','p3-v1.4-amostra-67-pareceres.csv','p3-v1.4-regressao-30-lotes.csv','regressao-independente-30-lotes-p3-v1.4.csv','regressao-independente-resumo-v1.4.json','resumo-p3-v1.4.json','qa-auditoria-P3-v1.4-centralizada.xlsx']
 for name in files:
  t=root/'08-Entregas/P3-v1.4'/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(out/name,t)
 for name in ['lotes-001-a-030-p3-v1.3.zip','fila-geral-p0-p1-p2-p3-v1.3.csv','p3-v1.3-fila-23965.csv','p3-v1.3-decisoes-por-id.csv']:
  t=root/'08-Entregas/P3-v1.4/FONTES-REPRODUCAO/08-Entregas/P3-v1.3'/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,t)
 data=[]
 for file in sorted(root.rglob('*')):
  if file.is_file() and file.name!='SHA256SUMS-P3-V1.4.txt':data.append((file.relative_to(root).as_posix(),sha(file),file.stat().st_size))
 sums='\n'.join(f'{h}  {p}' for p,h,_ in data)+'\n';(root/'SHA256SUMS-P3-V1.4.txt').write_text(sums,encoding='utf-8')
 manifest={'versao':'P3 v1.4','arquivos_com_hash':len(data),'originais_preservados':True,'arquivos': [{'path':p,'sha256':h,'bytes':n} for p,h,n in data]}
 a.zip.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(a.zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for file in sorted(root.rglob('*')):
   if file.is_file():z.write(file,arcname=file.relative_to(root).as_posix())
 with zipfile.ZipFile(a.zip) as z:
  bad=z.testzip();assert bad is None,bad
  for p,h,n in data:
   b=z.read(p);assert len(b)==n and hashlib.sha256(b).hexdigest()==h,p
  assert len(z.namelist())==len(data)+1
 print(json.dumps({'arquivo':str(a.zip),'bytes':a.zip.stat().st_size,'arquivos':len(data)+1,'sha256_zip':sha(a.zip),'manifesto':manifest['arquivos_com_hash']},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
