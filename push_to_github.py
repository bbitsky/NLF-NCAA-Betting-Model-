"""
push_to_github.py
==================
1. Finds the latest daily intel report in intel_reports/
2. Converts it to HTML and injects it into picks_dashboard.html's Intel tab
3. Copies picks_dashboard.html → index.html
4. Commits and pushes everything (dashboard + intel_reports/) to GitHub Pages

Run automatically after the daily intel task. Also safe to run manually.

One-time setup:
  1. GitHub Pages: repo Settings → Pages → Source: main branch, / (root)  ✅ Done
  2. git must be installed: https://git-scm.com/download/win
  3. Authenticate once via browser popup or Personal Access Token
"""

import os, re, subprocess, shutil, glob, sys
from datetime import datetime

# When run from run_daily_push.bat, stdout is redirected to push_log.txt and
# defaults to cp1252 on Windows — which crashes on the ✓/⚠ characters below.
# Force UTF-8 (with replacement) so logging can never kill the push.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

REPO_DIR      = r"C:\Users\bitsk\Claude\Projects\NFL Betting Model"
INTEL_DIR     = os.path.join(REPO_DIR, "intel_reports")
DASHBOARD_SRC = os.path.join(REPO_DIR, "picks_dashboard.html")
INDEX_HTML    = os.path.join(REPO_DIR, "index.html")
REMOTE_URL    = "https://github.com/bbitsky/NLF-NCAA-Betting-Model-.git"
PAGES_URL     = "https://bbitsky.github.io/NLF-NCAA-Betting-Model-/"


# ─────────────────────────────────────────
# Git helper
# ─────────────────────────────────────────
def git(*args):
    r = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_DIR, capture_output=True, text=True
    )
    if r.returncode != 0 and r.stderr.strip():
        print(f"  [git {' '.join(args[:2])}]: {r.stderr.strip()[:300]}")
    return r


# ─────────────────────────────────────────
# Section filter
# ─────────────────────────────────────────
# Headings matching these patterns are dropped from the report before it
# reaches the dashboard. Social/buzz sections were vague chatter that the
# BREAKING / INJURY / LINE MOVEMENT sections already cover with hard sourcing.
DROP_SECTION_PATTERNS = [
    r"social",
    r"bulletin\s*board",
    r"\bbuzz\b",
]


def strip_sections(md: str) -> str:
    """Remove any ##/### section whose heading matches DROP_SECTION_PATTERNS.

    A section runs from its heading to the next heading of the same or higher
    level (or EOF), so nested content is dropped with it.
    """
    out, drop_level = [], None
    for line in md.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level, text = len(m.group(1)), m.group(2)
            if drop_level is not None and level <= drop_level:
                drop_level = None
            if drop_level is None and any(
                re.search(pat, text, re.I) for pat in DROP_SECTION_PATTERNS
            ):
                drop_level = level
                print(f"  · dropped section: {text.strip()[:70]}")
                continue
        if drop_level is not None:
            continue
        out.append(line)
    return '\n'.join(out)


# ─────────────────────────────────────────
# Markdown → HTML (lightweight converter)
# ─────────────────────────────────────────
def md_to_html(md: str) -> str:
    lines = md.split('\n')
    html_lines = []
    in_table = False
    in_ul = False
    table_header_done = False

    def flush_table():
        nonlocal in_table, table_header_done
        if in_table:
            html_lines.append('</tbody></table>')
            in_table = False
            table_header_done = False

    def flush_ul():
        nonlocal in_ul
        if in_ul:
            html_lines.append('</ul>')
            in_ul = False

    def inline(text):
        # Bold+italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Inline code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', text)
        return text

    for line in lines:
        stripped = line.strip()

        # Horizontal rule
        if re.match(r'^---+$', stripped):
            flush_table(); flush_ul()
            html_lines.append('<hr>')
            continue

        # Headings
        if stripped.startswith('### '):
            flush_table(); flush_ul()
            html_lines.append(f'<h3>{inline(stripped[4:])}</h3>')
            continue
        if stripped.startswith('## '):
            flush_table(); flush_ul()
            html_lines.append(f'<h2>{inline(stripped[3:])}</h2>')
            continue
        if stripped.startswith('# '):
            flush_table(); flush_ul()
            html_lines.append(f'<h1>{inline(stripped[2:])}</h1>')
            continue

        # Blockquote
        if stripped.startswith('> '):
            flush_table(); flush_ul()
            html_lines.append(f'<blockquote>{inline(stripped[2:])}</blockquote>')
            continue

        # Table rows
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped[1:-1].split('|')]
            # Separator row (|---|---|)
            if all(re.match(r'^[-: ]+$', c) for c in cells if c):
                if not table_header_done:
                    html_lines.append('</tr></thead><tbody>')
                    table_header_done = True
                continue
            if not in_table:
                flush_ul()
                html_lines.append('<table><thead><tr>')
                tag = 'th'
                in_table = True
                table_header_done = False
            else:
                tag = 'td'
                html_lines.append('<tr>')
            html_lines.append(''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells))
            html_lines.append('</tr>')
            continue

        # Bullet list items
        if re.match(r'^[-*] ', stripped):
            flush_table()
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            html_lines.append(f'<li>{inline(stripped[2:])}</li>')
            continue

        # Numbered list
        if re.match(r'^\d+\. ', stripped):
            flush_table()
            if in_ul:
                flush_ul()
                html_lines.append('<ol>')
                in_ul = True  # reuse flag for ordered list
            item_text = re.sub(r"^\d+\. ", "", stripped)
            html_lines.append(f'<li>{inline(item_text)}</li>')
            continue

        # Empty line
        if not stripped:
            flush_table(); flush_ul()
            html_lines.append('')
            continue

        # Italic-only line footer (e.g. *Daily report generated..*)
        flush_table(); flush_ul()
        html_lines.append(f'<p>{inline(stripped)}</p>')

    flush_table(); flush_ul()
    return '\n'.join(html_lines)


