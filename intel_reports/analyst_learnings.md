# Analyst Card — Running Learnings

Living file. The Tuesday review task appends to this after grading each week's card.
Sections: Process rules (how we build the card), Pattern log (what the results are telling us), Open questions.

## Process rules (confirmed)

- **Never quote a line from a search-snippet summary.** 2026-09-13: four numbers were wrong (ARI +11.5 → real +9.5; DAL -1.5 → -2.5; NYJ +3 → +1.5; CLE +7 → +9.5). Fetch the Covers week-odds table or the user's book screenshot.
- **Re-check QB status the morning of.** Falcons went Penix → Tua → Cooper Rush in six days. The daily intel run at 1 AM can be stale by kickoff.
- **The model's ledger lags.** picks_ledger.csv rows were from 9/6 for a 9/13 slate. Model confidence is a prior; the current number vs the model's entry number is the edge.
- **Key numbers dominate the .ag mapping.** Saints +7 vs +6.5, Ravens -3 vs -3.5, Cowboys -3 vs -2.7 changed rankings more than any injury did.
- **Tiers:** A = model ≥55% AND number at/better than model entry AND no unpriced injury. B = strong model but worse number, or agreed-with sharps on a weak model number. C = at entry, small conf, or unmodeled injury risk. PASS rows are tracked to learn whether passing was right.
- **Weather flags need a same-day recheck before they drive a pick.** 2026-09-15: two of two early-week weather flags (DAL@NYG rain, DEN@KC wind/precip) had faded to "no material impact" by kickoff per day-of intel scans. Don't let a multi-day-old forecast flag stand in for a game-day check. UPDATE 2026-09-22: Week 2 ran the opposite way — the Gillette (PIT@NE) and MetLife (GB@NYJ) weather flags both correlated with genuinely low-scoring Unders hitting (2-for-2). The rule itself stands (still confirm same-day, still don't let a stale forecast alone drive a pick) but the outcome data is now genuinely mixed (2-for-2 fading in Wk1, 2-for-2 holding in Wk2) rather than one-directional — don't treat "weather flags fade" as settled.
- **Don't ship a prop row with a TBD price/line unless it's a binary anytime-TD market.** Flagged after Week 1 (Etienne rush yds, Evans/Egbuka receptions both NOGRADE). Recurred in Week 2 anyway — Montgomery rush yds, Mayer receptions, and Mac Jones passing yards all shipped TBD and all graded NOGRADE. Get a real number before the card locks or drop the row; this has cost two straight weeks of ungradable prop rows.
- **QB-availability rationale needs a same-day (Sunday-morning) recheck when it names a specific backup by name**, not just when a player carries a questionable/doubtful tag. 2026-09-22: MIA@SF card rows (W2-25, W2-26, W2-H2, W2-P4, W2-P5) were built on "Purdy out/unlikely, Jones starts" — Purdy started and played the whole game. Five rows were built on the wrong premise even though two of them (the spread/total) happened to lose for unrelated reasons anyway.

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

### 2026-09-22 — Week 2 graded (season-to-date: 39-27-2, 59.1%, +8.45u across 68 decided rows)
- Week 2 alone: 26-19-2, 57.8%, +4.64u (spread/total 17-13; team_total 3-2; 1h_spread lean 5-3-2; props 0-2 (3 more NOGRADE); PASS 1 would-WIN, 1 no-side).
- Tier A is 8-3 (+4.27u) combined across two weeks — both Week 2 A-tier totals hit (W2-13 at 64.7% conf, W2-30 at 56.0%). Small n but the tiering is earning its keep so far.
- New structural pattern: the 16:05/16:25 ET kickoff window is now a season-long net loser (12-14-1, -3.09u) vs. 13:00 ET's 22-10-1 (+10.0u). Week 2 produced a 7-game losing streak entirely inside that window (W2-18 through W2-22 plus W2-H9/W2-T2), broken only by W2-23 (the week's best pick). Tier mix is skewed (that window is mostly Tier C) so this isn't a rule change yet, but it's now tracked as its own line item — see open questions.
- Consistent-expression team totals are now 2-for-2 weeks showing "child more robust than parent": Week 1's W1-T1 hit by riding the spread leg after the total leg lost; Week 2's W2-T5 (SF Over 29) hit even though BOTH parent legs (MIA+13.5 spread, Under 45.0 total) lost. Derived team totals (8-3, +4.27u combined) remain the card's best-performing tag.
- Weather rule update: Week 1 was 0-for-2 on weather flags holding up (both faded by kickoff); Week 2 was 2-for-2 the other way (Gillette rain, MetLife wind both correlated with real Unders hitting). Net weather record is now 3-2 combined — treat as genuinely mixed, not a settled pattern.
- Process-rule violations recurred: three more TBD-line props shipped and NOGRADEd (same failure as Week 1), and a QB-availability premise (Purdy "out/unlikely" for MIA@SF) flipped by kickoff and was baked into five card rows. Both are now called out explicitly as process rules above rather than left as one-off notes.
- Home-opener 1H hypothesis (tracked since 2026-09-20) has its first real data: 5-3-1 on the 9 Week 2 rows built on a team's first home game. Positive early read, nowhere near enough to promote to a rule.
- Line-tracker gap is still unresolved — every Week 2 row confirmed `line_snapshots.csv`/`line_history.csv` are still frozen at their original 6/28-7/31 preseason pulls, so CLV remains blank for the entire week and the running average (+0.083 pts) is still only Week 1's 12 rows.

## Open questions to answer with data

- Do A-tier spreads at a *better* number than the model's entry actually hit more than B/C? (This is the CLV thesis.)
- Do totals with sharp-agree tags outperform model-only totals?
- Weather: does an Under lean on rain/wind-tagged games hit, or is it already priced?
- Are PASS calls on qb-change games correct, or is the market over-adjusting (i.e., should we be *buying* the backup-QB dog)?
- Streaks: after a 0-for-Sunday, does the model's next-week confidence carry any signal, or is it noise?
- Does a WATCH-tier row with "no model pick in ledger" earn its card slot, or should those injury/weather watch items just stay in the daily intel report instead of taking a card row that's guaranteed to be a PASS?
- **Does the 16:05/16:25 ET kickoff window underperform structurally, or is it a Tier-C sample artifact?** (Added 2026-09-22.) That window is 12-14-1 (-3.09u) season-to-date vs. 13:00 ET's 22-10-1 (+10.0u), and produced a 7-game losing streak in Week 2 alone. Track by tier within the window before concluding anything — the window may just be disproportionately Tier C rather than bad in itself.
- **Home-opener 1H bump (added 2026-09-20, user hypothesis):** user flagged NE (hosting PIT in Week 2, after opening on the road at SEA in Week 1) as a team likely to get an extra 1H home-field edge in its first home game of the season, and suggested this should generalize to any team playing its first home game. Checked first_half_log.csv: of Week 2's 15 Sun/Mon home teams, 10 are true first-time home teams this season (were road teams in Week 1) — ATL, BAL, CHI, NE, NYJ, TB, DEN, DAL, ARI, SF. The other 5 (HOU, TEN, LAC, KC, LAR) already had their home opener in Week 1. No 1H data exists yet to test this (first_half_log is all Week 1 so far, n=16) — this is an untested hypothesis, not a confirmed pattern. Track 1H performance for these 10 teams specifically in the Week 2 grading pass to start building a read on it.
