// Render del estilo ilustrado con Playwright (Chromium).
// node render.mjs <carpeta> stills 1,2,3        -> stills/t_XX.XX.jpg (control) + errores de consola
// node render.mjs <carpeta> thumb               -> out/miniatura.png (portada, 1280x720)
// node render.mjs <carpeta> events              -> events.json (sonidos) y cantidad de cuadros
// node render.mjs <carpeta> frames <W> [desde] [hasta] -> frames/fNNNNN.jpg del tramo (hasta excluido)
// node render.mjs <carpeta> encode [fps]        -> out/video_mudo.mp4 a partir de frames/
// Viewport: window.VW / window.VH de la página (largos 1920x1080).
const { chromium } = await import(process.env.PW || 'playwright');
import fs from 'fs'; import { execFileSync } from 'child_process';
const [src, mode, a1, a2, a3] = process.argv.slice(2);
const FPS = +(process.env.FPS || 24);
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
async function page(q = '') {
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } }); const errs = [];
  pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto(`file://${src}/index.html${q}`); await pg.waitForFunction('window.READY===true', null, { timeout: 60000 });
  return [pg, errs];
}
async function events() {
  const [pg, errs] = await page(); const dur = await pg.evaluate('window.DUR'); const ev = await pg.evaluate('window.EV');
  fs.writeFileSync(`${src}/events.json`, JSON.stringify({ dur, ev })); await pg.close();
  const n = Math.floor(dur * FPS); console.log('duracion', dur, 'cuadros', n, 'eventos', ev.length, 'errores', errs.slice(0, 3)); return n;
}
async function frames(W, from, to) {
  fs.mkdirSync(`${src}/frames`, { recursive: true });
  const res = await Promise.all([...Array(W).keys()].map(async w => { const [pg, e] = await page();
    for (let i = from + w; i < to; i += W) { const f = `${src}/frames/f${String(i).padStart(5, '0')}.jpg`; if (fs.existsSync(f)) continue;
      await pg.evaluate(`render(${i / FPS})`);
      await pg.screenshot({ path: f, type: 'jpeg', quality: 92 }); }
    return e; }));
  console.log('errores', res.flat().slice(0, 5), 'tramo', from, to);
}
function encode() {
  fs.mkdirSync(`${src}/out`, { recursive: true });
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', `${src}/frames/f%05d.jpg`,
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', `${src}/out/video_mudo.mp4`]);
  console.log('listo out/video_mudo.mp4');
}
if (mode === 'stills') { fs.mkdirSync(`${src}/stills`, { recursive: true }); const [pg, errs] = await page();
  for (const t of a1.split(',').map(Number)) { await pg.evaluate(`render(${t})`);
    await pg.screenshot({ path: `${src}/stills/t_${t.toFixed(2).padStart(7, '0')}.jpg`, type: 'jpeg', quality: 80 }); }
  console.log('errores', errs.slice(0, 5));
} else if (mode === 'thumb') { fs.mkdirSync(`${src}/out`, { recursive: true }); const [pg, errs] = await page('?thumb=1');
  await pg.evaluate('render(0)'); await pg.screenshot({ path: `${src}/out/cover1920.png` });
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', `${src}/out/cover1920.png`, '-vf', 'scale=1280:720:flags=lanczos', `${src}/out/miniatura.png`]);
  console.log('miniatura lista', errs.slice(0, 3));
} else if (mode === 'events') { await events();
} else if (mode === 'frames') { await frames(+a1, +a2, +a3);
} else if (mode === 'encode') { encode(); }
await b.close();
