# Reference Resume Maker

一个面向 Codex 的中文简历生成技能：以 Markdown 为唯一文字来源，可参考 PDF/图片的视觉风格，输出可编辑 HTML 与可打印 A4 PDF，并自动检查页数、纸张尺寸和内容完整性。

## 功能特点

- 严格保留 Markdown 中的可见文字，不擅自增删、改写、翻译、纠错或调整顺序。
- 支持参考 PDF/图片复刻版式、层级、字体、间距、分隔线和强调色。
- 内置并嵌入 `Noto Sans CJK SC` 与 `Noto Serif`，避免 macOS/Windows/Linux 的系统字体替换造成版式漂移。
- 工作经历中的“方向：”默认表现为紧凑的小号灰字元数据，无淡灰底、圆角、描边和额外冒号间距。
- 工作经历与项目经历的小标题统一使用主题蓝，正文和列表中的加粗统一使用黑色，颜色只表达一种稳定层级。
- 支持指定十六进制主题色，例如 `#2B3C86`。
- 支持 `compact`、`balanced`、`elegant` 三种排版密度。
- 默认生成一页竖版 A4 简历；内容过长时通过字号、行距、间距和页边距调优，不删除文字。
- 同时交付可编辑 HTML 和 PDF。
- 自动验证 HTML 文字顺序、PDF 字符完整性、页数和 A4 尺寸。
- 可把 PDF 全部页面渲染为 PNG，便于检查裁切、重叠和异常换行。

## 适用场景

- 把 Markdown 简历排版成专业的一页 A4 简历。
- 参考现有 PDF 或截图重做简历样式。
- 在不修改任何文字的前提下调整留白、行高和字号。
- 为简历应用指定品牌色或个人主题色。
- 生成可继续编辑的 HTML 版本和正式投递用 PDF。

## 仓库结构

```text
.
├── SKILL.md                         # Codex 技能说明与工作流
├── README.md                        # 中文使用说明
├── requirements.txt                 # Python 依赖
├── reference-resume-maker.skill     # 可直接安装的技能包
├── assets/
│   └── fonts/                        # Noto 字体及 OFL 许可文件
├── references/
│   ├── quality-gates.md             # 内容、页面、视觉与交付门禁
│   └── style-analysis.md            # 参考版式分析方法
├── scripts/
│   ├── build_resume.py              # Markdown → HTML
│   ├── render_pdf.py                # HTML → PDF
│   ├── render_preview.py            # PDF → PNG 预览
│   └── verify_resume.py             # 内容与页面完整性校验
└── templates/
    └── reference-resume.html        # 默认 HTML/CSS 模板
```

## 环境要求

- Python 3.10 或更高版本
- Google Chrome 或 Chromium
- Poppler 工具：`pdftoppm`、`pdfinfo`、`pdftotext`
- Python 包：`Markdown`、`beautifulsoup4`

无需在系统中单独安装 Noto 字体。技能会把自带字体复制到 HTML 同目录下的 `reference-resume-maker-fonts/`，并通过 `@font-face` 固定使用。

安装 Python 依赖：

```bash
python3 -m pip install -r requirements.txt
```

macOS 安装 Poppler：

```bash
brew install poppler
```

Ubuntu/Debian 安装 Poppler：

```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

## 安装技能

### 方式一：使用 `.skill` 安装包

1. 在仓库中下载 `reference-resume-maker.skill`。
2. 将文件附加到 Codex 对话。
3. 输入：`安装此技能`。
4. 安装完成后，在下一轮对话中使用。

### 方式二：从 GitHub 手动安装

当目标目录不存在时执行：

```bash
git clone https://github.com/Moonquakesss/reference-resume-maker.git ~/.codex/skills/reference-resume-maker
```

安装或更新后，重新打开 Codex，或在新的对话轮次中使用该技能。

## 在 Codex 中使用

### 最简单的提示词

```text
请使用 reference-resume-maker，把这份 Markdown 简历生成一页 A4 PDF，内容一个字都不要修改，同时给我可编辑 HTML。
```

### 指定主题色

```text
请使用 reference-resume-maker 生成一页 A4 简历，主题色使用 #2B3C86，保留全部原文，输出 PDF 和 HTML。
```

### 参考现有版式

```text
请使用 reference-resume-maker，参考我提供的 PDF/图片版式重新排版这份 Markdown 简历。只参考视觉样式，不复制参考文件中的文字、个人信息或图标。内容一个字都不要修改，输出一页 A4 PDF 和可编辑 HTML。
```

### 调整留白和密度

```text
请使用 reference-resume-maker 优化这份简历的行高和模块间距，使页面更舒展，但仍保持一页 A4，并且不修改任何可见文字。
```

## 默认字体与颜色层级

- 中文、姓名、栏目标题、联系信息、项目标题与中文强调文字：`Noto Sans CJK SC` Regular/Bold。
- 正文英文和数字：`Noto Serif` Regular/Bold；中文字符回退到 `Noto Sans CJK SC`。
- 默认不接受 PingFang、STSongti、Times New Roman 等系统字体替换；正式导出后应使用 `pdffonts` 核对实际嵌入字体。
- 主题蓝仅用于栏目标题、分隔线，以及工作经历和项目经历的同级小标题。
- 正文段落、项目描述和列表中的加粗统一使用 `#202020` 黑色与字重 `700`，不再使用主题蓝。
- 工作经历中的 `**方向**：` 会被自动识别。“方向”按正文规则使用黑色加粗，冒号后的文字使用 `11.5px`、`#6B7280`、字重 `500`。
- 冒号后不额外添加空格、外边距或字距；无底色、圆角、描边、内边距和阴影。Markdown 原文已有的空格仍会原样保留。

## Markdown 输入建议

