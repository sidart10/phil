# Playbook archive

Settled narrative moved out of `strategy/playbook.md` so the live file stays
readable. Nothing here is a live rule; any rule a moved section carried was
restated in the live file when it moved. Not read per cycle.

## Moved DEEP-2026-09-30: per-settlement counterfactual updates, Sep 26-29

## 2026-09-26 21:39Z update: one `wide-spread-veto` refusal settled (biggest-quake Sep25 ≥6.1)

`f7fcd3a05a31`, recorded 2026-09-26T04:16:55Z, own est 0.97 vs a bid-only
mid of 0.36 — Yes had no ask in the book at record time (USGS already
showed a confirmed M6.6, next-largest 5.5), so this was a **refusal**
("no ask at record time"), not a fillable trade — same shape as the
2026-09-09 `9eff80f25296` precedent. Settled WON. No new P&L row: a
refusal contributes to the settled-row count only, neither side's trade
tally. Current mechanical ledger (`core/counterfactual.py ledger
--skip-reason wide-spread-veto`): 23 settled declined forecasts, 20
fillable CF trades, 3 refused, 11W/9L, pnl −$25.04 (staked $100.00),
brier_delta −0.0444, held-out −$17.22. Side split unchanged by this row:
no 13 rows/11 trd/5W-6L/−$19.79; yes 10 rows/9 trd/6W-3L/−$5.25. Check:
−19.79−5.25=−25.04 ✓. Ruling: no boundary change — correct estimate,
correctly unfillable, doesn't move the standing (still net-negative)
wide-spread-veto read. Full grading in RETRO-20260926-2143.

## 2026-09-28 02:15Z update: one `wide-spread-veto` row settled (Burleson MLB RBI lead)

| Burleson RBI lead (`18a43357718b`, wide-spread-veto) | 0.93 / 0.73 | Yes | +0.040 | Yes | **+0.62** |

Fillable at the 0.89 ask (book 0.53/0.89, spread 0.36). Mechanical ledger
(`core/counterfactual.py ledger --skip-reason wide-spread-veto`): 24 settled
rows, 21 fillable CF trades, 3 refused, 12W/9L, pnl −$24.42 (was −$25.04;
−25.04+0.62=−24.42 ✓), dBrier −0.0454. Side split: no 13 rows/11 trd/5W-6L/
−$19.79 (unchanged); yes 11 rows/10 trd/7W-3L/−$4.63 (−5.25+0.62 ✓). Check:
−19.79−4.63=−24.42 ✓. Ruling: no boundary change. The realizable ask-edge
sat at the min_edge floor, so the 0.20 mid gap was stale-mid, not tradable.
Full grading in RETRO-20260928-0215.

## 2026-09-28 04:15Z update: one `wide-spread-veto` row settled (VMA Best Dance Stateside)

| VMA Best Dance Stateside (`e4564b71ab49`, wide-spread-veto) | 0.30 / 0.37 | No | −0.020 | No | **+1.94** |

Fillable at the 0.72 No ask (book 0.28/0.46). Mechanical ledger
(`core/counterfactual.py ledger --skip-reason wide-spread-veto`): 25 settled
rows, 22 fillable CF trades, 3 refused, 13W/9L, pnl −$22.48 (was −$24.42;
−24.42+1.94=−22.48 ✓), dBrier −0.0455. Side split: no 14 rows/12 trd/6W-6L/
−$17.84 (−19.79+1.94, rounding); yes 11 rows/10 trd/7W-3L/−$4.63 (unchanged).
Check: −17.84−4.63=−22.47 ≈ −22.48 (rounding) ✓. Ruling: no boundary change —
realizable edge was negative, a lucky CF win on a correctly declined trade.
Full grading in RETRO-20260928-0415.

## 2026-09-28 22:15Z update: 4 `outside-view-veto` + 2 `wide-spread-veto` rows settled (Treasury Sep ladder, box office Sep 26 weekend)

| 10y hit 5.20% Sep (`fdedb184ad3e`, OVV) | 0.28 / 0.06 (No frame) | No | +0.190 | Yes | −5.00 |
| 10y hit 5.20% Sep (`3ed526b57eca`, OVV) | 0.47 / 0.26 (No frame) | No | +0.200 | Yes | −5.00 |
| Heart of the Beast 17-20m (`cec5bff18abf`, OVV) | 0.40 / 0.76 | No | +0.350 | No | **+15.00** |
| Forgotten Island <13m (`bb60348ab311`, OVV) | 0.90 / 0.7525 | Yes | +0.145 | No | −5.00 |
| 30y hit 5.50% Sep (`99df204b7f85`, WSV) | 0.67 / 0.54 | Yes | +0.055 | Yes | **+3.13** |
| 30y hit 5.55% Sep (`84012264b65d`, WSV) | 0.31 / 0.51 | No | −0.107 | Yes | −5.00 |

Mechanical ledgers (`core/counterfactual.py ledger --skip-reason ...`):
outside-view-veto batch $0.00 (1W/3L): 179 rows, 171 trd, 72W/99L,
+$77.41 (unchanged). Side: no 126/118/54W-64L/+$43.21 (+5.00); yes
53/53/18W-35L/+$34.20 (−5.00). Check 43.21+34.20=77.41 ✓.
wide-spread-veto batch −$1.87 (1W/1L): 27 rows, 24 trd, 3 refused,
14W/10L, −$24.35 (−22.48−1.87 ✓), dBrier −0.0372. Side: no 15/13/6W-7L/
−$22.84; yes 12/11/8W-3L/−$1.50. Check −22.84−1.50=−24.34 ≈ −24.35
(rounding) ✓. Ruling: no boundary change; the rates misses were the
driftless est (new Treasury touch drift rule), not the veto. Full
grading in RETRO-20260928-2215.

## 2026-09-29 18:00Z update: JOLTS Aug ladder + one `outside-view-veto` row settled

| LGD -1.5 vs Xtreme (`c0ad4f0ec92d`, OVV) | 0.25 / 0.355 | No | +0.105 | No | **+2.46** |

Mechanical ledger (`core/counterfactual.py ledger --skip-reason
outside-view-veto`): 180 rows, 172 trd, 8 refused, 73W/99L, +$79.87 (was
+$77.41; 77.41+2.46=79.87 ✓), dBrier +0.0322. Side: no 127/119/55W-64L/
+$45.67 (43.21+2.46 ✓); yes 53/53/18W-35L/+$34.20 (unchanged). Check
45.67+34.20=79.87 ✓. Ruling: no boundary change. It is one draw on a
self-built Bo3 model. Full grading in RETRO-20260929-1800.

- **JOLTS: record the LinkUp model centre and do not tilt past consensus
  on soft signals (n=1, RETRO-20260929-1800).** Aug print 7,079k vs
  consensus 7.23M, LinkUp 7.185M. I tilted the centre UP to 7.25M on an
  Indeed/NFP read. The five ladder rows netted dBrier +0.0011 (a wash).
  The same shape showed up in the Canada GDP retro: a directional tilt
  on top of a sourced benchmark is unvalidated. Cap it at 0.05 of bracket
  mass there, and at zero past consensus for JOLTS until it has graded
  evidence.
