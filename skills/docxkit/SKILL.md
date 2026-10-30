---
name: docxkit
description: Use when prepared report content, uploaded user materials, Markdown, or report.json should be delivered as a polished editable Word .docx through the local docx-kit CLI — a report with a cover and contents, or a plain document such as a notice, letter, certificate, contract, minutes, résumé, form or oath, newly written or transcribed, in the template's look or in a format the user states. Use at the final export step after content is available, when a task naturally needs a formal Chinese Word deliverable, or when the user explicitly asks to use DocxKit. This skill formats and exports content; it does not gather sources or verify a transcription against its original by itself.
---

# DocxKit

Use this skill when the next deliverable is a polished, editable Word document: a report, or a plain document such as a notice, a letter, a contract or a 公文. The user may have uploaded materials for the agent to organize, the current task may naturally end in a report or a formal document, or the user may explicitly ask to use DocxKit.

This skill drives the local CLI after the agent has prepared content, sources, Markdown or `report.json`. It does not replace the agent's normal research or source-reading work.

DocxKit turns Markdown (or `report.json`) into a Word `.docx` the user can keep writing in Word or WPS: real styles, native numbering, updatable references. You write the content as ordinary Markdown and run one command. Do not produce the Word file any other way (python, OpenXML, a template of your own), and never patch the generated `.docx`: change the source and rebuild.

## Requirements

This skill matches `@dztabel/docxkit >= 0.2.0`; what decides is what the binary reports. At session start (once, before the first build), refresh the CLI and the installed skill copies. Every step is fail-soft: if offline or a step errors, keep going with the local versions — never block the build on updating.

```bash
npm install @dztabel/docxkit@latest   # session-start upgrade; on failure keep the local install
npx --no-install docx-kit --version
npx --no-install docx-kit sync-skill  # mirrors the packaged skill into ~/.claude/skills and ~/.agents/skills
```

`sync-skill` refreshes the machine-installed skill copies from the npm package (only into skills roots that already exist); an updated skill takes effect in the next session — do not re-read it mid-session. Skip the command silently if the local CLI predates it. Do not run `npm install` again mid-session: the CLI version must stay the same across a build and redline loop. If `docx-kit` is not found, run `npm install @dztabel/docxkit`, then use `npx --no-install docx-kit …`.

`docx-kit templates` says what the installed binary can do. It prints `by_structure` when it has plain documents, `:::` containers and lists as written, and names under `format.features` the stated-format features it has — all of them are `text_scale`, `role_font`, `role_latin_font`, `role_size`, `role_line_spacing`, `page_margins`, `table_appearance`, `table_without_header`, `table_spacing`, `table_merges`, `table_row_height`, `paragraph_spacing`, `parallel`, `page_position`. An older binary prints `:::` lines as text, makes a short text a report with a cover and rejects those keys: if something you need is missing, tell the user rather than building something else.

## First decision: does the user want a report?

| The user wants | Write |
| --- | --- |
| A report — most documents with chapters, where a cover and a contents page make sense | `document_mode: report` |
| A document that certainly needs no cover or contents (notice, letter, certificate, contract, minutes, résumé, oath, form) and has no chapter headings | no `document_mode`; usually no metadata at all |
| The same, but with chapter headings (`#`) | `document_mode: document`, and the title as `title:` |

If `document_mode` is not written, the content decides: any chapter heading makes it a report, none makes it a plain document. A first-line `# 标题` is the title, not a chapter (unless the metadata already has `title:`). A numbered line with its own content under it (paragraphs, a list, a table) is a heading — `# 二、议定事项`; a numbered line that is complete in itself is a list item. `effective_document` in the build receipt says what was built — read it every time. A plain document has no cover, contents or header, keeps the heading and list numbers you wrote, and shows page numbers only once it has a second page (on the 公文模板 the template numbers headings and lists, and the page number always shows).

The 公文模板 (`executive-cn-official-docx`) builds a plain document whatever the content: notices, plans, implementation schemes and ordinary official documents start with their title and have no cover or contents. Write `document_mode: report` there only when the user explicitly asks for a cover or contents, or the deliverable is genuinely a long report that needs them. In any report, switch on the lists of figures and tables (`list_of_figures: true`, `list_of_tables: true`) only for figure- or table-heavy reports.

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

