---
name: docxkit
description: Use when prepared content, uploaded materials, Markdown, or report.json should become an editable Word document through the local docx-kit CLI. Supports reports and transcription of contracts, notices, and letters. This skill formats and exports content; it does not gather sources or verify a transcription against its original by itself.
---

# DocxKit

Use this skill to export prepared content as a Word document the user can continue writing in Word or WPS. First distinguish **writing a report** from **transcribing an existing document**. A transcription must preserve the original wording, clause numbers and masks; report-writing advice is not permission to rewrite it.

## Requirements

This skill matches `@dztabel/docxkit >= 0.1.63`. At session start (once, before the first build), refresh the CLI and the installed skill copies. Every step is fail-soft: if offline or a step errors, keep going with the local versions — never block the build on updating. If the local CLI lacks a command or option used below, tell the user instead of building something else.

```bash
npm install @dztabel/docxkit@latest
npx --no-install docx-kit --version
npx --no-install docx-kit sync-skill
npx --no-install docx-kit templates
npx --no-install docx-kit components
```

`sync-skill` copies the packaged skill into existing `~/.claude/skills` and `~/.agents/skills` roots. Its changes take effect next session; do not re-read the skill or upgrade the CLI during a build/revision loop. Skip `sync-skill` if the local wrapper does not support it.

## Principles

- Keep Markdown or `report.json` as the source for agent rebuilds. Always pass `--filename <descriptive-name.docx>` to `build`; use only a filename, without directories. Deliver the returned `docx_path`, without copying or renaming it.
- Users can edit the delivered Word file directly. A later rebuild uses the saved source and does **not** import those Word edits. Before rebuilding a user-edited file, reconcile its content with the source; see [Revising documents](references/revising-documents.md).
- Choose typography independently of document mode: `executive-cn-docx` uses 楷体, `executive-cn-song-docx` uses 宋体 body and 黑体 headings, and `executive-cn-official-docx` is the 公文模板, with 仿宋_GB2312 body and no callouts. Run `templates` for supported modes and numbering policies; `components` describes content components, not template modes.
- All three templates support `document_mode: report` (cover and TOC by default) and `document_mode: document` (neither by default). When `document_mode` is not written, 公文 is a `document`; 楷体 and 宋体 follow the content: with chapters it is a `report`, without chapters a `document` (a `# 标题` that opens the text is its title, not a chapter), and `effective_document.document_mode` in the receipt says which. A 楷体 or 宋体 `document` also defaults to no automatic heading numbers, list numbers as written, and page numbers only when there is more than one page. Set the mode explicitly in new source files. `cover`, `toc`, `chapter_header`, `page_numbers` and the figure/table lists can each be switched on or off on top of the mode; see the contract's Metadata section.
- Use `heading_numbering: auto` for new automatically numbered reports; use `none` to retain an author's clause numbers. Put `numbering_rule: native-v1` in new Markdown templates and examples. Do not add this marker to old source merely to silence a warning: check its reference targets first.
- Keep fonts unembedded by default. Add `--embed-fonts` only when recipients lack the required fonts and the locally available fonts allow embedding.
- Do not patch the generated `.docx` or write OpenXML to repair a build. Change the input and rebuild. `--settle-figures` is opt-in; read the contract before using it for a visibly excessive gap before a tall figure.

## Writing the Input

Read [the Markdown contract](references/docx-markdown-contract.md) before writing. [Examples](references/examples.md) includes complete report and ordinary-document inputs.

For a new report:

1. Write unnumbered `#`, `##`, `###` headings with `heading_numbering: auto`; only the 公文模板 accepts `####` in input. Do not skip levels.
2. Give tables and figures captions in separate blocks, preceded by a blank line: `表：标题`, `图：标题`. Use `表[landscape]：标题` for a wide table. Font size is automatic.
3. Introduce each exhibit before it with a numbered reference. 楷体/宋体 with numbered chapters use `见表 2.1`; 公文, `none`, and chapterless documents use `见表 1`. The build receipt states the effective policy. Uncaptioned tables do not consume table numbers.
4. Use inline `[1]` citations and a final `# 资料来源` section with ordered entries. Sources are native numbered lists and citations are updatable references. Do not invent sources.
5. Use fenced `math` for block equations and `\( ... \)` for inline equations. Equation references use `式 2.1` or `式 1`, following the effective caption policy.
6. Prefer explanatory paragraphs. Lists support prose; callouts are optional and unavailable in the 公文模板. Do not invent glossary/checklist structures or force page breaks to fill a template.

