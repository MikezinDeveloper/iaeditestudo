import glsl from 'vite-plugin-glsl';
import arraybuffer from 'vite-plugin-arraybuffer';
const runner = '/workspace/research-cache/spark-runner';
const project = '/workspace/research-cache/spark';
export default {
  root: project,
  plugins: [arraybuffer(), glsl()],
  resolve: {alias: [
    {find: 'spark-rs/spark_rs_bg.wasm?arraybuffer&base64', replacement: `${runner}/wasm-binary-stub.js`},
    {find: 'spark-rs', replacement: `${runner}/wasm-stub.js`},
    {find: /^three\/addons\//, replacement: '/workspace/iaeditestudo/demos/remotion-codex/node_modules/three/examples/jsm/'},
    {find: /^three$/, replacement: '/workspace/iaeditestudo/demos/remotion-codex/node_modules/three/build/three.module.js'},
    {find: 'vitest', replacement: `${runner}/node_modules/vitest`},
    {find: 'fflate', replacement: `${runner}/node_modules/fflate`}
  ]},
  test: {include: ['test/unit/utils.test.ts','test/unit/PackedSplats.test.ts','test/unit/SparkRenderer.test.ts','test/unit/SplatMesh.test.ts','test/unit/SplatWorker.test.ts'], setupFiles: [`${project}/test/unit/setup.ts`], restoreMocks: true, environment: 'node', maxWorkers: 2, reporters: ['default','json'], outputFile: {json: `${runner}/result.json`}}
};
