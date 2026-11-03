import {readFileSync, mkdirSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {bundle} from '@remotion/bundler';
import {openBrowser, renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {validateProject} from '../src/project.ts';

const propsPath = process.argv[2] ?? 'project.json';
const p = validateProject(JSON.parse(readFileSync(propsPath, 'utf8')));
if (p.durationInFrames !== 180 || p.fps !== 30 || p.width !== 640 || p.height !== 360) {
  throw new Error('O experimento automatizado usa 640x360, 30 fps e 180 quadros; amplie o verificador antes de alterar esses metadados.');
}
for (const asset of [...p.clips.map((c) => ({source: c.source, needed: (c.trimBefore + c.durationInFrames) / p.fps})), {source: p.audio.source, needed: p.durationInFrames / p.fps}]) {
  const probe = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'json', resolve('public', asset.source)], {encoding: 'utf8'});
  if (probe.error || probe.status !== 0) throw probe.error ?? new Error(`ffprobe falhou: ${asset.source}`);
  if (Number(JSON.parse(probe.stdout).format.duration) + 0.001 < asset.needed) throw new Error(`Asset curto: ${asset.source}`);
}
mkdirSync('out', {recursive: true});
const started = Date.now();
const serveUrl = await bundle({entryPoint: resolve('src/index.ts'), outDir: resolve('.cache/bundle')});
const browser = await openBrowser('chrome', {browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? null});
const options = {serveUrl, puppeteerInstance: browser, inputProps: p};
const digest = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');
try {
  const composition = await selectComposition({...options, id: 'CodexStudy'});
  for (const frame of [0, 30, 89, 90, 120, 179]) {
    await renderStill({...options, composition, frame, output: resolve(`out/frame-${frame}.png`), imageFormat: 'png'});
  }
  await renderStill({...options, composition, frame: 30, output: resolve('out/frame-30-repeat.png'), imageFormat: 'png'});
  const variantProps = {...p, title: 'EDICAO POR DADOS'};
  // selectComposition returns resolved props. A changed plan needs a new selection.
  const variantComposition = await selectComposition({...options, inputProps: variantProps, id: 'CodexStudy'});
  await renderStill({...options, composition: variantComposition, frame: 30, inputProps: variantProps, output: resolve('out/frame-30-variant.png'), imageFormat: 'png'});
  if (digest('out/frame-30.png') !== digest('out/frame-30-repeat.png')) throw new Error('Mesmo quadro não se repetiu neste ambiente');
  if (digest('out/frame-30.png') === digest('out/frame-30-variant.png')) throw new Error('Alterar title não modificou o quadro');
  await renderMedia({...options, composition, codec: 'h264', audioCodec: 'aac', sampleRate: 48000, pixelFormat: 'yuv420p', crf: 18, concurrency: 2, imageFormat: 'png', outputLocation: resolve('out/codex-study.mp4')});
  const report = {remotion: '4.0.540', inputFile: propsPath, inputSha256: digest(propsPath), inputProps: p, browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? 'Remotion default', composition: {id: composition.id, fps: composition.fps, width: composition.width, height: composition.height, durationInFrames: composition.durationInFrames}, sameFrameRepeated: true, changedTitleChangedPixels: true, elapsedSeconds: (Date.now() - started) / 1000, hashes: Object.fromEntries(['frame-30.png', 'frame-30-repeat.png', 'frame-30-variant.png', 'codex-study.mp4'].map((name) => [name, digest(`out/${name}`)]))};
  writeFileSync('out/render-report.json', JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
} finally {
  await browser.close({silent: true});
}
