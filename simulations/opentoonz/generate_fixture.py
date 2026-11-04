"""Original cel artwork and OCA fixture matching the inspected OpenToonz exporter.
This does not execute OpenToonz or write its native .tnz/.pli formats.
"""
from pathlib import Path
import hashlib
import json
import math
from PIL import Image, ImageDraw, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'demos/remotion-codex/public/opentoonz'
FILES = DEST / 'walk_files'
FILES.mkdir(parents=True, exist_ok=True)
S = 3
INK = '#233644'

def artwork(pose=None):
    im = Image.new('RGBA', (640*S, 360*S))
    d = ImageDraw.Draw(im)
    def line(points, color=INK, width=4):
        d.line([(round(x*S), round(y*S)) for x,y in points], fill=color, width=width*S, joint='curve')
    def oval(box, fill):
        d.ellipse(tuple(round(x*S) for x in box), fill=fill, outline=INK, width=3*S)
    def polygon(points, fill):
        d.polygon([(round(x*S),round(y*S)) for x,y in points], fill=fill)
        line(points+[points[0]], width=3)
    if pose is None:
        line([(175,274),(465,274)], '#536278', 2)
        oval((278,272,362,280), '#293a49')
    else:
        a = pose * math.tau / 8
        swing = math.sin(a) * 24
        bob = abs(math.cos(a)) * 5
        # Fixed poses, held by the exposure sheet. No interpolation at playback.
        line([(309,221-bob),(301-swing/2,248),(305-swing,270)], width=7)
        line([(333,221-bob),(337+swing/2,248),(334+swing,270)], width=7)
        line([(300-swing,270),(312-swing,270)], '#62f4c6', 7)
        line([(329+swing,270),(343+swing,270)], '#62f4c6', 7)
        line([(339,211-bob),(370,202-bob),(378+math.cos(a)*9,180-bob)], width=7)
        line([(297,186-bob),(281+swing/2,213-bob),(283+swing,230-bob)], width=6)
        oval((289,172-bob,351,235-bob), '#ad9bff')
        line([(343,185-bob),(359-swing/2,211-bob),(355-swing,231-bob)], width=6)
        polygon([(285,126-bob),(281,92-bob),(307,108-bob)], '#62f4c6')
        polygon([(332,108-bob),(357,92-bob),(356,127-bob)], '#62f4c6')
        oval((280,104-bob,359,174-bob), '#62f4c6')
        oval((298,129-bob,304,139-bob), INK)
        oval((336,129-bob,342,139-bob), INK)
        polygon([(316,144-bob),(324,144-bob),(320,150-bob)], '#e27a94')
        line([(309,155-bob),(320,160-bob),(331,155-bob)], width=2)
        line([(284,147-bob),(265,143-bob)], width=2)
        line([(355,147-bob),(375,142-bob)], width=2)
    return im.resize((640,360), Image.Resampling.LANCZOS)

paths = []
for name, pose in [('Ground.0001.png',None)] + [(f'Cat.{i+1:04d}.png',i) for i in range(8)]:
    path = FILES / name
    artwork(pose).save(path)
    paths.append(path)

def cel(name, file, number, duration):
    return dict(name=name, fileName=f'walk_files/{file}' if file else '', frameNumber=number,
                duration=duration, width=640 if file else 0, height=360 if file else 0,
                position=[320,180], opacity=1)

def layer(name, frames):
    return dict(name=name, position=[320,180], width=640, height=360, frames=frames,
                childLayers=[], type='paintlayer', fileType='png', blendingMode='normal',
                animated=len(frames)>1, label=0, opacity=1, visible=True, passThrough=False,
                reference=False, inheritAlpha=False)

# Two-frame holds at 24fps; one explicit blank interval tests absent artwork.
frames = []
for row in range(0,72,2):
    pose = (row//2)%8
    blank = row == 46
    frames.append(cel('_blank' if blank else f'Cat.{pose+1:04d}', '' if blank else f'Cat.{pose+1:04d}.png',row,2))
scene = dict(name='Codex original cel fixture',frameRate=24,width=640,height=360,
             startTime=0,endTime=72,colorDepth='U8',backgroundColor=[16/255,25/255,35/255,1],
             layers=[layer('Ground',[cel('Ground.0001','Ground.0001.png',0,72)]),layer('Cat',frames)],
             originApp='CodexStudy',originAppVersion='1',ocaVersion='1.1.0')
oca = DEST / 'walk.oca'
oca.write_text(json.dumps(scene,indent=2)+'\n')
paths.append(oca)
report = dict(status='passed',generator='Original Pillow artwork and OCA fixture; not exported by native OpenToonz',
              pillowVersion=pillow_version,sourceRevision='572d59ac5fedfeaf7910967b439c6b8d73c9c3e1',
              scriptSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
(ROOT/'estudo/opentoonz/resultados/fixture.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assets':len(paths)-1,'ocaFrames':72,'fps':24,'pillow':pillow_version}))
