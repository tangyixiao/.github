#!/usr/bin/env python3
"""Render the configured project homepage using Python's standard library only."""

import argparse
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "project-homepage.html"
ICONS = {
    "home": '<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3z"/>',
    "trophy": '<path d="M8 3h8v6a4 4 0 0 1-8 0V3ZM8 5H4v3a4 4 0 0 0 4 4m8-7h4v3a4 4 0 0 1-4 4M12 13v5m-4 3h8m-8-3h8v3"/>',
    "layers": '<path d="m12 3 10 5-10 5L2 8l10-5Zm-9 10 9 5 9-5M3 18l9 5 9-5"/>',
    "book": '<path d="M5 3h15v18H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 14h15M7 7h9M7 11h6"/>',
    "code": '<path d="m7 5-6 7 6 7M17 5l6 7-6 7M14 2l-4 20"/>',
    "download": '<path d="M12 2v13m-5-5 5 5 5-5M3 15v6h18v-6"/>',
    "link": '<path d="m10 7 3-3a5 5 0 0 1 7 7l-3 3M14 17l-3 3a5 5 0 0 1-7-7l3-3m1 6 8-8"/>',
}


def _text(value, location, *, empty=False):
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ValueError(f"{location} must be a non-empty string")
    if len(value) > 10000:
        raise ValueError(f"{location} is too long")
    return value


def _object(value, location):
    if not isinstance(value, dict):
        raise ValueError(f"{location} must be an object")
    return value


def _list(value, location, *, minimum=1, maximum=12):
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError(f"{location} must contain {minimum}–{maximum} items")
    return value


def _url(value, location, *, image=False):
    value = _text(value, location)
    decoded = value
    for _ in range(4):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    if any(ord(c) < 33 or ord(c) == 127 for c in decoded) or "\\" in decoded:
        raise ValueError(f"{location} contains unsafe URL characters")
    try:
        parsed = urlsplit(value)
        decoded_parsed = urlsplit(decoded)
        if parsed.scheme:
            if image or parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                raise ValueError(f"{location} must use HTTPS or a safe relative path")
            parsed.port
        elif parsed.netloc or decoded.startswith("//") or decoded_parsed.scheme or ":" in decoded:
            raise ValueError(f"{location} must use HTTPS or a safe relative path")
        elif ".." in decoded_parsed.path.split("/"):
            raise ValueError(f"{location} cannot escape the site directory")
        if image and (not parsed.path or parsed.path.startswith("/") or parsed.fragment or parsed.query):
            raise ValueError(f"{location} must be relative to the site directory")
    except (ValueError, UnicodeError) as error:
        raise ValueError(f"{location}: unsafe URL") from error
    return value


def _action(value, location):
    value = _object(value, location)
    _text(value.get("label"), f"{location}.label")
    _url(value.get("href"), f"{location}.href")


def _icon(value, location):
    if not isinstance(value, str) or value not in ICONS:
        raise ValueError(f"{location} must be one of {', '.join(ICONS)}")


