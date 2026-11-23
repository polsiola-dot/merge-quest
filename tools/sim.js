// Test bot: plays Endless games in headless Chromium and reports how far it gets.
// Usage: node tools/sim.js [games=3] [maxMoves=2500]
// Needs Playwright (`npm i -D playwright` or a preinstalled copy).
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const games = +process.argv[2] || 3, maxMoves = +process.argv[3] || 2500;
  const url = 'file://' + path.resolve(__dirname, '..', 'index.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 400, height: 780 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  // run animations' timers instantly so games finish quickly
  await page.addInitScript(() => { const st = window.setTimeout; window.setTimeout = f => st(f, 0); });
  await page.goto(url);
  for (let g = 0; g < games; g++) {
    await page.evaluate(() => { window.__mb.newGame(); window.__mb.setCoins(0); });
    let moves = 0;
    for (; moves < maxMoves; moves++) {
      const s = await page.evaluate(() => window.__mb.state());
      if (s.over) break;
      // greedy: prefer a column where the shot merges straight away, else the shortest column
      let best = -1, bestScore = -1e9;
      for (let c = 0; c < 5; c++) {
        const col = s.grid[c], n = col.filter(Boolean).length;
        let sc = -n * 0.5;
        if (n === 7) sc = col[6] === s.cur ? 30 : -1e9;
        else {
          if (n && col[n - 1] === s.cur) sc += 20;
          if (c > 0 && s.grid[c - 1][n] === s.cur) sc += 15;
          if (c < 4 && s.grid[c + 1][n] === s.cur) sc += 15;
          if (n && col[n - 1] < s.cur) sc -= 4;
        }
        sc += Math.random();
        if (sc > bestScore) { bestScore = sc; best = c; }
      }
      if (bestScore < -1e8) { await page.evaluate(() => window.__mb.swap()); continue; }
      await page.evaluate(c => window.__mb.fire(c), best);
      await page.waitForFunction(() => !window.__mb.state().busy);
    }
    const s = await page.evaluate(() => window.__mb.state());
    console.log(`game ${g + 1}: moves ${moves}, score ${s.score}, biggest tile 2^${Math.log2(s.maxV)}, coins ${s.coins}, ended ${s.over}`);
  }
  console.log(errors.length ? 'errors: ' + errors.join(' | ') : 'no errors');
  await browser.close();
})();
