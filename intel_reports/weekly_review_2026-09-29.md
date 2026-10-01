# Weekly Card Review — Week 3 (graded 2026-09-29)

**Week 3: 13-14-1, -2.18u (48.1%)** · **Season: 52-41-3, +6.27u (55.9%)** · units at -110 equivalent (win +0.909, loss -1, push 0); decided = WIN/LOSS/PUSH only (PASS/NOGRADE excluded).

Sources: all 15 Thu/Sun games graded from Pro-Football-Reference boxscores (quarter lines + player stats). MNF PHI@CHI (PFR not yet posted) graded from ESPN, CBS Sports and VAVEL finals (27-7), with halftime (CHI 10-7) from NBC PFT. Closing lines come from the last pre-kickoff pull in `line_snapshots.csv` (median of DK, FD and MGM). For Sunday games that pull is **9/26 11:00 ET, about 1 day before kickoff, not a true game-day close**. There was no pull for MIN@TB.

Data fix made while grading: the five TNF rows (W3-01, W3-02, W3-T1, W3-H1, W3-X1) had an unquoted comma in `book` ("covers.com (Kalshi board, lines as of 9-23)") that shifted every later column. I quoted the field. Older W1/W2 rows still have unquoted commas inside `notes`, which break a strict CSV parse. They grade correctly, but a cleanup pass would help.

---

## Last Week Scorecard

| ID | Tier | Pick | Line | Result | Margin | Close | CLV |
|---|---|---|---|---|---|---|---|
| W3-01 | C | ATL +5.5 (at GB) | 5.5 | WIN | +26.5 | ATL +5.0 | +0.5 |
| W3-02 | B | UNDER 43.5 (ATL@GB) | 43.5 | LOSS | -5.5 | 43.0 | +0.5 |
| W3-T1 | C | ATL TT UNDER 19 (implied) | 19 | LOSS | -16 | – | – |
| W3-H1 | B | GB 1H fav (vs -2.75 half-spread) | TBD | LOSS | -12.75 | – | – |
| W3-X1 | PASS | no prop | – | PASS | – | – | – |
| W3-03 | C | LAC +7 (at BUF) | 7 | LOSS | -1 | LAC +7.0 | 0 |
| W3-04 | C | UNDER 42 (CAR@CLE) | 42 | WIN | +3 | 42.5 | -0.5 |
| W3-05 | B | UNDER 48.5 (NYJ@DET) | 48.5 | LOSS | -6.5 | 48.5 | 0 |
| W3-06 | B | HOU -1.5 (at IND) | -1.5 | LOSS | -3.5 | HOU -2.0 | +0.5 |
| W3-07 | C | UNDER 45 (KC@MIA) | 45 | WIN | +11 | 45.5 | -0.5 |
| W3-08 | B | UNDER 37.5 (TEN@NYG) | 37.5 | WIN | +18.5 | 37.5 | 0 |
| W3-09 | C | WAS +9 (vs SEA) | 9 | WIN | +11 | WAS +7.5 | +1.5 |
| W3-10 | B | ARI +7.5 (at SF) | 7.5 | WIN | +1.5 | ARI +8.5 | -1.0 |
| W3-11 | A | OVER 48 (ARI@SF) | 48 | WIN | +18 | 47.5 | -0.5 |
| W3-12 | C | TB +1 (vs MIN) | 1 | LOSS | -6 | n/a | – |
| W3-13 | C | OVER 42.5 (MIN@TB) | 42.5 | LOSS | -3.5 | n/a | – |
| W3-14 | B | BAL -3 (vs DAL) | -3 | PUSH | 0 | BAL -3.5 | +0.5 |
| W3-15 | C | LV +3.5 (at NO) | 3.5 | WIN | +11.5 | LV +3.0 | +0.5 |
| W3-16 | A | OVER 43.5 (LV@NO) | 43.5 | WIN | +18.5 | 43.5 | 0 |
| W3-T2 | B | ARI TT OVER 20.5 (implied) | 20.5 | WIN | +9.5 | – | – |
| W3-T3 | B | LV TT OVER 20 (implied) | 20 | WIN | +15 | – | – |
| W3-T4 | C | NYG TT UNDER 20 (implied) | 20 | WIN | +8 | – | – |
| W3-H2 | PASS | (KC 1H -6.5 -115) | -6.5 | PASS-would-WIN | +0.5 | – | – |
| W3-H3 | C | DET 1H -4 | -4 | LOSS | -1 | – | – |
| W3-P1 | C | Davante Adams anytime TD | +133 | LOSS | – | – | – |
| W3-P2 | PASS | (Deebo Samuel anytime TD) | +203 | PASS-would-WIN | – | – | – |
| W3-P3 | C | Oronde Gadsden anytime TD | +317 | LOSS | – | – | – |
| W3-P4 | C | David Montgomery anytime TD | -113 | LOSS | – | – | – |
| W3-X2 | PASS | (model Over 50.5 LAC@BUF) | 50.5 | PASS-would-LOSS | -10.5 | 50.25 | – |
| W3-X3 | PASS | coin flip CAR/CLE | 2.5 | PASS | – | – | – |
| W3-X4 | PASS | (model NYJ +6.5) | 6.5 | PASS-would-LOSS | -0.5 | NYJ +6.5 | – |
| W3-X5 | PASS | (model Over 42.5 HOU@IND) | 42.5 | PASS-would-LOSS | -6.5 | 42.5 | – |
| W3-X6 | PASS | NE/JAX spread+total | 2.5 | PASS | – | – | – |
| W3-X7 | PASS | (model KC -9.5) | -9.5 | PASS-would-WIN | +4.5 | KC -10.5 | – |
| W3-X8 | PASS | NYG -2.5 (qb-change, void) | -2.5 | PASS | – | NYG -2.5 | – |
| W3-X9 | PASS | (model CIN -3.5 / Under 42.5) | -3.5 | PASS-would-LOSS | -6.5 | CIN -3.5 / 42.5 | – |
| W3-X10 | PASS | SEA/WAS Over (qb-change, void) | 40 | PASS | – | 40.25 | – |
| W3-X11 | PASS | (model Over 53.5 BAL/DAL) | 53.5 | PASS-would-WIN | +11.5 | 53.5 | – |
| W3-18 | C | LAR -1.5 (at DEN) | -1.5 | LOSS | -5.5 | LAR -2.5 | +1.0 |
| W3-X12 | PASS | (model Over 44 LAR/DEN) | 44 | PASS-would-WIN | +12 | 44.5 | – |
| W3-17 | C | CHI +3.5 (vs PHI) | 3.5 | WIN | +23.5 | CHI +4.5 | -1.0 |
| W3-T5 | C | CHI TT UNDER 19 (implied) | 19 | LOSS | -8 | – | – |
| W3-X13 | PASS | PHI/CHI Under (qb-change, void) | 41.5 | PASS | – | 41.5 | – |

