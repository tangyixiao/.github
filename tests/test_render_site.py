"""Behavior checks for localized pages, project replacement and safe rendering."""

import contextlib
import copy
import html
import importlib.util
import io
import json
import posixpath
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from unittest import mock
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PAGES = {"home": "index.html", "features": "features.html",
         "download": "download.html", "community": "community.html"}
SPEC = importlib.util.spec_from_file_location("render_site", ROOT / "scripts/render_site.py")
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.language = None
        self.anchors = []
        self.alternates = {}
        self.images = []
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        self.elements.append((tag, attrs))
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "a" and attrs.get("href"):
            self.anchors.append(attrs["href"])
        if tag == "option" and attrs.get("value"):
            self.anchors.append(attrs["value"])
        if tag == "link" and "alternate" in attrs.get("rel", "").split():
            self.alternates[attrs.get("hreflang")] = attrs.get("href")
        if tag == "img":
            self.images.append(attrs)


def local_target(origin, href):
    """Resolve a static relative URL as a browser would below the site root."""
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None
    if not parsed.path:
        return origin
    path = posixpath.normpath(str(PurePosixPath(origin).parent / unquote(parsed.path)))
    if parsed.path.endswith("/") or path == ".":
        path = posixpath.join(path, "index.html")
    return path


def output_path(registration, page):
    return str(PurePosixPath(registration["directory"]) / PAGES[page])


