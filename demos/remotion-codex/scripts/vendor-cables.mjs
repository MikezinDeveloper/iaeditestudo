import {build} from 'esbuild';
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {resolve, relative} from 'node:path';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';

// Rebuild only from the two inspected source revisions. Runtime output is committed.
const core = resolve(process.argv[2] ?? '/workspace/research-cache/cables-core');
const shared = resolve(process.argv[3] ?? '/workspace/research-cache/cables-dev');
const revisions = {core: '93c81a30abf811f5e2421040dba1ba0ae4f34c8e', shared: '9513b65ee409ab1c356e24845f838c9858a287fb'};
for (const [key, folder] of Object.entries({core, shared})) {
  if (execFileSync('git', ['-C', folder, 'rev-parse', 'HEAD'], {encoding: 'utf8'}).trim() !== revisions[key]) throw new Error(`Revisão ${key} incorreta`);
  if (execFileSync('git', ['-C', folder, 'status', '--porcelain', '--untracked-files=no'], {encoding: 'utf8'}).trim()) throw new Error(`Fonte ${key} modificada`);
}
const folder = resolve('public/vendor/cables');
mkdirSync(folder, {recursive: true});
const sharedEntry = resolve('.cache/cables-shared-entry.js');
mkdirSync(resolve('.cache'), {recursive: true});
writeFileSync(sharedEntry, `export {default as Events} from ${JSON.stringify(`${shared}/shared/client/src/eventtarget.js`)};\nexport {default as Logger} from ${JSON.stringify(`${shared}/shared/client/src/logger.js`)};\nexport {default as helper} from ${JSON.stringify(`${shared}/shared/client/src/helper.js`)};\n`);
let registration = '';
const opFiles = [];
for (const name of ['Ops.Math.Sine', 'Ops.Math.Multiply']) {
  const base = `${core}/src/ops/base/${name}/${name}`;
  const metadata = JSON.parse(readFileSync(`${base}.json`, 'utf8'));
  opFiles.push(`${base}.js`, `${base}.json`);
  registration += `CABLES.OPS[${JSON.stringify(metadata.id)}] = {objName: ${JSON.stringify(name)}, f: class extends CABLES.Op {constructor(...args) {super(...args); const op = this;\n${readFileSync(`${base}.js`, 'utf8')}\n}}};\n`;
}
registration += `CABLES.OPS['codex-frame-time'] = {objName: 'Ops.Codex.FrameTime', f: class extends CABLES.Op {constructor(...args) {super(...args); this.outNumber('Time');}}};`;
const result = await build({
  stdin: {contents: `import CABLES from ${JSON.stringify(`${core}/src/core/index.js`)};\n${registration}`, resolveDir: process.cwd(), sourcefile: 'cables-selected-runtime.js'},
  alias: {'cables-shared-client': sharedEntry},
  outfile: `${folder}/runtime.js`, bundle: true, platform: 'browser', format: 'iife', target: 'es2022', minify: true, metafile: true,
  banner: {js: '/* Cables runtime: MIT. Sources and license: NOTICE.txt and provenance.json. */\n"use strict"; var CABLES = globalThis.CABLES || {};'},
});
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const inputs = [...Object.keys(result.metafile.inputs).filter((x) => !x.startsWith('cables-selected-runtime') && resolve(x) !== sharedEntry), ...opFiles];
const records = inputs.map((file) => {
  const path = resolve(file);
  const source = path.startsWith(`${core}/`) ? 'core' : 'shared';
  return {source, path: relative(source === 'core' ? core : shared, path), sha256: hash(readFileSync(path))};
});
writeFileSync(`${folder}/provenance.json`, JSON.stringify({revisions, sources: {core: 'https://github.com/cables-gl/cables', shared: 'https://github.com/cables-gl/cables_dev'}, files: records, runtimeSha256: hash(readFileSync(`${folder}/runtime.js`)), build: 'esbuild 0.28.2; selected original core, Events/Logger and two original ops; generated registrations and FrameTime are ours'}, null, 2) + '\n');
writeFileSync(`${folder}/NOTICE.txt`, 'Cables core: package.json declares MIT; no root LICENSE file in this core revision.\nhttps://github.com/cables-gl/cables/tree/' + revisions.core + '\nShared Events/Logger and project license: https://github.com/cables-gl/cables_dev/tree/' + revisions.shared + '\nGenerated build entry and FrameTime op are adaptations by iaeditestudo.\n\n' + readFileSync(`${shared}/LICENCE`, 'utf8'));
console.log(`Cables runtime generated from ${records.length} source inputs`);