Finals: ATL 35-14 GB · LAC 16-24 BUF · CAR 18-21 CLE · NYJ 24-31 DET · HOU 17-19 IND · KC 24-10 MIA · TEN 7-12 NYG · SEA 31-33 WAS · CIN 27-30 PIT · NE 6-35 JAX · ARI 30-36 SF · MIN 23-16 TB · BAL 34-31 DAL · LV 35-27 NO · LAR 26-30 DEN · PHI 7-27 CHI. **Underdogs won outright in 8 of 16 games.**

---

## Season-to-Date Record

| | Record | Units | Win% |
|---|---|---|---|
| Week 1 | 13-8-0 | +3.82 | 61.9 |
| Week 2 | 26-19-2 | +4.64 | 57.8 |
| Week 3 | 13-14-1 | -2.18 | 48.1 |
| **Season** | **52-41-3** | **+6.27** | **55.9** |

### By tier
| Tier | Season | Units | Week 3 | Units |
|---|---|---|---|---|
| A | 10-3-0 | +6.09 | 2-0-0 | +1.82 |
| B | 13-10-1 | +1.82 | 4-4-1 | -0.36 |
| C | 29-28-2 | -1.64 | 7-10-0 | -3.64 |

### By market
| Market | Season | Units | Week 3 | Units |
|---|---|---|---|---|
| spread | 18-12-1 | +4.36 | 5-4-1 | +0.55 |
| total | 17-12-0 | +3.45 | 5-3-0 | +1.55 |
| team_total | 10-5-0 | +4.09 | 3-2-0 | +0.73 |
| 1h_spread | 5-5-2 | -0.45 | 0-2-0 | -2.00 |
| prop | 2-7-0 | -5.18 | 0-3-0 | -3.00 |

### By tag (rows can carry several tags)
| Tag | Season | Units | Week 3 | Units |
|---|---|---|---|---|
| (none) | 12-5-0 | +5.91 | 1-0-0 | +0.91 |
| consistent-expression | 11-5-0 | +5.00 | 3-2-0 | +0.73 |
| derived | 15-10-2 | +3.64 | 3-4-0 | -1.27 |
| sharp-agree | 3-0-0 | +2.73 | 1-0-0 | +0.91 |
| weather | 5-2-0 | +2.55 | 2-0-0 | +1.82 |
| key-number | 6-3-1 | +2.45 | 3-1-1 | +1.73 |
| qb-change | 6-4-0 | +1.45 | 5-2-0 | +2.55 |
| home-opener | 6-4-1 | +1.45 | 1-1-0 | -0.09 |
| coin-flip | 2-2-0 | -0.18 | – | – |
| conditional | 1-1-0 | -0.09 | 1-1-0 | -0.09 |
| sharp-conflict | 0-1-0 | -1.00 | – | – |
| line-move | 9-10-0 | -1.82 | 4-6-0 | -2.36 |
| **injury** | **8-16-0** | **-8.73** | **2-8-0** | **-6.18** |

