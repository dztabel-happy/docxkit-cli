# Figures, tables, equations and sources

Use this guide for caption numbers, references in prose, citations, landscape tables, images and formulas.

## Numbering and References

| Effective policy | Captions / equations | Body reference |
| --- | --- | --- |
| 楷体/宋体 report, automatic numbered chapters | 表 2.1、图 2.1、（2.1） | 见表 2.1、如图 2.1、式 2.1 |
| 公文, any mode or heading policy | 表 1、图 1、（1） throughout the document | 见表 1、如图 1、式 1 |
| A 楷体/宋体 ordinary document (numbered headings or not); any template with `heading_numbering: none`, without chapters, or with captions before the first ordinary-document chapter | Continuous integers throughout the document | 见表 1、如图 1、式 1 |

Each numbered level-1 section counts as a chapter, including an opening summary: an opening `# 执行摘要` or `# 导论` is chapter 1 and pushes the later chapters up. When `dangling_caption_reference` fires, its message lists the numbers that exist — copy from there instead of guessing, or write the skeleton first, build once, then fill in the references. Tables, figures and equations have separate sequences. **An uncaptioned table consumes no table number.** Captions and their body references display a space between label and number, even when the source omits it. Captions/equation numbers use native Word fields; body table/figure/equation/source references are clickable, updatable fields. Editing in Word requires updating fields; rebuilding Markdown requires updating the source's reference locators as well.

**Another document's numbers.** A table, figure or equation of another document — the draft a review answers, the original under revision — is written with a backslash before the label: `修改稿\表 3.1`, `原稿\图2`, `\式 1.1`. The backslash is not shown; the number prints as ordinary text in the surrounding formatting (no field, no link, no code style), it is not checked against this document and does not count as a reference. Each such number gets an `info` check `escaped_caption_reference` with its path, so every use stays visible to a reviewer; if the number belongs to this document, remove the backslash. `report.json` keeps the backslash. The escape needs the number right after the label (one space allowed): `D:\图纸` keeps its backslash, and inside a code span or a code block the backslash is always literal. Never hide such a number in a code span or behind a no-break space.

Old 公文 references such as `见表 2.1` remain accepted: they locate the first table in the old second chapter, counting uncaptioned tables, then display its current number. `legacy_official_reference` is `info`, including under `--strict`. Integer reference recognition has boundaries: `附表 1`, `统计表 2 张` and `图 3 月` are not automatically treated as references.

Undeclared Markdown uses the new counting rule. If an old table locator and the new one point to different objects, `caption_reference_renumbered` is a **warning**, with the location and both targets. Resolve it by checking the intended object and correcting the reference before adding `numbering_rule: native-v1`. An explicit declaration prevents this migration warning; it does not repair a wrong reference. Historical JSON without a numbering marker instead retains old object lookup (`legacy-v0`). Rebuilt JSON records the rule, and new JSON is not guaranteed readable by old tools.

## Captions

For new reports, give each table or figure a caption in a separate block immediately before it. Leave a blank line between the preceding prose and the caption: a caption-looking line inside a prose paragraph remains prose. In a transcription, leave a table uncaptioned if the original has no caption.

`表1：标题`, `表 1：标题`, `表1.1：标题` and `表：标题` are recognized, with equivalent figure syntax. A real table/image must follow. Supplied numbers are recorded as `caption_number`, not used to control generated numbers; a mismatch gives `caption_number_replaced` (`info`). Captions are always numbered automatically; an original number that differs is not kept.

```markdown
见表 1.1，渠道效率对比应先由正文说明阅读目的，再放置表格。

表：渠道效率对比
| 渠道 | 状态 | 说明 |
| --- | --- | --- |
| 伙伴推荐 | 继续投入 | 线索质量稳定。 |

如图 1.1 所示，预算迁移按三个步骤推进。

图：预算迁移路径
![三个步骤](assets/migration.png)
```

