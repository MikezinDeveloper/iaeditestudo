#!/usr/bin/env bash
set -euo pipefail

cd /workspace/iaeditestudo/demos/remotion-codex
node -e 'if (Number(process.versions.node.split(".")[0]) < 24) throw new Error("Node.js >=24 necessário")'
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
command -v chromium >/dev/null
npm ci --no-audit --no-fund
npm run assets
npm run typecheck
npm test
