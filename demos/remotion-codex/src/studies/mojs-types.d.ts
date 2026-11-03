declare module '@mojs/core' {
  type Options = Record<string, unknown>;
  interface Motion {setProgress(progress: number): Motion; pause(): Motion;}
  interface Timeline extends Motion {add(...items: Motion[]): Timeline;}
  const mojs: {
    Shape: new (options: Options) => Motion;
    Burst: new (options: Options) => Motion;
    Timeline: new (options?: Options) => Timeline;
  };
  export default mojs;
}
