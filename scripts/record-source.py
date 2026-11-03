"""Record immutable source references for files actually consulted during research."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.parse import urlsplit
import argparse
import hashlib
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('study')
parser.add_argument('checkout', type=Path)
parser.add_argument('files', nargs='+')
args = parser.parse_args()
source = args.checkout.resolve()
def git(*parts):
    return subprocess.check_output(['git', '-C', str(source), *parts], text=True).strip()
revision = git('rev-parse', '--verify', 'HEAD^{commit}')
remote = urlsplit(git('remote', 'get-url', 'origin'))
if remote.hostname != 'github.com':
    raise SystemExit('Only inspected GitHub sources are supported by this recorder')
url = f'https://github.com/{remote.path.strip("/").removesuffix(".git")}'
records = []
for relative in args.files:
    path = (source / relative).resolve()
    path.relative_to(source)
    data = path.read_bytes()
    records.append({'path': relative, 'url': f'{url}/blob/{revision}/{relative}', 'sha256': hashlib.sha256(data).hexdigest(), 'lines': len(data.splitlines()), 'scope': 'Consulta integral ou parcial dos trechos relevantes; não é auditoria de todas as linhas.'})
output = Path(__file__).resolve().parent.parent / 'estudo' / args.study / 'evidencias.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({'source': url, 'revision': revision, 'consultedAt': datetime.now(ZoneInfo('America/Sao_Paulo')).date().isoformat(), 'files': records}, ensure_ascii=False, indent=2) + '\n')
print(f'{output}: {len(records)} referências')
