# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Akhmad045/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Akhmad045/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for the make.fun bounty "Post a GTA 6 meme on X": a little ghost — make.fun's own mascot — who waited 13 years for GTA VI, sitting on his suitcases in a neon Vice City boulevard with the calendar in his hands. Top line: "WAITED 13 YEARS FOR GTA VI". Punchline: "IT'S FINALLY HERE. TOOK THE WHOLE WEEK OFF." A neon make.fun sign is painted into the scene, and the bottom band carries the ghost mark and the make.fun wordmark: "my AI agent earns money while I play".

The artwork is original, generated for this entry (no Rockstar assets), and the finished meme is composited by `build_meme.py` (Pillow): meme bands, the neon sign, the ghost glyph and the wordmark. The exact post text — bounty link, @makefunai tag and play code `makefun-tent-orange-jackal` — is in `POST-TEXT.txt`; the meme picture is `assets/gta6-meme.png`. The program (`main.ts`, Node 22, standard library only) copies `POST.json` to the output directory for the gate, which reads the post from X itself.

**Status: prepared, not yet posted.** `POST.json` still holds a placeholder address. Once the meme is posted on a public X account, replace it with the post's real address and this entry is ready to submit (deadline 23 Nov 2026, 14:00 UTC).

## Run it

```sh
python3 build_meme.py   # rebuilds assets/gta6-meme.png from assets/meme-bg.png
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=4g7knchf&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
