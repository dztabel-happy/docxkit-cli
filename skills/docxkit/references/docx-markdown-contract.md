# DocxKit Markdown Contract

Use this reference when writing Markdown input for `docx-kit build`.

## Metadata

```markdown
---
title: 项目复盘报告
subtitle: v0.1
author: DocxKit
client: 内部验证
date: 2026-07-01
confidentiality: 内部资料
---
```

Supported keys: `title`, `subtitle`, `author`, `client`, `date`, `language`, `confidentiality`, `template`, `list_of_figures`, `list_of_tables`.

`template` defaults to `executive-cn-docx`. `executive-cn` is accepted as a ReportKit alias.

Available templates (identical layout, different Chinese font pairing):

| template id | 正文 | 标题/封面/目录标题 | 题注 |
| --- | --- | --- | --- |
| `executive-cn-docx`（默认） | 楷体 | 楷体加粗 | 楷体 |
| `executive-cn-song-docx` | 宋体 | 黑体加粗（GB/T 9704 搭配） | 宋体加粗 |

Latin text uses Times New Roman in both. Pick the song variant only when the user asks for 宋体/黑体 styling; otherwise keep the default.

Set `list_of_figures: true` / `list_of_tables: true` to append 图目录 / 表目录 after the main TOC. Entries link to the captions and jump in Word/WPS; page numbers refresh when Word opens the file. Enable them only for figure/table-heavy reports.

## Sections

- If frontmatter has `title`, `#` is a level-1 report section.
- If frontmatter has no `title`, the first `#` becomes the cover title.
- Use `##` and `###` for lower levels.
- Do not manually number headings. Write `# 研究背景与方法论`, not `# 一、研究背景与方法论`; write `## 资料来源`, not `## （一）资料来源`.

## Blocks

```markdown
普通段落会变成 paragraph。

- 无序列表会变成 bullet_list。

1. 有序列表会变成 ordered_list。

> 普通引用会变成 quote。
```

Prefer paragraphs, bullet lists, ordered lists, tables, figures, and code blocks for normal report content. Use callouts only for rare high-signal emphasis.

## Captions

Place captions directly before every table and figure.

```markdown
见表1.1，渠道效率对比应先由正文说明阅读目的，再放置表格。

表：渠道效率对比
| 渠道 | 状态 | 说明 |
| --- | --- | --- |
| Partner Program | 继续投入 | 线索质量稳定。 |

如图1.1所示，瀑布图用于解释关键指标的拆分路径。

图：结算瀑布图
![瀑布图](assets/waterfall.png)
```

Use `表[compact]：标题` only for dense numeric/status/checklist tables with many short cells; use normal `表：标题` for narrative or comparison tables. Use `表[landscape]：标题` for wide tables that must remain intact.

Introduce every table or figure before its caption in surrounding prose. Professional reports should not show a table or figure first and then explain it with `见表1.1` or `如图1.1所示` afterward.

## Sources

Put source material in a final `# 资料来源` section. Use ordered-list items only. DocxKit renders them as `[1] xxxx`, `[2] xxxx` reference entries.

```markdown
公开口径显示，预算压力主要来自回款周期延长[1]。

# 资料来源

1. [国家统计局](https://www.stats.gov.cn/)，公开数据，2026-07-02 访问。
2. [行业协会研究报告](https://example.com/report)，行业资料，2026-07-02 访问。
```

Do not paste naked long URLs into prose or tables. Use `[来源名称](URL)` in the source list. Inline `[1]` / `[2]` citations become clickable superscript Word references.

## Tables

Keep tables as real row/column data. If cells become long paragraphs, move the explanation into surrounding prose or split the table.

DocxKit infers column widths for normal Markdown tables. Use direct `report.json` with `widths` only when a table needs exact control.

## Figures

Image paths are resolved relative to the Markdown file. Keep alt text short and different from the formal `图：` caption.

## Callouts