### By kickoff window
| Window | Season | Units | Week 3 | Units |
|---|---|---|---|---|
| 13:00 | 27-16-1 | +8.55 | 5-6-0 | -1.45 |
| 16:05/16:25 | 18-16-2 | +0.36 | 6-2-1 | +3.45 |
| night (TNF/SNF/MNF) | 7-9-0 | -2.64 | 2-6-0 | -4.18 |

Window by tier, season: 16:05/16:25 is A 4-2, **B 8-3-1**, **C 6-11-1**. Night is A 1-0, **B 0-3**, C 6-6. 13:00 is A 5-1, B 5-4, C 17-11-1.

### Consistent-expression team totals: parent vs child (season, n=15)
| | Child hit | Child miss |
|---|---|---|
| **Parent hit** | 8 | 1 (W3-T5) |
| **Parent missed** | 1 (W2-T5) | 4 |
| **Parent split** | 1 (W1-T1) | 0 |

The child follows the parent 12 of 15 times. The "child more robust than parent" read from Week 2 rested on 2 rows; this week added one row in the opposite direction (CHI +3.5 won, CHI TT Under lost).

### Number quality (spread/total rows: taken line vs model entry parsed from rationale)
| Bucket | Record | Units |
|---|---|---|
| Better than model entry | 12-12-1 | -1.09 |
| Equal to model entry | 13-6-0 | +5.82 |
| Worse than model entry | 8-5-0 | +2.27 |
| n/a (model void or on the other side) | 2-1-0 | +0.82 |

Still no evidence that "better than model" means edge. The model entries are stale (9/06–9/19), so a "better" number often just reflects news the model hasn't seen (W3-05, W3-12, W3-13, W3-18 all lost).

### CLV (28 rows with a close: 12 from Week 1, 16 from Week 3; Week 2 has none)
- Average **+0.089 pts** (Week 1 +0.083, Week 3 +0.094).
- Week 3 split: 7 beat the close, 4 equal, 5 worse.
- Beat close 5-5-1 · equal 6-4 · worse 6-1. This is noise at this sample size, and the "close" is a 1-day-old pull.

### Weather-tagged rows
- Season 5-2 (+2.55u). **Unders on weather games 4-1** (W2-11, W2-13, W3-08, W3-T4 won; the W1-T5 miss was the DAL@NYG rain flag that faded).
- Week 3: TEN@NYG nor'easter was confirmed the same day (21.7 mph wind, 86% precip) and finished at 19 total. Both rows won.

### PASS analysis
- Season: 6 would-WIN, 5 would-LOSS, 11 with no gradable side. Week 3: 5 would-WIN, 4 would-LOSS, 6 no side.
- Passes that were right in Week 3: X2, X4, X5, X9 (stale-model Overs and CIN).
- Passes that were wrong: X7 (KC), X11 (BAL/DAL Over, passed on **sharp-conflict**), X12 (LAR/DEN Over), H2 (KC 1H by the hook), P2 (Deebo TD, +203).
- **Sharp-conflict passes: 0-2 on would-have results** (W2-X1 CIN, W3-X11 Over). In both, the sharp side lost.
- **qb-change passes (no gradable side by rule):** W3-X8, X10 and X13 have no staked side. For reference, the model's nominal side would have won all three (NYG -2.5 won by 5, WAS/SEA Over hit at 64, PHI/CHI Under hit at 34). Across Weeks 1–3 (5 rows), none are gradable.

---

