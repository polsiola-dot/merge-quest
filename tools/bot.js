// Shared greedy player for the test bots. Plays the current Level/Daily attempt
// to the end: shoots where the tile merges, avoids burying small tiles, switches
// tiles when the current one fits nowhere. Returns the final state.
async function playAttempt(page) {
  for (let m = 0; m < 400; m++) {
    const s = await page.evaluate(() => window.__mb.state());
    if (s.lv.result) break;
    const cols = s.cols, rows = s.rows;
    let best = -1, bestScore = -1e9;
    for (let c = 0; c < cols; c++) {
      const col = s.grid[c], k = col.filter(Boolean).length;
      let sc = -k * 0.5;
      if (k === rows) sc = col[rows - 1] === s.cur ? 30 : -1e9;
      else {
        if (k && col[k - 1] === s.cur) sc += 20;
        if (c > 0 && s.grid[c - 1][k] === s.cur) sc += 15;
        if (c < cols - 1 && s.grid[c + 1][k] === s.cur) sc += 15;
        if (k && col[k - 1] < s.cur) sc -= 4;
      }
      sc += Math.random();
      if (sc > bestScore) { bestScore = sc; best = c; }
    }
    if (bestScore < -1e8) {
      const sw = await page.evaluate(() => { const before = window.__mb.state().cur; window.__mb.swap(); return window.__mb.state().cur !== before; });
      if (!sw) break;
      continue;
    }
    await page.evaluate(c => window.__mb.fire(c), best);
    await page.waitForFunction(() => !window.__mb.state().busy);
  }
  const s = await page.evaluate(() => window.__mb.state());
  return { ...s, result: s.lv.result };
}
module.exports = { playAttempt };
