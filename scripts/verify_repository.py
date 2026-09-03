"""Verify committed reference evidence and documentation without third-party tools."""
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dcf.cli import run
from dcf.config import load, schema

def equivalent(a,b):
    if isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool):
        return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-6)
    if isinstance(a,dict) and isinstance(b,dict):
        return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):
        return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
    return a==b

def csv_equivalent(a,b):
    with a.open(newline='',encoding='utf-8') as sa,b.open(newline='',encoding='utf-8') as sb:
        ra,rb=list(csv.reader(sa)),list(csv.reader(sb))
    if len(ra)!=len(rb):return False
    for xa,xb in zip(ra,rb):
        if len(xa)!=len(xb):return False
        for va,vb in zip(xa,xb):
            if va==vb:continue
            try:
                if not equivalent(float(va),float(vb)):return False
            except ValueError:return False
    return True

def verify():
    c=load(ROOT/'configs/tropical-5mw.json')
    ref=ROOT/'artifacts/reference'
    manifest=json.loads((ref/'manifest.json').read_text())
    for name,digest in manifest.items():
        assert hashlib.sha256((ref/name).read_bytes()).hexdigest()==digest, f'Artifact modified: {name}'
    with tempfile.TemporaryDirectory() as temporary:
        run(ROOT/'configs/tropical-5mw.json',Path(temporary),ROOT/'data/site-candidates.csv')
        fresh=json.loads((Path(temporary)/'manifest.json').read_text())
        # libm floating-point differences across OSes may change low-order bytes.
        # Preserve strict integrity of committed files, but compare rerun numbers
        # at an explicit tolerance rather than requiring identical platform bytes.
        for name in manifest:
            original,new=ref/name,Path(temporary)/name
            if name.endswith('.json'):
                assert equivalent(json.loads(original.read_text()),json.loads(new.read_text())), f'Numeric JSON drift: {name}'
            elif name.endswith('.csv'):
                assert csv_equivalent(original,new), f'Numeric CSV drift: {name}'
            else:
                assert original.read_bytes()==new.read_bytes(), f'Geometry/text drift: {name}'
    assert json.loads((ROOT/'schemas/project.schema.json').read_text())==schema(), 'Schema drift'
    with (ROOT/'03_financial-model/cost-allowances.csv').open() as stream:
        total=sum(float(r['usd']) for r in csv.DictReader(stream))
    assert total==c['base_capex_usd'], 'Cost allowance does not reconcile with scenario'
    telemetry=json.loads((ref/'telemetry-sample.json').read_text())
    with (ref/'rack-assets.csv').open() as stream:
        ids={r['asset_id'] for r in csv.DictReader(stream)}
    assert {r['asset_id'] for r in telemetry}==ids, 'Telemetry identity mismatch'
    results=json.loads((ref/'commissioning-results.json').read_text())
    assert len(results)==6 and all(x['passed'] for x in results), 'Offline commissioning case failed'
    broken=[]
    for path in ROOT.rglob('*.md'):
        if any(p in {'.git','build','node_modules'} for p in path.relative_to(ROOT).parts):continue
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if re.match(r'^[a-zA-Z]+:',target) or target.startswith('#'):continue
            target=unquote(target.split('#')[0].strip('<>'))
            if target and not (path.parent/target).exists():broken.append((str(path.relative_to(ROOT)),target))
    assert not broken, f'Broken local Markdown links: {broken}'
    for artifact in ('facility-model.xlsx','facility-portfolio.pdf'):
        assert (ROOT/'deliverables'/artifact).stat().st_size>1000, f'Missing deliverable: {artifact}'
    print('PASS: reproducible calculations, committed hashes, schema, costs, asset IDs, six offline cases, local links and deliverables')

if __name__=='__main__':verify()