It gets a cover, a contents page, automatic chapter numbers (so write headings without numbers) and captions numbered by chapter. The cover shows `title` and, when you give them, `subtitle`, `client`, `date` and `confidentiality`. `numbering_rule: native-v1` declares that numbered references follow the current numbering; put it in every new source that refers to tables, figures or equations by number.

## Principles

- Keep the editable source as Markdown (`./output_docx/content.md`) or `report.json`. The CLI writes one user-facing Word file plus diagnostics (`build-result.json`, `report.json`) into the same `--out` directory: one folder per document, by default `./output_docx`; use a versioned sibling such as `./output_docx_v2` when the old build must be kept.
- Always pass `--filename <descriptive-name.docx>` on `build`: a concise name derived from the document's title, with no directory part. The returned `docx_path` is the only Word deliverable: never copy or rename it, and never hand over a second `.docx` from the same build.
- Templates. The default `executive-cn-docx` sets body and headings in 楷体. `executive-cn-song-docx` is 宋体 body with 黑体 headings. `executive-cn-official-docx` is the 公文模板, only for a 公文-style request: 二号 方正小标宋简体 title centred, 楷体_GB2312 subtitle without a prefix, 仿宋_GB2312 三号 body on a fixed 30 pt line, headings 一、（一）1.（1） in 黑体, bold 楷体_GB2312, bold 仿宋_GB2312 and 仿宋_GB2312, 小四 tables with a bold header, sources like the body, small print and footnotes 四号, definition and checklist tables 小四, page numbers as GB/T 9704 `— 1 —` in 四号宋体 centred 7 mm below the text area, no header, no callouts. Change the template only when the user asks for that look.
- Keep the default font behaviour (no embedding): the template fonts are written with alternative names, so Word shows a close system font where one is missing (on the 公文模板: 仿宋, 楷体 and 宋体 on Windows) and the file stays small and fully editable. Add `--embed-fonts` only when recipients may lack the Chinese fonts (for example readers abroad on non-Chinese systems).
- Never hand-edit the generated `.docx` or write OpenXML; every change goes through the Markdown or `report.json` source and a rebuild.
- `--settle-figures` is opt-in: add it to `build` only when the user asks to reduce the blank space a tall figure leaves at the bottom of the previous page, or you can see that problem in the delivered file. Read the contract's "Tall figures and blank page bottoms" section first.

## Writing the input

`references/docx-markdown-contract.md` is the single authoritative writing contract — read it before writing. `references/examples.md` has complete inputs to imitate: a full report, plain documents, a 公文, a transcription, a form, a certificate. When unsure which component fits, run `docx-kit components` for the machine-readable component contract (purpose, when to use and avoid it, fields, visual behaviour).

The highest-frequency rules:

1. **Headings.** In a report the template numbers the headings: write `# 研究背景`, never `# 一、背景`, and give long chapters real `##` subsections. In a plain document on 楷体 or 宋体, headings that carry written numbers are kept exactly as written (`# 第一条 服务内容`); unnumbered ones get the template's numbers (1, 1.1) when they span two levels or number four or more, otherwise none — write `heading_numbering: none` to keep a long one unnumbered. The 公文模板 numbers them 一、（一）1.（1） unless `heading_numbering: none`. Use `#` to `###` without skipping a level; `####` only on the 公文模板.
2. **Captions.** In a report every table gets `表：标题` on the line before it (`表[landscape]：标题` for a wide table that must stay whole on a landscape page) and every image gets `图：标题`; a table without one is a warning there, and so is an image with neither caption nor alt text. In a plain document a caption is optional: without one a table has no number and cannot be cited. Table font size is automatic — never try to control it.
3. **References by number, never by position.** Introduce each table or figure in the prose before it appears, by the number the reader will see — `见表 2.1` / `如图 2.1` in a report with numbered chapters, `见表 1` in a plain document or on the 公文模板; these become clickable, updatable references. Never point by position ("上图", "下图", "如下表所示"): it reads wrong as soon as the exhibit lands on another page. A wrong number fails the build and the error lists the valid ones; in a long document write the skeleton first, build once, then fill in the references.
4. **Sources.** Cite as `[1]` right after the claim it supports and list the sources in a final `# 资料来源` chapter as `1. [名称](url)，出处，日期。` items. Never invent a source, and never paste a naked URL into prose or a table.
5. **Equations.** A fenced `math` block (LaTeX, numbered automatically, cited as `式 2.1` or `式 1`); inline math as `\( … \)` inside the text.
6. **Prose first.** Conclusions and explanations are paragraphs; lists support them. The 公文模板 forbids callouts; with the other templates use callouts (`> [!note] 标题`, `> [!risk] 标题`) sparingly. Avoid `---PAGE---` unless the user asks for a page break, and never fabricate glossary or checklist blocks in Markdown.
7. **Nothing positioned by hand.** Never place text with spaces, tabs or empty paragraphs: use the alignment containers, `::: 留白` and `::: 并排` below.

