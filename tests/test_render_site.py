"""Behavior checks for project replacement, safe content, and repeatable output."""

import copy
import contextlib
import html
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("render_site", ROOT / "scripts/render_site.py")
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.images.append(dict(attrs))


class HomepageTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "project.json").read_text(encoding="utf-8-sig"))

    def test_replace_project_identity_and_actions(self):
        original_name = self.config["name"]
        original_repository = self.config["repository"]["href"]

        def replace_project(value):
            if isinstance(value, str):
                return value.replace(original_name, "Atlas Notes").replace(
                    original_repository, "https://github.com/example/atlas-notes")
            if isinstance(value, list):
                return [replace_project(item) for item in value]
            if isinstance(value, dict):
                return {key: replace_project(item) for key, item in value.items()}
            return value

        # Replace the demo's project content as an adopter would; a fixed demo
        # identity in the HTML template would still survive and fail this check.
        self.config = replace_project(self.config)
        self.config["name"] = "Atlas Notes"
        self.config["meta"]["title"] = "Atlas Notes - local research"
        self.config["hero"]["title"] = ["Collect your research.", "Find it again."]
        self.config["repository"]["href"] = "https://github.com/example/atlas-notes"
        self.config["hero"]["primary_action"]["href"] = "https://example.com/atlas/download"
        self.config["hero"]["secondary_action"]["href"] = "https://example.com/atlas/docs"
        renderer.validate_config(self.config)
        result = renderer.render(self.config)
        for value in ("Atlas Notes", "Collect your research.", "Find it again.",
                      "https://github.com/example/atlas-notes",
                      "https://example.com/atlas/download", "https://example.com/atlas/docs"):
            self.assertIn(value, result)
        self.assertNotIn(original_name, result, "The template must not hardcode its demo project")
        self.assertNotIn(original_repository, result)

    def test_untrusted_text_is_escaped_in_content_and_attributes(self):
        payload = '\"><img src=x onerror="alert(1)"> & unsafe'
        self.config["name"] = payload
        self.config["meta"]["description"] = payload
        self.config["hero"]["title"][0] = payload
        result = renderer.render(self.config)
        self.assertIn(html.escape(payload), result)
        self.assertNotIn(payload, result)
        images = Images()
        images.feed(result)
        self.assertFalse(any("onerror" in image for image in images.images))

    def test_reject_unsafe_links(self):
        for value in ("javascript:alert(1)", "data:text/html,hello", "//evil.example/x",
                      "../outside.html", "https://user:password@example.com/", "java\nscript:alert(1)"):
            with self.subTest(url=value):
                config = copy.deepcopy(self.config)
                config["repository"]["href"] = value
                with self.assertRaises(ValueError):
                    renderer.validate_config(config)

    def test_real_image_replaces_illustration_and_preserves_alt(self):
        illustration = renderer.render(self.config)
        self.config["preview"]["image"] = {
            "src": "assets/product-screen.png", "alt": 'A real screen with "notes"',
            "caption": "Captured from the application",
        }
        result = renderer.render(self.config)
        images = Images()
        images.feed(result)
        product_images = [image for image in images.images if image.get("src") == "assets/product-screen.png"]
        self.assertEqual(len(product_images), 1)
        self.assertEqual(product_images[0].get("alt"), 'A real screen with "notes"')
        self.assertIn("Captured from the application", result)
        self.assertNotIn("assets/product-screen.png", illustration)
        # An actual capture must not retain demo interface entries below it.
        for item in self.config["preview"]["items"]:
            self.assertNotIn(html.escape(item["title"]), result)

    def test_image_needs_alt_and_safe_local_path(self):
        for value in ("../private.png", "/private.png", "assets\\..\\private.png",
                      "assets/%2e%2e/%2e%2e/private.png",
                      "https://example.com/screen.png", "data:image/png;base64,AA==",
                      "//example.com/screen.png", "C:\\private.png"):
            with self.subTest(src=value):
                config = copy.deepcopy(self.config)
                config["preview"]["image"] = {"src": value, "alt": "Product screen", "caption": "Real capture"}
                with self.assertRaises(ValueError):
                    renderer.validate_config(config)
        self.config["preview"]["image"] = {"src": "assets/screen.png", "alt": " ", "caption": "Real capture"}
        with self.assertRaises(ValueError):
            renderer.validate_config(self.config)

    def cli(self, root, *args):
        return subprocess.run(
            [sys.executable, "-B", str(root / "scripts/render_site.py"), *args], cwd=root,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
        )

    def isolated_source(self):
        root = self.temporary_root()
        for name in ("project.json", "scripts/render_site.py", "templates/project-homepage.html"):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        return root

    def temporary_root(self):
        scratch = ROOT / "work"
        scratch.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="render-test-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

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

    def test_check_detects_config_and_output_drift_without_writing(self):
        root = self.isolated_source()
        self.assertNotEqual(self.cli(root, "--check").returncode, 0)
        self.assertFalse((root / "site").exists(), "A read-only check must not create its output directory")
        result = self.cli(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = root / "site/index.html"
        expected = output.read_bytes()
        timestamp = output.stat().st_mtime_ns
        result = self.cli(root, "--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(output.stat().st_mtime_ns, timestamp)

        config = copy.deepcopy(self.config)
        config["hero"]["title"][0] = "A new project headline"
        (root / "project.json").write_text(json.dumps(config), encoding="utf-8")
        self.assertNotEqual(self.cli(root, "--check").returncode, 0)
        self.assertEqual(output.read_bytes(), expected)
        self.assertEqual(output.stat().st_mtime_ns, timestamp)
        self.assertEqual(self.cli(root).returncode, 0)
        self.assertIn("A new project headline", output.read_text(encoding="utf-8"))

        output.write_text(output.read_text(encoding="utf-8") + "\n<!-- manual drift -->", encoding="utf-8")
        changed = output.read_bytes()
        self.assertNotEqual(self.cli(root, "--check").returncode, 0)
        self.assertEqual(output.read_bytes(), changed)

    def test_check_detects_template_drift_without_writing(self):
        root = self.isolated_source()
        self.assertEqual(self.cli(root).returncode, 0)
        output = root / "site/index.html"
        expected = output.read_bytes()
        template = root / "templates/project-homepage.html"
        template.write_text(template.read_text(encoding="utf-8") + "\n<!-- source change -->", encoding="utf-8")
        self.assertNotEqual(self.cli(root, "--check").returncode, 0)
        self.assertEqual(output.read_bytes(), expected)


if __name__ == "__main__":
    unittest.main()
