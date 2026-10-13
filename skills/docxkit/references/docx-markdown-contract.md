# DocxKit Markdown Contract

Use this reference when writing Markdown input for `docx-kit build`.

## Metadata

```markdown
---
title: 项目复盘报告
template: executive-cn-docx
document_mode: report
heading_numbering: auto
numbering_rule: native-v1
subtitle: v0.1
author: DocxKit
client: 内部验证
date: 2026-07-01
confidentiality: 内部资料
---
```

Supported keys: `title`, `subtitle`, `author`, `client`, `date`, `language`, `confidentiality`, `template`, `document_mode`, `heading_numbering`, `punctuation_mode`, `numbering_rule`, `list_of_figures`, `list_of_tables`.
Unknown keys fail the build. `list_of_figures` and `list_of_tables` accept only `true` / `false`, `yes` / `no`, or `1` / `0`.
`language` currently accepts only `zh-CN`.

`template` defaults to `executive-cn-docx`. `executive-cn` is accepted as a ReportKit alias.

Available templates (different Chinese font pairing and layout personality):

| template id | 正文 | 章节标题 | 题注 | 封面/目录标题 | 版式 |
| --- | --- | --- | --- | --- | --- |
| `executive-cn-docx`（默认） | 楷体 | 楷体加粗 | 楷体 | 楷体（封面加粗） | 楷体正文 |
| `executive-cn-song-docx` | 宋体 | 黑体（不加粗） | 宋体 | 宋体加粗 | 宋体正文，行距 20 磅 |
| `executive-cn-official-docx` | 仿宋_GB2312 三号 | H1 黑体；H2 楷体_GB2312 加粗；H3 仿宋_GB2312 加粗；H4 仿宋_GB2312 | 仿宋_GB2312 小四号，表题同字号 | 方正小标宋简体（二号封面标题） | 首页副标题无前缀、无页眉、A4 默认页边距、固定 30 磅行距、公文序号“一、”“（一）”“1.”“（1）”；禁止 callout |

Body Latin text uses Times New Roman; code, equations and some template roles have their own fonts. Chinese font declarations follow the template, including code and equations. Pick a non-default template only when the user asks for the corresponding typography.

All three templates support both modes:

| Template | Default mode | `report` | `document` |
| --- | --- | --- | --- |
| `executive-cn-docx` | report | Cover, TOC, chapter-name header | No cover, TOC or chapter-name header |
| `executive-cn-song-docx` | report | Cover, TOC, chapter-name header | No cover, TOC or chapter-name header |
| `executive-cn-official-docx` | document | Cover and TOC, no header | No cover, TOC or header |

Set the mode explicitly in new source. Only `report` can enable `list_of_figures: true` or `list_of_tables: true`; these add linked figure/table lists after the main TOC. Page numbers are fields that can be updated in Word. Run `docx-kit templates` to query the actual installed capabilities.

`heading_numbering` accepts `auto` (default) or `none` in every template and mode. `auto` supplies heading numbers; `none` keeps author-written clause numbers and supplies none of its own. Heading styles and outline levels remain usable. It does not disable list or caption numbering.

Put `numbering_rule: native-v1` in new Markdown. It declares that references were written against the new numbering rules; it does not choose a visual format. Do not add it to an old document before checking its reference targets. Markdown accepts only `native-v1`; legacy JSON rules are described below.

`punctuation_mode` accepts `normalize` (default for every template and mode) or `preserve`; any other value fails validation. The default can change punctuation and spaces in Chinese text. Use `preserve` when transcribing a contract, notice or letter. In JSON set `theme.punctuation_mode`. This controls text rendering, not the source stored in `report.json`; see “Punctuation and Spaces” below for the exact rules.

## Titles and Sections

Ordinary documents (`document_mode: document`) have three title cases:

| Input | Result |
| --- | --- |
| Metadata has `title` | One title block; every `#` is a real section, even if its text matches the title |
| No title, first nonblank body block is `# ...` | That heading becomes the document title and is consumed; later headings remain sections |
| No title, body starts with anything else | No title block; body starts immediately. No standalone subtitle is emitted |

A document without sections does not acquire a synthetic section. Never use whitespace or invisible characters as a title. For a report, use an explicit metadata title: legacy Markdown title inference and automatic section creation remain active in report mode and are disclosed in `effective_document.automatic_structure`.

