#!/usr/bin/env python3
"""Read-only, offline checks for this small community-defaults repository."""

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "work", "outputs", "__pycache__"}
REQUIRED = {
    "README.md", "README.zh-CN.md", "LICENSE", "NOTICE", "AGENTS.md",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md",
    "ACCESSIBILITY.md", "AI_POLICY.md", "docs/standard.md", "docs/adoption.md",
    ".github/toss.json", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/DISCUSSION_TEMPLATE/ideas.yml", ".github/DISCUSSION_TEMPLATE/q-a.yml",
    ".github/workflows/check.yml", ".github/workflows/pages.yml",
    "site/index.html", "site/features.html", "site/download.html", "site/community.html",
    "site/favicon.svg", "site/style.css", "site/script.js", "site/theme-init.js", "scripts/check.py",
    "project.json", "templates/project-homepage.html", "scripts/render_site.py",
    "tests/test_render_site.py",
}
errors = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                errors.append(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        for attr in ("href", "src", "poster"):
            if attrs.get(attr):
                self.links.append(attrs[attr])
        # Check both screenshot variants, including the one not selected by this host.
        if attrs.get("srcset"):
            for candidate in attrs["srcset"].split(","):
                parts = candidate.strip().split()
                if parts:
                    self.links.append(parts[0])


def fail(path, message):
    errors.append(f"{path.relative_to(ROOT).as_posix()}: {message}")


def source_files():
    def visit(directory):
        for path in sorted(directory.iterdir()):
            if path.name in EXCLUDED:
                continue
            if path.is_symlink():
                fail(path, "source symlinks are not allowed")
            elif path.is_dir():
                yield from visit(path)
            elif path.is_file():
                yield path
    return list(visit(ROOT))


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, ValueError) as exc:
        fail(path, f"invalid JSON-compatible YAML/JSON: {exc}")
        return None


