# Home-screen cast in Rive (prototype)

The four home-screen buddies rebuilt as a Rive file, with the same personalities
as the in-game code version:

| Buddy | Idle | Blinks | Signature move (auto, or tap it) |
| --- | --- | --- | --- |
| 2, curious | quick bob, pupils dart around | fast, some doubles | hop and head tilt |
| 4, sleepy | slow lazy bob, half-closed eyes | slow and heavy | big yawn, or dozes off with z's and startles awake (random on tap) |
| Purple, cheerful | dance bob, arms sway | normal, sometimes a wink | double jump, arms pump, sparkles |
| 8, determined | steady bob, slanted eyes | rare, quick snaps | squints, shakes, squash-and-stretch power-up with a glow |

## How it's put together
- **Artboard `HomeCast`** (800×600) and one state machine, **`Home cast`**.
- Each buddy has a **bob** layer and a **blinks** layer, each looping at its own
  length (blink loops of 19.3, 23.9, 19.9 and 22.1 s), so they never fall into step.
- **`auto moves`** is a 60-second loop that plays one signature move at a time,
  at irregular gaps, with a neighbour glancing over.
- **Tap layers** (one per buddy): a pointer-down on the buddy's body fires the
  trigger `tap two` / `tap four` / `tap purple` / `tap eight`, which plays its move once.
- Parts the moves need are separate nodes: `*_act` (body moves), `*_lidL/R` (blinks)
  with `*_lidLs/Rs` inside (move-driven lids), `*_pupL/R` and `*_pupLs/Rs` (looks),
  `purple_armL/R` (sway) with `armLs/Rs` (pump), plus `eight_aura`, `four_zz`,
  `four_yawn` and `purple_spark0-2`.

## Use it
```bash
rive .                 # live preview window; click the buddies
rive . --publish       # writes build/home-cast.riv (needs `rive login`)
```

## Changing it
`scene.rml` is generated. Edit `tools/gen_svg.py` (the drawing) or
`tools/build.py` (timings, moves, state machine), then run `tools/rebuild.sh`
(needs `pip install fonttools brotli`). Once you start polishing in the Rive
Editor instead (`rive push`), stop regenerating, or you'll overwrite that work.
