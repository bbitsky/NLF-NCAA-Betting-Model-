"""
generate_analyst_card_tab.py — Refreshes the "Analyst Card" tab in
picks_dashboard.html from data/analyst_card.csv.

Mirrors generate_dashboard.py's approach: only the region between
<!-- ANALYST_CARD_CONTENT_START --> and <!-- ANALYST_CARD_CONTENT_END -->
is touched. Everything else in the dashboard (NFL/NCAAF picks tables,
Bet Tracker, Intel tabs, layout, CSS, JS) is left completely alone.

Run this any time analyst_card.csv changes and you want the dashboard's
Analyst Card tab to reflect it.
"""

import csv
import html
import os
import re

BASE_DIR = r"C:\Users\bitsk\Claude\Projects\NFL Betting Model"
DASHBOARD_PATH = os.path.join(BASE_DIR, "picks_dashboard.html")
CARD_CSV_PATH = os.path.join(BASE_DIR, "data", "analyst_card.csv")

MARKET_LABELS = {
    "spread": "Spread",
    "total": "Total",
    "team_total": "Team total",
    "1h_spread": "1H spread",
    "1h_total": "1H total",
    "1h_team_total": "1H team total",
    "prop": "Prop",
}

MARKET_ORDER = ["spread", "total", "team_total", "1h_spread", "1h_total", "1h_team_total", "prop"]


def replace_marker(html_text, name, new_inner):
    pattern = re.compile(
        r'((?:<!--)\s*' + re.escape(name) + r'_START\s*(?:-->)?)(.*?)((?:<!--)\s*' + re.escape(name) + r'_END)',
        flags=re.S)
    m = pattern.search(html_text)
    if not m:
        print(f"  ⚠ marker {name} not found — skipped")
        return html_text
    return html_text[:m.start()] + m.group(1) + new_inner + m.group(3) + html_text[m.end():]


def esc(s):
    return html.escape(str(s), quote=False)


def tier_badge(tier):
    tier = (tier or "").strip().upper()
    if tier not in ("A", "B", "C", "PASS"):
        return ""
    return f'<span class="ac-tier ac-tier-{tier}">{tier}</span>'


def format_pick_cell(row):
    pick = row.get("pick", "").strip()
    line = row.get("line", "").strip()
    price = row.get("price", "").strip()
    bits = [esc(pick)] if pick else []
    extra = []
    if line and line not in pick:
        extra.append(line)
    if price and price.upper() != "TBD":
        extra.append(price)
    if extra:
        bits.append(f'<span style="color:var(--muted);font-weight:400"> ({esc(", ".join(extra))})</span>')
    return "".join(bits) if bits else "—"


def load_rows():
    with open(CARD_CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_html():
    rows = load_rows()
    if not rows:
        return '<div class="ac-empty">No analyst card rows found.</div>'

    # group by week, then by game (away/home), preserving first-seen order
    weeks = {}
    for r in rows:
        wk = r.get("week", "").strip()
        weeks.setdefault(wk, {})
        game_key = (r.get("away", "").strip(), r.get("home", "").strip(), r.get("game_date", "").strip())
        weeks[wk].setdefault(game_key, []).append(r)

    out = []
    for wk in sorted(weeks.keys(), key=lambda w: (int(w) if w.isdigit() else 0), reverse=True):
        games = weeks[wk]
        out.append(f'<div class="ac-week-group"><div class="ac-week-title">Week {esc(wk)}</div>')
        # order games by kickoff/date of their first row
        def game_sort_key(item):
            (away, home, gdate), grows = item
            return (gdate, grows[0].get("kickoff_et", ""))
        for (away, home, gdate), grows in sorted(games.items(), key=game_sort_key):
            kickoff = grows[0].get("kickoff_et", "").strip()
            out.append('<div class="ac-game">')
            out.append(
                f'<div class="ac-game-header"><span>{esc(away)} @ {esc(home)}</span>'
                f'<span class="ac-kickoff">{esc(gdate)} · {esc(kickoff)} ET</span></div>'
            )
            out.append('<table class="ac-rows"><tbody>')
            ordered = sorted(grows, key=lambda r: MARKET_ORDER.index(r.get("market", "").strip())
                              if r.get("market", "").strip() in MARKET_ORDER else 99)
            for r in ordered:
                market = r.get("market", "").strip()
                label = MARKET_LABELS.get(market, market.title() or "—")
                tier = r.get("tier", "").strip()
                rationale = r.get("rationale", "").strip()
                out.append(
                    "<tr>"
                    f'<td class="ac-market">{esc(label)}</td>'
                    f'<td class="ac-pick">{format_pick_cell(r)}{tier_badge(tier)}</td>'
                    f'<td class="ac-rationale">{esc(rationale)}</td>'
                    "</tr>"
                )
            out.append("</tbody></table></div>")
        out.append("</div>")
    return "".join(out)


def main():
    print("=" * 60)
    print("  ANALYST CARD TAB GENERATOR")
    print("=" * 60)

    if not os.path.exists(CARD_CSV_PATH):
        print(f"  ✗ {CARD_CSV_PATH} not found — aborting, dashboard untouched")
        return

    with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
        dash_html = f.read()

    content = build_html()
    new_html = replace_marker(dash_html, "ANALYST_CARD_CONTENT", content)

    if new_html == dash_html:
        print("  ⚠ no changes written (marker missing or content identical)")
        return

    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)

    n_rows = len(load_rows())
    print(f"  ✓ Analyst Card tab refreshed — {n_rows} rows from analyst_card.csv")


if __name__ == "__main__":
    main()
