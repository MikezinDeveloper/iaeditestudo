"""Run the original native solver through our exporter and verify its cache."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--binary', type=Path, required=True)
parser.add_argument('--output', type=Path, default=ROOT / 'demos/remotion-codex/src/studies/splish-fluid.json')
parser.add_argument('--report', type=Path, default=ROOT / 'estudo/splishsplash/resultados/simulation.json')
args = parser.parse_args()
binary = args.binary.resolve()
env = dict(os.environ, OMP_NUM_THREADS='1')

with tempfile.TemporaryDirectory(prefix='codex-sph-') as temp:
    results = []
    for run in range(2):
        file = Path(temp) / f'run-{run}.json'
        subprocess.run([str(binary), str(file)], check=True, env=env, capture_output=True, text=True)
        results.append(json.loads(file.read_text()))
    assert results[0] == results[1], 'Fresh native runs did not match'
data = results[0]
frames = data['frames']
count = data['metrics']['particles']
assert len(frames) == 90 and count == 168
assert all(len(frame) == count and all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in frame) for frame in frames)
mass0, mass1 = data['metrics']['initialMass'], data['metrics']['finalMass']
assert mass0 > 0 and abs(mass1 - mass0) < 1e-10
time_error = max(abs(t - i / data['fps']) for i, t in enumerate(data['times']))
assert time_error < 1e-8, 'Native time drifted from the frame clock'
extent = [min(p[axis] for f in frames for p in f) for axis in (0, 1)] + [max(p[axis] for f in frames for p in f) for axis in (0, 1)]
assert extent[0] >= -1.20 and extent[1] >= -0.05 and extent[2] <= 1.20 and extent[3] <= 1.65, 'Fluid escaped the sampled boundary'
width0 = max(p[0] for p in frames[0]) - min(p[0] for p in frames[0])
width30 = max(p[0] for p in frames[30]) - min(p[0] for p in frames[30])
assert width30 > width0 + 0.15, 'Dam-break did not spread'
center_y0 = sum(p[1] for p in frames[0]) / count
center_y30 = sum(p[1] for p in frames[30]) / count
assert center_y30 < center_y0 - 0.04, 'Gravity did not lower the fluid'
encoded = (json.dumps(data, separators=(',', ':')) + '\n').encode()
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_bytes(encoded)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sources = {name: sha(Path(__file__).parent / name) for name in ['CMakeLists.txt', 'bake_fluid.cpp', 'bake_verify.py']}
report = {'status': 'passed', 'sourceRevision': 'dba6b26b9387ab6bdd187d6df0a7c9d490d03500', 'runtime': 'native C++ source build, double precision, CPU, OMP_NUM_THREADS=1', 'solver': data['solver'], 'frames': 90, 'fps': data['fps'], 'particles': count, 'sameFreshRuns': True, 'initialMass': mass0, 'finalMass': mass1, 'maxNativeTimeError': time_error, 'extent': extent, 'widthAtStart': width0, 'widthAtOneSecond': width30, 'centerYAtStart': center_y0, 'centerYAtOneSecond': center_y30, 'maxObservedDensity': data['metrics']['maxDensity'], 'cacheSha256': hashlib.sha256(encoded).hexdigest(), 'generatorHashes': sources, 'binarySha256': sha(binary), 'wheelStatus': '2.19.1 failed to import in Python 3.12 and 3.11; native build used instead'}
args.report.parent.mkdir(parents=True, exist_ok=True)
args.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
