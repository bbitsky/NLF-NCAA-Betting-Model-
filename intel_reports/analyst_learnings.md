# Analyst Card — Running Learnings

Living file. The Tuesday review task appends to this after grading each week's card.
Sections: Process rules (how we build the card), Pattern log (what the results are telling us), Open questions.

## Process rules (confirmed)

- **Never quote a line from a search-snippet summary.** 2026-09-13: four numbers were wrong (ARI +11.5 → real +9.5; DAL -1.5 → -2.5; NYJ +3 → +1.5; CLE +7 → +9.5). Fetch the Covers week-odds table or the user's book screenshot.
- **Re-check QB status the morning of.** Falcons went Penix → Tua → Cooper Rush in six days. The daily intel run at 1 AM can be stale by kickoff.
- **The model's ledger lags.** picks_ledger.csv rows were from 9/6 for a 9/13 slate. Model confidence is a prior; the current number vs the model's entry number is the edge.
- **Key numbers dominate the .ag mapping.** Saints +7 vs +6.5, Ravens -3 vs -3.5, Cowboys -3 vs -2.7 changed rankings more than any injury did.
- **Tiers:** A = model ≥55% AND number at/better than model entry AND no unpriced injury. B = strong model but worse number, or agreed-with sharps on a weak model number. C = at entry, small conf, or unmodeled injury risk. PASS rows are tracked to learn whether passing was right.
- **Weather flags need a same-day recheck before they drive a pick.** 2026-09-15: two of two early-week weather flags (DAL@NYG rain, DEN@KC wind/precip) had faded to "no material impact" by kickoff per day-of intel scans. Don't let a multi-day-old forecast flag stand in for a game-day check.

## Pattern log

### 2026-09-14 — Week 1 graded (21 decided bets, 13-8, +3.82u)
- Team-total "consistent expression" bets were the best market (4-1, +2.64u), including one row (W1-T1) that hit despite its total-side parent losing, because the spread-side parent covered. Keep team_total tracked as its own market, not merged into spread/total.
- Two props (Etienne rush yds, Evans/Egbuka receptions) were dead on arrival — TBD lines that never resolved into a gradable number. Process fix: don't ship a prop row with a TBD line; get a real number before the card locks or drop the row.
- Both qb-change PASS rows (ATL/PIT spread, Bijan rush yds) stayed genuinely ungradable — no implied side, by design, because the model's own number was invalidated by the Tua→Rush switch. This is the system working correctly, not a gap.
- Weather tag went 0-2, but both rows trace to the same DAL@NYG game, and recaps said rain had no material impact — not a real test of the weather thesis (see open questions).
- Number-quality buckets (taken vs. model's entered line) are all too small to read yet: BETTER 5-3, EQUAL 0-1, WORSE 2-1. No signal, no rule change.
- Line-tracker gap (dark since 9/4) meant 7 of 12 CLV closing-line reads were 1-3 days stale. CLV average (+0.083 pts) is not trustworthy until the tracker is fixed — see [[line-tracker-gap-2026-09-06]].
- First-half dataset now has 15 games (added the two Wed/Thu Week 1 openers, SEA/NE and SF/LAR, which the Sunday-night log had missed). Early reads only (n<30): 1H ≈ 49.95% of final total; favorites covered half their closing spread at the break 64.3% of the time (9/14, pick'em game excluded).

### 2026-09-15 — Week 1 closed out (MNF graded, card fully resolved)
- Graded the last open row, W1-X5 (DEN@KC MNF, tier WATCH, "no model pick in ledger"): resolved to PASS, no gradable side. KC won 31-10 outright (led 14-7 at half), which would have crushed a naive -2.5 take, but nothing was staked. Decided record stays 13-8, +3.82u — this run didn't add a bet, just closed the book on the week (28/28 card rows now resolved).
- Second data point on early-week weather flags not holding up: W1-X5's rationale flagged Arrowhead wind/precip, but the day-of intel scan found nothing material (same pattern as DAL@NYG's rain flag in Week 1, which recaps said had no impact). Two-for-two on early weather flags fading by kickoff — not proof it's always noise, but reason enough to require a same-day recheck before a weather tag drives a total lean. Added as a process rule below.
- Line-tracker gap (see [[line-tracker-gap-2026-09-06]]) is still unresolved as of 9/15: both `line_snapshots.csv` and `line_history.csv` are frozen at their 6/28–7/27 preseason pulls, so W1-X5 had no usable closing-line snapshot at all. Had to source its Vegas line (KC -2.5, O/U 43.5) informationally from the PFR game page instead; not counted toward the CLV average since the row carried no stake. CLV still not trustworthy until the Windows job is fixed.
- Open process question added: does a WATCH-tier row with no model pick actually earn its card slot, or should injury/weather watch items just live in the daily intel report? W1-X5 generated no bet and only reconfirmed the weather-flag-fades-by-kickoff pattern.

## Open questions to answer with data

- Do A-tier spreads at a *better* number than the model's entry actually hit more than B/C? (This is the CLV thesis.)
- Do totals with sharp-agree tags outperform model-only totals?
- Weather: does an Under lean on rain/wind-tagged games hit, or is it already priced?
- Are PASS calls on qb-change games correct, or is the market over-adjusting (i.e., should we be *buying* the backup-QB dog)?
- Streaks: after a 0-for-Sunday, does the model's next-week confidence carry any signal, or is it noise?
- Does a WATCH-tier row with "no model pick in ledger" earn its card slot, or should those injury/weather watch items just stay in the daily intel report instead of taking a card row that's guaranteed to be a PASS?
