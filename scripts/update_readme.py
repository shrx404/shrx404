#!/usr/bin/env python3
"""
Safe README updater:
- Requires README.md to have exact markers:
  <!-- PROJECTS_START -->  and  <!-- PROJECTS_END -->
- If markers missing, aborts and does NOT overwrite README
- Makes a timestamped backup of README before writing
"""
import os
import sys
import time
import re
from pathlib import Path

# Ensure requests is available
try:
    import requests
except Exception:
    print("Missing dependency 'requests'. Install with: pip install requests")
    sys.exit(2)

# Environment variables
OWNER = os.environ.get("OWNER") or os.environ.get("GITHUB_REPOSITORY", "").split("/")[0]
TOKEN = os.environ.get("GITHUB_TOKEN")

if not OWNER:
    print("OWNER not set. Export OWNER or run in Actions.")
    sys.exit(2)

HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# Load README
README = Path("README.md")
if not README.exists():
    print("README.md not found. Aborting.")
    sys.exit(2)

content = README.read_text(encoding="utf8")

# Check required markers
if "<!-- PROJECTS_START -->" not in content or "<!-- PROJECTS_END -->" not in content:
    print("Missing markers: <!-- PROJECTS_START --> and <!-- PROJECTS_END --> not found in README.md. Aborting without changes.")
    sys.exit(2)

# Fetch repos
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

proj_lines = projects_block(repos, 5)

# Safety check: ensure project block isn't huge
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

# Replace between markers
def replace_between(text, start_marker, end_marker, new_lines):
    pattern = re.compile(re.escape(start_marker) + r"[\s\S]*?" + re.escape(end_marker), flags=re.M)
    replacement = start_marker + "\n" + "\n".join(new_lines) + "\n" + end_marker
    return pattern.sub(replacement, text, count=1)

new_content = replace_between(content, "<!-- PROJECTS_START -->", "<!-- PROJECTS_END -->", proj_lines)

# Update timestamp
ts = time.strftime("%a %b %d %H:%M:%S UTC %Y", time.gmtime())
if "<!-- LAST_UPDATED -->" in new_content:
    new_content = re.sub(
        r"_Last updated: <!-- LAST_UPDATED -->.*",
        f"_Last updated: <!-- LAST_UPDATED --> {ts}",
        new_content
    )

# Write changes if different
if new_content == content:
    print("No changes detected. README unchanged.")
else:
    README.write_text(new_content, encoding="utf8")
    print("README updated successfully. Changes written locally (Actions will commit).")
    print("Projects:\n" + "\n".join(proj_lines))
