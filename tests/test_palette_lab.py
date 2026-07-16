from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES_ENTRY = ROOT / "docs" / "index.html"
EXAMPLE_ENTRY = ROOT / "examples" / "palette-lab.html"


class PaletteLabTests(unittest.TestCase):
    def test_example_entry_points_to_the_maintained_pages_source(self) -> None:
        example = EXAMPLE_ENTRY.read_text(encoding="utf-8")
        self.assertIn('url=../docs/index.html', example)
        self.assertIn('href="../docs/index.html"', example)

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
            "inspectTab",
            "transferTab",
            "referenceFileInput",
            "targetFileInput",
            "seriesCount",
            "runTransfer",
            "exportTransferJson",
        ):
            self.assertIn(f'id="{element_id}"', document)
        self.assertNotIn("fetch(", document)
        self.assertNotIn("XMLHttpRequest", document)
        self.assertNotIn("https://", document)

    def test_transfer_rules_and_schema_are_present(self) -> None:
        document = PAGES_ENTRY.read_text(encoding="utf-8")
        for text in (
            "function transferRecommendation",
            "schema_version: 1",
            "observed_palette",
            "requested_series_count",
            "no colours were fabricated",
            "The only rare accent allocation",
        ):
            self.assertIn(text, document)

    def test_transfer_layout_has_narrow_screen_fallback(self) -> None:
        document = PAGES_ENTRY.read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 830px)", document)
        self.assertIn(".transfer-inputs, .transfer-fields { grid-template-columns: 1fr; }", document)


if __name__ == "__main__":
    unittest.main()
