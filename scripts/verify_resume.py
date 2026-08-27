from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}")
    return proc.stdout


def normalize_markdown(text: str) -> str:
    visible: list[str] = []
    for line in text.splitlines():
        if re.fullmatch(r"\s*-{3,}\s*", line):
            continue
        line = re.sub(r"^\s*#{1,6}\s+", "", line)
        line = re.sub(r"^\s*[-*+]\s+", "", line)
        line = line.replace("**", "").replace("__", "")
        visible.append(line)
    return re.sub(r"\s+", "", "\n".join(visible))


def normalize_rendered(text: str) -> str:
    for marker in ("•", "●", "◦", "▪", "■"):
        text = text.replace(marker, "")
    return re.sub(r"\s+", "", text)


def parse_pdfinfo(pdf: Path) -> tuple[int, tuple[float, float] | None, str]:
    if not shutil.which("pdfinfo"):
        raise RuntimeError("pdfinfo is required")
    raw = run(["pdfinfo", str(pdf)])
    pages_match = re.search(r"^Pages:\s+(\d+)", raw, flags=re.MULTILINE)
    size_match = re.search(r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", raw, flags=re.MULTILINE)
    pages = int(pages_match.group(1)) if pages_match else -1
    size = (float(size_match.group(1)), float(size_match.group(2))) if size_match else None
    return pages, size, raw


def is_a4(size: tuple[float, float] | None, tolerance: float = 3.0) -> bool:
    if size is None:
        return False
    width, height = size
    portrait = abs(width - 595.276) <= tolerance and abs(height - 841.89) <= tolerance
    landscape = abs(width - 841.89) <= tolerance and abs(height - 595.276) <= tolerance
    return portrait or landscape


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a reference-style resume PDF.")
    parser.add_argument("--source", required=True, help="Original Markdown source")
    parser.add_argument("--html", required=True, help="Generated HTML")
    parser.add_argument("--pdf", required=True, help="Rendered PDF")
    parser.add_argument("--expected-pages", type=int, default=1)
    parser.add_argument("--report", default="", help="Optional JSON report path")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    html = Path(args.html).expanduser().resolve()
    pdf = Path(args.pdf).expanduser().resolve()

    expected = normalize_markdown(source.read_text(encoding="utf-8"))
    soup = BeautifulSoup(html.read_text(encoding="utf-8"), "html.parser")
    main_node = soup.find("main")
    html_actual = normalize_rendered((main_node or soup).get_text("\n"))

    pages, page_size, _ = parse_pdfinfo(pdf)
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext is required")
    with tempfile.TemporaryDirectory(prefix="resume_verify_") as tmp:
        extracted = Path(tmp) / "pdf.txt"
        run(["pdftotext", str(pdf), str(extracted)])
        pdf_actual = normalize_rendered(extracted.read_text(encoding="utf-8"))

    checks = {
        "expected_page_count": pages == args.expected_pages,
        "a4_page_size": is_a4(page_size),
        "html_dom_order_match": expected == html_actual,
        "pdf_character_count_match": len(expected) == len(pdf_actual),
        "pdf_character_multiset_match": Counter(expected) == Counter(pdf_actual),
    }
    report = {
        "pass": all(checks.values()),
        "checks": checks,
        "page_count": pages,
        "page_size_points": page_size,
        "visible_character_counts": {
            "source": len(expected),
            "html": len(html_actual),
            "pdf": len(pdf_actual),
        },
        "notes": "PDF text extraction may reorder positioned runs; character count and multiset checks verify content completeness without relying on extraction order.",
    }

    report_path = Path(args.report).expanduser().resolve() if args.report else pdf.with_suffix(".verify.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