## What you can express

Rules and edge cases for every row are in the contract; complete inputs are in [Examples](references/examples.md). `docx-kit templates` and `docx-kit components` list what the installed binary supports.

| Need | Write |
| --- | --- |
| Font | Nothing for 楷体; `template: executive-cn-song-docx` for 宋体 with 黑体 headings; `template: executive-cn-official-docx` for the 公文模板 (see Principles). Change it only when the user asks for that look |
| Stated format | Only what the user names: `body_font: 仿宋_GB2312`, `body_size: 三号` (or `16pt`), `body_line_spacing: 28pt` (fixed; `at-least 28pt`; `1.5x`); the same keys for `title`, `heading1`–`heading3` (`heading4` on the 公文模板) and `<role>_latin_font`. Sizes follow the body into tables, captions, lists and the headings you do not state; a body font reaches only the roles the template sets in the body's font (the 黑体 headings of 宋体 and the 公文模板, and the 公文模板's 小标宋 title and 楷体_GB2312 level-2 headings, keep theirs). Line spacing does not reach headings, so a spacing for the whole text is stated for `body` and each heading level used; under a fixed spacing a paragraph with an inline formula taller than the line gets "at least" that value so WPS does not cut the formula off (the warning names it — tell the user). Nothing stated is changed or shrunk for you. 公文-style values (仿宋 body, 小标宋 title) ask for the 公文模板. Write the full installed font name (`方正小标宋简体`) and say so; a font this machine lacks gives `font_not_found`: ask the user to install it or accept another, never substitute |
| Larger type | `text_scale: large`: all text at 4/3 (a 16 pt body; header and page number keep their size) for an oath or a speech, when the user wants it bigger without naming sizes; the document runs longer. If that is clearly too small for the purpose, propose a stated size |
| Page margins | Only when named, with the unit: `margin_top: 3.7cm`, `margin_bottom: 35mm`, `margin_left`, `margin_right`; edges not named keep the template's. Every page follows, and so does everything drawn to the text width. A margin that cannot be built fails with the smallest value that works: tell the user, do not choose another |
| Page position | `page_position: center` for a text that should stand alone in the middle of one page — an oath, an invitation, a certificate (with `text_scale: large` when it should also be bigger). Every body page is centred, a short last page after an automatic page break too, so use it only when the text fits on one page; the empty paragraph after a final table counts as content, so such a page sits slightly high. Cover and contents pages do not move; header, footer and page number do not change. There is no other position (a third down, half a page). LibreOffice previews show the page from the top |
| Parts | `cover`, `toc`, `chapter_header`, `list_of_figures`, `list_of_tables`: `true` / `false`. `page_numbers: always / none / auto`. `heading_numbering: auto / none`. Each overrides the mode's default: `cover: false` gives a report that starts with its title and contents. The page number sits centred in the footer, and on the 公文模板 follows GB/T 9704 (`— 1 —`; odd pages right and even pages left without a cover or contents, centred with one); its position and form cannot be chosen in this version |
| Alignment | Ordinary paragraphs are indented two characters on the first line. `::: 顶格` for a salutation or label lines (`甲方：…`, `时间：…`), `::: 靠右` for a sign-off, `::: 居中` for a line under the title (author, date) |
| Room for a stamp or signature | `::: 留白 三行` (or `一行`, `两行`; three lines — about 2.3 cm, 3.1 cm on the 公文模板 — is the most and the usual answer: a seal is stamped over the sign-off) alone on the line before the paragraph that should stand lower, above the container line for a `::: 靠右` sign-off. Never blank lines. Word drops the space before a body paragraph that lands first on a page: when the height must hold, use a `::: 并排` pane or a table with `spacing=roomy` / `extra` |
| Side by side | `::: 并排 widths=1,1`, the left paragraphs, a line `---COLUMN---`, the right paragraphs, `:::` — two parties' signature columns, or a job line with its dates in a `::: 靠右` right pane (`widths=2,1`). Panes hold ordinary paragraphs only (`::: 靠右` / `::: 居中` / `::: 留白` work inside). A block of up to 10 lines stays on one page; a longer one breaks where the page ends unless a `---PAGE---` stands before it |
| Numbered lists | Plain document: six forms are native lists that keep the numbers written — `1. ` `（1）` `1、` `一、` `(1)` `（一）`. Other forms (`a.`, `A.`, an indented sub-item) stay as text with an `info` check. Circled numbers (`①②③`) are always typed text: each line that starts with one is its own paragraph, on every template, and Enter does not continue them. For two levels, write the lower level flush left in another form (`一、` items followed by `（一）` lines: each form is a list of its own, not a nested list), or make the upper level headings when each item has content under it. Report and 公文模板: only `1. ` is a list and the template numbers it `（1）`, or `1）` under a numbered level-4 heading of the 公文模板; `list_numbering: author` switches them to as-written |
| Other blocks | `- 条目`; `> 引文`; `> [!note] 标题` callouts (not on the 公文模板); fenced code; `---PAGE---` page break (only on request); `**粗体**`; fill-in blanks and places to sign are underscores, `日期：____年____月____日` (three or more are literal) |
| Tables and figures | Pipe tables, with captions as in rule 2. `图：标题` on the line above `![说明](图片.png)`; a missing image file fails the build — never draw or invent one: leave the figure out, tell the user, and put a placeholder line in its place only if the user agrees. A ChartKit image with its `-manifest.json` beside it is sized from the manifest. `--settle-figures` (a large gap before a tall figure) is opt-in; read the contract first |
| Table looks | Without `appearance` a table's look follows its structure on every template: a header row gives a three-line table, `header=false` a grid; a written `appearance` wins. Write `grid` for a form to be filled in, `borderless` for aligned blocks and signature areas. For another look wrap ONE table, its caption line inside, in `::: 表格 appearance=grid header=false spacing=roomy widths=1,2,1,2` … `:::`. `appearance`: `grid`, `borderless` (e.g. A–D options in columns), `three-line`, drawn as written on every template; `header=false` when the first row is data too (a form); `spacing=roomy` for one handwritten line per cell, `extra` for several (one spacing per table); `row_height=9mm` makes every body row at least that tall, room included (one value per table); `alignments=left,center,right`; `layout=landscape`. A cell that is exactly `<` joins the cell on its left, `^` the cell above; the top-left cell of the rectangle holds the text, and the header row never merges. Columns are equal unless `widths=` gives a column of long English identifiers or URLs more weight; millimetres adding up to the text width (160 mm, 公文模板 159.2 mm) are exact widths; rows are of equal length; text is never shrunk |
| Form printed and filled in by hand | `template: executive-cn-song-docx`; each part a `::: 表格 appearance=grid header=false row_height=9mm` table (8–10 mm), labels in `**粗体**`, the part title as its first row merged across (`**一、基本信息**` in the first cell, `<` in every other); a photo box is a column of `^` with its width in millimetres; the declaration, then the signature table with a taller `row_height`, last. A row with other columns (an 18-box ID number) is a table of its own. For one page of A4, check the page count with `docx-kit pdf` before delivery. Full example in `references/examples.md` |
| Punctuation | Default `normalize` turns ASCII punctuation in Chinese text into full-width and drops the space after it (`甲, 乙: 丙.` becomes `甲，乙：丙。`); a single letter and a period that start a paragraph or list item (`A. 甲`) keep the period, but `A. … B. …` later in the line do not; numbers such as `9:30`, `480,000`, `12%` and the spaces in `2026 年 10 月` are left alone. `punctuation_mode: preserve` keeps every character: use it for option letters, codes, mixed-language lines and every transcription. A paragraph with a bare URL or a very long Latin string may break inside words and is set flush left instead of justified, so the string cannot run off the line. Lines of one paragraph are joined without a space where both sides are Chinese |