```markdown
> [!note] 关键说明
> 这句话必须从正文中被快速扫到。

> [!risk] 风险提示
> 只在用户明确需要视觉风险框时使用。
```

Supported kinds: `note`, `insight`, `risk`, `warning`. `tip` is normalized to `note`.

## Code Blocks

````markdown
```json renderer_contract
{
  "renderer": "docx-kit",
  "template": "executive-cn-docx"
}
```
````

The first word after the opening fence is the language. The remaining text becomes the optional code-block title. If no title is provided, DocxKit shows the language label. Code remains editable in Word and may use lightweight syntax colors.

## Equations

Block equations use fenced blocks. Write LaTeX in a `math` fence (preferred — highest reliability):

````markdown
```math
\sum_{i=1}^{n} \frac{x_i}{\sigma} \ge \sqrt{y}
```
````

Supported LaTeX subset: fractions (`\frac`), roots (`\sqrt`, `\sqrt[n]`), sub/superscripts, `\sum` `\prod` `\int` with limits, `\left(...\right)`, Greek letters, common operators/relations (`\times` `\le` `\ne` `\infty` `\to` …), and `\text{}`.

Use an `omml` fence only in two cases: the formula came from a Word source (paste its native OMML verbatim for lossless transfer), or the build reported a `formula rendered as plain text` warning for LaTeX outside the subset:

````markdown
```omml
<m:oMath><m:r><m:t>x</m:t></m:r></m:oMath>
```
````

The root element must be `m:oMath` or `m:oMathPara`. Invalid OMML and unsupported LaTeX never fail the build: the formula degrades to styled text and a warning appears in `build-result.json` — always check warnings and repair the formula.

Inline math inside any body text (paragraphs, list items, table cells, callouts) uses `\( ... \)` spans, e.g. `其中 \(P_{nev}\) 表示渗透率`. Spans render as native inline equations at the surrounding font size and are never numbered. The same LaTeX subset applies; an unsupported span degrades to literal text with a warning.

Every block equation is numbered per chapter — `（3.1）` on the right edge, same numbering family as tables/figures. Reference equations in body text as `式 3.1` or `公式 3.1`; the text stays normal body style (not superscript) and becomes a clickable jump, exactly like `见表3.1`.

Add `title=` after the fence language to attach a caption below the equation, e.g. ```` ```math title="增长率定义" ````.

## Page Breaks

Use `---PAGE---` only when the user explicitly asks for a hard page break. Normal reports should rely on automatic Word/WPS pagination.

## Content Checks

`build` and `validate` return structured `checks` (`{code, severity, path, message}`). Error-level checks fail the build:

| code | severity | meaning |
| --- | --- | --- |
| `dangling_caption_reference` | error | 正文引用的 表/图/式 x.x 不存在 |
| `dangling_source_reference` | error | `[n]` 超出资料来源条目数 |
| `table_row_wider_than_columns` | error | 行内单元格多于列数，数据会被丢弃 |
| `table_row_narrower_than_columns` | warning | 行内单元格少于列数，缺口渲染为空白 |
| `table_missing_caption` | warning | 表格缺“表：标题” |
| `table_consider_landscape` | warning | ≥6 列建议 `表[landscape]：` |
| `figure_missing_caption` | warning | 图既无题注也无 alt |
| `manual_numbering_in_title` | warning | 标题带手工编号（模板会自动编号） |
| `checklist_like_bullet_items` | warning | ≥3 个带 [状态] 前缀的列表项 |
| `section_reads_like_checklist` | warning | 章节列表项多且无正文段落 |

`docx-kit components` prints the full machine-readable component contract.

## Direct report.json

Use direct `report.json` only when Markdown cannot express the required structure or exact table widths. Supported first-stage block types are:

```text
paragraph
table
figure
ordered_list
source_list
bullet_list
quote
code_block
callout
page_break
```

Compatibility blocks can exist in explicit JSON, but Markdown should not generate them for ordinary reports:

```text
definition_list
checklist
metric_grid
equation
inline_math
```
