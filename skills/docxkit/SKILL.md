---
name: docxkit
description: Use when prepared content, uploaded materials, Markdown, or report.json should become an editable Word document through the local docx-kit CLI — reports with a cover and contents, and plain documents such as notices, letters, certificates, contracts, minutes, résumés, forms and oaths, newly written or transcribed, in the template's look or in a format the user states. This skill formats and exports content; it does not gather sources or verify a transcription against its original by itself.
---

# DocxKit

DocxKit turns Markdown (or `report.json`) into a Word `.docx` the user can keep writing in Word or WPS: real styles, native numbering, updatable references. You write the content as ordinary Markdown and run one command. Do not produce the Word file any other way (python, OpenXML, a template of your own), and never patch the generated `.docx`: change the source and rebuild.

## First decision: does the user want a report?

| The user wants | Write |
| --- | --- |
| A report — most documents with chapters, where a cover and a contents page make sense | `document_mode: report` |
| A document that certainly needs no cover or contents (notice, letter, certificate, contract, minutes, résumé, oath, form) and has no chapter headings | no `document_mode`; usually no metadata at all |
| The same, but with chapter headings (`#`) | `document_mode: document`, and the title as `title:` |

If `document_mode` is not written, the content decides: any chapter heading makes it a report, none makes it a plain document. A first-line `# 标题` is the title, not a chapter (unless the metadata already has `title:`). A numbered line with its own content under it (paragraphs, a list, a table) is a heading — `# 二、议定事项`; a numbered line that is complete in itself is a list item. `effective_document` in the build receipt says what was built — read it every time. A plain document has no cover, contents or header, keeps the heading and list numbers you wrote, and shows page numbers only once it has a second page (on the 公文模板 the template numbers headings and lists, and the page number always shows).

## Two complete inputs

A short document needs no settings:

```markdown
# 关于召开第三季度经营分析会的通知

::: 顶格
各部门：
:::

公司定于近期召开第三季度经营分析会，现将有关事项通知如下：

一、会议时间和地点：2026 年 10 月 20 日上午 9:30，总部三楼第一会议室。
二、有关要求：请于 10 月 16 日前报送汇报材料。

特此通知。

::: 靠右
综合管理部

2026 年 10 月 13 日
:::
```

`::: 顶格` sets paragraphs flush left (a salutation), `::: 靠右` right (a sign-off), `::: 居中` centred; inside a container, separate paragraphs with a blank line. The `一、` items become a native Word list numbered as written. The shortest report:

```markdown
---
title: 第三季度渠道复盘
document_mode: report
numbering_rule: native-v1
---

# 结论

本季度各渠道的投入建议见表 1.1。

表：渠道投入建议
| 渠道 | 建议 |
| --- | --- |
| 伙伴计划 | 继续投入 |

# 下一步

十月底前完成预算调整，十一月复核回款周期。
```

It gets a cover, a contents page, automatic chapter numbers (so write headings without numbers) and captions numbered by chapter. The cover shows `title` and, when you give them, `subtitle`, `client`, `date` and `confidentiality`. `numbering_rule: native-v1` declares that numbered references follow the current numbering; put it in every new source that refers to tables or figures by number.

## The working loop

This skill matches `@dztabel/docxkit >= 0.2.0`; what decides is what the binary reports. `docx-kit templates` prints `by_structure` when it has plain documents, `:::` containers and lists as written, and names under `format.features` the step-two features it has — all of them are `text_scale`, `role_font`, `role_latin_font`, `role_size`, `role_line_spacing`, `page_margins`, `table_appearance`, `table_without_header`, `table_spacing`, `paragraph_spacing`, `parallel`, `page_position`. An older binary prints `:::` lines as text, makes a short text a report with a cover and rejects those keys: if something you need is missing, tell the user rather than building something else.

```bash
npm install @dztabel/docxkit@latest; npx --no-install docx-kit --version; npx --no-install docx-kit sync-skill
```

