const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const fs = require('fs'), path = require('path');
(async () => { const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline2.json'), 'utf8'));
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] }); const pg = await br.newPage();
  await pg.addInitScript(`window.TL=${JSON.stringify(TL)}`); await pg.goto('file://' + path.join(__dirname, 'anim2.html'));
  const st = await pg.evaluate(() => window.stepTimes()); fs.writeFileSync(process.argv[2], JSON.stringify(st)); console.log(st.length, 'bước chân'); await br.close(); })();
