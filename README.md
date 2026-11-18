# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/stfu-onad/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/stfu-onad/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page for Wednesday 18 November 2026, titled
THE WORLD TODAY. The lead story is GULF IN FLAMES: US jets strike an
Iranian missile site on Qeshm, and Iran answers by droning Bahrain and
Kuwait. Below it, NVIDIA posts $115.8B, up 103% — a record quarter with
a $130B guide — while XI AND PUTIN MEET IN SHENZHEN ahead of Thursday's
trilateral summit with Trump. The footer "Also Today" strip rounds out
the day: a Kerch Bridge span falls, Peltola wins Alaska 56-44, Ebola
passes 11,000 cases, the US loses its measles-free status, Voyager 1
reaches one light-day from Earth, and OpenAI launches GPT-6.2.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That copies `entry.png` (a 1024x1024 JPEG, 287,874 bytes) into the
output directory and verifies it byte-for-byte: it checks the JPEG
markers, reads the dimensions from the SOF header, and enforces the
1 MiB size limit. Python 3.13, standard library only — no extra
dependencies.

## Sources

- Reuters, via the Zark News daily briefing of 18 November 2026
- One Turn world news of 18 November 2026
- The Open Chronicle global brief of 18 November 2026
- The XTB morning wrap of 18.11.2026
- Briefing.com Story Stocks of 18 November 2026
- The aiagentupdate report on Nvidia's Q3 FY2027 results

The three photographs on the page are AI-rendered illustrations, not
real photos. The front page is reproduced exactly as designed — the
script never re-renders or alters the image, it only copies and
verifies it.
