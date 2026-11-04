import {readFileSync, writeFileSync, mkdirSync, existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';
import {openBrowser, selectComposition, renderStill, renderMedia} from '@remotion/renderer';

const catalogue = JSON.parse(readFileSync(new URL('./studies.json', import.meta.url), 'utf8'));
const key = process.argv[2];
if (!Object.hasOwn(catalogue, key)) throw new Error(`Escolha um estudo registrado: ${Object.keys(catalogue).join(', ')}`);
const target = catalogue[key];
const folder = `out/studies/${key}`;
mkdirSync(folder, {recursive: true});
const hash = (file) => createHash('sha256').update(readFileSync(file)).digest('hex');
const run = (program, args, encoding) => {
  const result = spawnSync(program, args, {encoding, maxBuffer: 8 * 1024 * 1024});
  if (result.error || result.status !== 0) throw result.error ?? new Error(`${program}: ${result.stderr}`);
  return result.stdout;
};
const started = Date.now();
const serveUrl = await bundle({entryPoint: resolve('src/index.ts'), outDir: resolve(`.cache/study-${key}`)});
const browser = await openBrowser('chrome', {browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? null, chromiumOptions: {gl: target.gl ?? 'angle'}});
const browsers = new Map([[target.gl ?? 'angle', browser]]);
const options = {serveUrl, puppeteerInstance: browser, inputProps: {}};
try {
  const composition = await selectComposition({...options, id: target.composition});
  const frames = [...new Set([0, 15, 30, Math.floor(target.frames / 2), target.frames - 1])];
  for (const frame of frames) await renderStill({...options, composition, frame, imageFormat: 'png', output: resolve(`${folder}/frame-${frame}.png`)});
  await renderStill({...options, composition, frame: 30, imageFormat: 'png', output: resolve(`${folder}/frame-30-repeat.png`)});
  if (hash(`${folder}/frame-30.png`) !== hash(`${folder}/frame-30-repeat.png`)) throw new Error('Retornar ao frame mudou os pixels');
  const video = `${folder}/video.mp4`;
  await renderMedia({...options, composition, codec: 'h264', audioCodec: 'aac', concurrency: 2, imageFormat: 'png', outputLocation: resolve(video)});
  const probe = JSON.parse(run('ffprobe', ['-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', video], 'utf8'));
  const v = probe.streams.find((s) => s.codec_type === 'video');
  const a = probe.streams.find((s) => s.codec_type === 'audio');
  if (!v || !a || v.codec_name !== 'h264' || a.codec_name !== 'aac' || v.width !== 640 || v.height !== 360 || Number(v.nb_read_frames) !== target.frames || v.avg_frame_rate !== `${target.fps}/1` || Math.abs(Number(probe.format.duration) - target.frames / target.fps) > 0.05) throw new Error('Metadados inesperados no export');
  const crop = (frame) => run('ffmpeg', ['-v', 'error', '-threads', '2', '-i', video, '-vf', `select=eq(n\\,${frame}),crop=320:220:160:80,format=rgb24`, '-frames:v', '1', '-threads', '1', '-f', 'rawvideo', 'pipe:1']);
  const first = crop(0), later = crop(30);
  if (first.length !== 320 * 220 * 3 || later.length !== first.length) throw new Error('Região visual vazia');
  const pixelChange = first.reduce((sum, value, index) => sum + Math.abs(value - later[index]), 0) / first.length;
  if (pixelChange < 0.1) throw new Error('Movimento não demonstrado na região visual');
  const regressions = {};
  const previousStudies = Object.entries(catalogue).slice(0, Object.keys(catalogue).indexOf(key)).map(([previousKey, previous]) => [previous.composition, `out/studies/${previousKey}/frame-30.png`, {}, previous.gl ?? 'angle']);
  for (const [id, baseline, inputProps, gl] of [['CodexStudy', 'out/frame-30.png', JSON.parse(readFileSync('project.json', 'utf8')), 'angle'], ['AnimeMotionStudy', 'out/anime/frame-30.png', {}, 'angle'], ...previousStudies]) {
    if (!existsSync(baseline)) {regressions[id] = 'not-run: missing baseline'; continue;}
    if (!browsers.has(gl)) browsers.set(gl, await openBrowser('chrome', {browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? null, chromiumOptions: {gl}}));
    const regressionOptions = {...options, puppeteerInstance: browsers.get(gl), inputProps};
    const cfg = await selectComposition({...regressionOptions, id});
    const file = `${folder}/regression-${id}.png`;
    await renderStill({...regressionOptions, composition: cfg, frame: 30, imageFormat: 'png', output: resolve(file)});
    if (hash(file) !== hash(baseline)) throw new Error(`Regressão na composição ${id}`);
    regressions[id] = 'passed';
  }
  const report = {status: 'passed', study: key, composition: composition.id, chromiumGl: target.gl ?? 'angle', frames: target.frames, fps: target.fps, durationSeconds: Number(probe.format.duration), codecs: [v.codec_name, a.codec_name], repeatedFrameAfterEnd: true, regionMeanPixelChange: pixelChange, regressions, elapsedSeconds: (Date.now() - started) / 1000, hashes: {video: hash(video), frame30: hash(`${folder}/frame-30.png`)}};
  writeFileSync(`${folder}/report.json`, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
} finally {for (const instance of browsers.values()) await instance.close({silent: true});}
