# Phil the self-improving forecaster

[![CI](https://github.com/sidart10/phil/actions/workflows/ci.yml/badge.svg)](https://github.com/sidart10/phil/actions/workflows/ci.yml)

<img src=".github/phil.png" alt="Phil, a groundhog peeking over a rising price chart" width="100" align="left"/>

**Phil is an AI agent that forecasts short-term prediction markets on Kalshi
and Polymarket US, scores itself against the market price, and rewrites its
own strategy after every resolved forecast.** It trades on paper only. Its
forecasts feed a separate, private set of trading tools that decide whether
any of them are worth real money.

> **Credit.** Phil was created by [bennyjo](https://github.com/bennyjo) at
> [bennyjo/phil](https://github.com/bennyjo/phil). This repository is a fork
> that moves Phil from international Polymarket to the two US-regulated
> venues and runs it as the research engine of a larger trading setup. The
> engine design, the cycle procedure, the honest-simulation rules and the
> agent's history up to the fork are bennyjo's work. See [NOTICE](NOTICE)
> for what changed, and [LICENSE](LICENSE) (Apache-2.0).

## What Phil does

Every three hours a headless [Claude Code](https://claude.com/claude-code)
session follows [`CYCLE.md`](CYCLE.md):

1. **Settle** yesterday's paper bets against each venue's official result.
2. **Score** its own probabilities against the market price it saw
   (`brier_delta` in `core/score.py`: is Phil a better forecaster than the
   price?).
3. **Retro**: write down what it got wrong and why.
4. **Self-edit**: change its playbook, risk policy, research tools, market
   discovery queries and screening prompt, then commit the diff.
5. **Screen**: a swarm of cheap subagents scores ~300 open markets against
   the live price (`core/screen.py`), and the biggest disagreements get
   researched.
6. **Forecast and bet**: record a probability for every researched market
   and place simulated bets where the edge clears its own gates.

The git history of `strategy/` is the product: each commit is a lesson Phil
paid for in paper money.

## How Phil fits the bigger setup

Phil answers one question: *where does fast AI research beat the market
price?* Its record so far says the direction of its disagreements is real
but smaller than it claims, so it is most useful blended with the market
rather than trusted alone. Research effort is aimed at the categories where
its settled record is best (countable metrics, politics, "say the word"
mention markets, soccer) and away from where it adds nothing (US major-league
moneylines, weather, monthly economic prints).

Outside this repository, private tooling reads Phil's open forecasts,
blends them with the live price, and posts small maker bids only where that
blend clears the bid after fees. Real-money strategies, sizing, limits and
trade records live there, not here. Nothing in this repository places a real
order: `real_trading_enabled` is `false` in `config/protected.json`.

## Honest-simulation rules

- Paper fills walk the live order book asks, cheapest first, like a real
  taker, and pay the venue's fee. A book that cannot fill the whole stake
  refuses the bet.
- Entry prices are recorded at bet time; resolutions are the venue's own.
- The agent cannot edit the engine (`core/`, `config/protected.json`).
  `loop.sh` reverts any attempt, and CI independently fails any agent commit
  that touches protected files. Caps: $10 per bet, 60 open positions, no
  market resolving under 20 minutes out, no entries outside 2¢ to 95¢,
  against a simulated $1,000 bankroll.

## Venues

| Venue | Status | How Phil reads it |
|---|---|---|
| Kalshi | Paper | Public market API, no key (`core/venue_kalshi.py`) |
| Polymarket US | Paper | Public gateway, no key (`core/venue_pmus.py`) |
| International Polymarket | Off, hard-locked | Not reachable from the US. Old rows still settle and score. |

## Repository layout

The operator owns the engine, and the agent owns its strategy and its
record:

| Path | What it holds | Owner |
|---|---|---|
| `core/` | The engine: venue adapters, market scan, screening, ledger and fills, settlement, scoring, the runner lease, integrity tripwires (`validate.py`), and offline tests (`test_*.py`) | Operator |
| `config/protected.json` | Bankroll, stake and position caps, venue settings, banned question patterns, screener tunables | Operator |
| `CYCLE.md`, `REAL.md` | The procedure the agent follows each cycle, and the (unused) real-mode addendum | Operator |
| `loop.sh` | Runs cycles headlessly and reverts agent edits to operator-owned paths | Operator |
| `.github/`, `.claude/` | CI, the boundary guard, community files, and subagent definitions | Operator |
| `strategy/` | Playbook, risk policy, discovery queries, screener prompt, pacing, watchlist, tools | Agent |
| `journal/` | Ledger, forecasts, retrospectives, cycle log, cycle costs, operator notes, proposals | Agent, with ledger rows written only through `core/` and operator notes by the operator |

Operator commits start with `operator:`. Every other commit is an agent
commit, and CI fails any agent commit that touches an operator-owned path.

## Quickstart

The engine is Python 3 standard library only. CI runs on Python 3.12.

```bash
git clone https://github.com/sidart10/phil.git
cd phil
python3 -m unittest discover -s core -p 'test_*.py'   # offline tests
python3 core/validate.py                              # integrity tripwires
python3 core/score.py --skip-mtm                      # calibration and P&L report
python3 core/edge_board.py                            # variant table and edge map, offline
```

Market data needs no API key: Kalshi and Polymarket US both publish market
data openly.

## Running cycles

```bash
./loop.sh 10 45    # 10 paper cycles, 45 minutes apart
```

- `loop.sh` needs `claude` on your `PATH` and uses your Claude Code account.
  A full cycle costs roughly $2.50; each cycle's cost is appended to
  `journal/cycle-costs.jsonl`.
- Each cycle commits and pushes to `main` on `origin`, after taking a runner
  lease (`core/lease.py`) so two runners never cycle at once. To run locally
  without pushing, remove the remote: `git remote remove origin`.
- In this deployment the cycle runs as a scheduled cloud routine every three
  hours, configured outside the repository.

## Configuration

Caps and engine settings live in `config/protected.json`; the agent's sizing
policy lives in `strategy/risk.json`, inside those caps. Optional
environment variables:

| Variable | Read by | Purpose |
|---|---|---|
| `ODDS_API_KEY` | `core/odds.py` | Bookmaker-odds benchmark from [the-odds-api.com](https://the-odds-api.com). Falls back to `~/.config/phil/odds-api-key`. |
| `PHIL_RUNNER` | `core/screen.py`, `core/lease.py` | Runner name for the lease and the screener quota. Defaults to `operator` under `loop.sh`, else `cloud`. |
| `HEADLINE_ARENA_AGENT_ID`, `HEADLINE_ARENA_CLIENT_SECRET` | `core/headline_arena.py` | Optional Headline Arena daily questions, inherited from upstream. |
| `PEARL_CONNECT_STORE`, `CONNECT_POLYMARKET_VENV` | `loop.sh`, `core/real.py` | Upstream's real-money path through [Pearl Connect](https://github.com/valory-xyz/connect). Kept in the code, unused in this fork. |

Keep keys and tokens out of the repository. **This repository is public**,
and every cycle commits the journal and strategy.

## Status

Phil is a running experiment, not a release. The agent commits to `main`
many times a day. For the current score, run `python3 core/score.py` or read
the newest retrospective in `journal/retros/`.

## Disclaimer

This is a research experiment in agent self-improvement. Everything in this
repository is simulated. Nothing here is financial, investment, or betting
advice, and past performance, paper or real, predicts nothing.
Prediction-market trading is restricted in some jurisdictions; know your own
rules before trading with real funds.

## Contributing and security

- [Contributing guide](.github/CONTRIBUTING.md)
- [Code of conduct](.github/CODE_OF_CONDUCT.md)
- [Security policy](.github/SECURITY.md): report anything that touches keys
  or the protected boundary privately.

## License

[Apache-2.0](LICENSE), as in the original project. See [NOTICE](NOTICE) for
attribution and the list of changes made in this fork. The journal and
strategy files are part of the experiment's record and are covered by the
same license.
