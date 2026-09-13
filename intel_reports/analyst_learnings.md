# Analyst Card — Running Learnings

Living file. The Tuesday review task appends to this after grading each week's card.
Sections: Process rules (how we build the card), Pattern log (what the results are telling us), Open questions.

## Process rules (confirmed)

- **Never quote a line from a search-snippet summary.** 2026-09-13: four numbers were wrong (ARI +11.5 → real +9.5; DAL -1.5 → -2.5; NYJ +3 → +1.5; CLE +7 → +9.5). Fetch the Covers week-odds table or the user's book screenshot.
- **Re-check QB status the morning of.** Falcons went Penix → Tua → Cooper Rush in six days. The daily intel run at 1 AM can be stale by kickoff.
- **The model's ledger lags.** picks_ledger.csv rows were from 9/6 for a 9/13 slate. Model confidence is a prior; the current number vs the model's entry number is the edge.
- **Key numbers dominate the .ag mapping.** Saints +7 vs +6.5, Ravens -3 vs -3.5, Cowboys -3 vs -2.7 changed rankings more than any injury did.
- **Tiers:** A = model ≥55% AND number at/better than model entry AND no unpriced injury. B = strong model but worse number, or agreed-with sharps on a weak model number. C = at entry, small conf, or unmodeled injury risk. PASS rows are tracked to learn whether passing was right.

## Pattern log

(empty — first grading is Week 1, review on 2026-09-15)

## Open questions to answer with data

- Do A-tier spreads at a *better* number than the model's entry actually hit more than B/C? (This is the CLV thesis.)
- Do totals with sharp-agree tags outperform model-only totals?
- Weather: does an Under lean on rain/wind-tagged games hit, or is it already priced?
- Are PASS calls on qb-change games correct, or is the market over-adjusting (i.e., should we be *buying* the backup-QB dog)?
- Streaks: after a 0-for-Sunday, does the model's next-week confidence carry any signal, or is it noise?
