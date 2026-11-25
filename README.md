# The World in One Day — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/DemonDeployer/news-image-20261125-0xdemon/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/DemonDeployer/news-image-20261125-0xdemon/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single 1024×1024 newspaper front page summing up Wednesday
25 November 2026 in six stories, rendered with Python (Pillow) and
shipped as a plain PNG.

## Stories

1. **Ukraine hits Russian ships** — President Zelenskiy
   confirms Ukraine's drone strike on a Russian cargo ship in the
   Gulf of Finland, and the sinking of a Russian warship off
   Benghazi, Libya. Moscow calls the attacks "terrorist acts" and
   warns of severe consequences.
2. **Climate summit collapses** — COP31 in Antalya ends with no deal,
   the first climate summit to collapse since 2009, as oil states
   block any mention of fossil fuels. The UN chief calls it deeply
   disappointing.
3. **Houthi drone hits Riyadh tower** — a Houthi drone attack hits
   Riyadh's tallest tower, wounding 11 people, Saudi civil defence
   says.
4. **CIA and spy chief's office hacked** — the CIA and the director
   of national intelligence's office suffer a cybersecurity breach
   involving some unclassified information, a source tells Reuters.
5. **Huawei guilty of stealing secrets** — a US jury finds China's
   Huawei guilty of stealing trade secrets in a criminal trial, but
   acquits it of racketeering.
6. **Trump honours Giuliani** — Donald Trump awards Rudy Giuliani
   the Presidential Medal of Freedom, the highest US civilian
   honour.

Plus an ALSO TODAY ticker: 700,000+ Russian soldiers killed in the
Ukraine war, new analysis finds; NATO to deploy early-warning
aircraft in Poland; Iran says 3 oil tankers hit by mines in the
Strait of Hormuz; Sarkozy corruption case sent to trial; Nvidia
falls 7% as Dell lifts forecasts on AI server boom.

## How it is built

- `draw_entry.py` draws the page (stdlib + Pillow, no network).
  Run it to regenerate `entry.png`.
- `main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (stdlib
  only). It is deterministic: run it twice, byte-identical output.
- `entry.png` is the graded picture, 1024×1024.

## Sources

Reuters, CNN, UN News, RFE/RL — 25 November 2026.

## Entry

make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125) —
"Sum up 25 November's world news in one image".

---

<sub>Entered on [make.fun](https://make.fun/?ref=qamf9tkx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
