# Phil (self-improving forecaster)

A self-improving forecasting agent for short-term prediction markets on
**Kalshi** and **Polymarket US**, paper only. The agent (Claude Code,
headless, every 3 hours) runs `CYCLE.md`: settle → score → retrospective →
edit its own strategy → screen → research → forecast and place simulated
bets. Created by bennyjo ([bennyjo/phil](https://github.com/bennyjo/phil));
this fork is Sid's. Keep that credit intact in README.md and NOTICE.

This repository is **public**. Every cycle commits `journal/` and
`strategy/`. Never commit keys, account balances, real-money sizes, trade
logs or private desk strategy.

## Layout

- `core/` + `config/protected.json`: PROTECTED engine (venue adapters,
  honest order-book fills with venue fees, bankroll caps, official
  resolutions, scoring). The agent must never edit these; `loop.sh` reverts
  any such change. Also operator-owned: top-level docs (this file,
  README.md, CYCLE.md, REAL.md, NOTICE, LICENSE), `loop.sh`, `.gitignore`,
  `.github/` (CI) and `.claude/` (subagent definitions).
- `strategy/`: the agent's own playbook, risk policy, discovery, screener
  prompt and tools. This is what self-improves; its git history is the
  experiment's product.
- `journal/`: ledger (JSONL, written only through core), forecasts, retros,
  cycle log, `cycle-costs.jsonl`, `operator-notes.md` (operator only).
- `CYCLE.md`: the per-cycle procedure the headless agent follows.

## Venues

- Kalshi (`core/venue_kalshi.py`) and Polymarket US (`core/venue_pmus.py`),
  public data, no keys. Soccer and foreign leagues listed there are in scope.
- International Polymarket is off and hard-locked
  (`core/test_intl_lock.py`); old rows still settle and score. Do not
  re-enable it or work around region blocks.

## Purpose and scoring

Find WHERE fast research beats the market price: calibration per category
and edge class (`brier_delta` in `core/score.py`, `core/edge_board.py`).
Phil's record so far: worse than the market on Brier alone, but its
disagreements point the right way at about a third of the size it claims,
so its output is used blended with the market. Research priority is in
`journal/operator-notes.md`.

Standards for any claim of edge: no lookahead (only information available at
decision time), score against the market price not against zero, P&L after
fees at prices actually fillable, and state the sample size and standard
error.

## Real money

None here. `real_trading_enabled` is `false` and CI
(`core/validate.py`) keeps it false. `core/real.py`, `REAL.md` and the
Pearl Connect / Olas mech path are inherited from upstream and unused in
this fork. Real-money decisions happen in separate private tooling that
reads Phil's published forecasts.

## Commits and CI

- CI (`.github/workflows/ci.yml`) runs on every push: `core/validate.py`
  tripwires (real trading stays off, JSONs parse, ledger rows respect the
  protected caps, Python compiles), a bug-class-only ruff pass, and a
  boundary guard (`.github/scripts/boundary.sh`).
- Commits not prefixed `operator:` are agent commits and must not touch
  operator-owned paths. Human or operator-session commits to protected
  files MUST start with `operator:` or CI fails.
- Tests: `python3 -m unittest discover -s core -p 'test_*.py'` (offline,
  stdlib only, Python 3.12 in CI).

## For operator sessions (not the cycle agent)

- Work on a branch and open a PR; operator sessions may merge their own PRs
  once CI is green (Sid's standing permission).
- Process: investigate → plan → review with Sid → break down → build →
  review → finalize. Changes to caps, venues or `real_trading_enabled` need
  Sid's explicit approval first.
- Keys (`ODDS_API_KEY`, etc.) come from environment settings, never chat
  or files. `core/odds.py` errors can echo the key: never paste them.
  The Odds API is the only approved paid service (Phil's share: 3,000
  credits/month); ask Sid before adding another.
- A full cycle costs about $2.50 (logged in `journal/cycle-costs.jsonl`);
  weigh changes that raise it.
