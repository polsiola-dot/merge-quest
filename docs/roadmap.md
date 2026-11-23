# Merge Quest roadmap

Build a level mode on the existing engine first, with small boards that grow from 2×2 to 5×7 and teach one idea at a time. Add a light story layer only once the levels are fun. The full research and plan live in the "Merge Blaster Roadmap" doc.

| Phase | What | Gate to move on |
| --- | --- | --- |
| Now | Endless quick wins: bag randomiser, ∞ pays coins, two-tile preview, free rescue *(done)* | none |
| 1 | **Level mode MVP** *(built, now in playtesting)*: variable board size, 24 teaching levels, goals + shot limits + 1–3 stars, level map, free helper samples | Bot wins levels 1–6 every time; a new player finishes 1–12 without help |
| 2 | Rewards: win-streak ladder, chest every 10 levels, milestone bounties | Players replay levels for 3 stars |
| 3 | Variety: one new blocker per world, daily challenge, skins as coin sinks | New worlds still feel fresh |
| 4 | Story: spend stars to restore an illustrated scene, one caption at a time | none |

## Design rules from the research

- One new idea per level; levels 1–6 use a fixed tile queue and can't be lost.
- Limit shots, not time. Difficulty is a sawtooth: a Hard level about every 10, then an easy one.
- 2×2 only works with scripted tiles; random tiles start at 3×3. "Clear all blocks" is impossible, so use "leave ≤ N blocks".
- Each helper is introduced with free uses before it costs coins.
- Never: lives or energy timers, piggy banks, loot boxes, streaks that reset to zero, guilt notifications.
