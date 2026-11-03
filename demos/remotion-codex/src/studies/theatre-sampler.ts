import * as TheatreModule from '@theatre/core';
// Node resolves this release as CJS; Webpack can expose its named module shape.
const theatre = (TheatreModule as typeof TheatreModule & {default?: typeof TheatreModule}).default ?? TheatreModule;

export const createTheatreSampler = async (state: object, projectId = 'IAEditEstudo-Theatre-Study-v1') => {
  const {getProject, createRafDriver} = theatre;
  const project = getProject(projectId, {state});
  await project.ready;
  const sheet = project.sheet('Scene');
  const duration = theatre.val(sheet.sequence.pointer.length);
  const object = sheet.object('Card', {x: 0, angle: 0, scale: 1});
  const driver = createRafDriver({name: 'Remotion explicit frame driver'});
  let value = {x: 0, angle: 0, scale: 1};
  let disposed = false;
  const unsubscribe = object.onValuesChange((next) => {value = {...next};}, driver);
  return {
    sample(seconds: number) {
      if (disposed) throw new Error('Sampler descartado');
      if (!Number.isFinite(seconds)) throw new Error('Tempo inválido');
      sheet.sequence.position = Math.max(0, Math.min(duration, seconds));
      driver.tick(seconds * 1000);
      return {...value};
    },
    dispose() { if (!disposed) unsubscribe(); disposed = true; },
  };
};