1. Save the content as `./output_docx/content.md` (or edit the existing `report.json`), one output folder per document. This source is what any later rebuild uses; keep it.
2. Build, always with `--filename <descriptive-name.docx>` (a file name, no directories). The build writes `build-result.json` and `report.json` beside the `.docx`. The other options are `--strict`, `--embed-fonts` and `--settle-figures`; there is no `--help`.
3. Read the whole `build-result.json`. `errors`: fix the named field, line or missing file in the source and rebuild. `effective_document`: is it the kind of document you meant — mode, cover, contents, heading and list numbering, and under `format` the fonts, sizes, line spacing, margins and page position in effect? `automatic_structure` lists what was decided for you. `checks` and `warnings`: in new writing resolve every warning (`--strict` makes them failures); `info` needs no action. `text_normalization`: `applied: true` means punctuation or spaces were changed — if the text must stay as written, or you cannot tell what changed, add `punctuation_mode: preserve`.
4. Run `qa`. It inspects the package, not the content: `check_scope: structure_only` and `not_checked` mean exactly that, and a pass is not delivery approval. The receipt has no page count: when the user set one or the look matters, render the copy (notes at the end) and look; if you cannot, say the page count is unconfirmed.
5. Deliver the `docx_path` the build returned, without copying or renaming it. Give the source path, what you checked (at least the receipt, and `report.json` against what you wrote), any warning you could not resolve and why, anything the user asked for that could not be done, every fact you left blank or made up, and the instructions below.

```bash
npx --no-install docx-kit build ./output_docx/content.md --out ./output_docx --filename 经营分析会通知.docx
npx --no-install docx-kit qa ./output_docx/经营分析会通知.docx --report-json ./output_docx/report.json --out ./output_docx/qa
```

### Tell the user

Edits made in Word never flow back into the source: before rebuilding a file the user has edited, reconcile it with the source ([Revising documents](references/revising-documents.md)). In the user's language, say what they can do with the file; for Chinese deliveries use these lines — the first and the last always (drop from the first what the document does not have), the others only when the document has what they mention; they may be shortened:

- 这份 Word 可以直接接着写：标题后回车就是正文，表格、代码块后面可以直接输入；改“正文”“标题 1”“题注”“三线表”这些样式，全篇跟着变。
- 增删表、图、公式或资料来源后，全选按 F9（Mac 上是 fn+F9），编号和正文里的引用会一起更新，Word 和 WPS 都是这样。只想更新某一处，在它上面点右键选“更新域”。
- 用“插入题注”之前，先在题注对话框里建好“表”“图”标签并设好编号：按章编号的文档勾选“包含章节号”（章节起始样式“标题 1”、分隔符“句点”），全文连续编号的文档不勾。先设置再插入——Word 会按当前设置改写文档里已有的同类题注。WPS 自带这两个标签，在“编号”里勾选“题注关联章节编号”，分隔符改成句点。
- 新起一个有序列表：复制文档里已有的一条列表项来改，再右键选“重新开始于 1”，样子和原有的列表一致；也可以选中正文点“编号”。
- 紧跟在标题下面的那一段正文，不要直接点“编号”按钮：Word 会把它接进标题的编号、变成标题（标题带自动编号的 Word 文档都是这样）。从按钮旁的下拉里选一种编号格式就不会。取消编号之后，给这一段再套一次“正文”样式，首行缩进才回来。
- 新插的图片，给它所在的段落套“图片”样式；自己用“交叉引用”加的来源引用，套“来源引用”样式；粘贴来的表格，给单元格套“表格文字”样式。
- WPS 里新插的表格不会自动是三线表；文档在 WPS 里保存过之后，回到 Word 里新插的表格也一样。复制文档里已有的一张表来改最省事。
- 左右并排的两栏是一张没有框线的表格：在栏里直接输入，回车就是这一栏的下一行；要填写的表格在最后一格按 Tab 会多出一行。
- 目录里的页码打开后要更新一次才对：Word 打开时问是否更新域，选“是”；WPS 里在目录上右键选“更新域”（或全选按 F9）。没更新之前 WPS 里目录页码都显示 1。
- 只有一页的文档不显示页码；写到第二页，页码会自己出现。
- 这份文档的正文在页面上下居中：写到第二页以后每一页都居中，最后一页内容少时会偏下；要改回从顶端排，在“页面设置”的“版式”里把“垂直对齐方式”改成“顶端对齐”。
- 在 Word 或 WPS 里改过的内容不会回到源文件；以后需要重新生成时，请把改过的文件一起发来。

## What you can express

Rules and edge cases for every row are in [the Markdown contract](references/docx-markdown-contract.md); complete inputs are in [Examples](references/examples.md). `docx-kit templates` and `docx-kit components` list what the installed binary supports.

