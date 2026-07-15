from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "top-journal-palette-miner" / "scripts" / "mine_palette.py"
SPEC = importlib.util.spec_from_file_location("mine_palette", SCRIPT)
assert SPEC and SPEC.loader
mine_palette = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mine_palette)


class PaletteMinerTests(unittest.TestCase):
    def test_classify_background_and_rare_accent(self) -> None:
        background = np.array([250, 250, 248], dtype=np.uint8)
        accent = np.array([255, 60, 20], dtype=np.uint8)

        self.assertEqual(mine_palette.classify(background, 0.90)[0], "background-neutral")
        self.assertEqual(mine_palette.classify(accent, 0.01)[0], "rare-accent-candidate")

    def test_kmeans_is_deterministic_for_a_seed(self) -> None:
        pixels = np.array([[0, 0, 0]] * 20 + [[255, 255, 255]] * 20, dtype=np.float32)
        first_centres, first_labels = mine_palette.kmeans(pixels, 2, seed=17)
        second_centres, second_labels = mine_palette.kmeans(pixels, 2, seed=17)

        np.testing.assert_array_equal(first_centres, second_centres)
        np.testing.assert_array_equal(first_labels, second_labels)

    def test_cli_writes_expected_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            image_path = temp / "input.png"
            output_dir = temp / "result"
            image = Image.new("RGB", (20, 10), "#FAFAF8")
            for x in range(10, 20):
                for y in range(10):
                    image.putpixel((x, y), (77, 119, 155))
            image.save(image_path)

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(image_path), "--output-dir", str(output_dir), "--colors", "2"],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Wrote 2 colour candidates", completed.stdout)
            self.assertTrue((output_dir / "palette.csv").is_file())
            self.assertTrue((output_dir / "palette-preview.png").is_file())
            payload = json.loads((output_dir / "palette.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["cluster_count"], 2)
            self.assertEqual(payload["original_size_px"], [20, 10])


if __name__ == "__main__":
    unittest.main()