Use `#` through `###`; only the 公文模板 accepts `####` in source input. The first real section must be level 1, and levels cannot be skipped. For automatically numbered reports, do not add author numbering:

```markdown
# 市场规模与需求结构

正文先说明本章范围。

## 渗透率走势

本节说明指标。

## 区域结构变化

本节说明差异。
```

For transcriptions with `heading_numbering: none`, retain `# 第一条 整理范围` or `## 1.1 核对时间` exactly. This turns off `manual_numbering_in_title`, but not unpaired-marker checks. See the skill's transcription workflow and the complete contract/notice/letter examples.

## Numbering and References

| Effective policy | Captions / equations | Body reference |
| --- | --- | --- |
| 楷体/宋体, automatic numbered chapters | 表 2.1、图 2.1、（2.1） | 见表 2.1、如图 2.1、式 2.1 |
| 公文, any mode or heading policy | 表 1、图 1、（1） throughout the document | 见表 1、如图 1、式 1 |
| Any template with `heading_numbering: none`, without chapters, or with captions before the first ordinary-document chapter | Continuous integers throughout the document | 见表 1、如图 1、式 1 |

Each numbered level-1 section counts as a chapter, including an opening summary. Tables, figures and equations have separate sequences. **An uncaptioned table consumes no table number.** Captions and their body references display a space between label and number, even when the source omits it. Captions/equation numbers use native Word fields; body table/figure/equation/source references are clickable, updatable fields. Editing in Word requires updating fields; rebuilding Markdown requires updating the source's reference locators as well.

Old 公文 references such as `见表 2.1` remain accepted: they locate the first table in the old second chapter, counting uncaptioned tables, then display its current number. `legacy_official_reference` is `info`, including under `--strict`. Integer reference recognition has boundaries: `附表 1`, `统计表 2 张` and `图 3 月` are not automatically treated as references.

Undeclared Markdown uses the new counting rule. If an old table locator and the new one point to different objects, `caption_reference_renumbered` is a **warning**, with the location and both targets. Resolve it by checking the intended object and correcting the reference before adding `numbering_rule: native-v1`. An explicit declaration prevents this migration warning; it does not repair a wrong reference. Historical JSON without a numbering marker instead retains old object lookup (`legacy-v0`). Rebuilt JSON records the rule, and new JSON is not guaranteed readable by old tools.

## Blocks

```markdown
普通段落会变成 paragraph。

- 无序列表会变成 bullet_list。

1. 有序列表会变成 ordered_list。

> 普通引用会变成 quote。
```

Prefer paragraphs, bullet lists, ordered lists, tables, figures, and code blocks for normal report content. Use callouts only for rare high-signal emphasis. The official template rejects callouts. The default kaiti template draws an admonition box (colored left bar, light fill for risk/warning); the song template renders a plain body paragraph led by a bold label（标题或默认"风险提示"/"注"）— the formal-report idiom, no box or color.

An ordered list is one numbering instance. Items separated only by blank lines remain one list, even if every item is written as `1.`. After an intervening paragraph, code block, table or bullet list, numbering one greater than the last authored item number continues the same instance (even when earlier items were all written as `1.`); restarting at `1.` starts a new instance. New instances display from 1. Word supports demoting/promoting list items; this is not a new Markdown nested-list syntax.

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

Markers must be paired and hug their content (`**9.1%**`, not `** 9.1% **`); unpaired markers stay literal and trigger the `unparsed_inline_markdown` warning. Only three escapes are interpreted: `\*` for a literal star, `\|` in a table cell, and line-start `1\.` (any digits, followed by whitespace) for a literal numbered paragraph. Other backslash behavior is unchanged. Code spans/blocks, math and URL targets do not decode these escapes. A masked value such as `Z*****99` is written `Z\*\*\*\*\*99`. Unpaired stars intended as literal characters should be escaped, never deleted to clear a warning. Inline markers inside section headings and table/figure/equation captions are not styled: the document shows the text with the markers removed (headings and captions already carry their own uniform style), while `report.json` keeps the heading or caption exactly as you wrote it. To keep literal `*` or `~` characters in a heading or caption, use `\*` for a star, or a code span for literal text — `` 表：`电量*电价` 测算 `` is shown as `电量*电价 测算`.

