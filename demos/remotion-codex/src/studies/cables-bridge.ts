export type CablesPort = {set: (value: number) => void; get: () => number};
export type CablesPatch = {ops: unknown[]; getOpById: (id: string) => {getPort: (name: string) => CablesPort}; pause: () => void; timer: {pause: () => void}; dispose: () => void};
export type CablesRuntime = {Patch: new (config: Record<string, unknown>) => CablesPatch};

export const createCablesSampler = (runtime: CablesRuntime, data: unknown) => {
  const failures: unknown[] = [];
  const patch = new runtime.Patch({patch: structuredClone(data), doRequestAnimation: false, silent: true, onError: (...args: unknown[]) => failures.push(args)});
  patch.pause(); patch.timer.pause();
  if (failures.length || patch.ops.length !== 3) {patch.dispose(); throw new Error('Patch Cables não carregou');}
  const input = patch.getOpById('time').getPort('Time');
  const output = patch.getOpById('scale').getPort('result');
  let disposed = false;
  return {
    sample: (timeMs: number) => {
      if (disposed || !Number.isFinite(timeMs) || timeMs < 0) throw new Error('Tempo ou patch Cables inválido');
      input.set(timeMs / 1000);
      const value = output.get();
      if (!Number.isFinite(value) || failures.length) throw new Error('Grafo Cables retornou valor inválido');
      return value;
    },
    dispose: () => {if (!disposed) {disposed = true; patch.dispose();}},
  };
};
