# Merge Quest

Number merge and game quest mash-up. Shoot numbered tiles up into columns; equal tiles that touch merge and double, chains make combos, and combos earn coins for helpers (Swap, Hammer, Undo).

Two modes, picked on the **home screen** (🏠 at the top left of the game returns there):

- **Levels**: 24 levels whose board grows from 2×2 to 5×7, teaching one idea at a time. Each level has a goal (make a tile, reach a score, make a combo, merge 3 or 4 at once, thin the board out, or survive), a shot limit and up to 3 stars. Levels 1–6 are scripted tutorials. New players start here.
- **Endless**: the original Merge Blaster game, with K/M tiers, ∞ blocks and the scoreboard.

Rewards: a 🔥 win streak (3 new levels in a row → start with a free Hammer, 5 → a free Swap too; a loss only drops it by 2), 🎁 chests on levels 10 and 20, and 🏅 one-time bounties for your first 2048, 4K, 4M and ∞.

See [docs/roadmap.md](docs/roadmap.md) for what's next.

## Play

Live: **https://polsiola-dot.github.io/merge-quest/** (installable as an app, works offline). Every push to `main` deploys automatically via GitHub Pages (`.github/workflows/pages.yml`). The older Netlify copy at play-merge-quest.netlify.app also deploys from `main` while the Netlify account has credits.

Open `index.html` in any browser. No build or install needed, and it works offline. When hosted (e.g. on Netlify, configured by `netlify.toml`) it can be installed as an app from the browser's **Add to Home Screen** or **Install app**.

Controls: tap a column (or ← → and Space / keys 1–5) to shoot; S switches the current and next tile; H hammer; U undo; N new game / restart level; M menu.

## Getting started on your computer

```
git clone https://github.com/polsiola-dot/merge-quest.git
cd merge-quest
npx serve .          # then open the address it prints
```

There's no build step: `index.html` is the whole game. Serving it (rather than opening the file) lets the service worker, install-as-app and offline mode work. Edit, refresh, and push to `main` to publish.

Need once, to run the test bots: `npm i -D playwright && npx playwright install chromium`.

### Putting it in the app stores (Phase 5)

The plan is to wrap this same web app with [Capacitor](https://capacitorjs.com/), keeping the browser version too. Rough steps, from the repo root:

```
npm init -y
npm i @capacitor/core @capacitor/cli @capacitor/android @capacitor/ios
npx cap init "Merge Quest" com.yourname.mergequest --web-dir=www
```

1. Capacitor wants the web files in one folder. Copy `index.html`, `sw.js`, `manifest.webmanifest`, the icon PNGs and `fonts/` into `www/` (the Pages workflow does the same into `_site/`; a small `npm run build` script that does this copy is enough).
2. `npx cap add android` and `npx cap add ios`, then after each change `npm run build && npx cap sync`.
3. Android: open with `npx cap open android` in **Android Studio**, build a signed app bundle (`.aab`) and upload it in the Google Play Console.
4. iOS: needs a **Mac with Xcode**. `npx cap open ios`, set your team and bundle id, archive, and upload through Xcode to App Store Connect / TestFlight.
5. Ads and purchases: add an AdMob plugin and an in-app-purchase plugin (both Capacitor plugins), plus the consent prompt, privacy policy and store forms listed in [docs/roadmap.md](docs/roadmap.md).
6. Pick the real app id (`com.yourname.mergequest` above is a placeholder). It can't be changed after you publish.

Accounts: Google Play Console ($25 one-off) and Apple Developer Program ($99 a year). Google may require a closed test with testers for about 14 days before production, so open the account early.

## Test bots

Both need Playwright and run headless Chromium.

- `node tools/sim.js [games] [maxMoves]` plays Endless games and reports moves, score, biggest tile, coins and any page errors.
- `node tools/levels.js [attempts] [first] [last]` plays each level many times and reports its win rate plus what the bot typically reaches (score, biggest tile, combo). Level goals were tuned so this simple greedy bot wins roughly 20–70% of random levels (a person planning ahead does better). Levels 1–6 must stay at 100%.

## Project layout

| Path | What |
| --- | --- |
| `index.html` | The whole game: HTML, CSS and JavaScript |
| `sw.js`, `manifest.webmanifest`, icons | Offline support and install-as-app |
| `.github/workflows/pages.yml`, `_headers`, `netlify.toml` | Hosting settings (GitHub Pages, Netlify) |
| `tools/sim.js`, `tools/levels.js` | Balance-testing bots (Endless, Levels) |
| `docs/roadmap.md` | Plan and design rules |
| `docs/art-prompts.md` | Image prompts for the final artwork |
| `fonts/` | Bundled Fredoka and Lilita One fonts |

## Credits

Fonts: [Fredoka](https://fonts.google.com/specimen/Fredoka) and [Lilita One](https://fonts.google.com/specimen/Lilita+One), both under the SIL Open Font License, bundled in `fonts/` so the game works offline.