Warning-level checks name something a reader would notice — an exhibit mentioned only after it appears, an unpaired `**`, a table too wide for the page; the full list with levels and actions is under "Content Checks" and "When a Build or Check Fails" in the contract. `redline` refuses two drafts that differ in stated format, margins, page position, a table's look, a side-by-side block or a spacing level: build those versions separately.

**Transcribe only when the user says the wording must not change** (照录、原文不能改、一字不改). "排成 Word", "做成 Word" or "整理成文档" alone is not a transcription: keep the content and the facts, fix obvious errors (a typo, a figure or an example that contradicts the rest of the material) and turn spoken or note-like wording into written prose, then tell the user in the delivery message what you changed. When it is a transcription, keep its wording, numbers, masks and order; nothing in this skill is permission to rewrite it. Add `punctuation_mode: preserve` and `heading_numbering: none`. On the 公文模板 also add `list_numbering: author`. Write a literal asterisk as `\*` (`Z\*\*\*\*\*99`) and a pipe inside a table cell as `\|`. Never add, move or delete original text to clear a check: `info` needs nothing, and for the warning `caption_before_reference` keep the original order and tell the user it follows the original. After building, compare the result with the original — title, order, clause numbers, every table cell, masked characters — and tell the user what you compared; the tool cannot know whether the transcription is right.