class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "project.json").read_text(encoding="utf-8-sig"))
        self.locales = renderer.load_locales(self.config)

    def render_site(self, config=None, locales=None):
        return renderer.render_site(config or self.config, locales or self.locales)

    def temporary_root(self):
        scratch = ROOT / "work"
        scratch.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="render-test-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def isolated_source(self):
        root = self.temporary_root()
        for name in ("project.json", "scripts/render_site.py", "templates/project-homepage.html"):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        for registration in self.config["locales"]:
            name = f"locales/{registration['code']}.json"
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        return root

    def cli(self, root, *args):
        return subprocess.run(
            [sys.executable, "-B", str(root / "scripts/render_site.py"), *map(str, args)],
            cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
        )

    def snapshot(self, directory):
        return {path.relative_to(directory).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in directory.rglob("*.html")}

    def test_eight_static_pages_have_localized_navigation_and_same_page_switches(self):
        pages = self.render_site()
        expected = {output_path(registration, page)
                    for registration in self.config["locales"] for page in PAGES}
        self.assertEqual(len(expected), 8)
        self.assertEqual(set(pages), expected)
        for registration in self.config["locales"]:
            code = registration["code"]
            for page in PAGES:
                path = output_path(registration, page)
                with self.subTest(path=path):
                    document = Page(pages[path])
                    self.assertEqual(document.language, code)
                    targets = {local_target(path, href) for href in document.anchors}
                    self.assertTrue({output_path(registration, item) for item in PAGES} <= targets)
                    for other in self.config["locales"]:
                        other_code = other["code"]
                        self.assertIn(other_code, document.alternates)
                        self.assertEqual(local_target(path, document.alternates[other_code]),
                                         output_path(other, page))
                        if other_code != code:
                            self.assertIn(output_path(other, page), targets,
                                          "Language switches must preserve the current page")
                    self.assertNotIn("{{", pages[path], "No unrendered template slots")

    def test_common_identity_and_download_replace_demo_in_every_locale(self):
        config = copy.deepcopy(self.config)
        original_name = config["name"]
        original_download = config["links"]["download"]
        config["name"] = "Atlas Notes"
        config["links"]["repository"] = "https://github.com/example/atlas-notes"
        config["links"]["download"] = "https://example.com/atlas/download"
        pages = self.render_site(config=config)
        for path, source in pages.items():
            with self.subTest(path=path):
                self.assertIn("Atlas Notes", source)
                self.assertNotIn(original_name, source, "Locale text must use the common project identity")
                self.assertNotIn(original_download, source)
        for registration in config["locales"]:
            for page in ("home", "download"):
                self.assertIn('href="https://example.com/atlas/download"',
                              pages[output_path(registration, page)])

    def test_untrusted_text_and_expanded_tokens_are_escaped(self):
        payload = '\"><img src=x onerror="alert(1)"> & unsafe'
        config = copy.deepcopy(self.config)
        locales = copy.deepcopy(self.locales)
        config["name"] = payload
        for locale in locales.values():
            locale["meta"]["description"] = payload
            locale["hero"]["title"][0] = payload
            locale["ui"]["navigation"] = payload
        for path, source in self.render_site(config, locales).items():
            with self.subTest(path=path):
                self.assertIn(html.escape(payload), source)
                self.assertNotIn(payload, source)
                document = Page(source)
                self.assertFalse(any(any(key.startswith("on") for key in attrs)
                                     for _, attrs in document.elements))

    def test_configured_license_label_and_destination_propagate_to_every_page(self):
        config = copy.deepcopy(self.config)
        config["license_label"] = "MIT"
        config["links"]["license"] = "https://example.com/atlas/LICENSE"
        pages = self.render_site(config=config)
        self.assertEqual(len(pages), 8)
        for path, source in pages.items():
            with self.subTest(path=path):
                self.assertIn('href="https://example.com/atlas/LICENSE">MIT</a>', source)
                self.assertNotIn('>Apache-2.0</a>', source)

    def test_reject_unsafe_common_links(self):
        for key in self.config["links"]:
            for value in ("javascript:alert(1)", "data:text/html,hello", "//evil.example/x",
                          "../outside.html", "https://user:password@example.com/",
                          "java\nscript:alert(1)"):
                with self.subTest(link=key, value=value):
                    config = copy.deepcopy(self.config)
                    config["links"][key] = value
                    with self.assertRaises(ValueError):
                        renderer.validate_config(config)

    def test_reject_unsafe_asset_and_locale_directory_paths(self):
        for value in ("../private.png", "/private.png", "assets\\..\\private.png",
                      "assets/%2e%2e/%2e%2e/private.png", "https://example.com/screen.png",
                      "data:image/png;base64,AA==", "//example.com/screen.png", "C:\\private.png"):
            with self.subTest(image=value):
                config = copy.deepcopy(self.config)
                config["preview"] = {"image": {"src": value}}
                with self.assertRaises(ValueError):
                    renderer.validate_config(config)
                locale = copy.deepcopy(next(iter(self.locales.values())))
                locale["features"]["groups"][0]["image"]["src"] = value
                with self.assertRaises(ValueError):
                    renderer.validate_locale(locale)
        for value in ("../outside", "/en", "en\\..\\private", "//evil.example", "javascript:x"):
            with self.subTest(directory=value):
                config = copy.deepcopy(self.config)
                config["locales"][1]["directory"] = value
                with self.assertRaises(ValueError):
                    renderer.validate_config(config)

    def test_real_product_image_uses_localized_alternative_text_and_caption(self):
        config = copy.deepcopy(self.config)
        locales = copy.deepcopy(self.locales)
        config["preview"] = {"image": {"src": "assets/product-screen.png"}}
        for code, locale in locales.items():
            locale["preview"]["image"] = {"alt": f'{code} screen with "notes"',
                                           "caption": f"{code} captured from the application"}
        pages = self.render_site(config, locales)
        for registration in config["locales"]:
            code = registration["code"]
            path = output_path(registration, "home")
            document = Page(pages[path])
            images = [image for image in document.images
                      if local_target(path, image.get("src", "")) == "assets/product-screen.png"]
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].get("alt"), f'{code} screen with "notes"')
            self.assertIn(f"{code} captured from the application", pages[path])
            self.assertNotIn('class="device"', pages[path])

    def test_third_locale_extends_registry_without_renderer_changes(self):
        root = self.isolated_source()
        config = copy.deepcopy(self.config)
        config["locales"].append({"code": "fr", "label": "Français", "directory": "fr"})
        source_code = self.config["locales"][1]["code"]
        translation = copy.deepcopy(self.locales[source_code])
        translation["hero"]["title"][0] = "Retrouvez vos projets."
        (root / "locales/fr.json").write_text(json.dumps(translation), encoding="utf-8")
        locales = renderer.load_locales(config, config_path=root / "project.json")
        pages = renderer.render_site(config, locales)
        self.assertEqual(len(pages), 12)
        for page in PAGES:
            path = f"fr/{PAGES[page]}"
            self.assertEqual(Page(pages[path]).language, "fr")
            self.assertEqual(local_target(path, Page(pages[path]).alternates["fr"]), path)

    def test_locale_files_require_matching_translation_shape(self):
        root = self.isolated_source()
        code = self.config["locales"][1]["code"]
        target = root / f"locales/{code}.json"
        original = copy.deepcopy(self.locales[code])
        broken = copy.deepcopy(original)
        broken["extra_translation_key"] = "Unmatched translation"
        target.write_text(json.dumps(broken), encoding="utf-8")
        with self.assertRaises(ValueError):
            renderer.load_locales(self.config, config_path=root / "project.json")
        broken = copy.deepcopy(original)
        broken["preview"]["tabs"].pop()
        target.write_text(json.dumps(broken), encoding="utf-8")
        with self.assertRaises(ValueError):
            renderer.load_locales(self.config, config_path=root / "project.json")

    def test_check_detects_each_missing_or_modified_page_without_writing(self):
        root = self.isolated_source()
        self.assertNotEqual(self.cli(root, "--check").returncode, 0)
        self.assertFalse((root / "site").exists())
        result = self.cli(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = root / "site"
        self.assertEqual(len(self.snapshot(output)), 8)
        for relative in sorted(self.snapshot(output)):
            path = output / relative
            original = path.read_bytes()
            path.unlink()
            before = self.snapshot(output)
            with self.subTest(missing=relative):
                self.assertNotEqual(self.cli(root, "--check").returncode, 0)
                self.assertFalse(path.exists(), "A check must not regenerate a missing page")
                self.assertEqual(self.snapshot(output), before)
            path.write_bytes(original + b"\n<!-- manual drift -->")
            before = self.snapshot(output)
            with self.subTest(drift=relative):
                self.assertNotEqual(self.cli(root, "--check").returncode, 0)
                self.assertEqual(self.snapshot(output), before)
            path.write_bytes(original)
        before = self.snapshot(output)
        result = self.cli(root, "--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.snapshot(output), before)

    def test_check_detects_common_locale_and_template_drift_without_writing(self):
        for kind in ("common", "locale", "template"):
            with self.subTest(source=kind):
                root = self.isolated_source()
                result = self.cli(root)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                before = self.snapshot(root / "site")
                if kind == "common":
                    config = copy.deepcopy(self.config)
                    config["name"] = "Another configured project"
                    (root / "project.json").write_text(json.dumps(config), encoding="utf-8")
                elif kind == "locale":
                    code = self.config["locales"][1]["code"]
                    locale = copy.deepcopy(self.locales[code])
                    locale["hero"]["title"][0] = "A revised localized headline"
                    (root / f"locales/{code}.json").write_text(json.dumps(locale), encoding="utf-8")
                else:
                    template = root / "templates/project-homepage.html"
                    template.write_text(template.read_text(encoding="utf-8") + "\n<!-- source drift -->",
                                        encoding="utf-8")
                self.assertNotEqual(self.cli(root, "--check").returncode, 0)
                self.assertEqual(self.snapshot(root / "site"), before)

    def test_cli_supports_a_separate_output_directory(self):
        root = self.isolated_source()
        output = root / "published"
        result = self.cli(root, "--output-dir", output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(self.snapshot(output)), 8)
        self.assertFalse((root / "site").exists())
        before = self.snapshot(output)
        self.assertEqual(self.cli(root, "--output-dir", output, "--check").returncode, 0)
        self.assertEqual(self.snapshot(output), before)

    def test_retired_locale_pages_fail_check_without_deleting_manual_content(self):
        root = self.isolated_source()
        config = copy.deepcopy(self.config)
        config["locales"].append({"code": "fr", "label": "Français", "directory": "fr"})
        source_code = self.config["locales"][1]["code"]
        (root / "locales/fr.json").write_text(json.dumps(self.locales[source_code]), encoding="utf-8")
        (root / "project.json").write_text(json.dumps(config), encoding="utf-8")
        result = self.cli(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = root / "site"
        self.assertEqual(len(self.snapshot(output)), 12)

        # Retire the language without discarding either its prior generated pages
        # or an unrelated page that the adopter maintains manually.
        manual = output / "manual.html"
        manual.write_text("<!doctype html><title>Manual documentation</title><p>Keep this page.</p>",
                          encoding="utf-8")
        (root / "project.json").write_text(json.dumps(self.config), encoding="utf-8")
        result = self.cli(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        before = self.snapshot(output)
        result = self.cli(root, "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fr/", result.stdout + result.stderr)
        self.assertEqual(self.snapshot(output), before, "A check must preserve all generated and manual files")
        self.assertTrue(manual.is_file())

        for page in PAGES.values():
            (output / "fr" / page).unlink()
        before = self.snapshot(output)
        result = self.cli(root, "--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.snapshot(output), before, "An unmarked manual HTML page is allowed")

    def test_checker_accepts_binary_assets_and_counts_their_disk_budget(self):
        spec = importlib.util.spec_from_file_location("source_check", ROOT / "scripts/check.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        root = self.temporary_root()
        for name in (".github/toss.json", "LICENSE"):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        image = root / "site/assets/screen.png"
        image.parent.mkdir(parents=True)
        image.write_bytes(b"\x89PNG\r\n\x1a\n\xff\x00")
        with mock.patch.object(checker, "ROOT", root), mock.patch.object(checker, "REQUIRED", set()):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(checker.main(), 0)
            budget = json.loads((root / ".github/toss.json").read_text(encoding="utf-8-sig"))["resources"]
            image.write_bytes(b"\xff" * (int(budget["site_source_budget_kib"] * 1024) + 1))
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(checker.main(), 1)
            self.assertIn("Static site exceeds its configured size budget", checker.errors)


if __name__ == "__main__":
    unittest.main()
