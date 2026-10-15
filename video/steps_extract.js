// Trích thời điểm bước chân từ bộ xương. Dùng: node steps_extract.js steps.json
const path = require('path'), fs = require('fs');
function loadPlaywright() { const paths = [process.cwd(), __dirname, ...(process.env.NODE_PATH ? process.env.NODE_PATH.split(path.delimiter) : [])]; for (const p of paths) { try { return require(require.resolve('playwright', { paths: [p] })); } catch (e) {} } console.error('Chưa cài playwright'); process.exit(2); }
const { chromium } = loadPlaywright();
(async () => {
  const TL = JSON.parse(fs.readFileSync(path.resolve(__dirname, process.env.TIMELINE || 'timeline2.json'), 'utf8'));
  const opts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH, args: ['--no-sandbox'] } : { args: ['--no-sandbox'] };
  const br = await chromium.launch(opts), pg = await br.newPage();
  await pg.addInitScript(`window.TL=${JSON.stringify(TL)}`); await pg.goto('file://' + path.resolve(__dirname, process.env.ANIM || 'anim2.html'));
  const st = await pg.evaluate(() => window.stepTimes ? window.stepTimes() : []); fs.writeFileSync(process.argv[2], JSON.stringify(st)); console.log(st.length, 'bước chân'); await br.close();
})();