### Punctuation and Spaces

**The default is `punctuation_mode: normalize`.** In text that contains Chinese characters, the ASCII punctuation `, ; : ? ! .` becomes `，；：？！。`, and ASCII spaces between that punctuation and Chinese characters are removed. For example, `甲,  乙: 丙.` becomes `甲，乙：丙。`.

Left alone in either mode: bare `http(s)` URLs and email addresses, link targets, code spans and code blocks, native equations, and colons, commas and dots inside Latin or numeric text such as `10:00`, `1,000` and `Node.js`. A Windows drive colon next to Chinese text is not protected: `C:\资料` can become `C：\资料`.

Set `punctuation_mode: preserve` to skip this step. Author punctuation and spaces are then kept character for character. Markdown structure, inline markers, the three escapes and automatic numbering still apply. Half-width spaces and tabs at the edges of a table cell or heading are Markdown padding and are dropped; full-width spaces there are kept, so `| 甲方：　　　　 |` keeps its blank for a signature. The source text in `report.json` is never rewritten in either mode; the build receipt reports how many characters normalization changed.

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

Introduce every table or figure before its caption in surrounding prose. Professional reports should not show a table or figure first and then explain it with `见表 1.1` or `如图 1.1 所示` afterward.

## Sources

Put source material in a final `# 资料来源` section. Use ordered-list items only. DocxKit renders them as native numbered `[1] xxxx`, `[2] xxxx` reference entries. With `heading_numbering: none`, an author-numbered title such as `# 第二条 资料来源` is also recognized without changing its visible title.

```markdown
公开口径显示，预算压力主要来自回款周期延长[1]。

# 资料来源

1. [国家统计局](https://www.stats.gov.cn/)，公开数据，2026-07-02 访问。
2. [行业协会研究报告](https://example.com/report)，行业资料，2026-07-02 访问。
```

Do not paste naked long URLs into prose or tables. Use `[来源名称](URL)` in the source list. Inline `[1]` / `[2]` citations become clickable superscript Word REF fields. Adjacent `[1][2]` citations work; range forms such as `[1–3]` are not expanded. After adding a source in Word, update the reference fields. New references inserted through “交叉引用 → 编号项” need the “来源引用” character style.

## Tables

Keep tables as real row/column data. If cells become long paragraphs, move the explanation into surrounding prose or split the table.

DocxKit infers column widths for normal Markdown tables. Use direct `report.json` with `widths` only when a table needs exact control.

## Figures

Image paths are resolved relative to the Markdown file. Keep alt text short and different from the formal `图：` caption.
The generated `report.json` rebases relative figure paths to its own output directory, so `docx-kit build report/report.json --out report --filename 目标文件名.docx` remains reproducible.

PNG, JPEG, GIF, and BMP files are embedded directly. PDF figures use the first page and require `pdftoppm` on `PATH` (macOS can fall back to `sips`); otherwise convert the figure to PNG/JPEG before building.
Unsupported extensions, mismatched file signatures, and corrupt bitmap files fail validation instead of producing a broken Word image.

### Tall figures and blank page bottoms (`--settle-figures`, opt-in)

Word moves an indivisible tall figure to the next page if it cannot fit. On request, add `--settle-figures` to `build` to measure pagination and try moving it after following ordinary paragraphs. Only the delivered document is rearranged; source and `report.json` keep the author's order. Review the moved paragraphs for reading order.

Measurement uses Word on Windows, otherwise LibreOffice plus poppler. Missing tools or an interrupted measurement produce warnings and still deliver a document; these warnings alone do not fail `--strict`. Inspect `figure_settling.measured`, `moved_paragraphs`, `improved`, `measurements`, `figures`, `held` and `notes`. The built-in LibreOffice path uses a render-only copy; a custom converter uses the original unless `DOCXKIT_DOCX2PDF_RENDER_COPY=1` is explicitly set. Do not promise that this option will eliminate every gap.

### Render-only copies

```bash
docx-kit render-copy ./report/report.docx --out ./report/preview --filename report.render-only.docx
```

LibreOffice and similar renderers recalculate Word caption and reference fields incorrectly. `render-copy` writes a copy in which those fields are replaced by what they currently show; the original is never changed, and tables of contents, page numbers, headers and footers keep their fields. A freshly built document can be copied directly; for a file edited in Word or WPS, update fields and save first. The default output is `<input-stem>.render-only.docx` beside the input. Use the copy for preview and conversion only; deliver the original.

