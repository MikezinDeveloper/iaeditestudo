"""Bake a small original mass-spring scene with real Taichi CPU kernels."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import taichi as ti

ROWS, COLS, FRAMES, FPS, SUBSTEPS = 10, 12, 90, 30, 8
DT, SPACING, GRAVITY, STIFFNESS, DAMPING = 1 / 240, 0.06, 0.8, 240.0, 2.5
ROOT = Path(__file__).resolve().parents[2]

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=ROOT / 'demos/remotion-codex/src/studies/taichi-cloth.json')
parser.add_argument('--report', type=Path, default=ROOT / 'estudo/taichi/resultados/simulation.json')
args = parser.parse_args()

ti.init(arch=ti.cpu, default_fp=ti.f32, cpu_max_num_threads=2, random_seed=42, fast_math=False)
position = ti.Vector.field(2, dtype=ti.f32, shape=(ROWS, COLS))
velocity = ti.Vector.field(2, dtype=ti.f32, shape=(ROWS, COLS))
next_velocity = ti.Vector.field(2, dtype=ti.f32, shape=(ROWS, COLS))
neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


@ti.kernel
def reset():
    for i, j in position:
        position[i, j] = ti.Vector([0.17 + j * SPACING, 0.88 - i * SPACING])
        velocity[i, j] = ti.Vector([0.0, 0.0])


@ti.kernel
def compute_velocity():
    for i, j in position:
        force = ti.Vector([0.0, -GRAVITY])
        for di, dj in ti.static(neighbors):
            row, col = i + di, j + dj
            if 0 <= row < ROWS and 0 <= col < COLS:
                delta = position[row, col] - position[i, j]
                distance = delta.norm()
                rest = SPACING * ti.sqrt(float(di * di + dj * dj))
                force += STIFFNESS * (distance - rest) * delta / ti.max(distance, 1e-6)
        next_velocity[i, j] = (velocity[i, j] + DT * force) * ti.exp(-DAMPING * DT)


@ti.kernel
def integrate():
    for i, j in position:
        if i == 0 and (j == 0 or j == COLS - 1):
            velocity[i, j] = ti.Vector([0.0, 0.0])
        else:
            velocity[i, j] = next_velocity[i, j]
            position[i, j] += DT * velocity[i, j]
            if position[i, j].y < 0.08:
                position[i, j].y = 0.08
                velocity[i, j].y = ti.max(0.0, -velocity[i, j].y * 0.3)


def bake():
    reset()
    frames = [position.to_numpy().reshape(-1, 2).copy()]
    for _ in range(1, FRAMES):
        for _ in range(SUBSTEPS):
            compute_velocity()
            integrate()
        frames.append(position.to_numpy().reshape(-1, 2).copy())
    return np.stack(frames)


# Verify a physical known case: the initial relaxed springs exert zero force.
reset()
before = position.to_numpy().copy()
compute_velocity()
integrate()
after = position.to_numpy()
expected_drop = GRAVITY * DT * DT * np.exp(-DAMPING * DT)
assert abs((before[-1, COLS // 2, 1] - after[-1, COLS // 2, 1]) - expected_drop) < 2e-7
frames = bake()
repeated = bake()
assert np.array_equal(frames, repeated), 'Reset did not reproduce the simulation'
assert np.isfinite(frames).all()
assert (frames[:, :, 1] >= 0.08 - 1e-6).all()
anchors = [0, COLS - 1]
assert np.allclose(frames[:, anchors], frames[0, anchors], atol=1e-7, rtol=0)
movement = float(np.max(np.linalg.norm(frames[30] - frames[0], axis=1)))
assert movement > 0.01
max_neighbor_length = float(max(np.linalg.norm(frames.reshape(FRAMES, ROWS, COLS, 2)[:, :, 1:] - frames.reshape(FRAMES, ROWS, COLS, 2)[:, :, :-1], axis=-1).max(), np.linalg.norm(frames.reshape(FRAMES, ROWS, COLS, 2)[:, 1:] - frames.reshape(FRAMES, ROWS, COLS, 2)[:, :-1], axis=-1).max()))
assert max_neighbor_length < SPACING * 3, 'Spring system became unstable'
data = {'schemaVersion': 1, 'engine': 'taichi', 'engineVersion': '.'.join(map(str, ti.__version__)), 'backend': 'cpu-x64', 'fps': FPS, 'rows': ROWS, 'columns': COLS, 'anchors': anchors, 'frames': np.round(frames.astype(np.float64), 6).tolist()}
encoded = (json.dumps(data, separators=(',', ':')) + '\n').encode()
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_bytes(encoded)
report = {'status': 'passed', 'backend': 'cpu-x64', 'gpuValidation': 'not-run: no GPU device in this executor', 'taichiVersion': data['engineVersion'], 'numpyVersion': np.__version__, 'frames': FRAMES, 'fps': FPS, 'particles': ROWS * COLS, 'substepsPerFrame': SUBSTEPS, 'dt': DT, 'sameResetBitwise': True, 'initialFreeFallError': float(abs((before[-1, COLS // 2, 1] - after[-1, COLS // 2, 1]) - expected_drop)), 'maxDisplacementAtFrame30': movement, 'maxNeighborLength': max_neighbor_length, 'cacheSha256': hashlib.sha256(encoded).hexdigest(), 'parameters': {'spacing': SPACING, 'gravity': GRAVITY, 'stiffness': STIFFNESS, 'damping': DAMPING}}
report['generatorSha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
args.report.parent.mkdir(parents=True, exist_ok=True)
args.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
