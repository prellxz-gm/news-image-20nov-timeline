# The World in One Day — Friday 20 November 2026

**Variant C — "Timeline + Proof"** for the make.fun bounty
[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120).

A 1024×1024 front page drawn entirely with PIL (no AI-generated image):
all 41 verified stories from Friday 20 November 2026, each with a short
outlet attribution and region colour-coding, on a UTC timeline spine.

- **Masthead:** THE WORLD IN ONE DAY — FRIDAY 20 NOVEMBER 2026
- **Date-check box:** "Every event verified — Friday 20 November 2026"
- **Three drawn lead panels:** Russia's 110-missile barrage on Kyiv,
  Cyclone Akvan's landfall on India's east coast, and the COP31 final-day
  deadlock in Antalya.
- **Story grid:** 38 further stories across 7 regions (Asia 14, Europe 9,
  Oceania 6, Latin America 4, North America 3, Africa 3, Middle East 2),
  with a small world-map inset.

Every story was verified against a live source for the 20 November 2026
date; misdated items (e.g. the 19 November GTA VI sales figures, the
US sanctions story, the APEC declaration) are excluded.

## Run

`main.py` is a pure-stdlib byte relay: it copies the committed `entry.png`
into `$MAKEFUN_OUTPUT_DIR`. It runs identically twice with no network.

```sh
MAKEFUN_OUTPUT_DIR=./output python3 -S main.py
```

`draw.py` is the build-time script that renders `entry.png` (requires PIL
and the DejaVu fonts); it is not used at grade time.