This fragment assumes a first numbered chapter and the supplied `examples/assets/migration.png`; the complete report example provides the surrounding metadata and chapters.

Table font size is resolved automatically from the content: tables render at the normal size, and only drop to the dense tier when the measured content cannot fit at normal size (typically 7-8 short columns in portrait). Do not try to control table font size; `表[compact]：` from older documents is still accepted but no longer changes anything and triggers a `table_compact_layout_ignored` warning. Use `表[landscape]：标题` for wide tables that must remain intact.

Whether a table fits is decided only by how long each column's text is — its header and its longest cell — and never by `widths`, so changing widths does not clear `table_consider_landscape`. The message names the column that takes the most width at the normal size. To clear it, shorten the longest header or cell, use fewer columns, or make the table `表[landscape]：标题`. When the table reads well in the compact size (or wrapped, once a size is stated), the warning may stay; say so when delivering.

Introduce every table or figure before its caption in surrounding prose. Professional reports should not show a table or figure first and then explain it with `见表 1.1` or `如图 1.1 所示` afterward.

## Sources

Put source material in a final `# 资料来源` section. Use ordered-list items only. DocxKit renders them as native numbered `[1] xxxx`, `[2] xxxx` reference entries. On the 公文模板 the entries are set like the body (same font, size and line spacing), with `[n]` in a hanging indent two characters wide; on 楷体 and 宋体 they are one size smaller than the body (五号). With `heading_numbering: none`, an author-numbered title such as `# 第二条 资料来源` is also recognized without changing its visible title.

```markdown
公开口径显示，预算压力主要来自回款周期延长[1]。

# 资料来源

1. [国家统计局](https://www.stats.gov.cn/)，公开数据，2026-07-02 访问。
2. [行业协会研究报告](https://example.com/report)，行业资料，2026-07-02 访问。
```

Do not paste naked long URLs into prose or tables. A paragraph that still contains a bare URL or a very long Latin string (an identifier, a path) is written to allow line breaks inside words, and a justified one is set flush left, so the string wraps instead of running off the line; Word shows this as "允许西文在单词中间换行". This is deliberate: say so if the user asks why an English word was broken. Use `[来源名称](URL)` in the source list. Inline `[1]` / `[2]` citations become clickable superscript Word REF fields. Adjacent `[1][2]` citations work; range forms such as `[1–3]` are not expanded. After adding a source in Word, update the reference fields. New references inserted through “交叉引用 → 编号项” need the “来源引用” character style.

## Tables

