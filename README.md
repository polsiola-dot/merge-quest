# Merge Quest

Number merge and game quest mash-up. Shoot numbered tiles up into columns; equal tiles that touch merge and double, chains make combos, and combos earn coins for helpers (Swap, Hammer, Undo).

This repository starts from the **Merge Blaster** endless game, which becomes Merge Quest's **Endless mode**. Next comes a level-based mode with growing boards, tutorial levels, stars and rewards, then a light story layer. See [docs/roadmap.md](docs/roadmap.md).

## Play

Open `index.html` in any browser. No build or install needed, and it works offline. When hosted (e.g. on Netlify, configured by `netlify.toml`) it can be installed as an app from the browser's **Add to Home Screen** or **Install app**.

Controls: tap a column (or ← → and Space / keys 1–5) to shoot; S switches the current and next tile; H hammer; U undo; N new game.

## Test bot

`node tools/sim.js [games] [maxMoves]` plays games in headless Chromium (needs Playwright) and reports moves, score, biggest tile, coins and any page errors. Use it to check balance after changing rules.

## Project layout

| Path | What |
| --- | --- |
| `index.html` | The whole game: HTML, CSS and JavaScript |
| `sw.js`, `manifest.webmanifest`, icons | Offline support and install-as-app |
| `_headers`, `netlify.toml` | Hosting settings |
| `tools/sim.js` | Balance-testing bot |
| `docs/roadmap.md` | Plan and design rules |