The result is JSON on stdout with `command: render-copy`, `input_sha256`, `docx_path` and `artifacts.render_copy`; `template_id` is `not-applicable`, and no `report.json` is created.

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

## Page Breaks

Use `---PAGE---` only when the user explicitly asks for a hard page break. Normal reports should rely on automatic Word/WPS pagination.

## Content Checks

`build` and `validate` return structured `checks` (`{code, severity, path, message}`). Error-level checks fail the build:

| code | report | document | Meaning and action |
| --- | --- | --- | --- |
| `dangling_caption_reference` | error | error | Reference target does not exist; use the available reference locators listed in the message, which may include legacy locators different from the displayed numbers |
| `dangling_source_reference` | error | error | `[n]` exceeds the source list; correct the reference or source |
| `table_row_wider_than_columns` | error | error | Extra cells would be lost; repair the table |
| `table_row_narrower_than_columns` | warning | warning | Missing cells render blank; check original data |
| `table_consider_landscape` | warning | warning | Table cannot fit at normal portrait size; consider landscape |
| `table_compact_layout_ignored` | warning | warning | Obsolete compact flag; remove it, sizing is automatic |
| `manual_numbering_in_title` | warning | warning | Author numbering conflicts with `auto`; use `none` when it belongs to the original |
| `unparsed_inline_markdown` | warning | warning | Unpaired markers remain literal, or a link has an unsupported target; preserve original characters, escape literal stars or repair intended formatting; use current display numbers such as 表 1 / 表 1.1 for exhibit references |
| `caption_reference_renumbered` | warning | warning | Undeclared Markdown's table reference changes target under new counting; inspect both targets before declaring the rule |
| `legacy_official_reference` | info | info | A legacy chapter locator was resolved to the intended object and displayed with its new number |
| `caption_number_replaced` | info | info | Supplied caption number differs from generated number; check fidelity |
| `table_missing_caption` | warning | info | Uncaptioned table consumes no number, enters no table list and cannot be referenced by table number; add a separate caption only if those functions are needed |
| `figure_missing_caption` | warning | info | Figure has neither caption nor alt text |
| `unreferenced_caption` | warning | info | Captioned table/figure has no body reference |
| `caption_before_reference` | warning | info | Table/figure occurs before its first numbered introduction |
| `positional_caption_reference` | warning | info | Position-based exhibit wording such as 上图/下表; new reports should reference the current displayed number, such as 表 1 or 表 1.1 |
| `checklist_like_bullet_items` | warning | info | Three or more bullet items start with status labels |
| `section_reads_like_checklist` | warning | info | Many list items with no explanatory prose |
| `flat_section_structure` | warning | info | Large chapters without subsections; the TOC follows heading levels, while numbering depends on `heading_numbering` |
| `mechanical_section_nesting` | warning | info | Repeated single-child section structure |

`manual_numbering_in_title` is suppressed by `heading_numbering: none`; unpaired-marker warnings are not. For new reports, resolve errors and warnings before delivery. In ordinary-document transcription, do not add or rewrite original text to clear `info`. It remains useful evidence when comparing with the original.

`build --strict` fails on warning-level checks and rendering warnings, including formula fallback or a requested figure/table list with no entries; `info` never fails it. An interrupted/skipped figure-settling pass can put a warning in top-level `warnings` without failing strict mode. Read both `checks` and `warnings`, not just `ok`.

`qa` is separate: it checks package structure, fields, links, styles and font declarations. Its output explicitly says `check_scope: structure_only`, `original_content_consistency: not_checked`, and `original_layout_consistency: not_checked`; read `scope_notice`. Passing QA does not mean the text matches an original, the layout matches an original, or the document is ready to deliver. It does not cancel build checks.

`docx-kit components` prints the full machine-readable component contract.

`docx-kit sync-skill` mirrors the packaged skill into the machine-installed copies (`~/.claude/skills/docxkit`, `~/.agents/skills/docxkit`; only roots that already exist) and prints `{ok, command: "sync-skill", source, synced, skipped, errors}`. Updated skill files take effect in the next session.

## Machine-Readable Results (cli-contract 0.2)

