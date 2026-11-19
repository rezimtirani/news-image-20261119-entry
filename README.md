# news-image-20261119-entry

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/rezimtirani/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/rezimtirani/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A single front page for Thursday 19 November 2026. The lead story is
the first Trump–Xi–Putin trilateral in China; around it, the Kerch
Bridge struck for the third time in a week, Hakeem Jeffries nominated
to become the first Black Speaker, Anthropic's record $81bn IPO,
Israeli tanks crossing the Gaza ceasefire line, and four more headlines
— Voyager 1, GTA VI, Cyclone Akvan and a record Van Gogh — with the
EU's €45bn Ukraine loan along the bottom.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
after checking it is a whole PNG no larger than 1024 by 1024 pixels
and 1 MiB. `main.py` uses only the Python standard library, needs no
network, and writes identical bytes on every run.

To redraw the image from its data, run the Pillow renderer:

```sh
python3 render.py
```

It reads `news.json` — the day's stories as reported on 19 November
2026 by Reuters, AP, BBC and Al Jazeera — and draws `entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
