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

import os, re, subprocess, shutil, glob
from datetime import datetime

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
def find_latest_report():
    pattern = os.path.join(INTEL_DIR, "daily_intel_*.md")
    files = sorted(glob.glob(pattern), reverse=True)
    return files[0] if files else None


# ─────────────────────────────────────────
# Inject intel report into dashboard HTML
# ─────────────────────────────────────────
def inject_intel(report_path: str):
    with open(report_path, encoding='utf-8') as f:
        md = f.read()

    report_date = os.path.basename(report_path).replace('daily_intel_', '').replace('.md', '')
    generated_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    meta_html = (
        f'<div class="intel-meta">'
        f'Report date: <strong>{report_date}</strong> &nbsp;·&nbsp; '
        f'Updated: {generated_at}'
        f'</div>'
    )
    body_html = md_to_html(md)
    content_html = meta_html + body_html

    with open(DASHBOARD_SRC, encoding='utf-8') as f:
        dashboard = f.read()

    new_dashboard = re.sub(
        r'<!-- INTEL_CONTENT_START -->.*?<!-- INTEL_CONTENT_END -->',
        f'<!-- INTEL_CONTENT_START -->\n{content_html}\n<!-- INTEL_CONTENT_END -->',
        dashboard,
        flags=re.DOTALL
    )

    with open(DASHBOARD_SRC, 'w', encoding='utf-8') as f:
        f.write(new_dashboard)

    print(f"✓ Injected intel report ({report_date}) into picks_dashboard.html")
    return report_date


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
def main():
    print("=" * 56)
    print("  GitHub Pages push — NLF-NCAA-Betting-Model-")
    print("=" * 56)

    # 1. Find and inject latest intel report
    report_path = find_latest_report()
    if report_path:
        report_date = inject_intel(report_path)
    else:
        print("⚠ No intel reports found in intel_reports/ — skipping injection")
        report_date = "no-report"

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

    # 5. Commit
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = git("commit", "-m", f"Daily update — {date_str} — intel {report_date}")
    out = result.stdout + result.stderr
    if "nothing to commit" in out:
        print("No changes since last push — already up to date.")
        print(f"  Live at: {PAGES_URL}")
        return
    print(f"✓ Committed: Daily update — {date_str}")

    # 6. Push
    print("Pushing to GitHub...")
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
