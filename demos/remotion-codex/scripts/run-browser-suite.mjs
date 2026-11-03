import {openBrowser} from '@remotion/renderer';
import {mkdirSync, writeFileSync} from 'node:fs';
import {dirname} from 'node:path';

const [url, output] = process.argv.slice(2);
if (!url || !output) throw new Error('Informe URL local da suíte e caminho do relatório');
const browser = await openBrowser('chrome', {browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? '/usr/bin/chromium', chromiumOptions: {gl: 'swangle'}});
try {
  const page = await browser.newPage({context: () => null, logLevel: 'error', indent: false, pageIndex: 0, onBrowserLog: null, onLog: () => {}});
  await page.goto({url, timeout: 30000});
  let result;
  for (let i = 0; i < 300; i++) {
    result = await page.evaluate(() => window.studyResult ?? null);
    if (result) break;
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  if (!result) result = {error: 'timeout', text: await page.evaluate(() => document.body.innerText.slice(-2000))};
  mkdirSync(dirname(output), {recursive: true});
  writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify(result));
  if (result.error || result.failed || !result.total) process.exitCode = 1;
} finally {await browser.close({silent: true});}
