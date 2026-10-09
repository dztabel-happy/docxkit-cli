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

Supported keys: `title`, `subtitle`, `author`, `client`, `date`, `language`, `confidentiality`, `template`, `document_mode`, `list_of_figures`, `list_of_tables`.
Unknown keys fail the build. `list_of_figures` and `list_of_tables` accept only `true` / `false`, `yes` / `no`, or `1` / `0`.
`language` currently accepts only `zh-CN`.

`template` defaults to `executive-cn-docx`. `executive-cn` is accepted as a ReportKit alias.

Available templates (different Chinese font pairing and layout personality):

| template id | 正文 | 章节标题 | 题注 | 封面/目录标题 | 版式 |
| --- | --- | --- | --- | --- | --- |
| `executive-cn-docx`（默认） | 楷体 | 楷体加粗 | 楷体 | 楷体（封面加粗） | 现代商务风 |
| `executive-cn-song-docx` | 宋体 | 黑体（不加粗，GB/T 9704 搭配） | 宋体 | 宋体加粗 | 正式规范风（行距 20 磅、标题段距阶梯、清北学位论文体系） |
| `executive-cn-official-docx` | 仿宋_GB2312 三号 | H1 黑体；H2 楷体_GB2312 加粗；H3 仿宋_GB2312 加粗；H4 仿宋_GB2312 | 仿宋_GB2312 小四号，表题同字号 | 方正小标宋简体（二号封面标题） | 首页副标题无前缀、无页眉、A4 默认页边距、固定 30 磅行距、公文序号“一、”“（一）”“1.”“（1）”；禁止 callout |

Latin text uses Times New Roman in all templates; Chinese always renders in the template's Chinese font, including inside inline code, code blocks and equations. Pick a non-default template only when the user asks for the corresponding typography.

`executive-cn-official-docx` defaults to `document`: the title and subtitle appear at the top of page 1 followed immediately by the body, with no separate cover or TOC. Set `document_mode: report` only when the user explicitly requests a cover or TOC, or the deliverable genuinely needs them. The two legacy templates continue to default to `report`. `document` cannot be combined with `list_of_figures` or `list_of_tables`.

Set `list_of_figures: true` / `list_of_tables: true` to append 图目录 / 表目录 after the main TOC. Entries link to the captions and jump in Word/WPS; page numbers refresh when Word opens the file. Enable them only for figure/table-heavy reports.

## Sections

- If frontmatter has `title`, `#` is a level-1 report section.
- If frontmatter has no `title`, the first `#` becomes the cover title.
- Use `##` and `###` for lower levels. `####` is supported only by `executive-cn-official-docx`; the legacy templates reject level 4. Long chapters should be split into `##` subsections. The legacy templates number them 2.1 / 2.2, while the official template uses “一、”“（一）”“1.”“（1）”:
- The first section must use `#`. Do not skip heading levels (`#` → `###`); invalid hierarchy fails validation instead of generating numbers such as `1.0.1`.

```markdown
# 市场规模与需求结构

## 渗透率走势

## 区域结构变化
```
- Chapter numbering counts every level-1 section from 1 — an opening `# 执行摘要` or `# 导论` **is chapter 1**, pushing later chapters up. Table/figure/equation numbers follow their chapter (`表 2.1` = first table in chapter 2). When a `dangling_caption_reference` error fires, its message lists the actual numbers that exist — copy from there instead of guessing, or write the skeleton first, build once, then fill in references.
- Do not manually number headings. Write `# 研究背景与方法论`, not `# 一、研究背景与方法论`; write `## 资料来源`, not `## （一）资料来源`.

## Blocks

```markdown
普通段落会变成 paragraph。

- 无序列表会变成 bullet_list。

1. 有序列表会变成 ordered_list。

> 普通引用会变成 quote。
```

Prefer paragraphs, bullet lists, ordered lists, tables, figures, and code blocks for normal report content. Use callouts only for rare high-signal emphasis. The official template rejects callouts. The default kaiti template draws an admonition box (colored left bar, light fill for risk/warning); the song template renders a plain body paragraph led by a bold label（标题或默认"风险提示"/"注"）— the formal-report idiom, no box or color.

## Inline Formatting

Body text (paragraphs, list items, quotes, callouts, table cells, source-list entries, `report.json` text fields alike) supports inline markers:

| syntax | renders as |
| --- | --- |
| `**粗体**` / `__粗体__` | bold run |
| `*斜体*` | italic run（单下划线 `_斜体_` 不支持，避免误伤 snake_case） |
| `***粗斜体***` | bold + italic run |
| `~~删除线~~` | strikethrough run |
| `` `行内代码` `` | monospaced-styled run with light gray shading, content kept literal; Chinese inside code keeps the template's Chinese font |
| `[标题](https://…)` | external hyperlink (http/https only) |
| `\( … \)` | native inline equation (see Equations) |

