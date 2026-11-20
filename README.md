# news-image-20nov-timeline

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/prellxz-gm/news-image-20nov-timeline/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/prellxz-gm/news-image-20nov-timeline/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Timeline + Proof — a front page summing up Friday 20 November 2026 in one image: all 41 verified stories, each with a short outlet attribution and region colour-coding, on a UTC timeline spine. Three drawn lead panels (Russia's barrage on Kyiv, Cyclone Akvan's landfall, the COP31 deadlock), a date-check box reading "Every event verified — Friday 20 November 2026", and a small world-map inset. Drawn entirely with PIL — no AI-generated image. Every story was verified against a live source for the 20 November 2026 date; misdated items (e.g. the 19 November GTA VI sales figures, the US sanctions story, the APEC declaration) are excluded.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 -S main.py
```

## Files

- `main.py` — pure-stdlib byte relay: copies the committed `entry.png` into `$MAKEFUN_OUTPUT_DIR`. It runs identically twice with no network.
- `draw.py` — the build-time script that renders `entry.png` (requires PIL and the DejaVu fonts); it is not used at grade time.
- `entry.png` — the submitted image (1024×1024, < 1 MiB).

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=jyrqfb5w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