推荐使用以下结构：

```markdown
# 姓名

**手机**：...　|　**邮箱**：...　|　**工作年限**：...

## 教育经历

**学校**　|　专业　|　学历　|　起止时间

---

## 工作经历

### 起止时间　公司　职位

工作描述。

---

## 项目经验

### 起止时间　项目名称

项目描述。

- 成果一
- 成果二
```

标题符号、列表符号、粗体标记、空白行和分隔线会被转换成排版结构；姓名、联系方式、日期、标点、数字、项目名称、技术词和正文句子会原样保留。

## 手动生成流程

以下示例假设技能已安装在 `~/.codex/skills/reference-resume-maker`。

### 1. 生成 HTML

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/build_resume.py \
  --source /绝对路径/resume.md \
  --output /绝对路径/resume.html \
  --theme-color '#2B3C86' \
  --density elegant
```

### 2. 渲染 PDF

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/render_pdf.py \
  --in /绝对路径/resume.html \
  --out /绝对路径/resume.pdf \
  --paper A4
```

### 3. 生成预览图片

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/render_preview.py \
  --pdf /绝对路径/resume.pdf \
  --output-dir /绝对路径/preview \
  --dpi 220
```

### 4. 验证结果

```bash
python3 ~/.codex/skills/reference-resume-maker/scripts/verify_resume.py \
  --source /绝对路径/resume.md \
  --html /绝对路径/resume.html \
  --pdf /绝对路径/resume.pdf \
  --expected-pages 1 \
  --report /绝对路径/resume.verify.json
```

当报告中的 `pass` 为 `true`，表示以下检查全部通过：

- PDF 页数符合要求。
- 页面尺寸为 A4。
- HTML 可见文字与 Markdown 归一化后的文字顺序一致。
- PDF 可见字符数量与字符集合和源文件一致。

## 常用参数

### `build_resume.py`

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--source` | Markdown 源文件的绝对路径 | 必填 |
| `--output` | HTML 输出路径 | 必填 |
| `--theme-color` | 六位十六进制主题色 | `#2B3C86` |
| `--density` | `compact`、`balanced` 或 `elegant` | `elegant` |
| `--page-padding` | CSS 页边距，上、左右、下 | `15mm 15mm 7mm` |
| `--title` | HTML 文档标题 | 自动使用姓名 |

### 密度选择

| 密度 | 适合情况 |
|---|---|
| `compact` | 内容非常多，需要优先压缩到一页 |
| `balanced` | 内容量适中，希望版面中性稳妥 |
| `elegant` | 页面有余量，希望字号和留白更舒展 |

建议先尝试 `elegant`。如果内容溢出，依次切换到 `balanced`、`compact`；如果页底留白过大，则反向调整。

## 输出文件

- `resume.html`：可直接用文本编辑器修改，也可在浏览器中预览。
- `reference-resume-maker-fonts/`：HTML 使用的四个 Noto 字体文件；移动 HTML 时请一并保留此目录。
- `resume.pdf`：无浏览器页眉、页脚、日期或 URL，可直接打印和投递。
- `preview/page-*.png`：视觉检查用预览图。
- `resume.verify.json`：页数、A4 尺寸和内容一致性校验结果。

## 质量门禁

交付前应满足：

1. 不新增、删除、改写、重排、翻译或纠正可见文字。
2. PDF 页数符合要求，默认一页。
3. 页面为 A4，且没有浏览器默认页眉页脚。
4. HTML 与 PDF 的可见内容完整。
5. 默认字体实际嵌入 `NotoSansCJKsc-Regular/Bold` 与 `NotoSerif-Regular/Bold`，没有发生系统字体替换。
6. 工作经历与项目经历的小标题统一为主题蓝，正文和列表中的加粗统一为黑色。
7. “方向：”后的文字为紧凑小号灰字，且没有淡灰底、圆角或额外冒号间距。
8. 所有页面均已渲染为图片并完成视觉检查。
9. 没有裁切、重叠、孤行、异常换行、层级混乱或明显失衡的页底留白。

## 常见问题

### 找不到 `markdown` 或 `bs4`

```bash
python3 -m pip install Markdown beautifulsoup4
```

### 找不到 Chrome

安装 Google Chrome/Chromium，或在运行 `render_pdf.py` 时通过 `--chrome` 指定可执行文件路径。

### 找不到 `pdftoppm`、`pdfinfo` 或 `pdftotext`

安装 Poppler，并确认这些命令已加入 `PATH`。

### PDF 超过一页

按 `elegant → balanced → compact` 的顺序降低密度；仍超页时，小幅减少行高、列表间距、模块间距和页边距。不要删除文字。

### 页面底部留白过大

按 `compact → balanced → elegant` 的顺序提高密度档位，再小幅增加正文行高、段落间距和模块间距。

### PDF 中文字体显示异常

确认 HTML 同目录存在 `reference-resume-maker-fonts/`，并包含四个 Noto 字体文件。重新运行 `build_resume.py` 可自动恢复该目录；随后重新导出 PDF，并用 `pdffonts` 确认没有被 PingFang、STSongti 或其他系统字体替换。

## 隐私说明

简历通常包含姓名、电话和邮箱。建议在本地运行生成与验证流程，不要把个人简历、参考文件或生成结果提交到公开仓库。本仓库只包含通用技能、脚本和模板。

## 许可说明

随技能分发的 Noto 字体采用 SIL Open Font License 1.1，许可文本位于 `assets/fonts/OFL-NotoSansCJK.txt` 与 `assets/fonts/OFL-NotoSerif.txt`。本仓库其余代码和文档目前未附加统一开源许可证；如需允许第三方复制、修改或分发，请由仓库所有者选择并添加合适的许可证。