Markers must be paired and hug their content (`**9.1%**`, not `** 9.1% **`); unpaired markers stay literal and trigger the `unparsed_inline_markdown` warning. Backslash escapes are not interpreted. Inline markers inside section headings and table/figure/equation captions are not styled: the document shows the text with the markers removed (headings and captions already carry their own uniform style), while `report.json` keeps the heading or caption exactly as you wrote it. To keep literal `*` or `~` characters in a heading or caption, wrap them in a code span — `` 表：`电量*电价` 测算 `` is shown as `电量*电价 测算`.

## Captions

Place captions directly before every table and figure.

Prefixed caption numbers are accepted and discarded: `图 1.1：年度趋势` and `表 2.1：方法比较` import as `年度趋势` / `方法比较`, because DocxKit always renumbers tables and figures per chapter. Upstream systems can keep their own numbering in Markdown without causing double numbers.

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

Table font size is resolved automatically from the content: tables render at the normal size, and only drop to the dense tier when the measured content cannot fit at normal size (typically 7-8 short columns in portrait). Do not try to control table font size; `表[compact]：` from older documents is still accepted but no longer changes anything and triggers a `table_compact_layout_ignored` warning. Use `表[landscape]：标题` for wide tables that must remain intact.

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
The generated `report.json` rebases relative figure paths to its own output directory, so `docx-kit build report/report.json --out report --filename 目标文件名.docx` remains reproducible.

PNG, JPEG, GIF, and BMP files are embedded directly. PDF figures use the first page and require `pdftoppm` on `PATH` (macOS can fall back to `sips`); otherwise convert the figure to PNG/JPEG before building.
Unsupported extensions, mismatched file signatures, and corrupt bitmap files fail validation instead of producing a broken Word image.

### Tall figures and blank page bottoms (`--settle-figures`, opt-in)

Word cannot split a figure across pages. A figure taller than the space left on the page moves to the next page as a whole and leaves the bottom of the previous page empty — often a third to two thirds of it.

`docx-kit build <input> --out <dir> --filename <name.docx> --settle-figures` measures the real pagination after the normal build and, **in the delivered `.docx` only**, lets such a figure fall back by one or two of the ordinary paragraphs that follow it, so those paragraphs fill the page and the figure opens the next one. The paragraphs keep their order and wording; only the figure's position among them changes. The input and `report.json` keep the author's order, and every build starts again from that order.

