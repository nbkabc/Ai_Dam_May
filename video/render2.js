// node render.js <box|stick> <outDir> [fromFrame] [toFrame]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [style, out, a, b] = [process.argv[2], process.argv[3], process.argv[4], process.argv[5]];
  const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline2.json'), 'utf8'));
  fs.mkdirSync(out, { recursive: true });
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const pg = await br.newPage({ viewport: { width: 1280, height: 720 } });
  await pg.addInitScript(`window.TL=${JSON.stringify(TL)}`);
  await pg.goto('file://' + path.join(__dirname, 'anim2.html'));
  const N = TL.fps * TL.dur, from = a ? +a : 0, to = b ? +b : N - 1;
  for (let f = from; f <= to; f++) {
    await pg.evaluate(([t, s]) => window.draw(t, s), [f / TL.fps, style]);
    await pg.screenshot({ path: path.join(out, `f_${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await br.close();
})();
