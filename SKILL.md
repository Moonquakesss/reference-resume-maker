---
name: reference-resume-maker
description: Recreate or refine a Chinese résumé from Markdown using the visual style of reference PDFs/images, preserve every visible source character, apply a requested theme color, export editable HTML and an A4 PDF, and verify page count and content integrity. Use when users ask to imitate a résumé layout, restyle an existing résumé, fit it to one page, adjust whitespace/line-height, or require “内容一个字都不要修改”.
---

# Reference Resume Maker

Use this skill to convert a Markdown résumé into an editable HTML résumé and printable PDF while treating reference documents as visual guidance only. Preserve the original Markdown as the sole text source.

## Non-negotiable rules

Do not add, delete, rewrite, reorder, summarize, translate, or correct visible résumé text. Convert only Markdown structure such as headings, list markers, bold markers, blank lines, and horizontal rules. When the user specifies a color, use that exact hex value as the primary accent.

Keep the requested page count. Default to one portrait A4 page. Never achieve page fit by deleting text; adjust typography and spacing instead.

## Default typography and work-direction style

Unless the user explicitly requests another typeface, use the bundled font assets and require this mapping in the exported PDF:

- Chinese text, headings, contact information, entry titles, and emphasized Chinese text: `Noto Sans CJK SC` Regular/Bold.
- Latin text and numerals in body paragraphs: `Noto Serif` Regular/Bold, with `Noto Sans CJK SC` as the Chinese fallback.
- Do not accept silent substitution by PingFang, STSongti, Times New Roman, or another system font. Confirm the embedded font names with `pdffonts` after rendering.

When a work-experience paragraph starts with `**方向**：`, keep `方向：` at the normal work-experience size and style only the visible text after the colon as compact metadata: `11.5px`, `#6B7280`, weight `500`, no background, border, padding, or border radius. Do not inject a space, CSS margin, or letter spacing after the colon. Preserve any whitespace that already exists in the Markdown because it is source content.

## Workflow

1. Inspect the source Markdown once and record the page-count, content-preservation, color, and delivery constraints.
2. When references are provided, read `references/style-analysis.md`. Render PDF references to images and inspect every relevant page. Record page geometry, fonts, alignment, hierarchy, line styles, list indentation, emphasis color, and whitespace.
3. Build HTML from the Markdown with `scripts/build_resume.py`. The script copies the bundled Noto assets beside the HTML, embeds them through `@font-face`, and applies the work-direction metadata style. Start with the density profile that best matches the target: `elegant` for more breathing room, `balanced` for a neutral layout, or `compact` for dense content.
4. Render the HTML with `scripts/render_pdf.py`. Do not use browser print defaults that add headers, footers, dates, or URLs.
5. Render all PDF pages to PNG with `scripts/render_preview.py`. Visually inspect clipping, overlap, awkward wrapping, hierarchy, alignment, list rhythm, and top/bottom whitespace.
6. Read `references/quality-gates.md`, run `scripts/verify_resume.py`, and inspect `pdffonts` output. Require all content, page, font, and visual checks to pass before delivery.
7. Iterate only on CSS parameters or the template. Rebuild, rerender, preview, and verify after each meaningful change.
8. Deliver the PDF and editable HTML. Keep the verification JSON and previews as internal supporting artifacts unless the user asks for them.

## Commands

Create HTML:

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/build_resume.py \
  --source /absolute/path/resume.md \
  --output /absolute/path/resume.html \
  --theme-color '#2B3C86' \
  --density elegant
```

Render PDF:

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/render_pdf.py \
  --in /absolute/path/resume.html \
  --out /absolute/path/resume.pdf \
  --paper A4
```

Render visual evidence:

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/render_preview.py \
  --pdf /absolute/path/resume.pdf \
  --output-dir /absolute/path/preview \
  --dpi 220
```

Verify content and page requirements:

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/verify_resume.py \
  --source /absolute/path/resume.md \
  --html /absolute/path/resume.html \
  --pdf /absolute/path/resume.pdf \
  --expected-pages 1 \
  --report /absolute/path/resume.verify.json
```

## Density and whitespace adjustments

| Situation | First adjustment | Second adjustment |
|---|---|---|
| Bottom whitespace is too large | Switch `compact → balanced → elegant` | Increase body line-height, item gaps, and section margins slightly |
| Content spills to another page | Switch `elegant → balanced → compact` | Reduce line-height, item gaps, section margins, then page padding |
| Text feels small but whitespace remains | Increase body font by 0.1–0.3px | Recheck wrapping and page count |
| Hierarchy feels weak | Increase heading weight or accent contrast | Keep body color neutral and avoid adding decoration |

Prefer line-height and vertical rhythm changes over large font-size changes. Keep bottom whitespace intentional rather than forcing content to the physical page edge.

## Template ownership

Use `templates/reference-resume.html` as the default style owner. Its default visual language is a centered name, compact contact line, full-width accent rule, accent-colored section headings with thin rules, dark neutral body text, blue project headings, and selective keyword emphasis. Modify a copy of the template or expose additional script parameters when a reference requires a materially different structure.

The template owns the Noto font mapping and the `work-direction` / `direction-tag` rules. Keep the bundled files in `assets/fonts/`; `build_resume.py` copies them to `reference-resume-maker-fonts/` beside each generated HTML file so the editable output does not depend on fonts installed on the host system. If the user explicitly requests a different font, update both the font assets and `@font-face` mapping, then verify the actual PDF fonts rather than relying on CSS family names alone.

Do not copy visible text, personal data, icons, or project content from reference documents. Use them only to infer layout and styling.
