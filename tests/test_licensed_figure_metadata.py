from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_ROOT = ROOT / "examples" / "licensed-figures"


class LicensedFigureMetadataTests(unittest.TestCase):
    def test_every_case_is_traceable_and_hash_matches_source(self) -> None:
        metadata_files = sorted(CASES_ROOT.glob("*/metadata.yml"))
        self.assertEqual(len(metadata_files), 4)

        for metadata_path in metadata_files:
            with self.subTest(case=metadata_path.parent.name):
                metadata = metadata_path.read_text(encoding="utf-8")
                self.assertIn('licence: "CC BY 4.0"', metadata)
                self.assertIn("licence_evidence_url:", metadata)
                self.assertIn("doi:", metadata)
                self.assertIn("third_party_material_check: \"passed\"", metadata)
                self.assertIn("excluded_from_repository_mit_licence: true", metadata)

                source_files = list(metadata_path.parent.glob("source-figure.*"))
                self.assertEqual(len(source_files), 1)
                expected = re.search(r'source_sha256: "([0-9a-f]{64})"', metadata)
                self.assertIsNotNone(expected)
                actual = hashlib.sha256(source_files[0].read_bytes()).hexdigest()
                self.assertEqual(actual, expected.group(1))


if __name__ == "__main__":
    unittest.main()
