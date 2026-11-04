import {PackedSplats} from '@sparkjsdev/spark';
import {Vector3, Quaternion, Color} from 'three';

export const createProceduralSplats = (count = 192) => {
  if (!Number.isInteger(count) || count < 16 || count > 4096) throw new Error('Quantidade de splats inválida');
  const splats = new PackedSplats();
  const center = new Vector3(), scales = new Vector3(), rotation = new Quaternion(), color = new Color();
  for (let i = 0; i < count; i++) {
    const t = i / count * 2 * Math.PI;
    center.set(1.3 * Math.cos(t), 0.7 * Math.sin(2 * t), 0.5 * Math.sin(t));
    scales.set(0.08, 0.04, 0.06);
    rotation.setFromAxisAngle(new Vector3(0, 0, 1), t);
    color.setRGB(0.25 + 0.6 * i / count, 0.85 - 0.5 * i / count, 0.7);
    splats.pushSplat(center, scales, rotation, 0.85, color);
  }
  return splats;
};
