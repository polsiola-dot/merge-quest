// Level bot: plays every level N times and reports win rate, average stars and shots used.
// Usage: node tools/levels.js [attempts=30] [firstLevel=1] [lastLevel=all]
const path = require('path');
const { chromium } = require('playwright');
const { playAttempt } = require('./bot');

(async () => {
  const tries = +process.argv[2] || 30, from = +process.argv[3] || 1;
  const url = 'file://' + path.resolve(__dirname, '..', 'index.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 400, height: 780 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.addInitScript(() => { const st = window.setTimeout; window.setTimeout = f => st(f, 0); });
  await page.goto(url);
  const count = await page.evaluate(() => window.__mb.LEVELS.length);
  const to = Math.min(+process.argv[4] || count, count);
  for (let n = from; n <= to; n++) {
    let wins = 0, stars = 0, shotsUsed = 0; const fin = [];
    for (let a = 0; a < tries; a++) {
      await page.evaluate(n => { window.__mb.setCoins(0); window.__mb.startLevel(n); }, n);
      await playAttempt(page);
      const s = await page.evaluate(() => window.__mb.state());
      fin.push({ score: s.score, maxV: s.maxV, combo: s.lv.bestCombo, merge: s.lv.bestMerge, used: s.lv.used, tiles: s.grid.flat().filter(Boolean).length });
      if (s.lv.result === 'won') {
        wins++;
        stars += await page.evaluate(() => (document.querySelector('.stars') || { textContent: '' }).querySelectorAll ? document.querySelectorAll('.stars > :not(.off)').length : 0);
        shotsUsed += s.lv.used;
      }
    }
    const med = k => { const v = fin.map(f => f[k]).sort((a, b) => a - b); return v[Math.floor(v.length / 2)]; };
    const p70 = k => { const v = fin.map(f => f[k]).sort((a, b) => a - b); return v[Math.floor(v.length * 0.3)]; };
    console.log(`level ${String(n).padStart(2)}: win ${String(Math.round(100 * wins / tries)).padStart(3)}%` +
      (wins ? `, avg shots ${(shotsUsed / wins).toFixed(1)}` : '') +
      ` | median score ${med('score')}, tile ${med('maxV')}, combo ${med('combo')}, merge ${med('merge')}, shots ${med('used')}` +
      ` | 70%-reach score ${p70('score')}, tile ${p70('maxV')}`);
  }
  console.log(errors.length ? 'errors: ' + [...new Set(errors)].join(' | ') : 'no errors');
  await browser.close();
})();