| Need | Write |
| --- | --- |
| Font | Nothing for 楷体 (`executive-cn-docx`). Set `template` to `executive-cn-song-docx` for 宋体 body with 黑体 headings, or to `executive-cn-official-docx` for the 公文模板: 仿宋, headings numbered 一、（一）1.（1）, always a plain document unless you write `report`. Change it only when the user asks for that look. Fonts are not embedded; add `--embed-fonts` to `build` only when recipients lack them |
| Stated format | Only what the user names: `body_font: 仿宋_GB2312`, `body_size: 三号` (or `16pt`), `body_line_spacing: 28pt` (fixed; `at-least 28pt`; `1.5x`); the same keys for `title`, `heading1`–`heading3` (`heading4` on the 公文模板) and `<role>_latin_font`. Sizes and fonts follow the body into tables, captions, lists and unstated headings; line spacing does not reach headings, so a spacing for the whole text is stated for `body` and each heading level used. Nothing stated is changed or shrunk for you. 公文-style values (仿宋 body, 小标宋 title) ask for the 公文模板. Write the full installed font name (`方正小标宋简体`) and say so; a font this machine lacks gives `font_not_found`: ask the user to install it or accept another, never substitute |
| Larger type | `text_scale: large`: all type at 4/3 (a 16 pt body) for an oath or a speech, when the user wants it bigger without naming sizes; the document runs longer. If that is clearly too small for the purpose, propose a stated size |
| Page margins | Only when named, with the unit: `margin_top: 3.7cm`, `margin_bottom: 35mm`, `margin_left`, `margin_right`; edges not named keep the template's. Every page follows, and so does everything drawn to the text width. A margin that cannot be built fails with the smallest value that works: tell the user, do not choose another |
| Page position | `page_position: center` for a text that should stand alone in the middle of one page — an oath, an invitation, a certificate (with `text_scale: large` when it should also be bigger). Every body page is centred, a short last page after an automatic page break too, so use it only when the text fits on one page; the empty paragraph after a final table counts as content, so such a page sits slightly high. Cover and contents pages do not move; header, footer and page number do not change. There is no other position (a third down, half a page). LibreOffice previews show the page from the top |
| Parts | `cover`, `toc`, `chapter_header`, `list_of_figures`, `list_of_tables`: `true` / `false`. `page_numbers: always / none / auto`. `heading_numbering: auto / none`. Each overrides the mode's default: `cover: false` gives a report that starts with its title and contents. The page number sits centred in the footer; its position and form cannot be chosen in this version |
| Headings | `#` `##` `###` (`####` only on the 公文模板), no skipped level. Report: no numbers in the text. Plain document: kept as written (`# 第一条 服务内容`) |
| Alignment | Ordinary paragraphs are indented two characters on the first line. `::: 顶格` for a salutation or label lines (`甲方：…`, `时间：…`), `::: 靠右` for a sign-off, `::: 居中` for a line under the title (author, date). Never position text with spaces or empty paragraphs |
| Room for a stamp or signature | `::: 留白 三行` (or `一行`, `两行`; three lines, about 2.3 cm, is the most and the usual answer — a seal is stamped over the sign-off) alone on the line before the paragraph that should stand lower, above the container line for a `::: 靠右` sign-off. Never blank lines. Word drops the space before a body paragraph that lands first on a page: when the height must hold, use a `::: 并排` pane or a table with `spacing=roomy` / `extra` |
| Side by side | `::: 并排 widths=1,1`, the left paragraphs, a line `---COLUMN---`, the right paragraphs, `:::` — two parties' signature columns, or a job line with its dates in a `::: 靠右` right pane (`widths=2,1`). Panes hold ordinary paragraphs only (`::: 靠右` / `::: 居中` / `::: 留白` work inside). A block of up to 10 lines stays on one page; a longer one breaks where the page ends |
| Numbered lists | Plain document: six forms are native lists that keep the numbers written — `1. ` `（1）` `1、` `一、` `(1)` `（一）`. Other forms (`a.`, `A.`, `①`, an indented sub-item) stay as text with an `info` check; for two levels make the upper one headings. Report and 公文模板: only `1. ` is a list and the template numbers it; `list_numbering: author` switches them to as-written |
| Other blocks | `- 条目`; `> 引文`; `> [!note] 标题` callouts (not on the 公文模板); fenced code; `---PAGE---` page break; `**粗体**`; fill-in blanks and places to sign are underscores, `日期：____年____月____日` (three or more are literal) |
| Tables and figures | Pipe tables. A caption is optional (without one the table has no number and cannot be cited); write it on the line above: `表：标题`, or `表[landscape]：标题` for a wide table on a landscape page. `图：标题` on the line above `![说明](图片.png)`; a missing image file fails the build — never draw or invent one: leave the figure out, tell the user, and put a placeholder line in its place only if the user agrees. `--settle-figures` (a large gap before a tall figure) is opt-in; read the contract first |
| Table looks | A plain pipe table is the three-line table. For another look wrap ONE table, its caption line inside, in `::: 表格 appearance=grid header=false spacing=roomy widths=1,2,1,2` … `:::`. `appearance`: `grid`, `borderless` (e.g. A–D options in columns), `three-line`; `header=false` when the first row is data too (a form); `spacing=roomy` for one handwritten line per cell, `extra` for several (one spacing per table); `alignments=left,center,right`; `layout=landscape`. Columns are equal unless `widths=` gives a column of long English identifiers or URLs more weight; rows are of equal length; text is never shrunk |
| References and sources | The number the reader will see: `见表 2.1` in a report with numbered chapters, `见表 1` in a plain document or on the 公文模板; introduce a table or figure before it appears; a wrong number fails the build and the error lists the valid ones. `[1]` in the text and a final `# 资料来源` with `1. …` entries; never invent a source |
| Equations | A fenced `math` block; `\( … \)` inline; refer to them as `式 1` / `式 2.1` |
| Punctuation | Default `normalize` turns ASCII punctuation in Chinese text into full-width and drops the space after it (`A. 甲` becomes `A。甲`); numbers such as `9:30`, `480,000`, `12%` and the spaces in `2026 年 10 月` are left alone. `punctuation_mode: preserve` keeps every character: use it for option letters, codes, mixed-language lines and every transcription. A paragraph with a bare URL or a very long Latin string may break inside words and is set flush left instead of justified, so the string cannot run off the line |