- **Econ ladders: record every bracket whose book was read, centre
  included.** The Aug JOLTS ladder recorded the tails and the upper
  brackets, but not 7.0-7.1 or 7.1-7.2, and the print landed in 7.0-7.1.
  A ladder with no row near the outcome can't be graded as a
  distribution. This is the validated-feed sweep rule ("forecasts for
  every leg read") applied to BLS/BEA/StatCan ladders.

## 2026-09-29 22:15Z update: one `wide-spread-veto` row settled (10y hit 5.25% Sep)

| 10y hit 5.25% Sep (`a41e6e996b85`, WSV, superseded by `5e46d21ef6ca`) | 0.46 / 0.65 | No | fillable per ledger | Yes | −5.00 |

Mechanical ledger (`core/counterfactual.py ledger --skip-reason
wide-spread-veto`): 28 rows, 25 trd, 3 refused, 14W/11L, −$29.35 (was
−$24.35; −24.35−5.00=−29.35 ✓), dBrier −0.0299. Side: no 16/14/6W-8L/
−$27.84 (was 15/13/6W-7L/−$22.84; −22.84−5.00 ✓); yes 12/11/8W-3L/−$1.50
(unchanged). Check −27.84−1.50=−29.34 ≈ −29.35 (rounding) ✓. Ruling: no
boundary change. The loss comes from the pre-drift-rule driftless blend (Sep 25),
not from the veto. The superseding drift-plus-futures row (0.76 vs 0.74)
beat the mid by 0.010. It is still the single September up-trend regime, so
the October split-by-trend re-grade stands. Full grading in
RETRO-20260929-2215.

## 2026-09-29 23:42Z update: one `outside-view-veto` row settled (Trump renames AI, 3-snapshot chain) — unexplained-move tracking, n=2

| Trump renames AI (`e22fb0445ebe`, OVV, supersedes `f85a9b197bc6`) | 0.30 / 0.535 | No | +0.23 | Yes | **-5.00** |

Mechanical ledger (`core/counterfactual.py ledger --skip-reason
outside-view-veto`): 181 rows, 173 trd, 8 refused, 73W/100L, +$74.87 (was
+$79.87; 79.87-5.00=74.87 ✓), dBrier +0.0336 (was +0.0322). Side: no
128/120trd/55W-65L/+$40.67 (was 127/119/55W-64L/+$45.67; 45.67-5.00=40.67
✓); yes 53/53/18W-35L/+$34.20 (unchanged). Check 40.67+34.20=74.87 ✓.
Ruling: no boundary change — the declined No bet would have lost, so the
veto did its job on the trade decision.

**Unexplained-move tracking (paired with the 2026-09-21 Opus case,
RETRO-20260922-0619): 1-for-2 so far, not a rule either way.** This
market's book moved 0.255->0.535 between Sep27 and Sep29 with, per the
row's note, "no source I can find." Per the Sep21 lesson ("a price move
with no sourced cause is not itself evidence") the estimate was NOT
revised toward the market (held at 0.30 vs market 0.535) and the bet was
vetoed. This time the market was right — event resolved Yes, own's
whitehouse.gov/presidential-actions search method never surfaced whatever
the book saw. Sep21's case had the opposite result: an unsourced jump
that reversed, where discounting it was correct. Two data points, one
each way, on the specific question "should an unexplained price move
against a public-record-search estimate shift the estimate itself
(separately from whether it should ever be traded)." Full grading in
RETRO-20260929-2342. Stays a tracked observation, not a playbook rule —
n=2 is far below the ~15-settlement floor CYCLE.md sets for acting on a
read, and the two cases are in different categories (ai-model-release vs
news). Re-visit if a third instance settles either way.

## Moved 2026-11-14 (operator): international-only and frozen material

Moved verbatim when international Polymarket was hard-locked off. None of it is a
live rule: the V2 sweep expired 2026-11-15 and applied to international V2 books only;
the hand table was frozen on 2026-10-07; the settled-row logs carry no ruling beyond
"no boundary change".

### V2 first-week forecast sweep (operator note 2026-11-07 ~08:30Z; integrated 2026-11-07 12:1xZ FULL, cloud)

**Rule (forecast rows only; bet rules unchanged).** From **2026-11-09 through
2026-11-15** (UTC dates of the FULL tick), every FULL cycle records a step-5b forecast
for **every live V2 book** the scan kept, whether or not the screener sampled it into
the pool. "Live V2 book" = a scan record with `version: "v2"` (scan stderr: `v2
markets kept: N`; the thin/empty-book drops are core's call, not mine). Re-quote each
with `strategy/tools/quote.py` before recording, as for any row.
- NBA (and any other sport) moneylines: benchmark on sportsbook odds via `python3
  core/odds.py odds basketball_nba` -> `strategy/tools/devig.py`. One call covers
  every game on the slate, so the sweep costs ~1-3 credits a cycle, inside the
  10-12/day budget. Form the estimate from the devigged book, then compare.
- Skip reason: `bet` only if the normal gates pass (min_edge vs the live ask, V2
  binary only; neg-risk/combinatorial V2 is refused by ledger.py anyway); otherwise
  `no-edge` / `market-agrees` as usual. Category: the existing family slug
  (`nba-moneyline`).
- A market already forecast this window and not materially moved (no new
  injury/lineup news, book within 0.03 of the last record) is not re-recorded:
  one row per market per day at most, superseding the earlier row when re-recorded,
  so the cell counts events, not repeats.
- If odds.py reports the key missing or the budget exhausted, record no row for
  that game (never invent an estimate) and log it in the cycle line.

**Scoring.** The cell is `v2` on the TIGHT slice only (spread at record
`best_ask_at_record - best_bid_at_record <= 0.06`); wide books flatter dBrier
(DEEP-2026-11-07: wide -0.067 vs tight +0.011 over 24h). Until `core/edge_board.py`
grows a version table, compute it with `python3 strategy/tools/v2cell.py --since
2026-11-09` and quote its `v2 TIGHT` line in every retro that settles a V2 row,
next to the `v1 TIGHT` baseline it prints.

**Baseline at integration (2026-11-07 12:1xZ, `v2cell.py --since 2026-11-01`):**
`v2 TIGHT n=2 events=2 brier_delta=-0.0558`, `v2 wide n=2 +0.0081`, `v1 TIGHT n=69
+0.0116`. n=2 is nothing; the first read is due at ~50 settled rows (~11-14).

**Why (evidence).** Forecast rows/day fell 53 (11-01) -> 30 (11-06), and Phil recorded
4 V2 rows on 11-04 and none since (`journal/forecasts.jsonl` version counts), while the
11-07 12:13Z scan kept 7 live V2 books, all NBA moneylines (`v2 markets kept: 7`), in
a family the edge board rates Real (allocation `prefer family=sports-moneyline`).
They settle in 2-3 days, so the sweep is the fastest feedback channel available.
**Early start (CORRECTED by DEEP-2026-11-08):** the 11-07 12:16Z cycle claimed to forecast
the live V2 books, but all 7 NBA rows it wrote (`89f933d16902`, `a1e32bfe49a9`,
`339b313b18fe`, `5869b8013740`, `530b12235ac6`, `70d16c0a0336`, `954a916e0905`) are
**v1** markets (slugs `nba-<a>-<b>-<date>`, `version: "v1"` stamped by core). The V2 books
are separate markets with slugs `polyv2-<sport>-...` (the only 4 v2 rows in the file are
11-04 `polyv2-nba-*`). Recording the v1 twin does NOT feed the v2 cell.
- **Procedure:** take the market id from the scan record with `version: "v2"` (slug
  starts `polyv2-`), not from the same game's v1 listing. After the batch, run
  `python3 strategy/tools/v2cell.py --since 2026-11-09` and check the v2 n rose by the
  number of V2 rows you meant to write; if it did not, you recorded v1 twins - say so in
  the cycle line.
- **One-sided depth caveat for the TIGHT slice:** both "v2 TIGHT" rows in the baseline
  (`0dd569698c25` Knicks .73/.74, `45ad4328d413` Spurs .68/.69) had ~5-share top asks with
  the next level +0.19 (proposals.md 2026-11-04 20:4xZ). Tight by spread, not by depth:
  their -0.0558 is a mid-scoring artifact of the same kind as wide books. When recording a
  V2 row, put the top-ask size in the note (`topask=<shares>`); in the retro read, count a
  row whose top ask is under $25 as wide, whatever its spread.
- **DEEP-2026-11-09: v2cell.py now applies the depth test itself.** A row with a sub-$25
  top ask (first `topask=` x best_ask) is demoted to wide automatically, and the two
  pre-topask artifacts (`0dd569698c25`, `45ad4328d413`) are hard-demoted. Re-run on
  `--since 2026-11-01`: the 11-04 "v2 TIGHT -0.0558" becomes **n=0**, which confirms it was
  wholly the depth artifact. Day 1 of the sweep: IND-DAL `27014641943a` (topask=31 sh at
  .61 = $19) is wide, so 3 of 4 rows are tight. Write the recorded side's `topask=` FIRST
  in the note (`f645a3370abb` lists Spurs then Suns; the tool reads the first).
- **Benchmark tag (DEEP-2026-11-09):** an ML inferred from a point spread is an
  unvalidated conversion. Write `spread-derived` in the note when you use it (both 11-09
  rows `d9302a833288`, `27014641943a` already do); v2cell splits the TIGHT line into
  odds-bench vs spread-derived so method noise cannot masquerade as a V2 effect.
- **No-benchmark skips (DEEP-2026-11-09):** MEM-TOR and CLE-CHA were skipped at 02:13Z with
  no line. That is allowed once, but the operator asked for EVERY live V2 book: a skipped
  book must be re-swept on the next FULL before its tip (lines post on game day), and a
  game that reaches tip with no row is named in the cycle line. Volume check: the operator
  expected 10-20 rows/day and ~50 settled by ~11-14; day 1 gave 4 (3 tight). If fewer than
  25 v2 TIGHT rows have settled by the 11-14 deep retro, the first read is **insufficient
  data**, not a verdict.
- **DEEP-2026-11-10: `ai-release-mid` kept, and its scope is pinned to one category label.** The
  long-run record backs the hourly swap (RETRO-20261109-2215). score.py has release-date rows
  behind the book in both labels they were filed under: `ai-model-release` n=52 at +0.056 and
  `product-release` n=13 at +0.046. The Fable 5.2 family was split across both labels
  (`59f1933102a7`/`b0877b5340db` ai-model-release, `8388516aeff8`/`5c1c1d3f700b`
  product-release), which halves every per-category read. From now on, file AI-model
  release-date rungs as `ai-model-release` and tag them `ai-release-mid`. Use
  `product-release` only for non-AI products.
- **Gemini Carbon settled Yes Nov 10 (RETRO-20261110-1820).** 12 rows over 9 days, all below the mid
  and all worse than it (sum dBrier about +0.99). Each one cited the lack of a Google date or
  changelog entry, which is the negative-check pattern the clause above already rules out. This
  is the second family in two days with the same failure (Fable 5.2+). Belief update, not a rule:
  "no official date yet" is the normal state right before every AI release this autumn, so it is
  not evidence of lateness. A dated precedent (Argon 13d defenders->GA) is evidence, and the book
  priced it better than I did. Allocation (procedure only): on a release-rung family, record at most
  ONE row per rung per UTC day. Re-research only when a positive primary source appears or the mid
  moves >=0.10 since my last row. Otherwise the slot goes to other candidates.
- **Box-office family openers (DEEP-2026-11-10, procedure only, no probability rule).**
  - Evidence: Cat in the Hat 20M+ `ada749212e1c` (own .10 vs mid .611, Yes, +0.659) and the
    Drummer Boy 9M+ under-read `281c94228034` (.62 vs .85 on a tight book, Yes, +0.122) both
    came from Friday-only arithmetic.
  - On every family/animated opener, write the Fri->weekend multiplier you used in the
    rationale, taken from at least 2 named comps. A bare Friday x constant is not enough.
  - The category record is drifting the wrong way: score.py box-office is n=60 at +0.027,
    against n=42 at +0.005 when the modal floor was frozen. By my row-level bootstrap
    (correlated rows, so optimistic), wide books are n=26 at +0.094 [+0.027,+0.170] and tight
    books are n=53 at -0.018 [-0.054,+0.015].
  - So on WIDE box-office books the mid has been right against our deviations, the opposite
    of the whole-stream wide-book pattern. The category stays no-bet. Revisit at the
    DEEP-2026-11-17 retro.
- **Large deviations against TIGHT books still lose (DEEP-2026-11-10, whole forecast stream,
  my row-level bootstrap, not score.py).** This is supporting evidence for the existing >0.10
  claimed-edge veto. No change.
  - Tight books with |est-mid|>=0.10: n=368 at +0.026 [+0.005,+0.050]. The November rows are
    n=23 at +0.075. October was n=145 at -0.017, so the effect is not uniform.
  - Tight books with |est-mid|<0.10: n=1988 at +0.0002 (at the book).

### Frozen hand table (all rows, original order)

| Row | est vs mkt | Side | Realizable edge | Result | CF P&L |
|---|---|---|---|---|---|
| SC Nordone (57f222efb516) | 0.33 / 0.595 | No | +0.260 | Yes | −1.00 |
| SC Fry (e5666c235356) | 0.27 / 0.071 | Yes | +0.196 | No | −1.00 |
| MN Flanagan (75f2545a7a0e) | 0.52 / 0.715 | No | +0.190 | Yes | −1.00 |
| MN Craig (9ab914d80a5b) | 0.45 / 0.295 | Yes | +0.150 | No | −1.00 |
| PPI 5.3% (5ad483698a95) | 0.036 / 0.171 | No | +0.097 | No | **+0.15** |
| PPI 5.4% (169b4fd6c04a) | 0.027 / 0.049 | No | −0.019 | No | non-trade |
| PPI ≥6.0% (4908388c9fd7) | 0.003 / 0.042 | No | ~0.000 | No | non-trade |
| Musk 120-139 (5ef2f363f039) | 0.165 / 0.085 | Yes | +0.080 | No | −1.00 |
| Musk 140-159 (b7a58fd571c8) | 0.64 / 0.415 | Yes | +0.220 | No | −1.00 |
| Musk 160-179 (e06e9b2bea70) | 0.189 / 0.385 | No | +0.191 | No | **+0.61** |
| Musk 180-199 (eb09f3632c5d) | 0.003 / 0.095 | No | +0.087 | Yes | −1.00 |
| Musk 2d 40-64 (10029a75295e) | 0.499 / 0.39 | Yes | +0.099 | Yes | **+1.50** |
| Musk 2d 65-89 (53c5bf348303) | 0.501 / 0.62 | No | +0.109 | No | **+1.56** |
| Japan GDP 0.0-0.8% (d684f9caff81) | 0.2475 / 0.49 | No | +0.2125 | No | **+0.85** |
| Musk 2d <40 (8f663df4a762) | 0.0146 / 0.195 | No | +0.175 | Yes | −1.00 |
| Oak Street 17-20m (f0672a1a69e7) | 0.29 / 0.455 | No | +0.140 | No | **+0.75** |
| Spider-Man <66m (9ad9a1e605a5) | 0.42 / 0.31 | Yes | +0.020 | No | −1.00 |
| Spider-Man 66-68m (db6bd4ff0cb7) | 0.31 / 0.54 | No | +0.190 | No | **+1.00** |
| Spider-Man 68-70m (64695326b358) | 0.19 / 0.0695 | Yes | +0.061 | No | −1.00 |
| HD earnings (65aea7cd91f4) | 0.68 / 0.84 | No | +0.130 | Yes | −1.00 |
| Musk wk 180-199 (99feadecc33b) | 0.494 / 0.325 | Yes | +0.164 | No | −1.00 |
| Musk wk 220-239 (cf16f6424af7) | 0.024 / 0.145 | No | +0.116 | No | **+0.16** |
| Musk wk 240-259 (cd3af116ed2a) | 0.16 / 0.2575 | No | +0.092 | Yes | −1.00 |
| Musk wk 280-299 (cc08840449e9) | 0.31 / 0.165 | Yes | +0.141 | No | −1.00 |
| TI VISION/Yandex (6b84771a3bd6) | 0.383 / 0.235 | Yes | +0.143 | No | −1.00 |
| BTC touch-$80k (fc4a9d5caace) | 0.5034 / 0.388 | No | +0.115 | Yes | −1.00 |
| WI Hong <5% (6a7decac51f2) | 0.007 / 0.0785 | No | +0.070 | No | **+0.08** |
| WI Hong 5-10% (7ae672a0a6db) | 0.031 / 0.096 | No | +0.051 | No | **+0.09** |
| WI Hong 15-20% (e6c093fc7660) | 0.178 / 0.209 | No | +0.023 | No | **+0.25** |
| WI Hong 20-25% (597ed3729e91) | 0.241 / 0.1845 | Yes | +0.052 | No | −1.00 |
| WI Hong 25-30% (1aab3bbe55be) | 0.224 / 0.135 | Yes | +0.084 | No | −1.00 |
| WI Hong ≥30% (aac304cdebf7) | 0.227 / 0.100 | Yes | +0.117 | No | −1.00 |
| KL 30C weather (ff0e79b1b303) | 0.26 / 0.0735 | Yes | +0.181 | No | −1.00 |
| Amsterdam 25C weather (f352b500005a) | 0.13 / 0.45 | No | +0.31 | No | **+0.79** |
| WI Crowley win (7dac557c4c19) | 0.0012 / 0.032 | No | +0.011 | Yes | −1.00 |
| PCE MoM 0.1% (381c3e38473c) | 0.219 / 0.129 | Yes | +0.070 | No | −1.00 |
| PCE MoM 0.2% (b6df56da3754) | 0.594 / 0.57 | Yes | +0.014 | Yes | **+0.72** |
| PCE MoM 0.3% (c07caa45a8dc) | 0.175 / 0.25 | No | +0.065 | No | **+0.32** |
| BoK hold (a8fa1e2ac41d) | 0.38 / 0.69 | No | +0.300 | No | **+2.13** |
| BoK hike 25bps (d102445cc5d5) | 0.60 / 0.32 | Yes | +0.270 | Yes | **+2.03** |
| UMich <49.0 (a5703b36d60a) | 0.334 / 0.177 | Yes | +0.157 | No | −1.00 |
| UMich 49.0-51.9 (fdfd9e781481) | 0.321 / 0.38 | No | +0.059 | Yes | −1.00 |
| GTA VI <10M views (9163ef072ce7) | 0.45 / 0.36 | No | +0.090 | Yes | −1.00 |
| Mythos No (4aceafc01b6b) | 0.95 / 0.80 | No | +0.150 | No | **+0.25** |
| Mythos No (e35e582a4d22) | 0.70 / 0.35 | No | +0.350 | No | **+1.86** |
| Mythos No (5d388f8d5585) | 0.65 / 0.54 | No | +0.110 | No | **+0.85** |
| Mythos No (c69958e0193a) | 0.93 / 0.73 | No | +0.200 | No | **+0.37** |
| GTA VI trailer (ce1727b53bd5) | 0.55 / 0.32 | Yes | +0.230 | No | −1.00 |
| Gas $3.90 Low (e2cbca37fe88) | 0.035 / 0.18 | No | +0.145 | No | **+0.22** |
| Gas $3.70 Low (9dffc25cddd9) | 0.01 / 0.04 | No | +0.030 | No | **+0.04** |
| Gas $3.50 Low (cca60b062716) | 0.01 / 0.01 | No | +0.000 | No | **+0.01** |
| Gas $3.25 Low (e45e186476b0) | 0.01 / 0.12* | No | +0.110 | No | **+0.14** |
| Gas $3.00 Low (38c726c1c695) | 0.01 / 0.01 | No | +0.000 | No | **+0.01** |
| Gas $4.25 High (d59e9243dfb4) | 0.019 / 0.09 | No | +0.071 | No | **+0.10** |
| Gas $4.50 High (59f65e95ed5e) | 0.01 / 0.10 | No | +0.090 | No | **+0.11** |
| Gas $4.75 High (9140e7f850f4) | 0.01 / 0.16* | No | +0.150 | No | **+0.19** |
| Mythos by-Sep9 No (1f20cadb2b53) | 0.85 / 0.27 | No | +0.580 | Yes | −1.00 |
| Mythos by-Sep1 No (720781176db9) | 0.20 / 0.68 | No | +0.480 | Yes | −1.00 |
| Mythos by-Sep1 No (237402dd3f1e) | 0.06 / 0.31 | No | +0.250 | Yes | −1.00 |
| Mythos exact-Sep1 No (4c648c2e6afb) | 0.03 / 0.29 | No | +0.260 | Yes | −1.00 |
| Mythos by-Sep2 No (f9a6e09224dd) | 0.12 / 0.55 | No | +0.430 | Yes | −1.00 |
| Odyssey ≥570m (d48834ed8f41) | 0.08 / 0.14 | No | +0.057 | No | **+0.16** |
| Spider-Man ≥900m (1f552d2c510f, Aug22 check) | 0.25 / 0.336 | No | +0.085 | No | **+0.50** |
| Spider-Man ≥900m (1e889dd4dd33, Aug25 update) | 0.15 / 0.092 | Yes | +0.058 | No | −1.00 |
| Spider-Man <900m (9f40def4f61c) | 0.85 / 0.915 | No | +0.060 | Yes | −1.00 |
| Enzo stay-Chelsea (dc81cc744a86) | 0.60 / 0.312 | Yes | +0.288 | No | −1.00 |
| Enzo join-ManCity (e481c796f8d1) | 0.25 / 0.17 | No | +0.080 | Yes | −1.00 |
| Gemini Flash by-Sep2 No (4a680e8bca1e, initial check) | 0.13 / 0.655 | No | +0.53 | Yes | −1.00 |
| Gemini Flash by-Sep2 No (a554a9f53079, re-check) | 0.50 / 0.675 | No | +0.19 | Yes | −1.00 |
| Gemini Flash by-Sep2 No (8f8fa61af2a2, re-check) | 0.58 / 0.79 | No | +0.22 | Yes | −1.00 |
| Gemini Flash on-Sep2 No (655167550ada, sibling) | 0.58 / 0.775 | No | +0.21 | Yes | −1.00 |
| ETH $2600 Aug touch (9f1fedaa0386) | 0.52 / 0.326 | No | +0.194 | No | **+2.07** |
| BTC >$76k Sep2 (d16f83d68630) | 0.162 / 0.06 | No | +0.102 | Yes | −1.00 |
| Astra by-Sep2 (2daa083970d8) | 0.10 / 0.185 | No | +0.028 | No | **+0.15** |
| Singapore 32C Sep3 (e48e803b2103) | 0.233 / 0.07 | Yes | +0.143 | No | −1.00 |
| Shanghai 32C Sep3 (3cf21078d1a0) | 0.049 / 0.355 | No | +0.271 | No | **+0.47** |
| Singapore 33C Sep3 (32d046d6981c) | 0.323 / 0.845 | No | +0.497 | Yes | −1.00 |
| Ankara 30C Sep3 (aac6d9fc2b4a) | 0.287 / 0.565 | No | +0.273 | Yes | −1.00 |
| Ankara 31C Sep3 (428600857382) | 0.140 / 0.375 | No | +0.220 | No | **+0.56** |
| GTA VI <20M wk1 (b5c5c134d7cb) | 0.55 / 0.60 | No | +0.030 | No | **+1.38** |
| GTA VI <20M wk1 (e398cebab2e6) | 0.30 / 0.82 | No | +0.510 | No | **+4.26** |
| Astra by-Sep3 (925eb1c697f9) | 0.20 / 0.87 | No | +0.660 | No | **+6.14** |
| Astra on-Sep3 (b1d2b955da88) | 0.18 / 0.8305 | No | +0.632 | No | **+4.32** |
| Astra by-Sep3 re-check (cfda85a4abde) | 0.15 / 0.885 | No | +0.730 | No | **+7.33** |
| Astra on-Sep3 re-check (a8d12b4831b4) | 0.80 / 0.944 | No | +0.140 | No | **+15.67** |
| NFP add 0-50k (d2c8054e1df6) | 0.1794 / 0.265 | No | +0.071 | No | **+0.33** |
| NFP add 50-100k (7800470f6fab) | 0.218 / 0.315 | No | +0.082 | No | **+0.43** |
| NFP add 100-150k (adc70585857a) | 0.1963 / 0.141 | Yes | +0.055 | No | −1.00 |
| NFP add >=150k (a8a368a644f4) | 0.2266 / 0.145 | Yes | +0.082 | **Yes** | **+6.14** |
| Shanghai 31C weather (6aff2db6ddbe) | 0.58 / 0.885 | No | +0.280 | Yes | −1.00 |
| Astra by-Sep4 (99d1545b2ec7) | 0.08 / 0.863 | No | +0.783 | Yes | −1.00 |
| Astra by-Sep5 (7adc67fe86cc) | 0.18 / 0.685 | No | +0.505 | Yes | −1.00 |
| Astra by-Sep6 (b249eb7256a0) | 0.28 / 0.64 | No | +0.360 | Yes | −1.00 |
| Astra by-Sep7 (d179339fe4c0) | 0.35 / 0.525 | No | +0.175 | Yes | −1.00 |
| Astra by-Sep15 (037ae430d6f3) | 0.80 / 0.885 | No | +0.085 | Yes | −1.00 |
| GPT-6 by-Sep15 (44a62d640ae1) | 0.46 / 0.87 | No | +0.40 | Yes | −1.00 |
| Astra on-Sep4 (17db5ec8f494) | 0.92 / 0.852 | No | +0.067 | Yes | −1.00 |
| Munich 30C weather (355715e4ce82) | 0.28 / 0.565 | No | +0.28 | Yes | −1.00 |
| Miami 92-93F weather (0b7b13d60127) | 0.11 / 0.06 | Yes | +0.040 | No | −1.00 |
| GenG-HLE O/U3.5 (bf608b923988) | 0.65 / 0.40 | Yes | −0.120 | Yes | +0.30 |
| GenG-HLE O/U4.5 (5b76118ad958) | 0.716 / 0.79 | No | −0.106 | Yes | −1.00 |
| Guangzhou 35°C same-day weather (eb95af0bfe24) | 0.82 / 0.9665 | No | +0.076 | Yes | −1.00 |
| Munich 25°C same-day weather (bc29b9874a48) | 0.26 / 0.23 | Yes | +0.01 | No | −1.00 |
| Hong Kong 26°C same-day weather (2eb38db512c9) | 0.80 / 0.715 | Yes | +0.030 | Yes | **+0.30** |
| Wellington 10°C same-day weather (b838efbe4ade) | 0.4522 / 0.7985 | No | +0.317 | Yes | −1.00 |
| SPD ≥9% Sachsen-Anhalt (3df069438d36) | 0.22 / 0.088 | Yes | +0.132 | Yes | **+10.36** |
| Tokyo 22°C Sep7 (ff7e0fda3407) | 0.17 / 0.10 | No | +0.070 | Yes | −1.00 |
| Jeddah 38°C same-day weather (39dbfcb80a90) | 0.0168 / 0.165 | No | +0.148 | No | **+0.23** |
| Toronto 25°C Sep7 (291e9630e91e) | 0.307 / 0.57 | No | +0.253 | Yes | −5.00 |
| China CPI 0.7-0.8% Aug26 (19cf14c87979) | 0.67 / 0.53 | No | +0.140 | Yes | −1.00 |
| China CPI ≥0.9% Aug26 (7bacc91ddf91) | 0.38 / 0.331 | Yes | +0.049 | No | −1.00 |
| Chewy "Consumable" wide-spread duplicate (`e7a452fef1be`) | 0.93 / 0.59 | Yes | +0.340 | Yes | **+3.47** |
| RNC "2028/Campaign" (`906a1a65abc8`) | 0.80 / 0.71 | Yes | +0.090 | Yes | **+2.04** |
| RNC "Tax on Tips/Overtime" (`83321f868e0f`) | 0.75 / 0.77 | Yes | −0.020 | Yes | **+1.49** |
| Emmys Variety Series, Last Week Tonight (`697a7f4f3799`) | 0.19 / 0.14 | Yes | +0.050 | No | **−5.00** |
| F1 Italian GP safety car, fact-final (`705c1219decd`) | 0.99 / 0.899 | Yes | +0.091 | Yes | **+0.56** |
| Israel x Lebanon by-Sep15 (`7d43ec49805b`) | 0.75 / 0.855 | No | +0.060 | Yes | **−5.00** |
| Chewy "Consumable" say-the-word (ffc3fcdcbaa6) | 0.93 / 0.58 | Yes | +0.350 | Yes | **+3.62** |
| RNC "Radical Left" trump-mention (36ff9feec021) | 0.87 / 0.66 | Yes | +0.210 | Yes | **+2.58** |
| RNC "MAGA/MAGA-full" say-the-word (87736f3e8ab9) | 0.90 / 0.72 | Yes | +0.180 | Yes | **+1.94** |
| RNC "Endorse/Endorsed/Endorsement" say-the-word (16e13abfec2f) | 0.58 / 0.43 | Yes | +0.150 | No | **−5.00** |
| RNC "America First" say-the-word (11ea1286d8c7) | 0.62 / 0.28 | Yes | +0.340 | No | **−5.00** |
| Aug headline MoM 0.4% bracket, No leg (5a6d5321c25a) | 0.66 / 0.515 | No | +0.140 | print was 0.4% (No leg lost) | **−5.00** |
| Aug core MoM 0.2% bracket, No leg (79e72c3002c3) | 0.62 / 0.45 | No | +0.160 | print was 0.3% (No leg won) | **+5.87** |
| Israel x Lebanon by-Sep18 (9894fc8df165) | 0.55 / 0.835 | No | +0.260 | Yes | **−5.00** |
| Israel x Lebanon by-Sep16 (459635ab318c) | 0.62 / 0.935 | No | +0.281 | Yes | **−5.00** |
| Spider-Man overtake Star Wars by Sep15 (6eb52610fb5c) | 0.68 / 0.885 | No | +0.170 | Yes | **−5.00** |
| Warsh "Anchor"/"Anchored" (fd03d4763d62) | 0.20 / 0.325 | No | +0.120 | Yes | **−5.00** |
| Warsh "Inflation" 40+ (340afae4c4b8) | 0.08 / 0.215 | No | +0.130 | No | **+1.33** |
| Warsh "Echo" (5ed39e44acd1) | 0.75 / 0.475 | Yes | +0.270 | No | **−5.00** |
| Warsh "Scenario" (03962bee9d8d) | 0.30 / 0.465 | No | +0.150 | No | **+4.09** |
| Warsh "Luck"/"Lucky" (e94a328d4e7f) | 0.20 / 0.37 | No | +0.150 | No | **+2.69** |
| Warsh "Labor Force" (0dd29ac81ce4, wide-spread-veto) | 0.30 / 0.47 | No | +0.140 | No | **+3.93** |
| MAHA (0c64397063d4, outside-view-veto) | 0.48 / 0.63 | No | +0.130 | Yes | **−5.00** |
| Egg (56c24f26e025, wide-spread-veto) | 0.45 / 0.735 | No | +0.050 | Yes | **−5.00** |
| Trump NC "Furniture" (3a539d9be02d, wide-spread-veto) | 0.15 / 0.57 | No | +0.250 | No | **+3.33** |
| Sweden Liberals re-forecast 1 (07a026bde227) | 0.23 / 0.49 | No | +0.260 | Yes | **−5.00** |
| Sweden Liberals re-forecast 2 (fb5dc4ef2365) | 0.12 / 0.47 | No | +0.350 | Yes | **−5.00** |
| Sweden Liberals re-forecast 3 (42edbef0f086) | 0.27 / 0.049 | No | +0.221 | Yes | **−5.00** |
| BoE 25bp hike (bc482ffb3606) | 0.20 / 0.061 | Yes | +0.139 | No | **−5.00** |
| BTC touch-$80k Sep14-20 (61bc26d805b6) | 0.84 / 0.79 | Yes | +0.040 | Yes | **+1.25** |
| MV AfD most seats (506bc4c8087e) | 0.90 / 0.77 | Yes | +0.120 | Yes | **+0.28** |
| Berlin CDU most seats (86267581486d) | 0.40 / 0.215 | Yes | +0.180 | No | −1.00 |
| AfD most seats MV (506bc4c8087e) | 0.90 / 0.77 | Yes | +0.120 | Yes | **+0.28** |
| CDU most seats Berlin (86267581486d) | 0.40 / 0.215 | Yes | +0.180 | No | −5.00 |
| Berlin SPD <10% (d0396e9b0cdd, Sep 12) | 0.20 / 0.40 | No | +0.161 | No | **+2.82** |
| Berlin SPD <10% (62f72f65c634, Sep 14) | 0.28 / 0.5675 | No | +0.274 | No | **+6.21** |
| MV SPD >=31% (e056578ff5cf, Sep 14) | 0.81 / 0.86 | No | +0.040 | Yes | −5.00 |
| MV SPD 28-31% (52c0faf90ae2, Sep 14) | 0.24 / 0.095 | Yes | +0.140 | No | −5.00 |
| Berlin Grüne 14-17% (8601f47e8b85) | 0.50 / 0.625 | No | +0.120 | Yes | −5.00 |
| Opus Sep21 snap 1 (668120246d84) | 0.04 / 0.3665 | No | +0.324 | No | +2.86 |
| Opus Sep21 snap 2 (d54f8f258424) | 0.68 / 0.8275 | No | +0.091 | No | +16.83 |
| Resident Evil 55-60m (94f5d2c84c0f) | 0.48 / 0.283 | Yes | +0.174 | No | -5.00 |
| Resident Evil 60-65m (9e900c404320) | 0.44 / 0.6255 | No | +0.131 | Yes | -5.00 |
| Resident Evil 65-70m (299cd54171c9) | 0.03 / 0.0955 | No | +0.061 | No | +0.50 |
| Trump-Greenland Sep23 No (935afbfc7d19) | 0.40 / 0.25 | No | +0.140 | Yes | -5.00 |
| Trump-Greenland Sep23 Yes (a893f32972f0) | 0.90 / 0.74 | Yes | +0.150 | Yes | +1.67 |
| Opus by-Sep30 first read (`b52006c6d15c`) | 0.70 / 0.805 | No | +0.100 | Yes | -5.00 |
| Opus by-Sep30 re-check (`7f1358aa709a`) | 0.60 / 0.855 | No | +0.240 | Yes | -5.00 |
| Opus exact-Sep22 re-check (`9ca6adf96fc8`) | 0.62 / 0.732 | No | +0.098 | Yes | -5.00 |
| Opus exact-Sep22 first read (`3de604a7cf7a`, wide-spread-veto) | 0.48 / 0.6855 | No | +0.127 | Yes | -5.00 |
| Berlin Linke 5-10% margin (`3723b83673c1`, wide-spread-veto, settled 2026-09-22T02:03:42Z, graded in RETRO-20260922-0211, flagged missing by the 10:25Z TRIGGERED cycle today) | 0.40 / 0.754 | No | +0.109 | Yes | -5.00 |
| Lowe's GAAP EPS beat (`df7062f3e89d`, wide-spread-veto, settled 2026-08-19T15:21:17Z, graded in RETRO-20260819-1522, never entered since) | 0.62 / 0.595 | Yes | -0.260 | Yes | +0.68 |
| GPT Luna release by-Sep22 (`328f88bd8da0`) | 0.45 / 0.7205 | No | +0.251 | Yes | -5.00 |
| 30y Treasury hit 5.39% Sep (`03f07792d701`) | 0.42 / 0.615 | No | +0.180 | Yes | -5.00 |
| Xi visit by Sep23 (`f5e8ad23ec2c`) | 0.75 / 0.895 | No | +0.140 | Yes | -5.00 |
| Xi arrival "China" 5+ (`ec3c94c891d7`) | 0.62 / 0.475 | Yes | +0.130 | No | -5.00 |
| Xi arrival "Ballroom" (`6302b86d1d9a`) | 0.85 / 0.735 (No) | No | +0.110 | No | +1.76 |
| 30y Treasury hit 5.42% Sep (`7771a4b3b7ac`) | 0.33 / 0.245 | Yes | -0.040 | Yes | +8.51 |
| 30y Treasury hit 5.45% Sep (`b8d163385f59`) | 0.20 / 0.106 | Yes | +0.090 | Yes | +40.45 |
| Xi toast "Economy" (`9a7a77a71c00`, outside-view-veto) | 0.22 / 0.435 | No | +0.200 | No | +3.62 |
| Xi toast "SI" (`ab5a3803b119`, outside-view-veto) | 0.35 / 0.665 | No | +0.260 | No | +7.82 |
| Xi toast "Trump" (`d805d4abc7c9`, wide-spread-veto) | 0.11 / 0.22 | No | +0.070 | No | +1.10 |
| Xi toast "Garden/Rose" (`cdabc385b3cb`, wide-spread-veto) | 0.15 / 0.28 | No | +0.040 | No | +1.17 |
| Xi toast "Million" 5+ (`b1957ef7af26`, wide-spread-veto; then bet as `674b6cfac193`) | 0.06 / 0.125 | No | +0.060 | No | +0.68 |
| Xi toast "Melania" (`5ee6e91cd3d2`) | 0.83 / 0.68 | Yes | +0.110 | Yes | +1.94 |
| Xi toast "Ballroom" (`f0790f007a85`) | 0.15 / 0.315 | No | +0.140 | Yes | -5.00 |
| Hong WI primary <5% (`03901079bd63`) | 0.09 / 0.089 | Yes | -0.017 | No | -5.00 |
| Hichilema Zambia (`fa185b55a5c3`) | 0.87 / 0.92 | No | +0.040 | Yes | -5.00 |
| Musk 140-159 tweets (`70331099597c`) | 0.007 / 0.052 | No | +0.044 | No | +0.27 |
| Musk 160-179 tweets (`c24926a5c9d7`) | 0.205 / 0.175 | Yes | +0.025 | Yes | +22.78 |
| Musk 200-219 tweets (`7808b6f5a4ef`) | 0.215 / 0.265 | No | +0.045 | No | +1.76 |
| Gold hit $4,600 Aug (`90fafe7b3c2a`) | 0.327 / 0.219 | Yes | +0.099 | Yes | +16.93 |
| Spider-Man domestic gross (`e9f9221a3afb`) | 0.90 / 0.85 | Yes | +0.040 | Yes | +0.81 |
| Beijing 26°C Aug 25 (`25cb8672c568`) | 0.23 / 0.22 | Yes | +0.000 | No | -5.00 |
| GPT-6 by Sep 15 (`846f0e23a43a`) | 0.28 / 0.865 | No | +0.570 | Yes | -5.00 |
| MrBeast wk1 60-70M (`92a9d80fc3c3`) | 0.59 / 0.3835 | Yes | +0.198 | No | -5.00 |
| MrBeast wk1 70-80M (`8adb0a184d87`) | 0.40 / 0.625 | No | +0.210 | Yes | -5.00 |
| MrBeast wk1 60-70M wide-spread (`d842a0332a5a`) | 0.18 / 0.094 | Yes | +0.045 | No | -5.00 |
| MrBeast wk1 70-80M wide-spread (`5badc7031d2c`) | 0.82 / 0.9045 | No | +0.040 | Yes | -5.00 |
| Musk Oct1-3 65-89 (`9238c01df3f3`) | 0.84 / 0.575 | Yes | +0.260 | Yes | +3.62 |
| Musk Oct1-3 40-64 (`eda7406d6518`) | 0.12 / 0.36 | No | +0.230 | No | +2.69 |
| Brazil R1 Lula most votes (`a37c2c7b10f9`) | 0.55 / 0.625 | No | +0.070 | No | +8.16 |
| Brazil Lula by 5-10 (`7ae14fb4b36e`) | 0.35 / 0.12 | Yes | +0.220 | No | -5.00 |
| Brazil Flávio >=39 valid (`4e52c227a60f`) | 0.45 / 0.85 | No | +0.390 | Yes | -5.00 |
| Brazil Lula 2nd (`b350adc7e95c`) | 0.15 / 0.2815 | No | +0.131 | Yes | -5.00 |
| Brazil Lula by <5 (`0137c5dd7495`) | 0.50 / 0.585 | No | +0.080 | No | +6.90 |
| Brazil Flávio >=39 valid (`e6afa32bb249`) | 0.84 / 0.88 | No | +0.030 | Yes | -5.00 |
| Brazil Lula 2nd (`9f0ee045afca`) | 0.45 / 0.3795 | Yes | +0.063 | Yes | +7.90 |
| Brazil Lula by <5 (`1c876ec5d358`) | 0.42 / 0.475 | No | +0.050 | No | +4.45 |
| "Primetime" OW 19-22m (`07bfb21eee33`, OVV) | 0.82 / 0.685 | Yes | +0.100 | No | -5.00 |
| ChatGPT exactly 2 outages Sep (`fe02bf0c9670`, OVV) | 0.15 / 0.915 | No | +0.720 | Yes | -5.00 |
| Gas < $3.75 any state Sep 30 (`0bee87f8d628`, WSV) | 0.03 / 0.24 | No | +0.030 | No | +0.32 |
| Brazil Flávio 2nd (`22d7ab1cf2f3`, superseded) | 0.85 / 0.72 | Yes | +0.120 | No | -5.00 |
| Brazil Renan Santos 3rd (`c9e0968700d5`) | 0.45 / 0.515 | No | +0.060 | No | +5.20 |
| Brazil Lula >=44 valid (`467f58b0ad62`, superseded) | 0.62 / 0.715 | No | +0.080 | Yes | -5.00 |
| Brazil Flávio 45-48 valid (`77ea98a905f9`) | 0.78 / 0.885 | No | +0.090 | Yes | -5.00 |
| DF Senate Bia Kicis 2nd (`5810b4aba221`) | 0.65 / 0.8245 | No | +0.170 | Yes | -5.00 |
| DF Senate Leila 2nd (`87034354d243`) | 0.31 / 0.125 | Yes | +0.180 | No | -5.00 |
| DF Senate Bia Kicis 2nd (`5810b4aba221`) | 0.65 / 0.8245 | No | +0.170 | Yes | -5.00 |
| DF Senate Leila do Volei 2nd (`87034354d243`) | 0.31 / 0.125 | Yes | +0.180 | No | -5.00 |
| "Heart of the Beast" OW bracket (`cec5bff18abf`, OVV) | 0.40 / 0.76 | No | +0.350 | No | +15.00 |
| "Forgotten Island" OW <13m (`bb60348ab311`, OVV) | 0.90 / 0.7525 | Yes | +0.145 | No | -5.00 |
| LGD -1.5 vs Xtreme (`c0ad4f0ec92d`, OVV) | 0.25 / 0.355 | No | +0.080 | No | +2.46 |
| 10y hits 5.25% Sep (`a41e6e996b85`, WSV) | 0.46 / 0.65 | No | -0.020 | Yes | -5.00 |
| Burleson MLB RBI lead (`18a43357718b`, WSV) | 0.93 / 0.73 | Yes | +0.040 | Yes | +0.62 |
| PinkPantheress Best Dance (`e4564b71ab49`, WSV) | 0.30 / 0.37 | No | -0.020 | No | +1.94 |
| MrBeast Gaming 26.75-27.5M (`ba4ad02817d3`, WSV) | 0.85 / 0.875 | No | -0.030 | Yes | -5.00 |
| AI 1530 Arena by Sep 30 (`a93c997dbdf5`, WSV) | 0.93 / 0.891 | Yes | -0.022 | Yes | non-trade (entry 0.952) |
| WTI > $90 Sep 30 (`853c6998ca45`, WSV) | 0.88 / 0.925 | No | -0.010 | Yes | -5.00 |
| ISM Mfg 55.0-55.9 Sep (`4b0493d215d6`, WSV) | 0.283 / 0.395 | No | +0.077 | No | +2.81 |
| Iran sanctions EO by Sep 30 (`e9bfda300d68`, WSV) | 0.04 / 0.215 | No | +0.040 | No | +0.43 |
| Hormuz 0 transits by Oct 31 first read (`d910eebe71cd`, OVV, superseded) | 0.38 / 0.21 | Yes | +0.150 | Yes | +16.74 |
| Lula 44-47% R1 (`a342eb964026`, OVV) | 0.79 / 0.885 | No | +0.080 | Yes | -5.00 |
| CAQ fewer than 1 seat (`607c62b57829`, OVV) | 0.40 / 0.11 | Yes | +0.260 | Yes | +30.71 |
| Grenada win Oct 5 (`321fa9da9ea9`, OVV) | 0.60 / 0.695 | No | +0.090 | No | +11.13 |
| Netflix #1 show 6-9M (`d464b1156ed9`, OVV) | 0.72 / 0.9365 | No | +0.190 | Yes | -5.00 |
| Trump NE rally "Data Center" (`30efc6ceefdd`, OVV) | 0.35 / 0.67 | No | +0.300 | No | +9.29 |
| Trump NE rally "Egg" first read (`5b84cae6b47f`, OVV) | 0.40 / 0.64 | No | +0.190 | Yes | -5.00 |
| Trump NE rally "Egg" re-check (`3b69bfef36a4`, OVV) | 0.74 / 0.605 | Yes | +0.120 | Yes | +3.06 |
| Heart of the Beast OW (`cec5bff18abf`, OVV, backfill Sep 28) | 0.40 / 0.76 | No | +0.350 | No | +15.00 |
| Forgotten Island OW (`bb60348ab311`, OVV, backfill Sep 28) | 0.90 / 0.7525 | Yes | +0.145 | No | -5.00 |
| LGD -1.5 vs Xtreme (`c0ad4f0ec92d`, OVV, backfill Sep 29) | 0.25 / 0.355 | No | +0.080 | Xtreme | +2.46 |
| Saint-François Tanguay (`a3314a17c247`, WSV) | 0.82 / 0.69 | Yes | +0.060 | Yes | +1.58 |
| Hochelaga-Maisonneuve Leduc (`2d634083dd78`, WSV) | 0.75 / 0.87 | No | +0.090 | Yes | -5.00 |
| Saint-Henri-Sainte-Anne Clermont (`0cdee07f6243`, WSV) | 0.56 / 0.70 | No | +0.100 | Yes | -5.00 |
| Bab el-Mandeb 190-209 (`d380a0c3a741`, WSV) | 0.36 / 0.37 | No | -0.060 | Yes | -5.00 |
| Trump NE rally "Tax" 25+ (`c3803f656959`, WSV) | 0.58 / 0.355 | Yes | +0.130 | Yes | +6.11 |
| Trump NE rally "Independent" (`4e4a0c06f526`, WSV) | 0.85 / 0.76 | Yes | +0.040 | Yes | +1.17 |
| 10y 5.25% Sep (`a41e6e996b85`, WSV, superseded, backfill Sep 29) | 0.46 / 0.65 | No | -0.020 | Yes | -5.00 |
| Burleson RBI lead (`18a43357718b`, WSV, backfill Sep 28) | 0.93 / 0.73 | Yes | +0.040 | Yes | +0.62 |
| Stateside award (`e4564b71ab49`, WSV, backfill Sep 28) | 0.30 / 0.37 | No | -0.020 | No | +1.94 |
| MrBeast Gaming 26.75-27M (`ba4ad02817d3`, WSV, backfill Oct 1) | 0.85 / 0.875 | No | -0.030 | Yes | -5.00 |
| AI Arena 1530 by Sep 30 (`a93c997dbdf5`, WSV, backfill Oct 1) | 0.93 / 0.891 | Yes | -0.022 | Yes | refused (entry 0.952) |
| WTI above $90 Sep 30 (`853c6998ca45`, WSV, backfill Oct 1) | 0.88 / 0.925 | No | -0.010 | Yes | -5.00 |
| ISM PMI 55.0-55.9 Sep (`4b0493d215d6`, WSV, backfill Oct 1) | 0.283 / 0.395 | No | +0.077 | No | +2.81 |
| Iran sanctions EO by Sep 30 (`e9bfda300d68`, WSV, backfill Oct 1) | 0.04 / 0.215 | No | +0.040 | No | +0.43 |
| prose-only row, graded in archive (cbbeb134c438) | see archive | Yes | +0.18 | No | −1.00 |
| prose-only row, graded in archive (9618a7d0872d) | see archive | No | +0.06 | No | **+0.22** |
| prose-only row, graded in archive (6317c8ab11b1) | see archive | No | +0.319 | Yes | −1.00 |
| prose-only row, graded in archive (fbc6aff9c7f4) | see archive | No | +0.142 | No | **+0.23** |
| prose-only row, graded in archive (5ae6bf97d6a9) | see archive | No | +0.229 | No | **+0.79** |
| prose-only row, graded in archive (a467140e14e7) | see archive | No | +0.163 | Yes | −1.00 |

### 2026-10-18 16:15Z: AAA gas Oct18 WSV family settled (RETRO-20261018-1615)

| Row | own/mkt | Side | Edge | Result | CF pnl |
|---|---|---|---|---|---|
| AAA gas Oct18 4.29-4.2999 (`23f62eecefcd`, WSV) | 0.47/0.35 | Yes | +0.080 | Yes | +7.82 |
| AAA gas Oct18 4.30-4.3099 (`e88c4535a758`, WSV) | 0.37/0.355 | Yes | -0.120 | No | -5.00 |
| AAA gas Oct18 <4.29 (`475313a77007`, WSV) | 0.11/0.295 | No | +0.040 | No | +0.38 |

  Totals (`core/counterfactual.py ledger --skip-reason wide-spread-veto`): WSV 88 rows, 78
  fillable, 40W/38L, CF -$66.09 (was -$69.29; +7.82 - 5.00 + 0.38 = +3.20 ✓). Side split for
  these three: Yes 1W/1L +2.82, No 1W/0L +0.38. Ruling: no boundary change; the drift model
  (d~N(-1.0c,0.7c)) is n=1 and needs >=3 graded AAA days before a bet cites it.

### 2026-10-21 22:13Z: Meta Q3 headcount ladder settled 66-68k (RETRO-20261021-2213)

- OVV totals: 269 rows, 110W/151L, CF +$170.13 (+15.06: Meta >68k/70k/72k/74k No, all won).
  Disclosure arithmetic (Q2 PR: ~8k impacted, "majority" off headcount by end Q3) beat the book
  by -0.469 dBrier on one event. No boundary change at n=1 event. Pattern to grade: a ladder whose
  centre follows from the company's own published guidance. If a second such event settles with
  the same sign, propose an OVV carve-out like the mechanical-econ one.

### 2026-10-22 00:12Z: Meta/Tesla call words + Paris/Marseille settled (RETRO-20261022-0012)

- WSV totals: 106 rows, 90 fillable, 48W/42L, CF -$64.20 (+2.04, Meta "Advertising" Yes @0.71).
  No boundary change.

### 2026-10-22 02:11Z: Trump SC rally slate settled, all 12 terms said (RETRO-20261022-0211)

- Hormuz/Blockade No bet `afc33780dc6a` lost -$5 (base 2/7 -> now 3/8 rallies said it). Say-the-word
  No bets now 7W/1L, +$12.27. Below-mid tight-book mirror set from 10-01: n=23, -0.731 (was n=19,
  -1.171; the SC sweep cost +0.440). Yes reopen set unchanged n=22, -0.024.
- WSV totals 110 rows, 94 fillable, 51W/43L, CF -$63.36. OVV totals 270 rows, 110W/152L, CF +$165.13
  (Russia/Ukraine No veto saved $5). No boundary change.
- Watch (pre-registered): if the Oct22 Iowa rally slate also sweeps and its below-mid rows cost the
  mirror set >+0.3 again, pause No-side rally bets until a rally-length/topic-sweep check is run.

### 2026-10-22 04:13Z: SC rally late legs settled (RETRO-20261022-0413)

- 6 late SC rows, own vs mid -0.105. The full SC slate was NOT a total sweep: count legs split 3/3
  (Border 20+, Biden/Kamala/Obama 15+, Crime 12+ missed), and "Ass"/"Bitcoin" resolved No. Yes reopen set n=24, -0.061; below-mid mirror set n=24, -0.806.
- Iowa watch refinement: grade single-mention legs and count-threshold legs separately when testing
  the rally-sweep pause. A sweep of single mentions says nothing about count legs on the same night.

### 2026-10-29 20:15Z: Alberta referendum + Saudi/Yemen forecasts settled (RETRO-20261029-2015)

- WSV totals (tool): 165 rows, 141 fillable, 71W/70L, CF -$75.91 (Saudi x Yemen Sep23 `ecca0a61ca2c` No-side lost, WSV saved $5; Alberta Leave-any-division `a99903a45e08` refused by tool). No boundary change.

### 2026-10-30 02:15Z: SC rally legs + WTI>101 + ETH 2200 settled (RETRO-20261030-0215)

- WSV totals (tool): 169 rows, 144 fillable, 72W/72L, CF -$85.36 (WTI>101 `a94a6b8ba179` Yes won but refused by tool at the 0.99 ask, so WSV cost $0). No boundary change; knife-edge-mid SHADOW 8 events paired +0.0395, rally-below-mid SHADOW 4 events paired -0.0132.
