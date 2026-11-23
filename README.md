# Merge Quest

Number merge and game quest mash-up. Shoot numbered tiles up into columns; equal tiles that touch merge and double, chains make combos, and combos earn coins for helpers (Swap, Hammer, Undo).

Two modes (switch from **Menu**):

- **Levels**: 24 levels whose board grows from 2×2 to 5×7, teaching one idea at a time. Each level has a goal (make a tile, reach a score, make a combo, merge 3 or 4 at once, thin the board out, or survive), a shot limit and up to 3 stars. Levels 1–6 are scripted tutorials. New players start here.
- **Endless**: the original Merge Blaster game, with K/M tiers, ∞ blocks and the scoreboard.

See [docs/roadmap.md](docs/roadmap.md) for what's next.

## Play

Open `index.html` in any browser. No build or install needed, and it works offline. When hosted (e.g. on Netlify, configured by `netlify.toml`) it can be installed as an app from the browser's **Add to Home Screen** or **Install app**.

Controls: tap a column (or ← → and Space / keys 1–5) to shoot; S switches the current and next tile; H hammer; U undo; N new game / restart level; M menu.

## Test bots

Both need Playwright and run headless Chromium.

- `node tools/sim.js [games] [maxMoves]` plays Endless games and reports moves, score, biggest tile, coins and any page errors.
- `node tools/levels.js [attempts] [first] [last]` plays each level many times and reports its win rate plus what the bot typically reaches (score, biggest tile, combo). Level goals were tuned so this simple greedy bot wins roughly 20–70% of random levels (a person planning ahead does better). Levels 1–6 must stay at 100%.

## Project layout

| Path | What |
| --- | --- |
| `index.html` | The whole game: HTML, CSS and JavaScript |
| `sw.js`, `manifest.webmanifest`, icons | Offline support and install-as-app |
| `_headers`, `netlify.toml` | Hosting settings |
| `tools/sim.js`, `tools/levels.js` | Balance-testing bots (Endless, Levels) |
| `docs/roadmap.md` | Plan and design rules |
