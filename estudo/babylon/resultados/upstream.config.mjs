// Adapted from Babylon.js vitest.config.mts (Apache-2.0), fixed revision in study.
import {transformWithEsbuild} from 'vite';
export default {
  oxc: false,
  plugins: [{name: 'babylon-tc39-decorators', enforce: 'pre', async transform(code, id) {
    if (!/\.tsx?$/.test(id.split('?')[0]) || id.includes('/node_modules/')) return null;
    const result = await transformWithEsbuild(code, id, {target: 'es2021', tsconfigRaw: {compilerOptions: {useDefineForClassFields: false}}});
    return {code: result.code, map: result.map};
  }}],
  root: '/workspace/research-cache/babylon',
  resolve: {alias: {core: '/workspace/research-cache/babylon/packages/dev/core/src', vitest: '/workspace/research-cache/babylon-runner/node_modules/vitest'}},
  test: {globals: true, pool: 'forks', setupFiles: ['/workspace/research-cache/babylon/vitest.setup.ts'], environment: 'node', include: ['packages/dev/core/test/unit/Math/babylon.math.vector.test.ts', 'packages/dev/core/test/unit/Animations/babylon.animation.test.ts'], reporters: ['default', 'json'], outputFile: {json: '/workspace/research-cache/babylon-runner/result.json'}, maxWorkers: 2}
};
