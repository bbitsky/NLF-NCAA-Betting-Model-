"""
generate_dashboard.py — Refreshes picks_dashboard.html's picks tables and
summary stats from the CURRENT picks_latest.csv / picks_ncaaf_latest.csv /
models/metrics.json.
===========================================================================
Problem this fixes (found 2026-09-20): the daily GitHub Pages push
(push_to_github.py) only ever refreshed the Intel tab. The NFL/NCAAF picks
tables were a static snapshot baked into picks_dashboard.html back when the
dashboard was first built (June/July 2026) and were NEVER regenerated after
that — so the live site kept showing months-old games/confidences/stakes
while the Intel tab looked freshly updated every day.

This script replaces the regions marked with HTML/JS comments
(NFL_DATA / NCAAF_DATA / HEADER_GENERATED / TRAINED_ON / *_TAB_COUNT /
NFL_BANNER / NFL_STATS / NCAAF_STATS) with freshly computed content, leaving
everything else (layout, CSS, JS logic, Intel/Weekly tabs, Bet Tracker) untouched.

Run this:
  - right after run_predictions.bat generates fresh picks (wired in), and
  - as a safety net inside push_to_github.py, right before it commits.
"""

import os, re, sys, json
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import pandas as pd
from datetime import datetime

DATA_DIR = r"C:\Users\bitsk\Claude\Projects\NFL Betting Model\data"
BASE_DIR = r"C:\Users\bitsk\Claude\Projects\NFL Betting Model"
MODEL_DIR = os.path.join(BASE_DIR, "models")
DASHBOARD_PATH = os.path.join(BASE_DIR, "picks_dashboard.html")
NFL_PICKS_PATH = os.path.join(BASE_DIR, "picks_latest.csv")
NCAAF_PICKS_PATH = os.path.join(BASE_DIR, "picks_ncaaf_latest.csv")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

BREAKEVEN = 0.524


def replace_marker(html, name, new_inner):
    """Replace the content between <!-- name_START --> and <!-- name_END -->
    (or // name_START / // name_END for JS regions), keeping the markers."""
    pattern = re.compile(
        r'((?:<!--|//)\s*' + re.escape(name) + r'_START\s*(?:-->)?)(.*?)((?:<!--|//)\s*' + re.escape(name) + r'_END)',
        flags=re.S)
    m = pattern.search(html)
    if not m:
        print(f"  ⚠ marker {name} not found — skipped")
        return html
    return html[:m.start()] + m.group(1) + new_inner + m.group(3) + html[m.end():]


def pct(x):
    return "" if x is None else f"{x:.1f}"


def num_or_zero(s):
    if pd.isna(s) or s == "":
        return 0.0
    return float(str(s).replace("%", ""))


def js_str(s):
    return json.dumps("" if pd.isna(s) else str(s))


def build_nfl_js(df):
    rows = []
    for _, r in df.iterrows():
        rows.append(
            "  {date:%s,time:%s,matchup:%s,spread_line:%s,total_line:%s,"
            "ats_pick:%s,ats_conf_num:%s,ats_kelly_num:%s,ats_edge:%s,"
            "tot_pick:%s,tot_conf:%s}" % (
                js_str(r.get("date")), js_str(r.get("time")), js_str(r.get("matchup")),
                r.get("spread_line") if pd.notna(r.get("spread_line")) else "null",
                r.get("total_line") if pd.notna(r.get("total_line")) else "null",
                js_str(r.get("ats_pick")), num_or_zero(r.get("ats_conf")),
                num_or_zero(r.get("ats_kelly")), js_str(r.get("ats_edge")),
                js_str(r.get("tot_pick")), js_str(r.get("tot_conf")),
            ))
    return "const NFL = [\n" + ",\n".join(rows) + ("\n" if rows else "") + "];"


def build_ncaaf_js(df):
    rows = []
    for _, r in df.iterrows():
        rows.append(
            "  {date:%s,matchup:%s,spread_line:%s,pred_margin:%s,"
            "ats_pick:%s,ats_conf_num:%s,ats_kelly_num:%s,ats_edge:%s}" % (
                js_str(r.get("date")), js_str(r.get("matchup")),
                r.get("spread_line") if pd.notna(r.get("spread_line")) else "null",
                r.get("pred_margin") if pd.notna(r.get("pred_margin")) else "null",
                js_str(r.get("ats_pick")), num_or_zero(r.get("ats_conf")),
                num_or_zero(r.get("ats_kelly")), js_str(r.get("ats_edge")),
            ))
    return "const NCAAF = [\n" + ",\n".join(rows) + ("\n" if rows else "") + "];"


