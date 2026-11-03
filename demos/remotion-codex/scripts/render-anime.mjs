import {readFileSync, writeFileSync, mkdirSync, existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';
import {openBrowser, selectComposition, renderStill, renderMedia} from '@remotion/renderer';

const folder = 'out/anime';
mkdirSync(folder, {recursive: true});
const hash = (file) => createHash('sha256').update(readFileSync(file)).digest('hex');
const command = (program, args, encoding) => {
  const result = spawnSync(program, args, {encoding, maxBuffer: 8 * 1024 * 1024});
  if (result.error || result.status !== 0) throw result.error ?? new Error(`${program}: ${result.stderr}`);
  return result.stdout;
};
const started = Date.now();
const serveUrl = await bundle({entryPoint: resolve('src/index.ts'), outDir: resolve('.cache/anime-bundle')});
const browser = await openBrowser('chrome', {browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? null});
const options = {serveUrl, puppeteerInstance: browser, inputProps: {}};
try {
  const composition = await selectComposition({...options, id: 'AnimeMotionStudy'});
  for (const frame of [0, 15, 30, 60, 90, 111, 28, 119]) {
    await renderStill({...options, composition, frame, imageFormat: 'png', output: resolve(`${folder}/frame-${frame}.png`)});
  }
  await renderStill({...options, composition, frame: 30, imageFormat: 'png', output: resolve(`${folder}/frame-30-after-end.png`)});
  if (hash(`${folder}/frame-30.png`) !== hash(`${folder}/frame-30-after-end.png`)) throw new Error('Frame mudou ao voltar do fim');
  const video = `${folder}/anime-motion.mp4`;
  await renderMedia({...options, composition, codec: 'h264', audioCodec: 'aac', sampleRate: 48000, pixelFormat: 'yuv420p', concurrency: 2, imageFormat: 'png', outputLocation: resolve(video)});
  const probe = JSON.parse(command('ffprobe', ['-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', video], 'utf8'));
  const v = probe.streams.find((s) => s.codec_type === 'video');
  const a = probe.streams.find((s) => s.codec_type === 'audio');
  if (!v || !a || v.codec_name !== 'h264' || a.codec_name !== 'aac' || v.width !== 640 || v.height !== 360 || v.nb_read_frames !== '120' || v.avg_frame_rate !== '30/1' || Math.abs(Number(probe.format.duration) - 4) > 0.05) throw new Error('Metadados do export inesperados');
  const crop = (frame) => command('ffmpeg', ['-v', 'error', '-threads', '2', '-i', video, '-vf', `select=eq(n\\,${frame}),crop=560:100:32:70,format=rgb24`, '-frames:v', '1', '-threads', '1', '-f', 'rawvideo', 'pipe:1']);
  const before = crop(0), after = crop(30);
  if (before.length !== 560 * 100 * 3 || before.length !== after.length) throw new Error('Região de análise vazia');
  const titlePixelChange = before.reduce((sum, byte, index) => sum + Math.abs(byte - after[index]), 0) / before.length;
  if (titlePixelChange < 1) throw new Error('A região do título não mudou no vídeo exportado');
  const inputProps = JSON.parse(readFileSync('project.json', 'utf8'));
  const baseOptions = {...options, inputProps};
  const base = await selectComposition({...baseOptions, id: 'CodexStudy'});
  const baseOutput = `${folder}/remotion-regression.png`;
  await renderStill({...baseOptions, composition: base, frame: 30, imageFormat: 'png', output: resolve(baseOutput)});
  const regression = existsSync('out/frame-30.png') ? {status: hash(baseOutput) === hash('out/frame-30.png') ? 'passed' : 'failed', baseline: 'out/frame-30.png'} : {status: 'not-run', reason: 'No previous local frame baseline'};
  if (regression.status === 'failed') throw new Error('A composição original mudou');
  const report = {status: 'passed', animejs: '4.5.0', remotion: '4.0.540', composition: composition.id, width: v.width, height: v.height, frames: Number(v.nb_read_frames), fps: v.avg_frame_rate, durationSeconds: Number(probe.format.duration), codecs: [v.codec_name, a.codec_name], repeatedFrameAfterEnd: true, titleRegionMeanPixelChange: titlePixelChange, baseCompositionRegression: regression, elapsedSeconds: (Date.now() - started) / 1000, hashes: Object.fromEntries(['frame-30.png', 'frame-30-after-end.png', 'anime-motion.mp4', 'remotion-regression.png'].map((file) => [file, hash(`${folder}/${file}`)]))};
  writeFileSync(`${folder}/report.json`, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
} finally {
  await browser.close({silent: true});
}
