# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/stfu-onad/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/stfu-onad/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up Wednesday 18 November 2026: a newspaper front page,
**THE WORLD TODAY**. The lead story is Nvidia's blowout quarter — $115.8B in
revenue with guidance up to $130B, the company's first report since Jensen
Huang stepped down, with an SEC probe now open. Below it, two photo panels:
a US carrier group in the Gulf as Hormuz tensions simmer, and President
Trump's Asia tour rolling on from Manila toward talks with Xi and Putin. The
"Also Today" strip rounds out the day — the ASX's steepest fall in six weeks,
David Jones owing $458M, Nvidia shares rising after hours, US curbs on AI-chip
access for China, Kerch Bridge strikes, and the UN meeting on an
autonomous-weapons ban.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This copies `entry.png` (1024×1024 JPEG, 306,013 bytes) into the output
directory and verifies it byte-for-byte: JPEG start/end markers, dimensions
read from the SOF header, and the 1 MiB size limit. Python 3.13, standard
library only — no dependencies to install.

## Sources

The headlines follow reporting from Reuters, the NY Post, The Register
Australia, and Dealroom on Nvidia's earnings of 17–18 November 2026, plus
same-day coverage of the Gulf carrier deployment, Trump's Asia trip, the ASX
drop, and the David Jones debt. The three photographs on the page are
AI-rendered illustrations, not real photos.
