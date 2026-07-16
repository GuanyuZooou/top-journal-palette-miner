from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES_ENTRY = ROOT / "docs" / "index.html"
EXAMPLE_ENTRY = ROOT / "examples" / "palette-lab.html"


class PaletteLabTests(unittest.TestCase):
    def test_pages_and_example_entries_match(self) -> None:
        pages = PAGES_ENTRY.read_text(encoding="utf-8").rstrip()
        example = EXAMPLE_ENTRY.read_text(encoding="utf-8").rstrip()
        self.assertEqual(pages, example)

    def test_demo_is_self_contained_and_exposes_core_controls(self) -> None:
        document = PAGES_ENTRY.read_text(encoding="utf-8")
        parser = HTMLParser()
        parser.feed(document)
        parser.close()

        for element_id in (
            "imageCanvas",
            "fileInput",
            "colorCount",
            "swatches",
            "exportJson",
            "exportCss",
        ):
            self.assertIn(f'id="{element_id}"', document)
        self.assertNotIn("fetch(", document)
        self.assertNotIn("XMLHttpRequest", document)
        self.assertNotIn("https://", document)


if __name__ == "__main__":
    unittest.main()
