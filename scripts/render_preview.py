from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render resume PDF pages to PNG for visual review.")
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dpi", type=int, default=220)
    args = parser.parse_args()

    if not shutil.which("pdftoppm"):
        raise RuntimeError("pdftoppm is required")

    pdf = Path(args.pdf).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(args.dpi), str(pdf), str(prefix)],
        check=True,
    )
    images = sorted(output_dir.glob("page-*.png"))
    if not images:
        raise RuntimeError("No preview images were generated")
    for image in images:
        print(image)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
