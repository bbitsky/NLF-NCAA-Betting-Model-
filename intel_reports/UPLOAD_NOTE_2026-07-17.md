# Upload Note — 2026-07-17

**Status:** ✅ GitHub upload COMPLETED (first attempt, no retry needed).

Committed 3 files directly to `main` ("Daily intel update 2026-07-17"), commit `d0ed2d1` — 12 commits total:
1. `index.html`
2. `picks_dashboard.html`
3. `daily_intel_2026-07-17.md`

Repo redirected to root after commit; github-pages deployment triggered. Live dashboard: https://bbitsky.github.io/NLF-NCAA-Betting-Model-/

## Notes / decisions made autonomously

- **Chrome extension was connected** this run — the failure mode from the first automated run (2026-07-15) did not recur.
- **Known repo quirk, unchanged:** GitHub's web upload flow drops the `.md` at repo **root**, not inside `intel_reports/`. The repo's `intel_reports/` folder is stale (last touched 2026-06-30). Local copies in `C:\Users\bitsk\Claude\Projects\NFL Betting Model\intel_reports\` remain the source of truth. Not "fixed" here since prior runs established the same pattern — worth a deliberate decision rather than a silent change.
- **No `daily_intel_2026-07-16.md` exists** locally or in the repo. Yesterday's run appears to have been skipped or failed silently. Flagging rather than backfilling.

## Content flags carried from today's report

Today's scan produced **more contradictions than signal**. Four items are unresolved and flagged inline in the report:

1. **Micah Parsons' team** — today's search said Cowboys; the 2026-07-15 report says Packers. Rehab timeline is usable, team attribution is not. **Verify before this touches the model.**
2. **Malik Nabers status** — three mutually inconsistent versions across today's sources and the 07-15 report.
3. **Patriots/Broncos win totals** — source self-contradicted; excluded from the report rather than reported.
4. **Atlanta QB room** (Tua vs. Penix) — flagged for depth-chart verification.

## Recommendation

This task is scheduled to begin ~Aug 26 (2 weeks pre-opener) but is running now, 54 days out. The injury-report, line-movement, and weather sections have no underlying data and will keep returning empty until camps open **July 21–28**, when PUP designations produce the first hard signal. Consider suspending or reducing the daily cadence until then.

---
*Note generated: 2026-07-17*