By default, `punctuation_mode: normalize` changes some ASCII punctuation to Chinese full-width punctuation in Chinese text and removes some spaces beside punctuation. Use `preserve` for transcription or whenever author punctuation and spaces must stay unchanged. This is separate from Markdown escaping; see the contract for exact triggers.

Three escapes exist: `\*` for a literal asterisk, `\|` for a literal pipe inside a table cell, and `1\.` at the start of a line for a paragraph that begins with a number instead of a list item. A masked value such as `Z*****99` is written `Z\*\*\*\*\*99`. Every other backslash is kept as written; code, math and link targets are never unescaped. Three or more consecutive underscores are literal text, so fill-in blanks such as `日期：____年____月____日` are written as they are; only exactly two (`__粗体__`) mark bold.

## Transcribing an Existing Document

For a contract, notice or letter, use `document_mode: document`, `heading_numbering: none`, `punctuation_mode: preserve`, and `numbering_rule: native-v1`. Select the font template that suits the source; do not switch to the 公文模板 just to remove the cover. A flush-left salutation, a right-aligned sign-off or a centred line goes in a `::: 顶格` / `::: 靠右` / `::: 居中` container (see "Paragraph Alignment" in the contract); never position text with spaces or empty paragraphs. On the 楷体 and 宋体 templates an ordinary document keeps the source's own list numbers and forms (`3.`, `（1）`, `1、`, `一、`, `(1)`, `（一）`) as native Word lists set like body paragraphs (see "Lists Numbered as Written" in the contract); on the 公文模板 add `list_numbering: author` to get this, because there only `1.` lines are lists by default and they use the template's numbering from 1. Other numbering (`a.`, `①`, an indented sub-item) is kept as text and reported as `unsupported_list_numbering` (`info`; it does not fail `--strict`).

Ordinary documents have three title cases: with metadata `title`, all `#` headings are real sections; without it, an initial `#` becomes the document title and is consumed; without it and without an initial `#`, the document starts directly with the body. Do not add an invisible title or repeat the title as a section.

Minimal complete input:

```markdown
---
title: 资料核对函
template: executive-cn-song-docx
document_mode: document
heading_numbering: none
punctuation_mode: preserve
numbering_rule: native-v1
---

青原资料室：

1\. 请核对资料编号 Z\*\*\*\*\*99。

| 项目 | 内容 |
| --- | --- |
| 交接方式 | 现场\|邮寄 |
```

Keep the original headings, paragraphs, table cells and characters. Do not add captions, references or sentences the original does not have just to clear a check: in ordinary documents such advice is `info`. The one exception is `caption_before_reference`, a warning in ordinary documents too: keep the original order and say in your delivery note that it follows the original. Captions are still numbered automatically; when the original caption number differs from the generated one, `caption_number_replaced` reports it.

If `unparsed_inline_markdown` appears, the text contains an unpaired marker: escape literal stars as `\*`, or pair the markers if emphasis was intended. A lone `__` is kept as written; bold needs a pair, and a blank of three or more underscores raises no check. Never delete original characters to clear a check.

After building, compare the result with the original — title, paragraph order, clause numbers, every table cell, masked characters — and tell the user which comparisons you made. The tool keeps what it is given; it cannot tell whether the original was transcribed correctly.

## Workflow

1. Save prepared content as `./output_docx/content.md`, or edit the active `report.json`.
2. Check CLI capabilities once (see Requirements), then build:

   ```bash
   npx --no-install docx-kit build ./output_docx/content.md --out ./output_docx --filename 项目复盘报告.docx
   ```

3. Read the complete `build-result.json`: `errors`, `warnings`, `checks`, `effective_document`, and `text_normalization`. The effective settings include mode, title block, cover/TOC, heading/caption numbering, punctuation mode, and any automatically supplied structure. `text_normalization` counts actual punctuation replacements and removed spaces; `applied` means a change occurred, not merely that normalization was enabled. Confirm these results match the task.
4. Resolve every error. For new reports, resolve warning-level checks and formula fallback warnings before delivery; `--strict` makes these failures. For transcription, preserve the original and explain any remaining warning that cannot be resolved without changing it. `info` does not fail strict builds and need not be cleared. QA's empty warnings never cancel build checks.
5. Run structural QA:

   ```bash
   npx --no-install docx-kit qa ./output_docx/项目复盘报告.docx --report-json ./output_docx/report.json --out ./output_docx/qa
   ```

   Read `check_scope`, `original_content_consistency`, `original_layout_consistency`, and `scope_notice`. `structure_only`/`not_checked` means content and layout fidelity have not been verified. A passed structure check is not delivery approval.