- **Use it only on request**: when the user asks to reduce the blank space before a figure, or you can see that problem in the delivered file. It is not a default and it does not replace sizing a figure sensibly.
- **What it measures with**: on Windows with Microsoft Word installed, Word itself (the reader's pagination). Otherwise LibreOffice (`soffice` on `PATH`, `DOCXKIT_SOFFICE`, or the standard install location) plus poppler's `pdftotext`. `DOCXKIT_SETTLE_WITH=libreoffice` skips Word; `DOCXKIT_DOCX2PDF=<executable>` uses your own converter (`<it> <input.docx> <output.pdf>`).
- **LibreOffice is not the reader's Word**: the two paginate these documents a line or two apart per page. A LibreOffice-measured arrangement is re-checked with the page one or two lines taller and shorter and is delivered only if it is no worse than the draft both ways; even so, in our sample roughly one changed document in nine came out worse in real Word. For a document that matters, measure with Word.
- **A figure never moves past** a paragraph that points at it (“上图”“图中”“如上所示”), its note or source line (“注：”“资料来源：”), a paragraph describing what is on it (“右上区域”“虚线”“箭头”), a lead-in sentence (ends with a colon, “如下”“以下”), or a paragraph directly followed by a table, figure, list, equation or other non-paragraph block (it is most likely that block's lead-in; a hard page break after it does not count); it never leaves a preceding sentence that points down at it (“如下图所示：”), and a figure placed directly after another figure stays with it. These word lists only stop a move — they do not prove a paragraph is position-independent. Referring to figures by number (`见图 2.1`) is what makes a move safe.
- **Read the result**: with the flag, `build-result.json` gains `figure_settling` — `measured`, `moved_paragraphs`, `improved`, `renderer` / `renderer_version`, `rounds`, `before_page_count` / `after_page_count`, `before_pages` / `after_pages` (pages whose bottom is ≥ 25% blank: `page`, `bottom_whitespace`, `figure`), `measurements` (`round`, `figure`, `score`, `page_count`, `outcome`: `draft` / `kept` / `undone`), `figures` (`figure`, `paragraph_count`, `paragraph_starts`, `blank_before`, `blank_after`), `held` (`figure`, `why` — figures still preceded by a blank page bottom and the reason they were not moved), `notes`, `reason`, `message`. When `moved_paragraphs > 0`, **check that the paragraphs listed in `figures[].paragraph_starts` still read naturally ahead of their figure** before delivering; if one does not, rebuild without the flag. Without the flag the field is absent.
- **It never fails a build**: with missing tools or a probe error the document is still delivered — the normal one, or the best arrangement already measured — and one entry is added to `warnings` (`图位置整理未执行: …` / `图位置整理中止: …`). That entry is not a content problem: leave it, tell the user, and note that `--strict` does not fail on it. The whole pass has a time budget of about three minutes; when it runs out, the best arrangement measured so far is delivered and `figure_settling.notes` says so.
- It cannot help when the figure is followed by a table, another figure, a list, or the end of the section: there is no paragraph to bring forward. Shrink the figure, move it, or accept the blank.

### Chart manifests (ChartKit)

If `<image>-manifest.json` sits next to a figure image (e.g. `assets/chart.png` + `assets/chart-manifest.json`), Markdown import consumes `layout.recommended_insert_width_mm` (falling back to `layout.rendered_width_mm`) to size the figure. Discovery is fail-soft: a sidecar that is not valid JSON or has no usable width is treated as absent and never blocks or changes a build. An explicit `width` on the figure always wins over the manifest.

In direct `report.json`, `chart_manifest` on a figure block is a strict reference: the file must exist and parse, otherwise the build fails with a structured error.

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

Supported LaTeX also includes accents: `\bar`/`\overline`（上横线）, `\hat`, `\tilde`, `\vec`, `\dot`, `\ddot`, `\check`, `\breve`, `\acute`, `\grave`. Unsupported commands degrade to plain text with a warning — prefer subscript forms like `x_{avg}` as fallback.

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
| `table_consider_landscape` | warning | 竖版按正常字号实测放不下才提示，建议 `表[landscape]：` |
| `table_compact_layout_ignored` | warning | 字号已自动化，`表[compact]：` 标记应移除 |
| `figure_missing_caption` | warning | 图既无题注也无 alt |
| `manual_numbering_in_title` | warning | 标题带手工编号（模板会自动编号） |
| `checklist_like_bullet_items` | warning | ≥3 个带 [状态] 前缀的列表项 |
| `section_reads_like_checklist` | warning | 章节列表项多且无正文段落 |
| `flat_section_structure` | warning | 全文无二级标题且存在大体量章节 |
| `mechanical_section_nesting` | warning | 多数一级章只挂唯一一个二级节，像为凑篇幅横向摊开；应合并为更少的章、每章配多个二级节 |
| `unreferenced_caption` | warning | 带题注的表/图从未在正文引用；应在正文用“见表/图 x.x”或叙述引出 |
| `caption_before_reference` | warning | 表/图排在正文第一次用编号提到它之前；先在正文用“见表/图 x.x”引出，再放表/图（之后再次提到排在它后面没有问题） |
| `positional_caption_reference` | warning | 正文用“上图”“下图”“如下表所示”“见上表”这类位置说法指图表；图表换页或增删后就指错了，改成编号引用（“见图 x.x”“表 x.x 中”）。只认明确的搭配；全文没有图也没有表时不查 |
| `unparsed_inline_markdown` | warning | 未配对的 `**`/`__`/`~~`/反引号 会原样出现在正文；`[文本](非 http 路径)` 链接语法只支持外部 URL |

Pass `--strict` to `docx-kit build` to promote every warning-level check (and formula-degradation warnings) to a build failure — intended for CI/batch pipelines. The default is iterate-until-clean. A `--settle-figures` run that could not measure or finish is reported in `warnings` but is never a `--strict` failure.

`docx-kit components` prints the full machine-readable component contract.

`docx-kit sync-skill` mirrors the packaged skill into the machine-installed copies (`~/.claude/skills/docxkit`, `~/.agents/skills/docxkit`; only roots that already exist) and prints `{ok, command: "sync-skill", source, synced, skipped, errors}`. Updated skill files take effect in the next session.

## Machine-Readable Results (cli-contract 0.2)

`build-result.json`, `redline-result.json`, and `qa-result.json` carry `contract_version: "0.2"`; stdout is always byte-identical to the persisted result file.

- All paths in results (`input_path`, `output_dir`, `report_path`, `docx_path`, `artifacts.*`) are absolute. Pass `--filename <name.docx>` to `build`; it accepts a file name only, not a path. `docx_path` is the single authoritative Word deliverable and must not be copied or renamed by the agent.
- `build` and `validate` results carry `input_sha256`: the SHA-256 of the exact input bytes that were parsed (a successful result always has a real 64-hex digest; an unreadable input leaves it empty). `redline` and `error` results keep it empty instead of fabricating one.
- `qa` results carry `docx_sha256` and `report_sha256`, computed from the same bytes the structural checks inspected; a passing QA always has both digests.

Any upstream system can verify what was built by comparing these digests against its own copy of the input and artifacts.

## Direct report.json

Use direct `report.json` only when Markdown cannot express the required structure or exact table widths. Supported first-stage block types are:

`report.json` is a strict contract: unknown properties, invalid enum values, null object/array fields, and non-empty `appendices` fail validation instead of being ignored.

The `report.json` that `build` persists alongside the named Word deliverable omits fields equal to their defaults (empty strings/arrays, `emphasis: "normal"`, `language: "zh-CN"`, default `theme`, …) — a paragraph is just `{"type": "paragraph", "text": "…"}`. Reading is unchanged: omitted fields deserialize to the same defaults, and the slim form round-trips losslessly — section titles and table/figure/equation captions are stored as written, inline markers included, so rebuilding from `report.json` any number of times gives the same document. Selective inline emphasis inside a paragraph is expressed with the inline markers above (e.g. `"text": "弃电率为 **16.6%**。"`), not a separate runs structure.

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