# ─────────────────────────────────────────
# Find latest intel report
# ─────────────────────────────────────────
def find_latest_report(prefix: str = "daily_intel_"):
    pattern = os.path.join(INTEL_DIR, f"{prefix}*.md")
    files = sorted(glob.glob(pattern), reverse=True)
    return files[0] if files else None


# ─────────────────────────────────────────
# Inject intel report into dashboard HTML
# ─────────────────────────────────────────
def inject_intel(report_path: str, prefix: str = "daily_intel_", marker: str = "INTEL_CONTENT"):
    with open(report_path, encoding='utf-8') as f:
        md = f.read()

    report_date = os.path.basename(report_path).replace(prefix, '').replace('.md', '')
    generated_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    meta_html = (
        f'<div class="intel-meta">'
        f'Report date: <strong>{report_date}</strong> &nbsp;·&nbsp; '
        f'Updated: {generated_at}'
        f'</div>'
    )
    body_html = md_to_html(strip_sections(md))
    content_html = meta_html + body_html

    with open(DASHBOARD_SRC, encoding='utf-8') as f:
        dashboard = f.read()

    new_dashboard, n = re.subn(
        rf'<!-- {marker}_START -->.*?<!-- {marker}_END -->',
        lambda _m: f'<!-- {marker}_START -->\n{content_html}\n<!-- {marker}_END -->',
        dashboard,
        flags=re.DOTALL
    )
    if n == 0:
        print(f"⚠ Marker {marker}_START not found in picks_dashboard.html — skipped")
        return None

    with open(DASHBOARD_SRC, 'w', encoding='utf-8') as f:
        f.write(new_dashboard)

    print(f"✓ Injected {marker} report ({report_date}) into picks_dashboard.html")
    return report_date


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
def main():
    print("=" * 56)
    print("  GitHub Pages push — NLF-NCAA-Betting-Model-")
    print("=" * 56)

    # 1. Find and inject latest daily intel report
    report_path = find_latest_report("daily_intel_")
    if report_path:
        report_date = inject_intel(report_path, "daily_intel_", "INTEL_CONTENT")
    else:
        print("⚠ No daily intel reports found in intel_reports/ — skipping injection")
        report_date = "no-report"

    # 1b. Find and inject latest weekly intel report (separate tab)
    weekly_path = find_latest_report("weekly_intel_")
    if weekly_path:
        inject_intel(weekly_path, "weekly_intel_", "WEEKLY_INTEL_CONTENT")
    else:
        print("⚠ No weekly intel reports found — weekly tab left as-is")

    # 2. Copy dashboard → index.html
    if not os.path.exists(DASHBOARD_SRC):
        print("ERROR: picks_dashboard.html not found.")
        return
    shutil.copy2(DASHBOARD_SRC, INDEX_HTML)
    print("✓ Copied picks_dashboard.html → index.html")

    # 3. Initialize git repo if first run
    if not os.path.exists(os.path.join(REPO_DIR, ".git")):
        print("First run — initializing git repo...")
        git("init")
        git("remote", "add", "origin", REMOTE_URL)
        git("branch", "-M", "main")
        print("✓ Git repo initialized")
    else:
        remotes = git("remote", "-v").stdout
        if "NLF-NCAA-Betting-Model-" not in remotes:
            git("remote", "set-url", "origin", REMOTE_URL)

    # 4. Stage all relevant files
    git("add", "index.html")
    git("add", "picks_dashboard.html")
    git("add", os.path.join("intel_reports", "."))   # all intel reports
    git("add", "push_to_github.py")  # keep this script's own fixes committed —
    # an unstaged edit here blocked `pull --rebase` every run and forced a
    # daily force-push (see push_log.txt entries before 2026-08-26)

    # 5. Commit
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = git("commit", "-m", f"Daily update — {date_str} — intel {report_date}")
    out = result.stdout + result.stderr
    if "nothing to commit" in out:
        print("No new local changes — will still sync/push any unpushed commits.")
    else:
        print(f"✓ Committed: Daily update — {date_str}")

    # 6. Sync with remote first (in case anything was committed on GitHub
    #    directly, e.g. via the web uploader), then push.
    print("Syncing with GitHub...")
    git("fetch", "origin")
    # --autostash: unstaged working-tree changes (logs, scratch files) no
    # longer abort the rebase and trigger a needless daily force-push.
    rebase = git("pull", "--rebase", "--autostash", "origin", "main")
    if rebase.returncode != 0:
        # A genuinely conflicting commit exists on GitHub (e.g. a same-day
        # web upload). Local files are the source of truth, so drop the
        # conflict and force-push our version.
        print("  ⚠ Remote has a conflicting commit — keeping LOCAL version (source of truth).")
        git("rebase", "--abort")
        push = git("push", "--force", "-u", "origin", "main")
    else:
        push = git("push", "-u", "origin", "main")
    if push.returncode == 0:
        print(f"\n✅ Dashboard live at: {PAGES_URL}")
        print(f"   Intel tab updated with report from {report_date}")
        print("   (GitHub Pages may take 1–2 min to reflect changes)")
    else:
        print("\n❌ Push failed. Common fixes:")
        print("   • First time: GitHub may ask for credentials in a browser popup")
        print("   • Use a Personal Access Token (PAT) as your password:")
        print("     github.com → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)")
        print("     Scopes needed: repo (full control)")
        print(f"   • Or run manually in terminal:")
        print(f'     git -C "{REPO_DIR}" push -u origin main')

    print("=" * 56)


if __name__ == "__main__":
    main()
