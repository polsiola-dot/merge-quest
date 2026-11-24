// Daily bot: plays the daily challenge for a run of days and reports each day's goal and win rate.
// Usage: node tools/daily.js [attempts=20] [days=14] [startDate=today, YYYY-MM-DD]
const path = require('path');
const { chromium } = require('playwright');
const { playAttempt } = require('./bot');

(async () => {
  const tries = +process.argv[2] || 20, days = +process.argv[3] || 14;
  const start = process.argv[4] ? new Date(process.argv[4] + 'T12:00:00') : new Date();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 400, height: 780 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.addInitScript(() => { const st = window.setTimeout; window.setTimeout = f => st(f, 0); });
  await page.goto('file://' + path.resolve(__dirname, '..', 'index.html'));
  const byGoal = {};
  for (let d = 0; d < days; d++) {
    const date = new Date(start.getTime() + d * 864e5);
    const key = await page.evaluate(t => window.__mb.todayKey(new Date(t)), date.getTime());
    const L = await page.evaluate(k => window.__mb.dailyDef(k), key);
    let wins = 0;
    for (let a = 0; a < tries; a++) {
      await page.evaluate(k => { window.__mb.setCoins(0); window.__mb.startDaily(k); }, key);
      if ((await playAttempt(page)).result === 'won') wins++;
    }
    const g = L.goal.join(' ');
    (byGoal[g] = byGoal[g] || []).push(wins / tries);
    const stones = L.start.flat().filter(v => v < 0).length;
    console.log(`${key}: ${g.padEnd(10)} ${L.cols}x${L.rows}, ${L.shots} shots, ${stones} stones -> win ${Math.round(100 * wins / tries)}%`);
  }
  console.log('\nby goal:');
  for (const [g, r] of Object.entries(byGoal)) console.log(`  ${g.padEnd(10)} avg win ${Math.round(100 * r.reduce((a, b) => a + b) / r.length)}% over ${r.length} day(s)`);
  console.log(errors.length ? 'errors: ' + [...new Set(errors)].join(' | ') : 'no errors');
  await browser.close();
})();