Warning-level checks name something a reader would notice — an exhibit mentioned only after it appears, an unpaired `**`, a table too wide for the page; the full list with levels and actions is under "Content Checks" and "When a Build or Check Fails" in the contract. `redline` refuses two drafts that differ in stated format, margins, page position, a table's look, a side-by-side block or a spacing level: build those versions separately.

**Transcribing an existing document** (or wording the user says must not change). Keep its wording, numbers, masks and order; nothing in this skill is permission to rewrite it. Add `punctuation_mode: preserve`. On the 公文模板 also add `heading_numbering: none` and `list_numbering: author`. Write a literal asterisk as `\*` (`Z\*\*\*\*\*99`) and a pipe inside a table cell as `\|`. Never add, move or delete original text to clear a check: `info` needs nothing, and for the warning `caption_before_reference` keep the original order and tell the user it follows the original. After building, compare the result with the original — title, order, clause numbers, every table cell, masked characters — and tell the user what you compared; the tool cannot know whether the transcription is right.

## What this version cannot do

Say so to the user, naming what is missing, instead of improvising with spaces, empty paragraphs, layout tables or another tool — and never drop or flatten the requirement silently. Do not promise a date.

- **Merged cells, slanted headers, a height for one row.** A form row that should span the full width keeps all its cells (`| 参训理由 |  |  |  |`); tell the user they are not merged and can be merged in Word or WPS (select them, 合并单元格). Do not split the form into a second table to imitate a merge.
- **More than two panes side by side, text flowing from one column into the next, and anything but paragraphs in a pane** (no list, table or figure).
- **Other spacing**: an amount in millimetres, more than three lines, space at the end of the file. **Keeping two blocks on one page** beyond the 10-line rule.
- **Decoration and special looks**: rules between résumé sections, a sealing line, a page border; a clause lead-in (`第一条`) in a style of its own — write `**第一条**` if bold is wanted. Bold, spacing or a size for one paragraph, paper other than A4, gutters and mirrored margins cannot be stated.

## Notes that must not be lost

- **PDF through Word automation.** Call `Repaginate()` on the opened document before exporting. Exporting in the same instant as opening can print list numbers that restart on page 2.
- **LibreOffice** (preview, PDF, page images) recalculates Word's caption, reference and page-number fields wrongly. First run `npx --no-install docx-kit render-copy <file.docx> --out <dir>` and render the copy; deliver the original.
- **A lone `# 资料来源`.** A text whose only heading is a first-line `# 资料来源` is a plain document titled 资料来源. Write `document_mode: report` if it is a list of sources.
