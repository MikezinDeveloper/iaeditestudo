import React from 'react';
import {Composition} from 'remotion';
import project from '../project.json';
import {StudyVideo} from './StudyVideo';
import {validateProject} from './project';
import {AnimeMotionStudy} from './AnimeMotionStudy';
import {MojsStudy} from './studies/MojsStudy';

export const Root: React.FC = () => (
  <>
  <Composition
    id="CodexStudy"
    component={StudyVideo}
    defaultProps={validateProject(project)}
    width={project.width}
    height={project.height}
    fps={project.fps}
    durationInFrames={project.durationInFrames}
    calculateMetadata={({props}) => {
      const p = validateProject(props);
      return {width: p.width, height: p.height, fps: p.fps, durationInFrames: p.durationInFrames};
    }}
  />
  <Composition id="AnimeMotionStudy" component={AnimeMotionStudy} width={640} height={360} fps={30} durationInFrames={120} />
  <Composition id="MojsStudy" component={MojsStudy} width={640} height={360} fps={30} durationInFrames={90} />
  </>
);