`build-result.json`, `redline-result.json`, and `qa-result.json` carry `contract_version: "0.2"`; stdout matches the persisted result file for these commands. `render-copy` instead returns its receipt only on stdout.

- All paths in results (`input_path`, `output_dir`, `report_path`, `docx_path`, `artifacts.*`) are absolute. Pass `--filename <name.docx>` to `build`; it accepts a file name only, not a path. `docx_path` is the single authoritative Word deliverable and must not be copied or renamed by the agent.
- `build` and `validate` results carry `input_sha256`: the SHA-256 of the exact input bytes that were parsed (a successful result always has a real 64-hex digest; an unreadable input leaves it empty). `redline` and `error` results keep it empty instead of fabricating one.
- `qa` results carry `docx_sha256` and `report_sha256`, computed from the same bytes the structural checks inspected; a passing QA always has both digests.

- `effective_document` on build/validate/redline describes the actual `template`, `document_mode`, `title_block`, `cover`, `toc`, `chapter_header`, `heading_numbering`, `caption_numbering` (`chapter` or `continuous`), and `punctuation_mode` (`normalize` or `preserve`). It is null when no usable model is available; on redline it describes the new side.
- `automatic_structure` records this import's changes: `document_title_from_first_h1` consumes the first ordinary-document heading as its title; `section_from_document_title_or_body` and `document_title_from_section_or_default` describe report-mode fallback structure. It is empty when none was added, including JSON rebuilds that already contain the resolved model. Ordinary documents never gain a synthetic chapter.

- `text_normalization` reports actual emitted-text changes: `mode`, `applied`, `changed_characters`, `punctuation_replacements`, `removed_spaces`, and `scope: emitted_text_including_field_caches_and_revisions`. Every replaced punctuation character and every removed ASCII space counts as one; `changed_characters` is their sum. `applied` is true only when something changed. Repeated text in a TOC cache is counted again; redline includes both sides using each side's own policy. Discarded layout attempts do not inflate the counts. Pure `validate`, `render-copy` and failures before rendering return null. Counts cover generated text, not future Word field updates.
- With only the paragraph `甲,  乙: 丙.`, the default receipt reports 3 punctuation replacements, 3 removed spaces, and 6 changed characters. Preserve mode reports zero changes and `applied: false`.

Any upstream system can verify what was built by comparing these digests against its own copy of the input and artifacts.

## Direct report.json

Use direct `report.json` only when Markdown cannot express the required structure or exact table widths. Run `components` for component fields and usage guidance.

`report.json` is a strict contract: unknown properties, invalid enum values, null object/array fields, and non-empty `appendices` fail validation instead of being ignored.

The `report.json` that `build` persists alongside the named Word deliverable omits fields equal to their defaults (empty strings/arrays, `emphasis: "normal"`, `language: "zh-CN"`, default `theme`, …) — a paragraph is just `{"type": "paragraph", "text": "…"}`. Reading is unchanged: omitted fields deserialize to the same defaults, and the slim form round-trips losslessly — section titles and table/figure/equation captions are stored as written, inline markers included, so rebuilding from `report.json` any number of times gives the same content and formatting. Selective inline emphasis inside a paragraph is expressed with the inline markers above (e.g. `"text": "弃电率为 **16.6%**。"`), not a separate runs structure.

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

New JSON fields preserve the input's meaning across rebuilds:

- Top-level `numbering_rule`: `native-v1` or `legacy-v0`; omitted historical JSON means the latter. New Markdown builds persist `native-v1`.
- `theme.document_mode`, `theme.heading_numbering` and `theme.punctuation_mode` match the Markdown options. Omitted `punctuation_mode` means `normalize`; use `preserve` for transcription.
- `sections[0].kind: body` stores ordinary-document content before any section, without creating a heading. It is allowed only as the first container in document mode, with an empty title and level 1. Other containers are `section` (default). A title-only ordinary document may have an empty sections array.
- `table`/`figure` blocks may carry `caption_number`, recording the supplied number without overriding automatic numbering.
- `ordered_list.list_id`: equal nonempty IDs continue one instance, different IDs restart at 1; an omitted/empty ID retains historical document-wide list numbering. Markdown supplies these IDs automatically.

Documents generated from different inputs never share bookmark names, so a chapter copied from one into another keeps its own references. Copies of the same document share names, as copies of any Word document do.