def heading_ids(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    ids, counts = set(), {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, flags=re.M):
        heading = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(heading, 0)
        counts[heading] = count + 1
        ids.add(heading if not count else f"{heading}-{count}")
    return ids


def check_link(origin, value, site=False):
    url = urlsplit(value)
    if url.scheme or url.netloc:
        return  # External availability and platform state are verified separately.
    if not url.path and not url.fragment:
        return
    target = (origin.parent / unquote(url.path)).resolve() if url.path else origin
    boundary = ROOT / "site" if site else ROOT
    if not target.is_relative_to(boundary):
        fail(origin, f"link escapes its source boundary: {value}")
        return
    if target.is_dir():
        target = target / "index.html"
    if not target.is_file():
        fail(origin, f"missing local link target: {value}")
        return
    if url.fragment and target.suffix.lower() in {".html", ".md"}:
        text = target.read_text(encoding="utf-8-sig")
        if target.suffix.lower() == ".html":
            page = Page()
            page.feed(text)
            ids = page.ids
        else:
            ids = heading_ids(text)
        if unquote(url.fragment) not in ids:
            fail(origin, f"missing fragment target: {value}")


def check_form(path):
    data = read_json(path)
    if not isinstance(data, dict):
        fail(path, "form/config must be an object")
        return
    if path.name == "config.yml":
        if not isinstance(data.get("blank_issues_enabled"), bool):
            fail(path, "blank_issues_enabled must be boolean")
        for contact in data.get("contact_links", []):
            if not all(contact.get(key) for key in ("name", "url", "about")):
                fail(path, "contact links need name, url, and about")
            if not str(contact.get("url", "")).startswith("https://"):
                fail(path, "contact links must use HTTPS")
        return
    if "ISSUE_TEMPLATE" in path.parts:
        for key in ("name", "description"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                fail(path, f"issue form needs {key}")
    body = data.get("body")
    if not isinstance(body, list) or not body:
        fail(path, "form needs a nonempty body")
        return
    if not any(isinstance(field, dict) and field.get("type") != "markdown" for field in body):
        fail(path, "form needs at least one non-Markdown input field")
    ids = set()
    for field in body:
        if not isinstance(field, dict):
            fail(path, "form fields must be objects")
            continue
        kind = field.get("type")
        attributes = field.get("attributes", {})
        if kind not in {"markdown", "input", "textarea", "dropdown", "checkboxes"}:
            fail(path, f"unsupported form field: {kind}")
        if kind == "markdown":
            if not attributes.get("value"):
                fail(path, "markdown field needs value")
            continue
        field_id = field.get("id", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", field_id) or field_id in ids:
            fail(path, f"missing, invalid, or duplicate field id: {field_id}")
        ids.add(field_id)
        if not attributes.get("label"):
            fail(path, f"field {field_id} needs a label")
        required = field.get("validations", {}).get("required", False)
        if not isinstance(required, bool):
            fail(path, f"field {field_id} required flag must be boolean")


def main():
    files = source_files()
    paths = {path.relative_to(ROOT).as_posix() for path in files}
    for name in sorted(REQUIRED - paths):
        errors.append(f"Missing required source: {name}")
    policy = read_json(ROOT / ".github/toss.json")
    if not isinstance(policy, dict):
        return finish(files, 0, 0)
    budgets = policy.get("resources", {})
    keys = (
        "free_space_reserve_gib", "temporary_growth_warning_gib",
        "temporary_growth_budget_gib", "max_heavy_jobs_per_machine", "max_log_mib",
        "repository_source_budget_kib", "site_source_budget_kib", "max_source_file_kib",
    )
    valid_budgets = all(type(budgets.get(key)) in (int, float) and budgets[key] > 0 for key in keys)
    if not valid_budgets:
        errors.append("Policy needs positive numeric resource budgets")
        return finish(files, 0, 0)
    if budgets["temporary_growth_warning_gib"] >= budgets["temporary_growth_budget_gib"]:
        errors.append("Temporary warning must be below temporary budget")
    if policy.get("schema_version") != 1 or policy.get("repository") != "tangyixiao/.github":
        errors.append("Unexpected sample policy schema or repository")
    desired = policy.get("desired_settings", {})
    for name in ("issues", "discussions", "wiki", "projects", "private_vulnerability_reporting"):
        if desired.get(name) is not True:
            errors.append(f"Applicable community setting should be enabled: {name}")
    total = site_total = 0
    for path in files:
        size = path.stat().st_size
        total += size
        in_site = path.is_relative_to(ROOT / "site")
        if in_site:
            site_total += size
        if size > budgets["max_source_file_kib"] * 1024:
            fail(path, "exceeds per-source-file budget")
        # Screenshots are valid site assets. Count their bytes above without
        # attempting to decode binary image contents as UTF-8 source text.
        if path.suffix.lower() not in {".md", ".html", ".css", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            fail(path, f"cannot read text source: {exc}")
            continue
        if path.suffix.lower() == ".md":
            text = re.sub(r"```.*?```", "", text, flags=re.S)
            for link in re.findall(r"\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+\"[^\"]*\")?\)", text):
                check_link(path, link)
        # The source template contains slots. Inspect its rendered site instead.
        if path.suffix.lower() == ".html" and not path.is_relative_to(ROOT / "templates"):
            page = Page()
            page.feed(text)
            for link in page.links:
                check_link(path, link, site=in_site)
        if path.suffix.lower() == ".css":
            for link in re.findall(r"url\(['\"]?([^)'\"]+)", text):
                check_link(path, link, site=in_site)
        if path.suffix.lower() == ".yml" and "workflows" not in path.parts:
            check_form(path)
        if path.suffix.lower() == ".yml" and "workflows" in path.parts:
            for action in re.findall(r"uses:\s*([^\s#]+)", text):
                if not re.fullmatch(r"[\w.-]+/[\w./-]+@[0-9a-f]{40}", action):
                    fail(path, f"Action must use full commit SHA: {action}")
            if "timeout-minutes:" not in text or "permissions:" not in text:
                fail(path, "workflow needs explicit timeout and permissions")
    if total > budgets["repository_source_budget_kib"] * 1024:
        errors.append("Repository source exceeds its configured size budget")
    if site_total > budgets["site_source_budget_kib"] * 1024:
        errors.append("Static site exceeds its configured size budget")
    if not (ROOT / "LICENSE").read_text(encoding="utf-8-sig").lstrip().startswith("Apache License"):
        errors.append("Expected the complete Apache-2.0 license text")
    if (ROOT / "scripts/render_site.py").is_file():
        check_command(["scripts/render_site.py", "--check"], "Rendered localized pages")
    if (ROOT / "tests/test_render_site.py").is_file():
        check_command(["-m", "unittest", "discover", "-s", "tests"], "Website template tests")
    return finish(files, total, site_total)


def check_command(arguments, label):
    """Keep validation read-only, bounded, and free of generated bytecode."""
    try:
        result = subprocess.run(
            [sys.executable, "-B", *arguments], cwd=ROOT,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        errors.append(f"{label}: {exc}")
        return
    if result.returncode:
        detail = (result.stdout + result.stderr).strip()
        errors.append(f"{label} failed:\n{detail[:12000]}")
    else:
        print(f"PASS: {label}")


def finish(files, total, site_total):
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"PASS: {len(files)} source files; {total:,} bytes total; {site_total:,} bytes in site/")
    print("Checked local sources only; browser behavior and live GitHub state need separate evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
