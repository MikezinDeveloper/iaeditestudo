import {mkdirSync} from 'node:fs';
import {spawnSync} from 'node:child_process';

mkdirSync('public', {recursive: true});
for (const [name, filter] of [['source-01', 'null'], ['source-02', 'hue=h=90']]) {
  const result = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=640x360:rate=30:duration=4', '-vf', filter, '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-threads', '2', `public/${name}.mp4`], {stdio: 'inherit'});
  if (result.error || result.status !== 0) throw result.error ?? new Error(`FFmpeg falhou: ${name}`);
}
const audio = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=6', '-c:a', 'pcm_s16le', 'public/tone.wav'], {stdio: 'inherit'});
if (audio.error || audio.status !== 0) throw audio.error ?? new Error('FFmpeg falhou: áudio');
console.log('Assets sintéticos gerados em public/; nenhum download externo.');