def validate_config(config: dict) -> None:
    """Reject missing content and unsafe URLs before producing any HTML."""
    c = _object(config, "config")
    if c.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if not re.fullmatch(r"[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{2,8})*", _text(c.get("language"), "language")):
        raise ValueError("language must be a valid language tag")
    _text(c.get("name"), "name")
    meta = _object(c.get("meta"), "meta")
    for key in ("title", "description"):
        _text(meta.get(key), f"meta.{key}")
    for i, action in enumerate(_list(c.get("navigation"), "navigation")):
        _action(action, f"navigation[{i}]")
    _action(c.get("repository"), "repository")
    hero = _object(c.get("hero"), "hero")
    for key in ("title", "description"):
        for i, value in enumerate(_list(hero.get(key), f"hero.{key}", maximum=4)):
            _text(value, f"hero.{key}[{i}]")
    for key in ("primary_action", "secondary_action"):
        _action(hero.get(key), f"hero.{key}")
    _text(hero.get("release_note"), "hero.release_note")
    preview = _object(c.get("preview"), "preview")
    _text(preview.get("caption"), "preview.caption")
    image = preview.get("image")
    if image is not None:
        image = _object(image, "preview.image")
        _url(image.get("src"), "preview.image.src", image=True)
        _text(image.get("alt"), "preview.image.alt")
        _text(image.get("caption"), "preview.image.caption")
    for i, tab in enumerate(_list(preview.get("tabs"), "preview.tabs", maximum=5)):
        tab = _object(tab, f"preview.tabs[{i}]")
        _text(tab.get("label"), f"preview.tabs[{i}].label")
        _icon(tab.get("icon"), f"preview.tabs[{i}].icon")
    for i, item in enumerate(_list(preview.get("items"), "preview.items", maximum=4)):
        item = _object(item, f"preview.items[{i}]")
        for key in ("title", "description"):
            _text(item.get(key), f"preview.items[{i}].{key}")
        _icon(item.get("icon"), f"preview.items[{i}].icon")
    features = _object(c.get("features"), "features")
    _text(features.get("title"), "features.title")
    for i, group in enumerate(_list(features.get("groups"), "features.groups", maximum=4)):
        group = _object(group, f"features.groups[{i}]")
        for key in ("title", "description", "detail"):
            _text(group.get(key), f"features.groups[{i}].{key}", empty=key == "detail")
        _icon(group.get("icon"), f"features.groups[{i}].icon")
        mini = _object(group.get("preview"), f"features.groups[{i}].preview")
        _text(mini.get("title"), f"features.groups[{i}].preview.title")
        if mini.get("theme") not in ("light", "dark"):
            raise ValueError("feature preview theme must be light or dark")
        for j, row in enumerate(_list(mini.get("rows"), "feature preview rows", maximum=5)):
            row = _object(row, f"feature preview rows[{j}]")
            _text(row.get("title"), f"feature preview rows[{j}].title")
            _text(row.get("meta"), f"feature preview rows[{j}].meta", empty=True)
    start = _object(c.get("getting_started"), "getting_started")
    _text(start.get("title"), "getting_started.title")
    for i, step in enumerate(_list(start.get("steps"), "getting_started.steps", maximum=4)):
        step = _object(step, f"getting_started.steps[{i}]")
        for key in ("title", "description"):
            _text(step.get(key), f"getting_started.steps[{i}].{key}")
        _url(step.get("href"), f"getting_started.steps[{i}].href")
        _icon(step.get("icon"), f"getting_started.steps[{i}].icon")
    community = _object(c.get("community"), "community")
    for key in ("title", "description"):
        _text(community.get(key), f"community.{key}")
    for i, action in enumerate(_list(community.get("links"), "community.links")):
        _action(action, f"community.links[{i}]")
    footer = _object(c.get("footer"), "footer")
    _text(footer.get("copyright"), "footer.copyright")
    _action(footer.get("license"), "footer.license")


def _escape(value):
    return html.escape(value, quote=True)


