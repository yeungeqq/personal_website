// Optional live-browser checks using Node 22+ and a local Chrome debugging port.
// No npm dependencies. See README for the browser/server prerequisites.
import assert from 'node:assert/strict';
import { writeFile, mkdir } from 'node:fs/promises';

const origin = process.env.SITE_URL || 'http://127.0.0.1:8765/personal_website/';
const debugging = process.env.CHROME_DEBUG_URL || 'http://127.0.0.1:9223';
const targets = await (await fetch(`${debugging}/json`)).json();
const target = targets.find((item) => item.type === 'page');
assert(target, 'Start a local Chrome debugging session first');
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener('open', resolve, { once: true });
  socket.addEventListener('error', reject, { once: true });
});
let sequence = 0;
const pending = new Map();
const errors = [];
socket.addEventListener('message', ({ data }) => {
  const message = JSON.parse(data);
  if (message.id) {
    const call = pending.get(message.id);
    if (!call) return;
    clearTimeout(call.timer);
    pending.delete(message.id);
    if (message.error) call.reject(new Error(JSON.stringify(message.error)));
    else call.resolve(message.result);
  } else if (message.method === 'Runtime.exceptionThrown') {
    errors.push(message.params.exceptionDetails.text);
  } else if (message.method === 'Network.responseReceived' && message.params.response.status >= 400) {
    errors.push(`${message.params.response.status}: ${message.params.response.url}`);
  }
});
function send(method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = ++sequence;
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new Error(`Timed out: ${method}`));
    }, 12000);
    pending.set(id, { resolve, reject, timer });
    socket.send(JSON.stringify({ id, method, params }));
  });
}
async function evaluate(expression) {
  const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  assert(!result.exceptionDetails, JSON.stringify(result.exceptionDetails));
  return result.result.value;
}
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function visit(path = '') {
  await send('Page.navigate', { url: origin + path });
  for (let i = 0; i < 60; i++) {
    await sleep(100);
    if (await evaluate(`location.href === ${JSON.stringify(origin + path)} && document.readyState === 'complete'`)) return;
  }
  throw new Error(`Page did not load: ${path}`);
}
async function viewport(width, height) {
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
}
async function noOverflow() {
  assert(await evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow');
  assert(await evaluate('[...document.images].every(image => image.complete && image.naturalWidth > 0)'), 'Broken image');
}
async function screenshot(name) {
  const image = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  await writeFile(new URL(`../.local/${name}.png`, import.meta.url), Buffer.from(image.data, 'base64'));
}

try {
  await mkdir(new URL('../.local/', import.meta.url), { recursive: true });
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Network.enable');
  await viewport(1440, 1000);
  await visit();
  await noOverflow();
  await screenshot('desktop');
  assert.equal(await evaluate('document.querySelectorAll("[data-project-card]").length'), 8);
  for (const [category, count] of [['full-stack', 3], ['machine-learning', 3], ['game-ai', 2], ['all', 8]]) {
    await evaluate(`document.querySelector('button[data-category="${category}"]').click()`);
    assert.equal(await evaluate('[...document.querySelectorAll("[data-project-card]")].filter(card => !card.hidden).length'), count);
    assert.equal(await evaluate(`document.querySelector('button[data-category="${category}"]').getAttribute('aria-pressed')`), 'true');
  }
  // The first keyboard stop should expose the skip link.
  await visit();
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  assert.equal(await evaluate('document.activeElement.className'), 'skip-link');
  for (const width of [768, 390, 320]) {
    await viewport(width, 844);
    await noOverflow();
  }
  await viewport(390, 844);
  await screenshot('mobile');
  assert.equal(await evaluate('getComputedStyle(document.querySelector("#site-navigation")).display'), 'none');
  await evaluate('document.querySelector("[data-menu-toggle]").click()');
  assert.equal(await evaluate('document.querySelector("[data-menu-toggle]").getAttribute("aria-expanded")'), 'true');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
  assert.equal(await evaluate('document.querySelector("[data-menu-toggle]").getAttribute("aria-expanded")'), 'false');
  assert(await evaluate('document.activeElement.matches("[data-menu-toggle]")'));
  await evaluate('document.querySelector("[data-menu-toggle]").click(); document.querySelector("#site-navigation a").click()');
  assert.equal(await evaluate('document.querySelector("[data-menu-toggle]").getAttribute("aria-expanded")'), 'false');
  const paths = await evaluate('[...document.querySelectorAll("[data-project-card] h3 a")].map(a => a.getAttribute("href").replace("./", ""))');
  for (const path of paths) {
    await visit(path);
    await noOverflow();
    assert.equal(await evaluate('document.querySelectorAll("h1").length'), 1);
    await viewport(1440, 1000);
    await noOverflow();
    if (path.includes('cortexdocs')) await screenshot('project-detail');
    await viewport(390, 844);
  }
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  assert.equal(await evaluate('getComputedStyle(document.documentElement).scrollBehavior'), 'auto');
  await send('Emulation.setScriptExecutionDisabled', { value: true });
  await visit();
  assert.equal(await evaluate('document.querySelectorAll("[data-project-card]:not([hidden])").length'), 8);
  assert.notEqual(await evaluate('getComputedStyle(document.querySelector("#site-navigation")).display'), 'none');
  assert(await evaluate('document.querySelector("[data-filters]").hidden'));
  await noOverflow();
  assert.deepEqual(errors, [], 'Browser exceptions or failed HTTP responses');
  console.log('PASS: desktop/tablet/mobile layouts; images; four filters; keyboard skip link; mobile menu and Escape; eight direct detail URLs; reduced motion; no-JavaScript navigation/content; no browser exceptions or HTTP errors.');
} finally {
  await send('Emulation.setScriptExecutionDisabled', { value: false });
  await send('Emulation.setEmulatedMedia', { features: [] });
  socket.close();
}