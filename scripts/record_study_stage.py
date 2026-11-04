"""Persist bounded sequential study evidence; does not certify missing native tools."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,re
R=Path(__file__).resolve().parents[1]
def save(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def record(spec):
 key=spec['key'];out=R/'estudo'/key;out.mkdir(parents=True,exist_ok=True);results=out/'resultados';results.mkdir(exist_ok=True)
 source=Path(spec['checkout']);rev=subprocess.check_output(['git','-c','safe.directory='+source.as_posix(),'-C',str(source),'rev-parse','HEAD'],text=True).strip()
 evidence=[]
 for name in spec['files']:
  p=source/name
  if not p.is_file():raise RuntimeError('Do not claim absent source: '+name)
  evidence.append({'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'url':spec['url']+'/blob/'+rev+'/'+name,'coverage':spec.get('coverage','Selected mechanisms/sections; not whole-file or whole-repository audit')})
 save(out/'evidencias.json',{'source':spec['url'],'revision':rev,'date':'2026-11-04','files':evidence})
 tests=[]
 for c in spec.get('commands',[]):
  env=None
  p=subprocess.run(c['args'],cwd=R/c.get('cwd','.'),capture_output=True,text=True,encoding='utf8',errors='replace')
  result={'command':c['args'],'cwd':c.get('cwd','.'),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'scope':c['scope']};save(results/(c['name']+'.json'),result);tests.append({'name':c['name'],'exit_code':p.returncode,'expected_exit':c.get('expected_exit',0)})
  if p.returncode!=c.get('expected_exit',0):raise RuntimeError('Unexpected experiment result: '+c['name'])
 save(results/'status.json',{'item':spec['item'],'key':key,'date':'2026-11-04','state':spec['state'],'revision':rev,'implemented':spec['implemented'],'pending':spec['pending'],'tests':tests,'scope':'Bounded mechanism study; native execution and perceptual approval are separate.'})
 (out/'README.md').write_text(spec['body'].replace('{REVISION}',rev),encoding='utf8')
 fila=R/'estudo/FILA.md';text=fila.read_text(encoding='utf8')
 pattern=r'(?m)^\|'+str(spec['item'])+r'\|[^\n]+$'
 replacement=f"|{spec['item']}|[{spec['name']}]({spec['url']})|[Estudo delimitado e evidências; limites abaixo]({key}/README.md)|"
 if not re.search(pattern,text):raise RuntimeError('Missing queue entry')
 text=re.sub(pattern,lambda m:replacement,text)
 text+=f"\nCheckpoint{spec['item']}: `{spec['state']}`; revisão`{rev}`. [Resultados]({key}/resultados/status.json). A continuidade do restante foi autorizada pelo usuário sem exigir conclusão dos testes nativos pendentes de cada estudo.\n"
 fila.write_text(text,encoding='utf8')
 fontes=R/'estudo/FONTES.md';fontes.write_text(fontes.read_text(encoding='utf8')+f"\n## {spec['source_id']} — {spec['name']}, item{spec['item']}\n\nFonte{spec['url']}, revisão`{rev}`. [Estudo]({key}/README.md) e [inventário]({key}/evidencias.json). Estado`{spec['state']}`; escopo e pendências no status.\n",encoding='utf8')
 integration=R/'estudo/INTEGRACOES.md';integration.write_text(integration.read_text(encoding='utf8')+f"\n### Item{spec['item']} — {spec['name']}\n\n[Estudo e ponte]({key}/README.md). Implementado: {'; '.join(spec['implemented'])}. Pendente: {'; '.join(spec['pending'])}.\n",encoding='utf8')
 return {'item':spec['item'],'revision':rev,'state':spec['state'],'tests':tests}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('spec');a=p.parse_args();print(json.dumps(record(json.loads(Path(a.spec).read_text(encoding='utf8'))),ensure_ascii=False,indent=2))