## Streaks
- Current overall: **1 loss** (W3-T5, MNF). The last 8 in order were P, W, W, W, L, L, W, L.
- Longest overall season-to-date: **5 wins, 7 losses** (the 7-loss run was Week 2's late window).
- Tier A: **4-win streak** (current). Longest 4 W / 2 L.
- Tier B: current 4 wins. Longest 5 W / 4 L.
- Tier C: current 1 loss. Longest 5 W / 6 L.

(Ordered by game date, then kickoff time.)

---

## First-Half Findings (first_half_log.csv, n=48, Weeks 1–3; past the 30-game threshold)
- **1H share of full-game total: 48.3%** (average 1H total 22.1). Week 3 alone: 45.5%. The earlier ~49–50% estimate has drifted down.
- **Favorites covering half the closing spread at the break: 25-20 (55.6%)**, down from 62.1% (18/29) quoted on the Week 3 card. Week 3 went 7-9. Favorites of 6.5 or more: 9/15 (60%), 2/5 in Week 3.
- **1H total vs 0.47 × closing total: 24 over / 24 under.** The 0.47 multiplier looks calibrated, with no directional edge.
- **Weather effect:** rain games average 13.8 1H points and 28.8 final (n=5); wind games 18.5 and 45.0 (n=4); domes 23.0 and 48.4 (n=14). Rain, wind and wet-field games went **Under the closing total 7 of 10 times**. The heat game (BAL/DAL Rio) went 65 total, over.
- Week 3's 8 outright underdog winners dragged the favorite-1H numbers down. Six dogs led at the half (ATL, CLE, IND, WAS, LV, CHI).

---

## What Worked / What Didn't
1. **Tier A keeps earning (10-3, +6.09u; 2-0 this week).** Both Week 3 A-tier rows were Overs at or better than the model entry (W3-11 at 48, W3-16 at 43.5) and won by 18+. Tier C is 29-28-2, roughly break-even minus juice. All of the season's profit sits in A and B.
2. **Injury-narrative rows are the leak: `injury` tag 8-16, -8.73u (2-8 this week).** Anytime-TD props built on "role vacancy" are **0-6 season-to-date** (Etienne, Montgomery x2, Black, Adams, Gadsden). The vacated-role player never scored. Adams got his volume (13 targets, 137 yards) but the TDs went elsewhere.
3. **The backup-QB underdog paid 2-for-2 (WAS +9, CHI +3.5, both won outright).** In both games the line moved 5+ points on public money through key numbers, and the nominal model side won in all three qb-change passes. This is the first direct data on the open question "should we buy the backup-QB dog?" It points toward yes, but n=2.
4. **Same-day-confirmed weather Unders hit again (TEN/NYG 19 total).** Weather Unders are 4-1. The only miss was the one flag that faded before kickoff, which is exactly what the recheck rule is meant to catch.
5. **1H favorite leans went 0-2 and the base rate fell to 55.6%.** The 62% figure the card leaned on was a small-sample high. W3-H3 laid -4 against a -3.25 half-spread and lost by one point.

---

## Adjustments for Next Card
1. **Props:** no anytime-TD prop built only on "teammate out / role vacancy" (0-6). A TD prop now needs a real price and a player who already holds a goal-line or red-zone role. Cap props at 2 per card. This is a structural change (the thesis type is 0-6 across three weeks), not a tier change.
2. **1H spreads:** use the updated base rate (favorites 55.6%, n=45). Only list a 1H favorite when the offered 1H line is **at or below** half the full-game spread. Otherwise PASS, as with W3-H2 (which would have won by the hook, so this is a price rule, not a direction rule).
3. **Backup-QB dog:** keep grading these as **C** (n=2, early). Tag them `backup-qb-dog` so they're counted separately. Require the line to have moved 3+ points through at least one key number, and take the best book number available.
4. **Sharp-conflict:** don't auto-PASS a model side ≥53% on sharp conflict alone. Log it as a C lean with a `sharp-conflict` tag so it gets graded (would-have record 0-2 against the sharps). Early, no tier change.
5. **Closing lines:** CLV is only meaningful with a Sunday-morning pull. Ask the line tracker for an 11:30 ET Sunday snapshot (and one before TNF/MNF kickoffs). MIN@TB was missing entirely.
6. **Night games, Tier B:** 0-3 this season. No rule change (n=3); flag night B rows in the rationale.

---

## Open Questions
- Is the backup-QB dog a real market over-adjustment or two lucky outright wins? Track `backup-qb-dog` rows to n≥10.
- Does the Tier C drag come from specific tags? `line-move` 9-10 and `injury` 8-16 are both concentrated in C. Should C rows with those tags be cut from the card?
- The 16:05/16:25 "structural" worry looks like a Tier C artifact (window B 8-3-1, C 6-11-1). Keep watching night games instead.
- Home-opener 1H hypothesis: 6-4-1 on tagged rows season-to-date. Home openers are mostly done after Week 3, so this may simply stop producing data.
- **Intel data quality:** the 9/28 daily intel "Social Pulse" mentions a Ravens 1-3 start and a Cowboys-Packers 40-40 tie. Neither matches the PFR results (BAL is 2-1). Several roster notes on the card were also wrong by kickoff (McCaffrey "on IR" played in Week 3; Kyler Murray started for MIN). Check where those intel items come from before trusting injury and roster notes.
- The Week 1 CLV closes are 1–3 days stale, and Week 3's are about 1 day stale. The +0.089 average is not decision-grade yet.
