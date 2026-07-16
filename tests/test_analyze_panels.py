from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "top-journal-palette-miner" / "scripts" / "analyze_panels.py"
SPEC = importlib.util.spec_from_file_location("analyze_panels", SCRIPT)
assert SPEC and SPEC.loader
analyze_panels = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = analyze_panels
SPEC.loader.exec_module(analyze_panels)


def two_panel_figure(path: Path) -> None:
    """Make white-background panels with a deliberately empty vertical gutter."""
    image = Image.new("RGB", (300, 180), "white")
    draw = ImageDraw.Draw(image)
    for left, accent in ((20, "#0072B2"), (170, "#D55E00")):
        right = left + 110
        draw.rectangle((left, 20, right, 150), outline="#202020", width=2)
        # The vertical data mark keeps every panel row above the blank-band limit.
        draw.rectangle((left + 51, 21, left + 56, 149), fill=accent)
        draw.line((left + 8, 132, right - 8, 50), fill=accent, width=3)
    image.save(path)


class PanelAnalysisTests(unittest.TestCase):
    def test_detects_two_panels_separated_by_white_gutter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "two-panels.png"
            two_panel_figure(image_path)

            panels = analyze_panels.detect_panels(
                Image.open(image_path), min_panel_size=80, padding=4
            )

            self.assertEqual(len(panels), 2)
            centres = [(left + right) // 2 for left, _, right, _ in panels]
            self.assertLess(centres[0], 150)
            self.assertGreater(centres[1], 150)

    def test_cli_writes_panel_json_and_annotation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            image_path = temp / "two-panels.png"
            output_dir = temp / "result"
            two_panel_figure(image_path)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(image_path),
                    "--output-dir",
                    str(output_dir),
                    "--min-panel-size",
                    "80",
                    "--colors",
                    "3",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Wrote 2 panel analyses", completed.stdout)
            self.assertTrue((output_dir / "panels-annotated.png").is_file())
            payload = json.loads((output_dir / "panel-analysis.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["algorithm_version"], "0.2.0")
            self.assertEqual(payload["review_scope"], "automatic-panel-candidates")
            self.assertEqual(payload["panel_count"], 2)
            self.assertEqual(payload["original_size_px"], [300, 180])
            self.assertEqual(len(payload["panels"][0]["colours"]), 3)
            self.assertEqual(payload["panels"][0]["colours"][0]["candidate_role"], "background-neutral")


if __name__ == "__main__":
    unittest.main()