def edge_record(metrics, section):
    d = metrics.get(section, {})
    n = sum(r.get("edge_games", 0) for s, r in d.items() if s.isdigit() and isinstance(r, dict))
    if not n:
        return None, 0
    acc = sum((r.get("edge_acc") or 0) * r.get("edge_games", 0)
              for s, r in d.items() if s.isdigit() and isinstance(r, dict)) / n
    return acc, n


def weighted(metrics, section, key):
    d = metrics.get(section, {})
    rows = [r for s, r in d.items() if s.isdigit() and isinstance(r, dict) and r.get(key) is not None]
    n = sum(r.get("games", 0) for r in rows)
    if not n:
        return None, 0
    val = sum(r[key] * r.get("games", 0) for r in rows) / n
    return val, n


def main():
    print("=" * 60)
    print("  DASHBOARD GENERATOR (picks tables + summary stats)")
    print("=" * 60)

    if not os.path.exists(DASHBOARD_PATH):
        print("  ❌ picks_dashboard.html not found — skipping.")
        return

    with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    metrics = {}
    if os.path.exists(METRICS_PATH):
        metrics = json.load(open(METRICS_PATH))
    else:
        print("  ⚠ models/metrics.json not found — stat tiles will keep their previous values.")

    nfl_df = pd.read_csv(NFL_PICKS_PATH) if os.path.exists(NFL_PICKS_PATH) else pd.DataFrame()
    ncaaf_df = pd.read_csv(NCAAF_PICKS_PATH) if os.path.exists(NCAAF_PICKS_PATH) else pd.DataFrame()
    print(f"  NFL picks: {len(nfl_df)} games | NCAAF picks: {len(ncaaf_df)} games")

    # ── picks data arrays ──
    html = replace_marker(html, "NFL_DATA", "\n" + build_nfl_js(nfl_df) + "\n")
    html = replace_marker(html, "NCAAF_DATA", "\n" + build_ncaaf_js(ncaaf_df) + "\n")

    # ── header: generated date + trained-on line ──
    gen_times = []
    for df in (nfl_df, ncaaf_df):
        if "generated" in df.columns and len(df):
            gen_times += list(pd.to_datetime(df["generated"], errors="coerce").dropna())
    gen_dt = max(gen_times) if gen_times else datetime.now()
    html = replace_marker(html, "HEADER_GENERATED", "Generated " + gen_dt.strftime("%B %-d, %Y · %-I:%M %p"))

    n_nfl_train = n_ncaaf_train = None
    try:
        sched_path = os.path.join(DATA_DIR, "nfl_schedules.csv")
        if os.path.exists(sched_path):
            sched = pd.read_csv(sched_path, low_memory=False)
            n_nfl_train = int(sched["result"].notna().sum())
    except Exception:
        pass
    try:
        games_path = os.path.join(DATA_DIR, "cfbd_games.csv")
        if os.path.exists(games_path):
            g = pd.read_csv(games_path, low_memory=False)
            n_ncaaf_train = int(((g["homeClassification"] == "fbs") & (g["awayClassification"] == "fbs") &
                                  (g["seasonType"] == "regular") & g["homePoints"].notna()).sum())
    except Exception:
        pass
    if n_nfl_train and n_ncaaf_train:
        html = replace_marker(html, "TRAINED_ON",
            f"XGBoost · Trained on {n_nfl_train:,} NFL + {n_ncaaf_train:,} NCAAF games")

    # ── tab counts ──
    html = replace_marker(html, "NFL_TAB_COUNT", str(len(nfl_df)))
    html = replace_marker(html, "NCAAF_TAB_COUNT", str(len(ncaaf_df)))

    # ── NFL banner + stats (only if metrics available) ──
    if metrics:
        ats_ext = metrics.get("nfl_ats", {}).get("extended", {})
        ats_acc = ats_ext.get("acc")
        ats_2024 = metrics.get("nfl_ats", {}).get("2024", {}).get("acc")
        ats_2025 = metrics.get("nfl_ats", {}).get("2025", {}).get("acc")
        ats_n = ats_ext.get("games")
        ats_edge_acc, ats_edge_n = edge_record(metrics, "nfl_ats")
        ats_stakes_ok = ats_edge_acc is not None and ats_edge_acc > BREAKEVEN

        tot_acc, tot_n = weighted(metrics, "nfl_totals", "acc")
        tot_2024 = metrics.get("nfl_totals", {}).get("2024", {}).get("acc")
        tot_2025 = metrics.get("nfl_totals", {}).get("2025", {}).get("acc")
        tot_edge_acc, tot_edge_n = edge_record(metrics, "nfl_totals")
        tot_stakes_ok = tot_edge_acc is not None and tot_edge_acc > BREAKEVEN

        brier, _ = weighted(metrics, "nfl_ats", "brier")

        stakes_note = (
            f"ATS edge picks {('ABOVE' if ats_stakes_ok else 'below')} breakeven "
            f"({(ats_edge_acc or 0):.1%} on {ats_edge_n} games) — stakes "
            f"{'ENABLED' if ats_stakes_ok else 'DISABLED (informational only)'}. "
            f"Totals edge picks {(tot_edge_acc or 0):.1%} on {tot_edge_n} games — stakes "
            f"{'enabled' if tot_stakes_ok else 'disabled'}."
        )
        prod_feats = metrics.get("nfl_ats", {}).get("production_features", "baseline")
        banner = (
            '<div style="background:#3a2b12;border:1px solid #8a6d1a;color:#e8c96a;'
            'padding:10px 16px;border-radius:8px;margin:10px 0;font-size:14px;">'
            f'⚠ <strong>Honest walk-forward results</strong> (production features: {prod_feats}). '
            f'Long-run ATS accuracy is {(ats_acc or 0):.1%} vs a {BREAKEVEN:.1%} breakeven — '
            f'{stakes_note} Picks below reflect the model trained on {gen_dt.strftime("%Y-%m-%d")}.'
            '</div>'
        )
        html = replace_marker(html, "NFL_BANNER", banner)

        nfl_stats = f'''
  <div class="stats-bar">
    <div class="stat-card stat-nfl1">
      <div class="label">NFL ATS Accuracy (walk-forward)</div>
      <div class="value">{(ats_acc or 0):.1%}</div>
      <div class="sub">Long-run 2018-25 walk-forward ({ats_n or 0:,} games) · 2024: {(ats_2024 or 0):.1%} · 2025: {(ats_2025 or 0):.1%} · breakeven {BREAKEVEN:.1%}</div>
    </div>
    <div class="stat-card stat-nfl2">
      <div class="label">NFL Totals Accuracy (walk-forward)</div>
      <div class="value">{(tot_acc or 0):.1%}</div>
      <div class="sub">2024: {(tot_2024 or 0):.1%} · 2025: {(tot_2025 or 0):.1%} · breakeven {BREAKEVEN:.1%}</div>
    </div>
    <div class="stat-card" style="background:var(--card)">
      <div class="label">Brier Score</div>
      <div class="value" style="color:var(--green)">{(brier or 0):.3f}</div>
      <div class="sub">Well-calibrated ATS probabilities</div>
    </div>
    <div class="stat-card stat-games">
      <div class="label">Games This Period</div>
      <div class="value">{len(nfl_df)}</div>
      <div class="sub" id="nfl-edge-sub">Loading…</div>
    </div>
  </div>
  '''
        html = replace_marker(html, "NFL_STATS", nfl_stats)

        # ── NCAAF stats ──
        nc = metrics.get("ncaaf", {})
        nc_2024 = nc.get("2024", {})
        nc_2025 = nc.get("2025", {})
        nc_ats_acc, nc_ats_n = weighted(metrics, "ncaaf", "ats_acc")
        nc_mae, _ = weighted(metrics, "ncaaf", "mae")
        ncaaf_stats = f'''
  <div class="stats-bar">
    <div class="stat-card stat-ncaaf">
      <div class="label">NCAAF ATS vs Closing Line</div>
      <div class="value">{(nc_ats_acc or 0):.1%}</div>
      <div class="sub">2024: {(nc_2024.get('ats_acc') or 0):.1%} · 2025: {(nc_2025.get('ats_acc') or 0):.1%} · vs closing book lines</div>
    </div>
    <div class="stat-card" style="background:var(--card)">
      <div class="label">NCAAF Margin MAE</div>
      <div class="value" style="color:var(--orange)">{(nc_mae or 0):.1f} pts</div>
      <div class="sub">Mean absolute error vs actual margin</div>
    </div>
    <div class="stat-card" style="background:var(--card)">
      <div class="label">Top Feature</div>
      <div class="value" style="color:var(--purple);font-size:18px">SP+ Diff</div>
      <div class="sub">Bill Connelly ratings (importance not recomputed this run)</div>
    </div>
    <div class="stat-card stat-games">
      <div class="label">Games This Period</div>
      <div class="value">{len(ncaaf_df)}</div>
      <div class="sub" id="ncaaf-edge-sub">Loading…</div>
    </div>
  </div>
  '''
        html = replace_marker(html, "NCAAF_STATS", ncaaf_stats)
    else:
        print("  ⚠ Skipped banner/stat-tile refresh (no metrics.json)")

    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ Dashboard regenerated: {len(nfl_df)} NFL + {len(ncaaf_df)} NCAAF games baked in.")


if __name__ == "__main__":
    main()