def _svg(name, class_name=""):
    return (f'<svg class="{class_name}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def _link(action, class_name="", suffix=""):
    return (f'<a class="{class_name}" href="{_escape(action["href"])}">'
            f'{_escape(action["label"])}{suffix}</a>')


def _product_preview(c):
    preview = c["preview"]
    if preview.get("image") is not None:
        image = preview["image"]
        return (f'<img class="product-image" src="{_escape(image["src"])}" '
                f'alt="{_escape(image["alt"])}" width="640" height="800">'
                f'<figcaption>{_escape(image["caption"])}</figcaption>')
    tabs = "".join(
        f'<span class="app-tab{" is-current" if i == 0 else ""}">{_svg(tab["icon"])}'
        f'<span>{_escape(tab["label"])}</span></span>'
        for i, tab in enumerate(preview["tabs"])
    )
    items = "".join(
        f'<div class="app-item">{_svg(item["icon"])}<div><strong>{_escape(item["title"])}</strong>'
        f'<span>{_escape(item["description"])}</span></div><span class="chevron" aria-hidden="true">›</span></div>'
        for item in preview["items"]
    )
    return (f'<div class="device" aria-hidden="true"><div class="device-status"><span>10:30</span>'
            f'<span class="device-signals"><i></i><i></i><i></i></span></div>'
            f'<div class="app-heading"><strong>{_escape(c["name"])}</strong>'
            f'<span class="app-tools"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg>'
            f'<span>⋮</span></span></div><div class="app-tabs">{tabs}</div>'
            f'<div class="app-items">{items}</div></div>'
            f'<figcaption>{_escape(preview["caption"])}</figcaption>')


def _feature(group):
    mini = group["preview"]
    rows = "".join(
        f'<div class="mini-row"><div><strong>{_escape(row["title"])}</strong>'
        f'{"<span>" + _escape(row["meta"]) + "</span>" if row["meta"] else ""}'
        f'</div><span class="chevron" aria-hidden="true">›</span></div>' for row in mini["rows"]
    )
    detail = f'<p class="feature-detail">{_escape(group["detail"])}</p>' if group["detail"] else ""
    return (f'<article class="feature"><span class="feature-icon">{_svg(group["icon"])}</span>'
            f'<div class="feature-copy"><h3>{_escape(group["title"])}</h3>'
            f'<p>{_escape(group["description"])}</p>{detail}</div>'
            f'<div class="mini-preview mini-{mini["theme"]}" aria-hidden="true">'
            f'<div class="mini-title">{_escape(mini["title"])}</div>{rows}</div></article>')


def render(config: dict) -> str:
    """Return static HTML; all project-supplied strings are escaped."""
    validate_config(config)
    c = config
    steps = "".join(
        f'<a class="start-step" href="{_escape(step["href"])}"><span class="step-icon">'
        f'{_svg(step["icon"])}</span><span><strong>{_escape(step["title"])}</strong>'
        f'<span>{_escape(step["description"])}</span></span></a>'
        for step in c["getting_started"]["steps"]
    )
    values = {
        "LANGUAGE": _escape(c["language"]),
        "META_TITLE": _escape(c["meta"]["title"]),
        "META_DESCRIPTION": _escape(c["meta"]["description"]),
        "NAME": _escape(c["name"]),
        "NAVIGATION": "".join(_link(action) for action in c["navigation"]),
        "REPOSITORY": _link(c["repository"], "repository-link", ' <span aria-hidden="true">↗</span>'),
        "HERO_TITLE": "<br>".join(_escape(line) for line in c["hero"]["title"]),
        "HERO_DESCRIPTION": "".join(f'<p>{_escape(p)}</p>' for p in c["hero"]["description"]),
        "HERO_ACTIONS": _link(c["hero"]["primary_action"], "button button-primary") + _link(c["hero"]["secondary_action"], "button button-secondary"),
        "RELEASE_NOTE": _escape(c["hero"]["release_note"]),
        "PRODUCT_PREVIEW": _product_preview(c),
        "FEATURES_TITLE": _escape(c["features"]["title"]),
        "FEATURE_GROUPS": "".join(_feature(group) for group in c["features"]["groups"]),
        "START_TITLE": _escape(c["getting_started"]["title"]),
        "START_STEPS": steps,
        "COMMUNITY_TITLE": _escape(c["community"]["title"]),
        "COMMUNITY_DESCRIPTION": _escape(c["community"]["description"]),
        "COMMUNITY_LINKS": "".join(_link(action) for action in c["community"]["links"]),
        "COPYRIGHT": _escape(c["footer"]["copyright"]),
        "LICENSE": _link(c["footer"]["license"]),
    }
    template = TEMPLATE.read_text(encoding="utf-8")
    def substitute(match):
        try:
            return values[match.group(1)]
        except KeyError as error:
            raise ValueError(f"Unknown template placeholder {match.group(0)}") from error
    return re.sub(r"\{\{([A-Z_]+)\}\}", substitute, template)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "project.json")
    parser.add_argument("--output", type=Path, default=ROOT / "site" / "index.html")
    parser.add_argument("--check", action="store_true", help="exit 1 if the generated page is out of date")
    args = parser.parse_args(argv)
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        expected = render(config)
        if args.check:
            if not args.output.is_file() or args.output.read_text(encoding="utf-8") != expected:
                print(f"Out of date: {args.output}", file=sys.stderr)
                return 1
            print("Project homepage is current.")
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(expected, encoding="utf-8", newline="\n")
            print(f"Rendered {args.output}")
        return 0
    except (OSError, ValueError, TypeError) as error:
        print(f"Cannot render homepage: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
