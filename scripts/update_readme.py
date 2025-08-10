#!/usr/bin/env python3
import os, sys, time, re
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing dependency 'requests'. Install with: pip install requests")
    sys.exit(2)

OWNER = os.environ.get("OWNER") or os.environ.get("GITHUB_REPOSITORY", "").split("/")[0]
TOKEN = os.environ.get("GITHUB_TOKEN")
if not OWNER or not TOKEN:
    print("OWNER or GITHUB_TOKEN not provided in environment.")
    sys.exit(2)

HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
API_BASE = f"https://api.github.com/users/{OWNER}"

def get_all_repos():
    repos = []
    page = 1
    while True:
        resp = requests.get(f"{API_BASE}/repos", params={"per_page": 100, "page": page, "type": "owner", "sort": "created"}, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print("Failed to fetch repos:", resp.status_code, resp.text)
            break
        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 10:
            break
    return repos

def compute_language_bytes(repos, repo_limit=50):
    lang_bytes = {}
    sliced = repos[:repo_limit]
    for r in sliced:
        url = r.get("languages_url")
        if not url:
            continue
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"Warning: languages_url for {r.get('name')} returned {resp.status_code}")
            continue
        data = resp.json()
        for lang, b in data.items():
            lang_bytes[lang] = lang_bytes.get(lang, 0) + b
    return lang_bytes

def format_languages_block(lang_bytes, top_n=8):
    total = sum(lang_bytes.values())
    if total == 0:
        return ["- No languages detected"]
    items = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)[:top_n]
    lines = []
    for lang, b in items:
        pct = b / total * 100
        lines.append(f"- {lang} — {b} bytes ({pct:.1f}%)")
    return lines

def format_projects_block(repos, count=5):
    # sort by creation date (newest first)
    sorted_repos = sorted(repos, key=lambda r: r.get("created_at") or "", reverse=True)[:count]
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
    return lines

def replace_block(text, marker_start, marker_end, new_lines):
    pattern = re.compile(re.escape(marker_start) + r"[\s\S]*?" + re.escape(marker_end), flags=re.M)
    replacement = marker_start + "\n" + "\n".join(new_lines) + "\n" + marker_end
    return pattern.sub(replacement, text)

def main():
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("README.md not found in repo root")
        sys.exit(2)

    print("Fetching repos...")
    repos = get_all_repos()
    if not repos:
        print("No repos found or failed to fetch repos.")
    else:
        print(f"Found {len(repos)} repos (owner={OWNER})")

    print("Computing language bytes (first 50 repos)...")
    lang_bytes = compute_language_bytes(repos, repo_limit=50)
    lang_block = format_languages_block(lang_bytes, top_n=8)

    print("Building projects block (latest 5)...")
    projects_block = format_projects_block(repos, count=5)

    text = readme_path.read_text(encoding="utf8")

    text = replace_block(text, "<!-- LANGUAGES_START -->", "<!-- LANGUAGES_END -->", lang_block)
    text = replace_block(text, "<!-- PROJECTS_START -->", "<!-- PROJECTS_END -->", projects_block + ["", "<!-- PROJECTS_END -->"] ) if False else text

    # For projects: replace only the inner part between markers, preserving the closing tag
    text = re.sub(r"<!-- PROJECTS_START -->[\s\S]*?<!-- PROJECTS_END -->",
                  "<!-- PROJECTS_START -->\n" + "\n".join(projects_block) + "\n<!-- PROJECTS_END -->",
                  text, flags=re.M)

    # Update last-updated line if present
    ts = time.strftime("%a %b %d %H:%M:%S UTC %Y", time.gmtime())
    text = re.sub(r"_Last updated: <!-- LAST_UPDATED -->.*", f"_Last updated: <!-- LAST_UPDATED --> {ts}", text)

    readme_path.write_text(text, encoding="utf8")
    print("README.md updated locally. Commit via Actions or locally to push changes.")
    print("Languages block:")
    print("\n".join(lang_block))
    print("Projects block:")
    print("\n".join(projects_block))

if __name__ == "__main__":
    main()
