"""Verify the actual exported media, using only Python's standard library and FFmpeg."""
from array import array
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess


def run(*args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


report = json.loads(Path('out/render-report.json').read_text())
assert digest(report['inputFile']) == report['inputSha256'], 'Configuração mudou desde o render'
for name, expected in report['hashes'].items():
    assert digest(f'out/{name}') == expected, f'Artefato alterado: {name}'
project = report['inputProps']
probe = json.loads(run('ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', 'out/codex-study.mp4'))
videos = [s for s in probe['streams'] if s['codec_type'] == 'video']
audios = [s for s in probe['streams'] if s['codec_type'] == 'audio']
assert len(videos) == len(audios) == 1, 'Esperadas uma stream de vídeo e uma de áudio'
video, audio = videos[0], audios[0]
assert (video['width'], video['height']) == (640, 360)
assert video['codec_name'] == 'h264' and audio['codec_name'] == 'aac'
assert Fraction(video['avg_frame_rate']) == 30
assert int(video['nb_read_frames']) == 180
assert abs(float(probe['format']['duration']) - 6) < 0.05
assert int(audio['sample_rate']) == 48000


def crop(path, frame):
    # This region is deliberately free of our title, counter and progress overlays.
    return run('ffmpeg', '-v', 'error', '-threads', '2', '-i', str(path), '-vf',
               f'select=eq(n\\,{frame}),crop=160:70:0:260,format=rgb24',
               '-frames:v', '1', '-threads', '1', '-f', 'rawvideo', 'pipe:1')


def difference(a, b):
    assert len(a) == len(b) == 160 * 70 * 3, 'ROI ausente ou incompleta'
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


cuts = []
for frame in (89, 90):
    clip = next(c for c in project['clips'] if c['from'] <= frame < c['from'] + c['durationInFrames'])
    local = frame - clip['from']
    expected = crop(Path('public') / clip['source'], local + clip['trimBefore'])
    untrimmed = crop(Path('public') / clip['source'], local)
    actual = crop('out/codex-study.mp4', frame)
    correct_error = difference(actual, expected)
    untrimmed_error = difference(actual, untrimmed)
    assert correct_error < 12, f'Corte/trim incorreto no quadro {frame}: erro {correct_error}'
    assert correct_error < untrimmed_error, f'Trim não demonstrado no quadro {frame}'
    cuts.append({'outputFrame': frame, 'source': clip['source'], 'sourceFrame': local + clip['trimBefore'], 'meanPixelError': correct_error, 'untrimmedPixelError': untrimmed_error})

samples = array('f')
samples.frombytes(run('ffmpeg', '-v', 'error', '-i', 'out/codex-study.mp4', '-map', '0:a:0', '-ac', '1', '-ar', '48000', '-f', 'f32le', 'pipe:1'))


def rms(start, end):
    chunk = samples[int(start * 48000):int(end * 48000)]
    assert len(chunk), 'Janela de áudio vazia'
    return math.sqrt(sum(value * value for value in chunk) / len(chunk))


levels = {'start': rms(0, 0.1), 'steady': rms(1, 1.1), 'end': rms(5.9, 6)}
assert levels['steady'] > 0.005, 'Stream de áudio silenciosa'
assert levels['start'] < levels['steady'] * 0.35, 'Fade-in não demonstrado'
assert levels['end'] < levels['steady'] * 0.35, 'Fade-out não demonstrado'
assert digest('out/frame-30.png') == digest('out/frame-30-repeat.png')
assert digest('out/frame-30.png') != digest('out/frame-30-variant.png')
result = {'status': 'passed', 'frames': 180, 'fps': 30, 'durationSeconds': float(probe['format']['duration']), 'resolution': [640, 360], 'codecs': ['h264', 'aac'], 'cuts': cuts, 'audioRms': levels, 'sameFrameRepeated': True, 'changedTitleChangedPixels': True}
Path('out/verification-report.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
