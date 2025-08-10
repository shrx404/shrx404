#!/usr/bin/env python3
"""
Safe README updater:
- Requires README.md to have exact markers:
  <!-- PROJECTS_START -->  and  <!-- PROJECTS_END -->
  <!-- LANGUAGES_START --> and  <!-- LANGUAGES_END -->
- If markers missing, aborts and does NOT overwrite README
- Makes a timestamped backup of README before writing
"""
import os
import sys
import time
import re
from pathlib import Path

# try import requests; fail with clear message
try:
    import requests
except Exception:
    print("Missing dependency 'requests'. Install with: pip install requests")
    sys.exit(2)

OWNER = os.environ.get("OWNER") or os.environ.get("GITHUB_REPOSITORY", "").split("/")[0]
TOKEN = os.environ.get("GITHUB_TOKEN")

if not OWNER:
    print("OWNER not set. Export OWNER or run in Actions.")
    sys.exit(2)
# TOKEN is optional (unauthenticated will be rate-limited)
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

README = Path("README.md")
if not README.exists():
    print("README.md not found. Aborting.")
    sys.exit(2)

content = README.read_text(encoding="utf8")

# Ensure markers exist
required_markers = [
    ("<!-- PROJECTS_START -->", "<!-- PROJECTS_END -->"),
    ("<!-- LANGUAGES_START -->", "<!-- LANGUAGES_END -->")
]

for s, e in required_markers:
    if s not in content or e not in content:
        print(f"Missing markers: {s} ... {e} not found in README.md. Aborting without changes.")
        sys.exit(2)

# Fetch repos (safe, owner repos)
def get_repos(limit=50):
    url = f"https://api.github.com/users/{OWNER}/repos"
    params = {"per_page": 100, "type": "owner", "sort": "created"}
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=30)
        res.raise_for_status()
        repos = res.json()
        return repos[:limit]
    except Exception as ex:
        print("Failed to fetch repos:", ex)
        return []

repos = get_repos(50)

# Build projects block (latest 5)
def projects_block(repos, n=5):
    sorted_repos = sorted(repos, key=lambda r: r.get("created_at", ""), reverse=True)[:n]
    lines = []
    for r in sorted_repos:
        name = r.get("name")
        url = r.get("html_url")
        lang = r.get("language") or "Unknown"
        desc = (r.get("description") or "").strip()
        if desc:
            lines.append(f"- [{name}]({url}) — {lang} — {desc}")
        else:
            lines.append(f"- [{name}]({url}) — {lang}")
    return lines or ["- No recent projects"]

# Build languages block using repo language field (cheap & safe)
def languages_block(repos, top=8):
    counts = {}
    for r in repos:
        l = r.get("language")
        if l:
            counts[l] = counts.get(l, 0) + 1
    if not counts:
        return ["- No languages detected"]
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top]
    return [f"- {lang} ({count} repo{'' if count==1 else 's'})" for lang, count in items]

proj_lines = projects_block(repos, 5)
lang_lines = languages_block(repos, 8)

# Safety: ensure project marker doesn't cover most of the file
start_idx = content.find("<!-- PROJECTS_START -->")
end_idx = content.find("<!-- PROJECTS_END -->")
if start_idx >= 0 and end_idx > start_idx:
    covered_len = end_idx - start_idx
    if covered_len > len(content) * 0.8:
        print("Safety: project marker block is too large (covers >80% of README). Aborting.")
        sys.exit(2)

# Backup README
bak = Path(f"README.backup.{int(time.time())}.md")
bak.write_text(content, encoding="utf8")
print(f"Backup saved to {bak.name}")

# Replace blocks safely
def replace_between(text, start_marker, end_marker, new_lines):
    pattern = re.compile(re.escape(start_marker) + r"[\s\S]*?" + re.escape(end_marker), flags=re.M)
    replacement = start_marker + "\n" + "\n".join(new_lines) + "\n" + end_marker
    return pattern.sub(replacement, text, count=1)

new_content = replace_between(content, "<!-- PROJECTS_START -->", "<!-- PROJECTS_END -->", proj_lines)
new_content = replace_between(new_content, "<!-- LANGUAGES_START -->", "<!-- LANGUAGES_END -->", lang_lines)

# Update timestamp
ts = time.strftime("%a %b %d %H:%M:%S UTC %Y", time.gmtime())
new_content = re.sub(r"_Last updated: <!-- LAST_UPDATED -->.*", f"_Last updated: <!-- LAST_UPDATED --> {ts}", new_content)

if new_content == content:
    print("No changes detected. README unchanged.")
else:
    README.write_text(new_content, encoding="utf8")
    print("README updated successfully. Changes written locally (Actions will commit).")
    print("Projects:\n" + "\n".join(proj_lines))
    print("Languages:\n" + "\n".join(lang_lines))