Keep tables as real row/column data. If cells become long paragraphs, move the explanation into surrounding prose or split the table. For two lines in one cell write `<br>` (`| 2026年<br>第一季度 | … |`); see [inline formatting](docx-markdown-contract.md#inline-formatting).

DocxKit infers column widths for normal Markdown tables. For another look, stated widths or a table without a header, use the [table container](forms-and-layout.md).

A pipe table needs its separator line, the second line, with at least three hyphens per column (`| --- | --- |`). Lines that start with `|` and lack it would print as text with bars, so the build fails instead, naming the line and giving the separator to add; a separator of one or two hyphens per column (`|:-|--|`) is not recognised either and fails the same way. A single line that starts with `|` in running text is still text.

**Across pages** (every table, nothing to write): a short table — at most 10 rows besides the header, and with the header at most about a third of the text height (of the landscape page for a landscape table) — stays on one page; when it does not fit at the foot of a page it moves to the next page whole. A longer table splits normally, but its first row is not left alone at the foot of a page (under the header), and its last row is not left alone at the top of the next page — when those rows are short (up to 3 lines each); a taller row is a complete item and may stand alone. A row is split across pages only when it is tall: more than 3 lines in a grid table, more than 8 in a three-line or borderless one. The last row never keeps with the next paragraph, so rows a user adds at the end in Word or WPS (Tab in the last cell) continue the table on the page instead of pushing it to the next. Do not add `---PAGE---` before a table to keep it whole.

**Landscape pages** (`表[landscape]：标题` or `layout=landscape`): the table and its caption get landscape pages of their own, with the body's header and footer and the page numbers running on. When anything follows the table — a paragraph, a heading, `# 资料来源`, an appendix — the pages after it are portrait again. When the landscape table is the last thing in the document, the document ends on its landscape page: the empty paragraph after the table that Word requires (where the user goes on writing) is an ordinary body paragraph on that page, and no blank portrait page follows. The cost: what the user types after that table in Word or WPS stays on landscape pages; to go on in portrait, insert a next-page section break and set the new section to portrait.

A two-row table can therefore leave most of the preceding portrait page empty. For a short comparison, first see whether the columns read comfortably in portrait (shorter headers may be enough). Request landscape when the width is worth a separate page; the number of rows alone does not decide it.

## Figures

Image paths are resolved relative to the Markdown file (for `report.json`, relative to that file), not to the working directory. Keep alt text short and different from the formal `图：` caption. Every figure is a body figure with a numbered caption (`图 N`), and it fills the text width unless `report.json` (or a chart manifest beside the image) gives a width.
A figure whose file is missing fails validation; the error names the folder a relative path was resolved against and the full path that was looked for. When the user asked for a figure that does not exist, do not draw, generate or borrow one: build without that figure, tell the user which file was missing, and write a placeholder paragraph in its place (for example `［此处插入时序图］`) only if the user agrees to one.
The generated `report.json` rebases relative figure paths to its own output directory, so `docx-kit build report/report.json --out report --filename 目标文件名.docx` remains reproducible.

PNG, JPEG, GIF, and BMP files are embedded directly. PDF figures use the first page and require `pdftoppm` on `PATH` (macOS can fall back to `sips`); otherwise convert the figure to PNG/JPEG before building.
Unsupported extensions, mismatched file signatures, and corrupt bitmap files fail validation instead of producing a broken Word image.

### Chart manifests (ChartKit)

If `<image>-manifest.json` sits next to a figure image (e.g. `assets/chart.png` + `assets/chart-manifest.json`), Markdown import reads `layout.recommended_insert_width_mm` (falling back to `layout.rendered_width_mm`) to size the figure. A ChartKit image with its `-manifest.json` beside it is sized from the manifest. Discovery is fail-soft: a sidecar that is not valid JSON or has no usable width is treated as absent and never blocks or changes a build. An explicit `width` on the figure always wins over the manifest.

In direct `report.json`, `chart_manifest` on a figure block is a strict reference: the file must exist and parse, otherwise the build fails with a structured error.

## Equations

Supported LaTeX also includes accents: `\bar`/`\overline`（上横线）, `\hat`, `\tilde`, `\vec`, `\dot`, `\ddot`, `\check`, `\breve`, `\acute`, `\grave`. Unsupported commands degrade to plain text with a warning — use a supported equivalent only if it preserves the intended formula.

Block equations use fenced blocks. Write LaTeX in a `math` fence (preferred):

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

The root element must be `m:oMath` or `m:oMathPara`. Invalid OMML and unsupported LaTeX fall back to styled text with a warning in a normal build; `--strict` treats formula fallback warnings as failures. Check and repair them before delivery.

Inline math inside any body text (paragraphs, list items, table cells, callouts) uses `\( ... \)` spans, e.g. `其中 \(P_{nev}\) 表示渗透率`. Spans render as native inline equations at the surrounding font size and are never numbered. The same LaTeX subset applies; an unsupported span degrades to literal text with a warning.

Every block equation uses the effective caption policy: chapter numbers such as `（3.1）`, or continuous numbers such as `（1）`. Reference it as `式 3.1` / `公式 3.1` or `式 1` / `公式 1`. These are clickable native REF fields in body style, not superscript.

Add `title=` after the fence language to attach a caption below the equation, e.g. ```` ```math title="增长率定义" ````.