## What this version cannot do

Say so to the user, naming what is missing, instead of improvising with spaces, empty paragraphs, hand-made tables that imitate the missing feature, or another tool — and never drop or flatten the requirement silently. (The table looks, `::: 留白` and `::: 并排` above are the supported way, not improvising.) Do not promise a date.

- **Merged header cells, slanted headers, a height for one row, two column structures in one table.** Body cells merge with `<` and `^` and a table has one `row_height` for all its body rows; a taller signature row, or an 18-box ID number under a six-column form, is a table of its own directly after (an empty line separates the two tables). A slanted header is not drawn: tell the user it can be added in Word or WPS.
- **More than two panes side by side, text flowing from one column into the next, and anything but paragraphs in a pane** (no list, table or figure).
- **Other spacing**: an amount in millimetres, more than three lines, space at the end of the file. **Keeping two blocks on one page**: only a side-by-side block of up to 10 lines stays whole by itself; anything else only with a `---PAGE---` before it.
- **Decoration and special looks**: rules between résumé sections, a sealing line, a page border; a clause lead-in (`第一条`) in a style of its own — write `**第一条**` if bold is wanted. A paragraph style of its own, a size or line spacing for one paragraph, character spacing, paper other than A4, gutters and mirrored margins cannot be stated.

## The working loop

1. Prepare the content per the contract and save it as `./output_docx/content.md` (or edit the existing `report.json`), one output folder per document. This source is what any later rebuild uses; keep it.
2. Make sure the CLI is current — once, at session start (see Requirements).
3. Build, always with `--filename`:

   ```bash
   npx --no-install docx-kit build ./output_docx/content.md --out ./output_docx --filename 经营分析会通知.docx
   ```

   The result is also written to `./output_docx/build-result.json`, with `report.json` beside it — read that file; no `tee` needed. The other options are `--embed-fonts`, `--settle-figures` and `--strict`; `--strict` turns warnings into failures for CI and batch pipelines, while the default for a delivery is to iterate until clean.
