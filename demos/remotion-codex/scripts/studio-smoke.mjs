import {mkdirSync, writeFileSync} from 'node:fs';
import {openBrowser} from '@remotion/renderer';

// Version-pinned experimental browser probe, not an agent WebMCP integration.
const browser = await openBrowser('chrome', {browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? null});
try {
  const page = await browser.newPage({context: () => null, logLevel: 'error', indent: false, pageIndex: 0, onBrowserLog: null, onLog: () => {}});
  await page.goto({url: 'http://127.0.0.1:3000/CodexStudy', timeout: 30000});
  const state = await page.evaluate(async () => {
    const deadline = Date.now() + 30000;
    while (Date.now() < deadline) {
      const video = [...document.querySelectorAll('video')].find((v) => v.currentSrc.includes('source-01.mp4'));
      if (video && video.readyState >= 2 && Math.abs(video.currentTime - 0.5) < 0.1) {
        return {status: 'passed', compositionVisible: document.body.innerText.includes('CodexStudy'), source: new URL(video.currentSrc).pathname, readyState: video.readyState, mediaTimeSeconds: video.currentTime, expectedTrimSeconds: 0.5, videoWidth: video.videoWidth, videoHeight: video.videoHeight};
      }
      await new Promise((resolve) => setTimeout(resolve, 200));
    }
    return {status: 'failed', text: document.body.innerText.slice(0, 1800), videos: [...document.querySelectorAll('video')].map((v) => ({source: v.currentSrc, readyState: v.readyState, time: v.currentTime}))};
  });
  if (state.status !== 'passed' || !state.compositionVisible) throw new Error(JSON.stringify(state));
  mkdirSync('out', {recursive: true});
  writeFileSync('out/studio-report.json', JSON.stringify(state, null, 2) + '\n');
  console.log(JSON.stringify(state, null, 2));
} finally {
  await browser.close({silent: true});
}
