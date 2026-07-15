"""Regenerate palette-analysis outputs for every licensed publication case."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MINER = ROOT / "skills" / "top-journal-palette-miner" / "scripts" / "mine_palette.py"
CASES = (
    ("nature-communications-2017-s41467-017-01124-z-fig-2", "source-figure.webp", 10),
    ("nature-communications-2021-s41467-021-23807-4-fig-2", "source-figure.webp", 12),
    ("plant-phenomics-2020-1969142-fig-5", "source-figure.jpg", 10),
    ("scientific-reports-2024-s41598-024-55775-2-fig-1", "source-figure.png", 10),
)


def main() -> None:
    cases_root = Path("examples") / "licensed-figures"
    for case, image_name, colours in CASES:
        directory = cases_root / case
        command = [
            sys.executable,
            str(MINER.relative_to(ROOT)),
            str(directory / image_name),
            "--output-dir",
            str(directory),
            "--colors",
            str(colours),
            "--max-pixels",
            "120000",
            "--seed",
            "17",
        ]
        print(f"Analysing {case}", flush=True)
        subprocess.run(command, check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