6. Review content and layout to the extent the task requires. For LibreOffice or another renderer that cannot recalculate Word fields correctly, first create a render-only copy:

   ```bash
   npx --no-install docx-kit render-copy ./output_docx/项目复盘报告.docx --out ./output_docx/preview --filename preview.render-only.docx
   ```

   The command freezes what the fields currently show and never changes the original. For a file edited in Word or WPS, update fields and save before making the copy. Use the copy for preview or conversion only; deliver the original.
7. Verify `docx_path`, `report.json` and `build-result.json` exist. Deliver the original Word file, source path, review status and any unresolved warnings, together with the applicable continuation instructions below.

## Delivery Instructions — Tell the User

Tell the user, in their language, what they can do with the file. For Chinese deliveries use the lines below, keeping only those that apply to the document:

- 这份 Word 可以直接接着写：标题后回车就是正文，表格、代码块后面可以直接输入；改“正文”“标题 1”“题注”“三线表”这些样式，全篇跟着变。
- 增删表、图、公式或资料来源后，全选按 F9（Mac 上是 fn+F9），编号和正文里的引用会一起更新，Word 和 WPS 都是这样。只想更新某一处，在它上面点右键选“更新域”。
- 用“插入题注”之前，先在题注对话框里建好“表”“图”标签并设好编号：按章编号的文档勾选“包含章节号”（章节起始样式“标题 1”、分隔符“句点”），全文连续编号的文档不勾。先设置再插入——Word 会按当前设置改写文档里已有的同类题注。WPS 自带这两个标签，在“编号”里勾选“题注关联章节编号”，分隔符改成句点。
- 新起一个有序列表：复制文档里已有的一条列表项来改，再右键选“重新开始于 1”，样子和原有的列表一致；也可以选中正文点“编号”。
- 紧跟在标题下面的那一段正文，不要直接点“编号”按钮：Word 会把它接进标题的编号、变成标题（标题带自动编号的 Word 文档都是这样）。从按钮旁的下拉里选一种编号格式就不会。取消编号之后，给这一段再套一次“正文”样式，首行缩进才回来。
- 新插的图片，给它所在的段落套“图片”样式；自己用“交叉引用”加的来源引用，套“来源引用”样式。
- 粘贴来的表格，给单元格套“表格文字”样式。
- WPS 里新插的表格不会自动是三线表；文档在 WPS 里保存过之后，回到 Word 里新插的表格也一样。复制文档里已有的一张表来改最省事。
- 在 Word 或 WPS 里改过的内容不会回到源文件；以后需要重新生成时，请把改过的文件一起发来。

## Failure Playbook

| Situation | Action |
| --- | --- |
| Validation/build errors | Fix the named field or missing asset. Do not patch the generated Word file. |
| `dangling_caption_reference` | Check the available reference locators listed in the message and the effective numbering policy. Some locators support old input and differ from the displayed number. Opening sections count as chapters when chapter numbering applies. |
| `caption_reference_renumbered` | Compare the old and new target named at each location. Correct the source reference to the intended object before declaring `native-v1`. |
| `unsupported_list_numbering` | Only under `list_numbering: author` (the default for a 楷体 or 宋体 ordinary document). The named line looks like numbering but is not a supported form, or is indented; it was kept as text and will not renumber in Word. It is `info` and does not block a strict build. In new writing, rewrite it flush left as `1.`, `（1）`, `1、`, `一、`, `(1)` or `（一）` if it is a list; if it is not one (exam options `A. … B. …`) or a transcription must keep the original numbering, leave it. |
| `legacy_official_reference` / `caption_number_replaced` | Informational compatibility/renumbering notices; inspect their meaning, but do not block strict builds or change an original merely to clear them. |
| Formula rendered as plain text | Correct the LaTeX or use valid native OMML from the source. Check top-level `warnings` as well as `checks`. |
| Figure settling skipped/stopped | Inspect `figure_settling` and warn the user; this warning alone does not fail strict builds. A moved figure still needs a reading-order review. |
| QA fails | Rebuild from source. If it still fails, report the QA result as a tool issue. |
| Required command/option absent | Report the local capability gap; upgrade only if permitted. Do not silently produce a report when an ordinary document was requested. |