4. **Gate loop** — `ok: true` is not enough; read the whole `build-result.json`:
   - `errors`: fix the named field, line or missing file in the source and rebuild.
   - `checks` with `severity: error` (a dangling `表/图/式 x.x` reference, `[n]` beyond the source list, a table row wider than its header) fail the build. Fix the content at the reported `path` and rebuild — never work around the gate. A `dangling_caption_reference` message lists the numbers that exist; use those instead of guessing (an opening 执行摘要 or 导论 counts as chapter 1).
   - `checks` with `severity: warning`, and top-level `warnings` (a formula rendered as plain text, a requested figure list with nothing to list): fix them too, and iterate until `checks` and `warnings` are clean. Leave a warning only when the user explicitly wants that shape — a transcription that keeps the original order under `caption_before_reference` is one — and say so when delivering. `--strict` fails on all of these except the notes of `--settle-figures`.
   - `info` needs no action, unless it names something you meant otherwise: `unsupported_list_numbering` on a line you meant as a list means rewriting it in one of the six forms.
   - `effective_document`: is it the kind of document you meant — mode, cover, contents, heading and list numbering, and under `format` the fonts, sizes, line spacing, margins and page position in effect? `automatic_structure` lists what was decided for you.
   - `text_normalization`: `applied: true` means punctuation or spaces were changed — if the text must stay as written, or you cannot tell what changed, add `punctuation_mode: preserve`.
5. Run structural QA (package structure, Word fields, internal link anchors, style names, font declarations). It inspects the package, not the content: `check_scope: structure_only` and `not_checked` mean exactly that, and a pass is not delivery approval.

   ```bash
   npx --no-install docx-kit qa ./output_docx/经营分析会通知.docx --report-json ./output_docx/report.json --out ./output_docx/qa
   ```

6. Verify that the single `.docx` at `docx_path`, `report.json` and `build-result.json` exist. The receipt has no page count: when the user set one or the look matters, render the copy (Notes) and look; if you cannot, say the page count is unconfirmed.
7. Deliver only `docx_path` as the Word file, without copying or renaming it. Give the editable source path, what you checked (at least the receipt, and `report.json` against what you wrote), any warning left on purpose and why, anything the user asked for that could not be done, every fact you left blank or made up, and the instructions below.

**When the user wants changes to a document already generated** — rewording, a new section, another template, or a Word file with tracked-changes markup of what changed — read `references/revising-documents.md`. The short version: edit the same editable source (`content.md` or the always-written `report.json`), never the `.docx`, then rebuild and rerun the gate loop. Edits made in Word never flow back into the source: before rebuilding a file the user has edited, reconcile it with the source.

### Tell the user

In the user's language, say what they can do with the file; for Chinese deliveries use these lines — the first and the last always (drop from the first what the document does not have), the others only when the document has what they mention; they may be shortened:

