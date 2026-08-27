from __future__ import annotations

import argparse
import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup


DENSITY = {
    "compact": {
        "BODY_FONT_SIZE": "12.9",
        "BODY_LINE_HEIGHT": "1.38",
        "SECTION_MARGIN": "8px 0 6px",
        "ENTRY_MARGIN": "6px 0 3px",
        "PROJECT_TOP_GAP": "8px",
        "PARAGRAPH_BOTTOM_GAP": "4px",
        "LIST_MARGIN": "2px 0 6px 18px",
        "LIST_ITEM_GAP": "1.5px",
    },
    "balanced": {
        "BODY_FONT_SIZE": "13.1",
        "BODY_LINE_HEIGHT": "1.42",
        "SECTION_MARGIN": "9px 0 7px",
        "ENTRY_MARGIN": "7px 0 3px",
        "PROJECT_TOP_GAP": "9px",
        "PARAGRAPH_BOTTOM_GAP": "5px",
        "LIST_MARGIN": "2px 0 7px 18px",
        "LIST_ITEM_GAP": "2px",
    },
    "elegant": {
        "BODY_FONT_SIZE": "13.2",
        "BODY_LINE_HEIGHT": "1.46",
        "SECTION_MARGIN": "10px 0 7px",
        "ENTRY_MARGIN": "7px 0 4px",
        "PROJECT_TOP_GAP": "10px",
        "PARAGRAPH_BOTTOM_GAP": "5px",
        "LIST_MARGIN": "3px 0 8px 18px",
        "LIST_ITEM_GAP": "2.5px",
    },
}


def normalize_hex(value: str) -> str:
    value = value.strip()
    if not value.startswith("#"):
        value = "#" + value
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        raise ValueError(f"Invalid theme color: {value}")
    return value.upper()


def darken(hex_color: str, ratio: float = 0.82) -> str:
    raw = hex_color.lstrip("#")
    channels = [int(raw[i : i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{max(0, min(255, round(c * ratio))):02X}" for c in channels)


def normalize_markdown_structure(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() == "---":
            if output and output[-1].strip():
                output.append("")
            output.append(line)
            if index + 1 < len(lines) and lines[index + 1].strip():
                output.append("")
        else:
            output.append(line)
    return "\n".join(output)


def add_section_classes(soup: BeautifulSoup) -> None:
    section_map = {
        "个人信息": "personal",
        "教育经历": "education",
        "工作经历": "work",
        "项目经验": "projects",
    }
    current = ""
    for node in soup.children:
        if getattr(node, "name", None) == "h2":
            current = node.get_text(strip=True)
            node["class"] = ["section-title", f"section-{section_map.get(current, 'generic')}"]
        elif getattr(node, "name", None):
            slug = section_map.get(current, "generic")
            node["class"] = list(node.get("class", [])) + [f"section-{slug}"]


def collapse_personal_section(soup: BeautifulSoup) -> None:
    heading = soup.find("h2", string=lambda value: value and value.strip() == "个人信息")
    if not heading:
        return
    info = heading.find_next_sibling("p")
    if not info:
        return
    wrapper = soup.new_tag("div")
    wrapper["class"] = ["contact-block"]
    label = soup.new_tag("span")
    label["class"] = ["contact-label"]
    label.string = heading.get_text()
    info["class"] = ["contact-info"]
    heading.replace_with(wrapper)
    wrapper.append(label)
    info.extract()
    wrapper.append(info)


def fill_template(template: str, values: dict[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", result)))
    if unresolved:
        raise ValueError(f"Unresolved template placeholders: {', '.join(unresolved)}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a reference-style one-page resume HTML from Markdown.")
    parser.add_argument("--source", required=True, help="Source Markdown resume")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--theme-color", default="#2B3C86", help="Six-digit hex accent color")
    parser.add_argument("--density", choices=sorted(DENSITY), default="elegant")
    parser.add_argument("--page-padding", default="19mm 18mm 8mm")
    parser.add_argument("--title", default="")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    template_path = Path(__file__).resolve().parents[1] / "templates" / "reference-resume.html"

    source_text = source.read_text(encoding="utf-8")
    fragment = markdown.markdown(
        normalize_markdown_structure(source_text),
        extensions=["extra", "sane_lists"],
    )
    soup = BeautifulSoup(fragment, "html.parser")
    add_section_classes(soup)
    collapse_personal_section(soup)

    h1 = soup.find("h1")
    document_title = args.title or (h1.get_text(strip=True) + " - 简历" if h1 else source.stem)
    theme = normalize_hex(args.theme_color)

    values = {
        "DOCUMENT_TITLE": document_title,
        "THEME_COLOR": theme,
        "THEME_DARK": darken(theme),
        "PAGE_PADDING": args.page_padding,
        "CONTENT_HTML": str(soup),
        **DENSITY[args.density],
    }
    html = fill_template(template_path.read_text(encoding="utf-8"), values)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
