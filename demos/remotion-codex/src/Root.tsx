import React from 'react';
import {Composition} from 'remotion';
import project from '../project.json';
import {StudyVideo} from './StudyVideo';
import {validateProject} from './project';
import {AnimeMotionStudy} from './AnimeMotionStudy';
import {MojsStudy} from './studies/MojsStudy';
import {TheatreStudy} from './studies/TheatreStudy';
import {TwoStudy} from './studies/TwoStudy';
import {D3Study} from './studies/D3Study';
import {ThreeStudy} from './studies/ThreeStudy';
import {BabylonStudy} from './studies/BabylonStudy';
import {DreiStudy} from './studies/DreiStudy';

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
  <Composition id="TheatreStudy" component={TheatreStudy} width={640} height={360} fps={30} durationInFrames={90} />
  <Composition id="TwoStudy" component={TwoStudy} width={640} height={360} fps={30} durationInFrames={90} />
  <Composition id="D3Study" component={D3Study} width={640} height={360} fps={30} durationInFrames={90} />
  <Composition id="ThreeStudy" component={ThreeStudy} width={640} height={360} fps={30} durationInFrames={90} />
  <Composition id="BabylonStudy" component={BabylonStudy} width={640} height={360} fps={30} durationInFrames={90} />
  <Composition id="DreiStudy" component={DreiStudy} width={640} height={360} fps={30} durationInFrames={90} />
  </>
);
