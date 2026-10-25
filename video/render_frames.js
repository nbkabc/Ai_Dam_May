// Render các khung hình từ file hoạt hình HTML. Chạy được trên Mac/Linux/Windows.
// Biến môi trường: ANIM, TIMELINE, OUT (thư mục), FROM, TO, FPS, CHROMIUM_PATH (không bắt buộc)
const path = require('path'), fs = require('fs');
function loadPlaywright() {
  const paths = [process.cwd(), __dirname, ...(process.env.NODE_PATH ? process.env.NODE_PATH.split(path.delimiter) : [])];
  for (const p of paths) { try { return require(require.resolve('playwright', { paths: [p] })); } catch (e) {} }
  console.error('Chưa cài playwright. Chạy: npm i playwright && npx playwright install chromium'); process.exit(2);
}
const { chromium } = loadPlaywright();
(async () => {
  const anim = path.resolve(__dirname, process.env.ANIM || 'anim2.html');
  const TL = JSON.parse(fs.readFileSync(path.resolve(__dirname, process.env.TIMELINE || 'timeline2.json'), 'utf8'));
  const out = process.env.OUT; fs.mkdirSync(out, { recursive: true });
  const fps = process.env.FPS ? +process.env.FPS : TL.fps, N = Math.round(fps * (process.env.DUR ? +process.env.DUR : TL.dur));
  const from = process.env.FROM ? +process.env.FROM : 0, to = process.env.TO ? +process.env.TO : N - 1;
  const opts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH, args: ['--no-sandbox'] } : { args: ['--no-sandbox'] };
  const br = await chromium.launch(opts), pg = await br.newPage({ viewport: { width: 1280, height: 720 } });
  await pg.addInitScript(`window.TL=${JSON.stringify(TL)}`); await pg.goto(require('url').pathToFileURL(anim).href);
  for (let f = from; f <= to; f++) {
    await pg.evaluate(t => window.draw(t), f / fps);
    await pg.screenshot({ path: path.join(out, `f_${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await br.close();
})();
