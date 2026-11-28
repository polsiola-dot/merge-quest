# Sound effect prompts (ElevenLabs Sound Effects)

The game already plays code-made placeholders for every sound below. Each real
file you add replaces its placeholder with no code changes (see "Adding them to
the game" at the end).

## Settings for every sound
- **Duration:** set it by hand to the length given (auto tends to run long). 0.5 s is the minimum.
- **Prompt influence:** about **0.6**, so it sticks to the description.
- **Loop:** off.
- Generate **4 variations** of each and keep the best. Listen on your phone speaker, not just headphones.
- Keep the same "house style" words in every prompt so the set sounds like one game. They're already included below:
  *"cartoony mobile puzzle game, bright and clean, dry with no reverb tail, no background noise, no music, no voice"*.

## Step 1: the 8 sounds already in the game (do these first)

| # | File | Duration | Prompt |
| --- | --- | --- | --- |
| 1 | `land.mp3` | 0.5 s | A soft, short wooden "tok" of a small rounded block landing on a wooden board, gentle and satisfying, very short, cartoony mobile puzzle game, bright and clean, dry with no reverb tail, no background noise, no music, no voice |
| 2 | `merge.mp3` | 0.6 s | A playful bubble pop instantly followed by a single warm marimba note (middle C), two blocks squishing together into one, cheerful and rewarding, cartoony mobile puzzle game, bright and clean, dry with no reverb tail, no background noise, no music, no voice |
| 3 | `gulp.mp3` | 0.5 s | A tiny cute "gloop" slurp of a jelly block being sucked into another, short and bouncy, rising slightly in pitch, cartoony mobile puzzle game, bright and clean, dry with no reverb tail, no background noise, no music, no voice |
| 4 | `big.mp3` | 1.5 s | A short triumphant fanfare of bright brass and glockenspiel, four quick rising notes ending on a sparkling shimmer, celebrating a huge achievement, cartoony mobile puzzle game, bright and clean, short tail, no background noise, no voice |
| 5 | `win.mp3` | 2.5 s | A cheerful level-complete jingle, bouncy pizzicato strings and marimba playing a quick happy rising melody in C major, ending on a bright glockenspiel chord with sparkles, cartoony mobile puzzle game, polished and joyful, no background noise, no voice |
| 6 | `lose.mp3` | 1.5 s | A gentle, friendly "aww" fail sound, three soft descending pizzicato notes ending in a slow downward slide, sad but cute and not harsh, cartoony mobile puzzle game, clean, no background noise, no voice |
| 7 | `coin.mp3` | 0.5 s | A single bright gold coin "ching", a light metallic clink with a tiny sparkle, short and crisp, cartoony mobile game reward, clean, dry with no reverb tail, no background noise, no music, no voice |
| 8 | `tap.mp3` | 0.5 s | A very soft, short UI button tap, a gentle rounded "pop" click like pressing a squishy rubber button, quiet and subtle, mobile game menu, clean, dry with no reverb tail, no background noise, no music, no voice |

**Notes for step 1**
- **Merge and gulp pitch:** the game raises their pitch for bigger tiles and longer chains, so generate them at a **middle** pitch (a single mid note, not a chord or a melody). If a take already rises or falls, pick another.
- **Win:** the music dips under it automatically, so it doesn't need to be loud.
- **Coin:** it plays up to 12 times in a quick row, so pick the shortest, cleanest take.
- **Land:** you'll hear this one most, so choose the softest take that still feels satisfying.

## Step 3: the rest of the plan (later)

| File | Duration | Prompt |
| --- | --- | --- |
| `open.mp3` | 0.5 s | A soft quick "whoosh-pop" of a cartoon card panel springing open, light and airy, mobile game menu, clean, dry, no background noise, no music, no voice |
| `close.mp3` | 0.5 s | A soft quick reverse "whoosh" of a cartoon card panel closing, lighter and quieter than an opening sound, mobile game menu, clean, dry, no background noise, no music, no voice |
| `crack.mp3` | 0.7 s | A small cartoon stone block cracking, a crisp rocky "crack" followed by a few tiny pebbles crumbling, satisfying, mobile puzzle game, clean, dry, no background noise, no music, no voice |
| `thaw.mp3` | 0.8 s | A small ice cube cracking and melting, a crystalline "tink-crack" followed by a short sparkly drip, cartoony mobile puzzle game, clean, dry, no background noise, no music, no voice |
| `snow.mp3` | 0.6 s | A soft cartoon "whump" of a snowy ice block dropping onto a board from above, muffled and gentle, mobile puzzle game, clean, dry, no background noise, no music, no voice |
| `hammer.mp3` | 0.6 s | A chunky cartoon wooden mallet "thunk" smashing a small block, punchy but friendly, mobile puzzle game power-up, clean, dry, no background noise, no music, no voice |
| `swap.mp3` | 0.5 s | A quick playful "swish-swoosh" of two objects trading places, light and bouncy, mobile puzzle game, clean, dry, no background noise, no music, no voice |
| `undo.mp3` | 0.6 s | A short cartoon "rewind" sound, a quick reversed whoosh with a little tape-rewind wobble, mobile puzzle game power-up, clean, dry, no background noise, no music, no voice |
| `wild.mp3` | 0.8 s | A magical sparkle burst, twinkling chimes swirling upward, a rainbow wild card appearing, cartoony mobile puzzle game power-up, clean, short tail, no background noise, no voice |
| `heater.mp3` | 0.8 s | A warm cartoon fire "whoomp" with a gentle sizzle, cozy rather than scary, mobile puzzle game power-up melting ice, clean, short tail, no background noise, no music, no voice |
| `bonk.mp3` | 0.5 s | A dull, soft cartoon "bonk" of tapping a locked button, muted and slightly comic, mobile game, clean, dry, no background noise, no music, no voice |
| `buy.mp3` | 0.8 s | A cheerful cartoon cash register "ka-ching" with a coin sparkle, shop purchase, mobile game, clean, short tail, no background noise, no music, no voice |
| `equip.mp3` | 0.6 s | A soft magical shimmer, a few gentle chime twinkles, putting on a new cosmetic item, mobile game, clean, short tail, no background noise, no music, no voice |
| `chest.mp3` | 1.5 s | A wooden treasure chest creaking open followed by a bright golden treasure shimmer and a few coins jingling, exciting reward, cartoony mobile game, clean, no background noise, no music, no voice |
| `milestone.mp3` | 1.2 s | A short bright rising arpeggio on glockenspiel and marimba, an achievement unlocked, cartoony mobile game, clean, short sparkle tail, no background noise, no voice |
| `tick.mp3` | 0.5 s | A soft single heartbeat-like low "thump" tick, gentle tension for the last few moves, mobile puzzle game, clean, dry, no background noise, no music, no voice |

## Tidying each file
1. **Trim** the silence at the start (the sound must begin instantly) and any long tail, in Audacity or ElevenLabs' own trimmer.
2. **Mono, MP3 at 96–128 kbps.** That's about 10–20 KB per sound.
3. **Even loudness:** normalise each to the same peak (about −3 dB). Then play a level and adjust any that stand out; `land` and `tap` should sit quieter (about −9 dB).
4. Check the plan you're on allows **commercial use** before the store release.

## Adding them to the game
1. Put the files in the `sfx/` folder.
2. List them in `sfx/index.json`, for example:
   ```json
   { "land": "land.mp3", "merge": "merge.mp3", "gulp": "gulp.mp3", "big": "big.mp3",
     "win": "win.mp3", "lose": "lose.mp3", "coin": "coin.mp3", "tap": "tap.mp3" }
   ```
3. Any sound not listed keeps its placeholder, so you can add them one at a time.

The step 3 sounds also need a line of code each to trigger them. Send them over when you have them and I'll wire them in.