- 这份 Word 可以直接接着写：标题后回车就是正文，表格、代码块后面可以直接输入；改“正文”“标题 1”“题注”“三线表”这些样式，全篇跟着变。
- 增删表、图、公式或资料来源后，全选按 F9（Mac 上是 fn+F9），编号和正文里的引用会一起更新，Word 和 WPS 都是这样。只想更新某一处，在它上面点右键选“更新域”。
- 用“插入题注”之前，先在题注对话框里建好“表”“图”标签并设好编号：按章编号的文档勾选“包含章节号”（章节起始样式“标题 1”、分隔符“句点”），全文连续编号的文档不勾。先设置再插入——Word 会按当前设置改写文档里已有的同类题注。WPS 自带这两个标签，在“编号”里勾选“题注关联章节编号”，分隔符改成句点。
- 新起一个有序列表：复制文档里已有的一条列表项来改，再右键选“重新开始于 1”，样子和原有的列表一致；也可以选中正文点“编号”。
- 紧跟在标题下面的那一段正文，不要直接点“编号”按钮：Word 会把它接进标题的编号、变成标题（标题带自动编号的 Word 文档都是这样）。从按钮旁的下拉里选一种编号格式就不会。取消编号之后，给这一段再套一次“正文”样式，首行缩进才回来。
- 在列表最后一条后面连按两次回车结束列表，新的一行若没有首行空两格，就给它套一次“正文”样式。（WPS 里各种模板都会这样；Word 里楷体、宋体会这样，公文的列表本来就排得像正文。）
- 新插的图片，给它所在的段落套“图片”样式；自己用“交叉引用”加的来源引用，套“来源引用”样式；粘贴来的表格，给单元格套“表格文字”样式。
- WPS 里新插的表格不会自动是三线表；文档在 WPS 里保存过之后，回到 Word 里新插的表格也一样。复制文档里已有的一张表来改最省事。
- 左右并排的两栏是一张没有框线的表格：在栏里直接输入，回车就是这一栏的下一行；要填写的表格在最后一格按 Tab 会多出一行。
- 目录里的页码打开后要更新一次才对：Word 打开时问是否更新域，选“是”；WPS 里在目录上右键选“更新域”（或全选按 F9）。没更新之前 WPS 里目录页码都显示 1。
- 只有一页的文档不显示页码；写到第二页，页码会自己出现。
- 这份文档的正文在页面上下居中：写到第二页以后每一页都居中，最后一页内容少时会偏下；要改回从顶端排，在“页面设置”的“版式”里把“垂直对齐方式”改成“顶端对齐”。
- 在 Word 或 WPS 里改过的内容不会回到源文件；以后需要重新生成时，请把改过的文件一起发来。

## Failure playbook

The contract's "When a Build or Check Fails" has a row for every message; the common ones:

| Situation | Action |
| --- | --- |
| `errors` from build or validate (a missing field, an unknown template or key, a missing image, a `:::` line in the wrong place) | Fix the source at the reported field or line; each message names it. |
| `checks` with `severity: error` | Fix the content at `path`; the contract's code table explains every code. `dangling_caption_reference` lists the document's actual numbers — use those instead of guessing. |
| `warnings` like `formula rendered as plain text` | Repair the LaTeX (the subset is in the contract) or switch that formula to an ```` ```omml ```` fence. |
| `warnings` starting with `图位置整理未执行` / `图位置整理中止` (only with `--settle-figures`) | Not a content problem, and the document was still delivered — either the normal one or an arrangement measured before the pass stopped. Do not try to "fix" the content. Whether paragraphs were moved is told by `figure_settling.moved_paragraphs`, not by the warning: if it is above 0, check the moved paragraphs as usual. Tell the user; measuring needs Microsoft Word on Windows, or LibreOffice plus poppler elsewhere. |
| A key, container or command is refused as unknown or "not available yet" | The installed binary is older than this skill. Tell the user what cannot be done with this installation; do not imitate it, and do not produce the Word file another way. Updating happens at session start, not mid-loop. |
| `qa` fails | Do not hand-edit the docx; rebuild, and if QA still fails report the QA JSON to the user as a tool issue. |
| `docx-kit` not found | `npm install @dztabel/docxkit`, then use `npx --no-install docx-kit …`. |

## Notes that must not be lost

- **PDF and previews.** When the user wants a PDF, run `npx --no-install docx-kit pdf <file.docx> --out <dir>` (Word on Windows, LibreOffice elsewhere) and deliver the PDF beside the Word file. Read its `errors` and `notes`: on `no_pdf_engine`, or when a note says the page centring was lost, tell the user to export that file from Word or WPS. Never run LibreOffice on the delivered file directly: it recalculates Word's caption and reference fields wrongly, prints every page number of the contents as 1, shows no page number in a `page_numbers: auto` footer and does not centre a page. For a LibreOffice preview or page images run `npx --no-install docx-kit render-copy <file.docx> --out <dir>` first and render the copy; deliver the original. A binary that refuses `pdf` as unknown predates it.
- **A lone `# 资料来源`.** A sources heading is never a chapter and never the title: body text followed only by `# 资料来源`, or a text whose only heading is a first-line `# 资料来源`, is a plain document with its sources section (without a title unless you write `title`). Write `document_mode: report` if it should still be a report.
