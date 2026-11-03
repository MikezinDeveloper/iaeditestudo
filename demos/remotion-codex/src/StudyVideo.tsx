import React from 'react';
import {AbsoluteFill, Html5Audio, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Project} from './project';

const Title: React.FC<{title: string; accent: string}> = ({title, accent}) => {
  const frame = useCurrentFrame(); // Local clock: this title starts at global frame 10.
  const {fps} = useVideoConfig();
  const entrance = spring({frame, fps, config: {damping: 16, stiffness: 120}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{background: '#08121ee8', padding: '20px 26px', borderLeft: `5px solid ${accent}`, color: 'white', fontSize: 27, fontWeight: 800, opacity: interpolate(frame, [0, 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), transform: `translateY(${(1 - entrance) * 60}px)`}}>
        {title}
      </div>
    </AbsoluteFill>
  );
};

export const StudyVideo: React.FC<Project> = (p) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#08121e', fontFamily: 'DejaVu Sans, sans-serif'}}>
      {p.clips.map((clip) => (
        <Sequence key={`${clip.source}-${clip.from}`} from={clip.from} durationInFrames={clip.durationInFrames} name={clip.source}>
          <OffthreadVideo src={staticFile(clip.source)} trimBefore={clip.trimBefore} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </Sequence>
      ))}
      <Html5Audio src={staticFile(p.audio.source)} volume={(f) => interpolate(f, [0, p.audio.fadeFrames, durationInFrames - 1 - p.audio.fadeFrames, durationInFrames - 1], [0, p.audio.volume, p.audio.volume, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
      <div style={{position: 'absolute', top: 18, left: 22, background: '#08121ed9', padding: '8px 12px', color: 'white', fontSize: 13}}>
        REMOTION / CODEX — quadro {frame}
      </div>
      <Sequence from={10} durationInFrames={durationInFrames - 10} name="Título animado">
        <Title title={p.title} accent={p.accent} />
      </Sequence>
      <div style={{position: 'absolute', height: 5, bottom: 0, left: 0, background: p.accent, width: `${100 * frame / (durationInFrames - 1)}%`}} />
    </AbsoluteFill>
  );
};
