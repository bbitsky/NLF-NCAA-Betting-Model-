# Pre-Season Retrain Check — 2026-08-17

**Verdict: The retrain did NOT complete. Nothing changed materially — the run hung after stage 1, SP+ data still stops at 2024, and metrics.json is unchanged from the 2026-07-26 v4 training run.**

## Step 1 — Did the retrain run?

`retrain_log.txt` is timestamped 2026-08-17 06:00:01, so Task Scheduler did fire the job. But the log is only 50 lines and cuts off mid-stage-1, ending on:

```
Press Enter to close...
```

That's the `download_cfbd_data.py` script (or its wrapper) sitting at an interactive prompt with no one there to press Enter. The batch job never advanced past stage 1 — stage 2 (EPA features) and stage 3 (`build_model.py` retrain) never ran. There's no traceback, no exit code for stages 2/3, because they never started.

Within stage 1 itself, all four CFBD downloads (games, SP+, recruiting, team stats) reported **"⏭️ Already downloaded — skipping"** and pulled nothing new — the script's cache check saw existing 2015–2024 files and didn't attempt a 2025 pull at all.

## Step 2 — Did college data refresh?

No.

- `data/cfbd_sp_ratings.csv` last modified **2026-06-28**, not today.
- Max season in the file: **2024** (2015–2024, same as before).

This is the single most important check and it fails: the whole point of the retrain was to get 2025 SP+ into the model, and that did not happen.

## Step 3 — Walk-forward metrics comparison

`models/metrics.json` last modified **2026-07-26 20:34** — same file as the prior v4 run, not touched today. Confirms build_model.py never ran.

| Metric | Previous (7/26) | Today | Changed? |
|---|---|---|---|
| NFL ATS, 8-season extended (2018–2025, 2174 games) | 49.91% | 49.91% | No |
| NFL ATS, combined 2024+2025 | 50.62% | 50.62% | No |
| NFL ATS 2024 / 2025 | 47.69% / 53.52% | 47.69% / 53.52% | No |
| Production features | baseline | baseline | No |
| Breakeven | 52.40% | 52.40% | — |

Nothing crossed breakeven because nothing ran. `production_features` is still `"baseline"` — EPA remains rejected, as it should. Stakes remain auto-gated off: `ATS_STAKES_OK` requires edge_acc > 0.524, and current edge_acc is 46.2% (2024) / 52.1% (2025) — both below threshold, so `update_predictions.py` will keep stars/Kelly sizing disabled on its own. No sub-breakeven numbers are being presented as progress here — there simply are no new numbers.

## Step 4 — CLV harness status

`python track_lines.py --status`:

```
Snapshot rows      : 9,804
Distinct events    : 398
First poll         : 2026-07-27 14:51:06
Latest poll        : 2026-08-17 11:00:04
Distinct poll times: 7

sport  market  rows
ncaaf     h2h  2438
ncaaf spreads   972
ncaaf  totals   850
  nfl     h2h  4058
  nfl spreads   760
  nfl  totals   726

Lines tracked      : 3,460
Lines that moved   : 1,756 (50.8%)
Median updates/line: 2
```

Running since 2026-07-27 as expected, 7 poll cycles over ~3 weeks, half of tracked lines have moved at least once. `data/picks_ledger.csv` exists (last written 2026-08-16), so picks are being logged against live lines.

## Step 5 — Open decision: line shopping

Still undecided. The harness currently scores CLV against a three-book consensus rather than the best price actually available at bet time. Half a point on an NFL spread is worth roughly 1.5–2% of win rate — bigger than any edge this model has shown in eight seasons of walk-forward testing. Until that's resolved, CLV readings will flatter or penalize the model depending on which book happened to move, independent of whether the picks themselves are any good.

## What to do next

The retrain didn't fail loudly — it's parked at a prompt. Double-click `run_season_retrain.bat` and it should pick up where stage 1 left off (or restart cleanly); if `download_cfbd_data.py` prompts again, that prompt needs to be found and removed (likely an interactive confirmation before overwriting cached CSVs, or a leftover `pause`/`input()` call) so the scheduled run can complete unattended next time. I'll re-check once you've re-run it.
