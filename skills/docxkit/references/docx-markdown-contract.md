# Markdown structure and numbering

Look here for document-mode inference, cover and contents settings, headings, lists, inline text, punctuation and transcription.

A short plain document — a notice, a letter, a certificate — needs no metadata at all: start with `# 标题` and write the text. Metadata is for what the content cannot say by itself.

## Metadata

```markdown
---
title: 项目复盘报告
template: executive-cn-docx
document_mode: report
heading_numbering: auto
numbering_rule: native-v1
subtitle: v0.1
author: 项目复盘小组
client: 内部验证
date: 2026-07-01
confidentiality: 内部资料
---
```

Supported keys: `title`, `subtitle`, `author`, `client`, `date`, `language`, `confidentiality`, `template`, `document_mode`, `heading_numbering`, `punctuation_mode`, `numbering_rule`, `list_of_figures`, `list_of_tables`, `cover`, `toc`, `chapter_header`, `page_numbers`, `list_numbering`, the stated-format keys `text_scale`, `<role>_font`, `<role>_latin_font`, `<role>_size`, `<role>_line_spacing` (see [stated formats](forms-and-layout.md#stated-formats-and-the-type-scale)), `margin_top`, `margin_bottom`, `margin_left`, `margin_right` (see [page margins](forms-and-layout.md#page-margins)), and `page_position` (see [page position](forms-and-layout.md#page-position)).
`author` is written only into the Word document properties (作者, `dc:creator` in `docProps/core.xml`); it is not shown on the cover, in the title block or anywhere in the text, and a non-empty `author` gives the `info` check `author_not_displayed`. An issuing organisation that should appear on the cover goes in `subtitle` (`subtitle: 某某咨询有限公司 编制`).
Unknown keys fail the build. `list_of_figures`, `list_of_tables`, `cover`, `toc` and `chapter_header` accept only `true` / `false`, `yes` / `no`, or `1` / `0`.
`language` currently accepts only `zh-CN`.

`template` defaults to `executive-cn-docx`. `executive-cn` is accepted as a ReportKit alias.

Available templates (different Chinese font pairing and layout personality):

| template id | 正文 | 章节标题 | 题注 | 封面/目录标题 | 版式 |
| --- | --- | --- | --- | --- | --- |
| `executive-cn-docx`（默认） | 楷体 | 楷体加粗 | 楷体 | 楷体（封面加粗） | 现代商务风 |
| `executive-cn-song-docx` | 宋体 | 黑体（不加粗，GB/T 9704 搭配） | 宋体 | 宋体加粗 | 正式规范风（行距 20 磅、标题段距阶梯、清北学位论文体系） |
| `executive-cn-official-docx` | 仿宋_GB2312 三号 | H1 黑体；H2 楷体_GB2312 加粗；H3 仿宋_GB2312 加粗；H4 仿宋_GB2312 | 仿宋_GB2312 小四号，表题同字号 | 方正小标宋简体（二号封面标题） | 首页副标题无前缀、无页眉、A4 默认页边距、固定 30 磅行距、公文序号“一、”“（一）”“1.”“（1）”；禁止 callout |

The 公文模板 in words: 二号 方正小标宋简体 title centred, 楷体_GB2312 subtitle without a prefix, 仿宋_GB2312 三号 body on a fixed 30 pt line, headings 一、（一）1.（1） in 黑体, bold 楷体_GB2312, bold 仿宋_GB2312 and 仿宋_GB2312, 小四 tables with a bold header, sources like the body, small print and footnotes 四号, definition and checklist tables 小四, page numbers as GB/T 9704 `— 1 —` in 四号宋体 centred 7 mm below the text area, no header, no callouts.

Body Latin text uses Times New Roman; code, equations and some template roles have their own fonts. Chinese font declarations follow the template, including code and equations. Pick a non-default template only when the user asks for the corresponding typography.

All three templates support both modes (`document_mode: report` or `document`). A mode is a ready-made set of defaults; every item in it can also be written on its own.

| Template and mode | Cover, TOC, chapter-name header | `heading_numbering` | `list_numbering` | `page_numbers` |
| --- | --- | --- | --- | --- |
| kaiti or song, `report` | all three | `auto` | `template` | `always` |
| kaiti or song, `document` (an ordinary document) | none | by the headings (below) | `author` | `auto` |
| official, `document` | none | `auto` (公文序号) | `template` | `always` |
| official, `report` | cover and TOC, no header | `auto` | `template` | `always` |

The parts are `cover`, `toc`, `chapter_header`, `list_of_figures`, `list_of_tables`, `page_numbers` and `heading_numbering`. Each overrides the mode's default: `cover: false` gives a report that starts with its title and contents, and a plain document (`document_mode: document`) can have `cover: true` (it needs a `title`) and `toc: true` (it needs chapter headings) while its heading and caption numbering stay those of a plain document — no need to make it a report for that.

So an ordinary document on the kaiti or song template numbers its headings only when their structure calls for it (numbers the author wrote in headings are always kept, see `heading_numbering` below), keeps list numbers as written, and shows page numbers only when it runs to more than one page. Reports and the official template are as they always were. Page numbers are fields that can be updated in Word. Run `docx-kit templates` to query each mode's defaults.

### When `document_mode` Is Not Written

- Official template: `document`, whatever the content. Notices, plans, implementation schemes and ordinary official documents start with their title on page 1 and have no cover or contents. Set `document_mode: report` on the official template only when the user explicitly requests a cover or contents, or the deliverable is genuinely a long report that needs them.
- Kaiti, song, or no `template`: the block structure you wrote decides, before any title or section is inferred.
  - With no metadata `title`, a `# 标题` line that is the first content block is the document title, not a chapter.
  - Any other heading means the input has chapters: it is built as a `report`, exactly as before.
  - A sources heading never counts: `# 资料来源` (also 参考来源, 参考文献, 来源, References, Sources, at any level, with or without author numbering such as `六、资料来源`) is not a chapter and is never taken as the document title.
  - With no chapters it is built as a `document` with the defaults above, and that first `# 标题` is used once, as the title.

| Input without `document_mode` (kaiti, song, or no template) | Built as |
| --- | --- |
| Body text only; or a `# 标题` first and then body text | document |
| `# 文档名` first, and later a `##` or another `#` | report |
| Metadata `title`, and any heading in the body | report |
| Body text first, and a `# 事项` later | report |
| Body text, then only `# 资料来源` | document, with its sources section |
| `# 资料来源` as the only heading, on the first line | document without a title, with its sources section |
| Real chapters, and `# 资料来源` at the end | report |
| `#` inside a code or math fence | not a chapter |
| `1、事项`, `（1）事项` | not a chapter |

**A lone `# 资料来源`.** A sources heading is never a chapter and never the title: body text followed only by `# 资料来源`, or a text whose only heading is a first-line `# 资料来源`, is a plain document with its sources section (without a title unless you write `title`). Write `document_mode: report` if it should still be a report.

`effective_document.document_mode` in the receipt says which was used. When the content decided on `document`, `automatic_structure` also contains `document_mode_document_without_chapters`. Write `document_mode` whenever you know what the user wants: `report` for a short text that still needs a cover and contents, `document` for a long text with chapters that needs neither.

Two kinds of existing kaiti or song source now give a different result. A source with no `document_mode` and no chapters used to become a report with a cover, contents and one chapter made from the title; it is now an ordinary document. A source that says `document_mode: document` now gets the three defaults in the table; write `heading_numbering: auto`, `list_numbering: template` and `page_numbers: always` to keep the earlier result. Sources with chapters, the official template, and every `report.json` are unaffected (a `report.json` carries its settings; see [saved-model defaults](report-json.md)).

`cover`, `toc`, `chapter_header` and `page_numbers` switch the outer parts one at a time, in any template and either mode. Leave them out to get the defaults above; write one only to depart from them.

| Key | Values | Effect |
| --- | --- | --- |
| `cover` | `true` / `false` | A cover page with the title, subtitle, `client · date` and `confidentiality`; it never shows a page number. Without a cover, the title and subtitle head the first page as a title block and the other three fields are not shown. |
| `toc` | `true` / `false` | The main contents. `list_of_figures` and `list_of_tables` are separate switches and no longer depend on the mode or on `toc`. If any of the three has entries, the document gets a contents section numbered i, ii, … and the body starts again at 1; otherwise there is no such section. |
| `chapter_header` | `true` / `false` | A header on body pages naming the current chapter (level-1 heading). In a document with no level-1 heading it shows the document title instead. |
| `page_numbers` | `always` / `none` / `auto` | `always` puts the page number, centred, in the footer of contents and body pages; on the 公文模板 it follows GB/T 9704: `— 1 —` in 四号 宋体 with half-width digits, its line 7 mm below the text area, centred on every page (not alternating sides). Its position and form cannot be chosen; `none` shows no page number anywhere; `auto` shows page numbers only when the whole document has more than one page. Default: `auto` for a kaiti or song ordinary document, `always` otherwise. |

`page_numbers: auto` writes a conditional field into the footer (`IF NUMPAGES > 1`, counting every page of the file). Word and WPS evaluate it as they lay the pages out (on the 公文模板 the two dashes are inside the condition too): a one-page document shows no number, the numbers appear when it grows to a second page and disappear when it shrinks back, with nothing to update by hand. The receipt therefore does not say whether a number is currently shown. LibreOffice does not evaluate this footer and shows no page number at all, so `render-copy` puts a plain page number into its copy instead: the copy of a document of several pages is right, and the copy of a one-page document shows a "1" that the delivered file does not have. Binaries older than this feature reject `page_numbers: auto`.

The official template centres `— 1 —` in the footer whether or not the document has a cover or contents.

`document_mode` keeps deciding everything else: title and section rules, caption numbering and check severities. Typical uses: `cover: false` for a report that starts with its title and contents; `toc: false` for a short report; `document_mode: document` with `toc: true` or `cover: true` for a long ordinary document.

These fail validation instead of producing an empty part:

- `toc: true` in an ordinary document with no chapters (`theme.toc is true but the document has no chapters…`). Add `#` headings or leave `toc` off; no chapter is created for you.
- `chapter_header: true` with neither a level-1 heading nor a title.
- `cover: true` with no title.
- An ordinary document on the kaiti or song template with no title and no content at all (`the document is empty: it has no title and no content…`). This is what an empty Markdown file, or one with only metadata and no `title`, now gives; it is not built into a blank document. A document with only a title, or only body text, is fine. The official template and `report.json` without `layout_rule` are unchanged.

`list_of_figures: true` / `list_of_tables: true` add 图目录 / 表目录 after the main contents; their entries link to the captions, and their page numbers refresh when Word updates fields. Switch them on only for figure- or table-heavy reports. A figure or table list that is switched on but has nothing to list is skipped with a warning.

`list_numbering` accepts `template` or `author` in every template and mode; the default is `author` for a kaiti or song ordinary document and `template` otherwise. `template` shows ordered lists in the template's format, each starting at 1; `author` keeps the form and numbers the author wrote. See "Lists Numbered as Written".

`heading_numbering` accepts `auto` or `none` in every template and mode; a written value always wins. Unwritten, it is `auto`, except in a kaiti or song ordinary document, where the headings decide:

1. If any heading carries a written number (`一、`, `1.`, `1、`, `1.1 `, `（一）`, `第一章`, `第三条`, `（1）`, `(1)`), the headings are kept exactly as written and get no automatic numbers.
2. Otherwise, if the headings to be numbered span two or more levels, or there are four or more of them, they get the template's numbers: 1, 1.1, 1.1.1.
3. Otherwise (one to three headings, all at one level) they stay unnumbered.

The document title is not a heading here, and the sources section (`# 资料来源` or another sources heading, with the headings under it) is never counted and never numbered in an ordinary document. The receipt's `effective_document.heading_numbering` gives the value used and `automatic_structure` the reason: `heading_numbering_auto_by_structure`, `heading_numbering_none_numbers_written` or `heading_numbering_none_few_headings`. The saved `report.json` writes the value, so a rebuild comes out the same. Write `heading_numbering: none` when a long ordinary document must stay unnumbered, and `auto` to number a short one. `auto` supplies heading numbers; `none` keeps author-written clause numbers and supplies none of its own. Heading styles and outline levels remain usable. It does not disable list or caption numbering, and in an ordinary document captions are numbered through the document either way.

Put `numbering_rule: native-v1` in new Markdown that refers to tables, figures or equations by number; a text without such references does not need it. It declares that references were written against the new numbering rules; it does not choose a visual format. Do not add it to an old document before checking its reference targets. Markdown accepts only `native-v1`; see [legacy JSON rules](report-json.md).

`punctuation_mode` accepts `normalize` (default for every template and mode) or `preserve`; any other value fails validation. The default can change punctuation and spaces in Chinese text. Use `preserve` when transcribing a contract, notice or letter. In JSON set `theme.punctuation_mode`. This controls text rendering, not the source stored in `report.json`; see “Punctuation and Spaces” below for the exact rules.

## Titles and Sections

Ordinary documents (`document_mode: document`) have three title cases:

| Input | Result |
| --- | --- |
| Metadata has `title` | One title block; every `#` is a real section, even if its text matches the title |
| No title, first nonblank body block is `# ...` | That heading becomes the document title and is consumed; later headings remain sections |
| No title, body starts with anything else | No title block; body starts immediately. No standalone subtitle is emitted |

**A long title.** The document title (the title block of an ordinary document or an official document, and the cover title of a report) and the subtitle break where you write `<br>`, inside one paragraph: `title: 关于开展2026年第四季度<br>安全生产大检查的通知`. A title longer than one line wraps where Word puts it, which is often one or two characters before the end (“……大检查的通” / “知”). Break it yourself where the meaning is complete, with lines of similar length; on the 公文模板 a title of several lines is arranged as a trapezoid or a diamond (GB/T 9704: 词意完整、排列对称、长短适宜). When the title is estimated to wrap with a very short last line, the build succeeds with the warning `title_short_last_line` (see [content checks](diagnostics.md#content-checks)). Wherever else the title is used — the header of a document without chapters, comparisons in a redline — `<br>` is joined into one line (nothing between Chinese characters, one space otherwise). A `<br>` in a heading (`#`) is not a break: see "Line breaks inside a paragraph".

A document without sections does not acquire a synthetic section. Never use whitespace or invisible characters as a title. For a report, use an explicit metadata title: legacy Markdown title inference and automatic section creation remain active in report mode and are disclosed in `effective_document.automatic_structure`.

Use `#` through `###`; only the 公文模板 accepts `####` in source input. The first real section must be level 1, and levels cannot be skipped (invalid hierarchy fails validation instead of producing numbers such as `1.0.1`). In a report, split long chapters into `##` subsections rather than long flat runs of paragraphs (`flat_section_structure`); the 楷体 and 宋体 templates number them 2.1 / 2.2, the 公文模板 “一、”“（一）”“1.”“（1）”. For automatically numbered reports, do not add author numbering — write `# 研究背景与方法论`, not `# 一、研究背景与方法论`:

```markdown
# 市场规模与需求结构

正文先说明本章范围。

## 渗透率走势

本节说明指标。

## 区域结构变化

本节说明差异。
```

**A number written at the start of a heading is removed where the template numbers headings** (`heading_numbering: auto` — reports, the 公文模板, and a kaiti or song ordinary document only when `auto` is written), together with the spaces after it, and `build` / `validate` warn `manual_numbering_in_title` for each such heading, quoting it as written with its line number: `## 1.1 核对时间` becomes `核对时间` after the template's `1.1`, never `1.1 1 核对时间`. Removed are numbers that end in their own punctuation, whatever follows — `1.` `1、` `1．` `1.1.` `一、` `（一）` `(一)` `（1）` `(1)` — and `1.1`, `2.3.4`, `第一章`, `第1章`, `第一节`, `第三条`, `第一部分` (also 款, 篇, 部, 编) when a space follows. A number of two or more levels, or `第…章` / `第…节` / `第…部分`, run straight into the text (`1.2核对时间`, `2.3.4实施`, `第一章总则`, `第2节概况`) may be a number or part of the title (`1.5亿元投资`), so it is kept as written and warned `manual_numbering_in_title` with its line: delete it if it is a number, ignore the warning if it belongs to the title. Not numbers, kept as written and not reported: a number and a space (`90 天推进计划`, `2026 年展望`), a level of three or more digits (`2026.10.30 会议纪要`, `2025、2026 年对比`), and 条, 款, 篇, 编, 部 run straight into the text (`第一条生产线`, `第一部门`). The saved `report.json` holds the heading without the number, so a rebuild from it removes nothing and does not warn; a number written in a `report.json` heading is kept and warned. Ordinary kaiti and song documents that do not write `heading_numbering` keep every heading exactly as written (see `heading_numbering` above).

For transcriptions with `heading_numbering: none`, retain `# 第一条 整理范围` or `## 1.1 核对时间` exactly. This turns off `manual_numbering_in_title`, but not unpaired-marker checks. See the skill's transcription workflow and the complete contract/notice/letter examples.

## Blocks

```markdown
普通段落会变成 paragraph。

- 无序列表会变成 bullet_list。

1. 有序列表会变成 ordered_list。

> 普通引用会变成 quote。
```

Prefer paragraphs, bullet lists, ordered lists, tables, figures, and code blocks for normal report content. Use callouts only for rare high-signal emphasis. The official template rejects callouts. The default kaiti template draws an admonition box (colored left bar, light fill for risk/warning); the song template renders a plain body paragraph led by a bold label（标题或默认"风险提示"/"注"）— the formal-report idiom, no box or color.

For example, `> [!note] 关键说明` followed by `> 只统计已到账款项。` gives two different readings:

| Template | What the reader sees |
| --- | --- |
| 楷体 | The box starts with “只统计已到账款项。”; “关键说明” follows as a small right-aligned label in the same cell. |
| 宋体 | **关键说明：**只统计已到账款项。 The bold label leads the paragraph. |



A line directly under a list item (no blank line between), indented with spaces or a tab to where the item's text starts or by four spaces, continues that item: it joins the item's text, without a space where both sides are Chinese. This holds for ordered and bullet lists and for both kinds of numbering. A line written flush left is a paragraph of its own (in Chinese writing the text under `一、总体情况` starts a paragraph), and so is a line indented with full-width spaces, a line after a blank line, and an indented line that is itself numbered.

```markdown
1. 检查配电柜、开关箱和接地装置，
   发现隐患的立即停用并登记。
2. 填写检查记录。
```

An ordered list is one numbering instance. Items separated only by blank lines remain one list, even if every item is written as `1.`. After an intervening paragraph, code block, table or bullet list, numbering one greater than the last authored item number continues the same instance (even when earlier items were all written as `1.`); restarting at `1.` starts a new instance. New instances display from 1. Word supports demoting/promoting list items; this is not a new Markdown nested-list syntax.

### Callouts

```markdown
> [!note] 关键说明
> 这句话必须从正文中被快速扫到。

> [!risk] 风险提示
> 只在用户明确需要视觉风险框时使用。
```

Supported kinds: `note`, `insight`, `risk`, `warning`; `tip` is read as `note`. Use them sparingly, for the one sentence a reader must not miss; `[!risk]` only when the user wants a visible risk box. The official template rejects callouts.

## Lists Numbered as Written (`list_numbering: author`)

Under `list_numbering: template` only lines written `1. 条目` are ordered lists, they are shown in the template's own format, and every list starts at 1 — the rules in "Blocks" above. Under `list_numbering: author` the form and the numbers the author wrote are kept. `author` is the default for an ordinary document on the kaiti or song template; in a report or on the official template write `list_numbering: author` in the metadata to get it. In reports and on the official template nothing changes unless the option is written: a line such as `（1）正文` in an existing source stays a paragraph.

| Written in Markdown | `list_format` | Shown in Word |
| --- | --- | --- |
| `1. 条目` (whitespace is required after the dot) | `decimal-dot` | 1. 2. 3. |
| `（1）条目` | `decimal-full-paren` | （1）（2）（3） |
| `1、条目` | `decimal-comma` | 1、2、3、 |
| `一、条目` (一 to 九十九) | `chinese-comma` | 一、二、三、 |
| `(1)条目` | `decimal-paren` | (1) (2) (3) |
| `（一）条目` (一 to 九十九) | `chinese-full-paren` | （一）（二）（三） |

The numbers are native Word numbering, not typed text. The first item shows the number that was written (`3.` starts at 3), and adding or deleting an item in Word renumbers the rest.

These items are set like body paragraphs, the convention for notices, contracts and official-style text: the numbered line is indented two characters like the first line of a body paragraph, wrapped lines return to the left edge, and there is no hanging indent. Spacing, line pitch and alignment are the body's. After `1.` comes one space; the other forms run straight into the text, so the text after a wider number (9 → 10) simply starts further right. On the kaiti and song templates, template lists (`list_numbering: template`) keep their hanging-indent look. On the official template every list is set like this, the template's own lists included: its `（1）` numbers run straight into the text, and `1.`, `a.` and the bullet `•` are followed by one space. A template-numbered list that sits under a level-4 heading of the official template (which carries the automatic `（1）`) is numbered `1）2）3）` instead (half-width digits in the body's Latin font, a full-width bracket), so that two `（1）` levels are not nested. It is not ①②③: WPS draws automatic circled numbers larger and heavier than typed ones, whatever the font, and Word has the body font's circled digits only up to ⑩. Lists written under `list_numbering: author`, and every list when `heading_numbering: none`, keep their numbers.

How lines are grouped into lists:

- Adjacent lines of the same form whose numbers go up by one are one list; blank lines between them do not matter. It displays from the first number written.
- After something else (a paragraph, a table, a quote, a list in another form, …), a line whose number is exactly one more than the last number of the previous list in the same form continues that list. Any other number starts a new list at the number written. So `1.` `2.` / paragraph / `3.` is one list, and `1.` `2.` / paragraph / `1.` is two.
- A number that does not follow on starts a new list even with nothing in between: two consecutive `1.` lines are two lists that each show 1, and `1.` `2.` `5.` is a list of two followed by a list that starts at 5.
- A heading ends continuation. The first list after a heading starts at the number written and is a list of its own.
- A different form is a different list. `（一）` lines under a `一、` item, or `（1）` lines under a `1.` item, are their own list, and a following `二、` or `2.` continues the first list. No multi-level relationship is inferred; every item is at the first level.
- The item text does not decide anything: `1、2026 年工作安排` / `2、2027 年工作安排` are two items.

```markdown
一、总体安排
（一）设备管理部负责现场
（二）综合部负责通知
二、时间安排
（一）周六上午检修一号楼
```

One protection for sentences: a line with `、` whose number is not 1, that neither continues a list nor is followed by the next number, and whose text goes on like an enumeration (`2026、2027 年完成`, `三、四层的住户`, `10、20、30 三档`) is read as text, so a wrapped paragraph is not cut in two. A line that starts at 1 is always an item.

Numbering that is not one of the six forms gets no native numbering. Each such line is kept as it was written, as a paragraph of its own (consecutive lines are not joined), and `build` / `validate` report it with the check `unsupported_list_numbering` (level `info`), which names the line: Word will not renumber it when items are added or deleted. It is information, not a fault — the check cannot know whether the line was meant as a list (the options of a multiple-choice question, `A. … B. …`, are written exactly like this) — so it never fails `--strict`. This covers:

- letters and roman numerals (`a.`, `A、`, `(b)`, `iv.`, `Ⅳ、`, also circled or parenthesised letters such as `ⓐ`), full-width digits (`１.`);
- leading zeros and zero (`01.`, `0、`), a lone closing bracket or mixed brackets (`1)`, `1）`, `（1)`);
- Chinese numerals outside 一…九十九 or not in the usual spelling (`一百、`, `一十、`), and Chinese numerals in other shapes (`(一)`, `一.`);
- any numbered line that is indented. Below a list item that is a nested list, and multi-level import is not supported, so it is not flattened into the parent list or changed to another form: write the lower level flush left in another form, as in the example above. (Indented bullets are unchanged.)

**Circled numbers are kept as typed text, each line its own paragraph; they are not Word lists, so Enter does not continue them.** This holds on every template, in reports and plain documents, under either `list_numbering`. A line that starts with a circled, parenthesised or dotted number symbol (`①`–`⑳`, `㉑`–`㊿`, `⑴`–`⒇`, `⒈`–`⒛`, `❶`, `➀` and their kin) is a paragraph of its own even when the lines are written without blank lines between them; its text is unchanged, it is set like an item of a list numbered as written (indented two characters, wrapped lines back to the left edge), and it is not reported. A following line indented to the item's text continues it; a flush-left line starts a new paragraph. Circled numbers inside a sentence (`措施①和措施③`) are ordinary text. Use them for numbering that must look exactly as typed; for numbering Word keeps up to date, write one of the six forms.

Like every paragraph, a kept line follows `punctuation_mode`: under `normalize` an ASCII `. ` next to Chinese becomes `。`, except a single letter and its period at the start of the line (`A. 继续工作` stays; the `B.` after it does not); transcriptions use `preserve`. Dates, decimals, version numbers and ordinary sentences (`2026.10.13`, `1.5 倍`, `v1.2.3`, `A、B 两栋`, numbers above 32767) are not numbering and are not reported.

Unaffected by the option: `# 资料来源` sections (`1.` entries there are still the `[n]` source list; the other forms there are paragraphs), quotes, callouts, table cells, code blocks, `:::` alignment containers (numbered lines inside them stay text) and bullet lists.

In `report.json` an `ordered_list` block carries `list_format` (one of the six names above; `template`, the default, is omitted) and `list_start`, the number its numbering instance starts from (default 1, omitted). Blocks with the same `list_id` are one instance: they must have the same `list_format` and the same `list_start`, and a later block continues counting after the items of the earlier ones, so its own first number is not stored. An author `list_format` needs `theme.list_numbering: author`; a `list_start` other than 1 needs an author format; a `chinese-comma` or `chinese-full-paren` list must stay within 一…九十九. These rules fail validation with a message that names the block. JSON has no line numbers, so `unsupported_list_numbering` is reported only for Markdown.

`docx-kit redline` compares the form and the displayed numbers, not `list_id`. The parts of a list whose form or displayed numbers changed (renumbered, another form, continued differently) are shown as deleted and inserted, and accepting or rejecting all changes leaves each draft's own numbering.

Binaries older than this feature reject `list_numbering: author` (or the key itself). Check `docx-kit components ordered_list` for `list_format` and `list_start`.

## Inline Formatting

Body text (paragraphs, list items, quotes, callouts, table cells, source-list entries, `report.json` text fields alike) supports inline markers:

| syntax | renders as |
| --- | --- |
| `**粗体**` / `__粗体__` | bold run |
| `*斜体*` | italic run（单下划线 `_斜体_` 不支持，避免误伤 snake_case） |
| `***粗斜体***` | bold + italic run |
| `~~删除线~~` | strikethrough run |
| `____` (three or more underscores) | literal text: a fill-in blank, e.g. `日期：____年____月____日` |
| `` `行内代码` `` | monospaced-styled run with light gray shading, content kept literal; Chinese inside code keeps the template's Chinese font |
| `[标题](https://…)` | external hyperlink (http/https only) |
| `\( … \)` | native inline equation (see [equations](figures-tables-and-sources.md#equations)) |

Markers must be paired and hug their content (`**9.1%**`, not `** 9.1% **`); unpaired markers stay literal and trigger the `unparsed_inline_markdown` warning. Underscores are read by run length: only a run of exactly two, with no further underscore touching it, is a bold marker; a run of three or more is literal text wherever inline markers are read (body, table cells, headings, captions) and never warns, so fill-in blanks such as `姓名：______` are written as they are; a single `_` is literal. There is no `\_` escape: a lone `__` stays literal with the warning — pair it for bold, or use three or more underscores for a blank. Only five escapes are interpreted: `\*` for a literal star, `\|` in a table cell, line-start `1\.` (any digits, followed by whitespace) for a literal numbered paragraph, `\<br>` for a literal `<br>` (see "Line breaks inside a paragraph"), and `\表`, `\图`, `\式` directly before a number (`\表 3.1`, `\图2`) for another document's table, figure or equation number, shown as plain text and never taken as a reference (see [numbering and references](figures-tables-and-sources.md#numbering-and-references)). Other backslash behavior is unchanged. Code spans/blocks, math and URL targets do not decode these escapes. A masked value such as `Z*****99` is written `Z\*\*\*\*\*99`. Unpaired stars intended as literal characters should be escaped, never deleted to clear a warning. Inline markers inside section headings and table/figure/equation captions are not styled: the document shows the text with the markers removed (headings and captions already carry their own uniform style), while `report.json` keeps the heading or caption exactly as you wrote it. To keep literal `*` or `~` characters in a heading or caption, use `\*` for a star, or a code span for literal text — `` 表：`电量*电价` 测算 `` is shown as `电量*电价 测算`.

### Line breaks inside a paragraph (`<br>`)

`<br>`, `<br/>` and `<br />` (any letter case) are a line break inside the paragraph (Word's Shift+Enter, `w:br`): the text continues on the next line of the same paragraph, with no paragraph spacing in between. A break is the only way to put two lines in one table cell, since a Markdown table row is one line.

| Where | `<br>` |
| --- | --- |
| Document `title` and `subtitle`; body paragraphs, list items, quotes, callout text, alignment containers, side-by-side panes; every table cell (pipe tables, `::: 表格`, the header row included; in `report.json` also definition lists, checklists and metric cards) | breaks the line |
| Headings (`#`), table/figure/equation captions (and a figure's alt text when it stands in for the caption), source-list entries, callout and code-block titles, the metric-grid caption, `client` / `date` / `confidentiality` | not a break: the build succeeds with the warning `line_break_ignored` and the document shows one line — nothing in place of the break when the characters on both sides are Chinese, one space otherwise (the rule for joined lines below) |

`\<br>` prints a literal `<br>`; inside a code span or a code block `<br>` is always literal. Other tags (`<b>`, `</br>`, `< br>`) are text. In a `::: 表格` cell, `<br>` is not a merge marker: only a whole cell of `<` or `^` merges. `report.json` stores `<br>` as written (in text, cells, the title), and a rebuild breaks the line again; a newline character `\n` in a `report.json` text is not a line break (Word shows it as a space), so write `<br>`. Column widths are estimated from the longest line of a cell. In a redline, a changed paragraph is compared character by character as it is shown, breaks and inline markers included, with the change on the right line (details in `revising-documents.md`, "Showing what changed"); a changed table is deleted and inserted whole as before. Writing `<br />` instead of `<br>` is not a change.

A long `title` that would wrap with one or two characters (or one word) left on its last line: break it yourself with `<br>` where the meaning is complete, lines of similar length (`title: 关于开展2026年第四季度<br>安全生产大检查的通知`); the warning `title_short_last_line` points it out.

### Punctuation and Spaces

**The default is `punctuation_mode: normalize`.** In text that contains Chinese characters, the ASCII punctuation `, ; : ? ! .` becomes `，；：？！。`, and ASCII spaces between that punctuation and Chinese characters are removed. For example, `甲,  乙: 丙.` becomes `甲，乙：丙。`.

Left alone in either mode: bare `http(s)` URLs and email addresses, link targets, code spans and code blocks, native equations, and colons, commas and dots inside Latin or numeric text such as `10:00`, `1,000` and `Node.js`. A Windows drive colon next to Chinese text is not protected: `C:\资料` can become `C：\资料`.

**A label at the start keeps its period.** When a paragraph, a heading, a list item or a table cell starts — or a line in one starts after `<br>` — with one Latin letter or a number (`2.1` too), a period, and then a space or Chinese text (`A. 继续工作`, `b.核对材料`, `1. 每周一次`, `3.核对`, `### 1. 感知层`), that period stays a half-width `.`, so choice options laid out in a table keep `A. `. Inline markers around the start do not matter: `**1. 感知层。**感知层由……` and `**2. 传输层**采用……` keep `1.` and `2.` too, and a heading's contents entry shows it as the heading does. A kept period is not a change, so `text_normalization` does not count it. Where the template numbers the headings, a number written at the start of a heading is still removed as described under "Numbering and References" (`manual_numbering_in_title`). Only this shape: two letters (`AB.`, `IV.`), an `A.` or `1.` later in the paragraph, a period followed by something else (`A.1`), and the start of a quote, callout or caption follow the rule above; a real sentence end still changes (`已完成.` becomes `已完成。`). In Markdown a line that starts with `1. ` is a list item; write `1\. ` for a paragraph that starts with a literal number.

**Lines joined into one paragraph.** Adjacent lines of a paragraph (also in alignment containers and side-by-side panes) are joined with no space where the characters on both sides are Chinese — characters, kana, Chinese punctuation, and a curly quote, dash or ellipsis next to them — because a line break in Chinese is not a space: `第一，先切断电源。` + line break + `第二，……` gives `第一，先切断电源。第二，……`. Where both sides are Latin, or one side is Latin, the lines are joined with one space as before. This holds in both punctuation modes.

Set `punctuation_mode: preserve` to skip this step. Author punctuation and spaces are then kept character for character. Markdown structure, inline markers, the escapes, `<br>` and automatic numbering still apply. Half-width spaces and tabs at the edges of a table cell or heading are Markdown padding and are dropped; full-width spaces there are kept, so `| 甲方：　　　　 |` keeps its blank for a signature. The source text in `report.json` is never rewritten in either mode; the build receipt reports how many characters normalization changed.

A paragraph with a bare URL or a very long Latin string may break inside words and is set flush left instead of justified, so the string cannot run off the line. Lines of one paragraph are joined without a space where both sides are Chinese.

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

## Page Breaks

Use `---PAGE---` only when the user explicitly asks for a hard page break, or before a side-by-side block of more than 10 lines that must stay whole (see [side-by-side blocks](forms-and-layout.md)). Normal documents rely on automatic Word/WPS pagination.

## Transcribing an Existing Document

Transcribe only when the user says the wording must not change (照录、原文不能改、一字不改). A request to put material into Word ("排成 Word", "做成 Word", "整理成文档") is not a transcription: keep the content and the facts, fix obvious errors (a typo, a figure or an example that contradicts the rest of the material), and turn spoken or note-like wording into written prose. When repairing inconsistent section numbering, use actual headings and update references in the text (for example, `见 3.0`) to point to the same section under its new number. Tell the user what you changed.

A transcription keeps the original's wording, clause numbers, masks and order. Nothing in this contract is permission to rewrite it.

- Settings: `punctuation_mode: preserve` always, and `heading_numbering: none` on every template: a kaiti or song ordinary document keeps numbers written in headings, but one whose headings carry none would otherwise be numbered by their structure. On the kaiti and song templates an ordinary document already keeps list numbers as written; on the 公文模板 also add `list_numbering: author`. Write `document_mode: document` when the original has headings, and do not switch to the 公文模板 just to remove a cover.
- Position: a flush-left salutation, a right-aligned sign-off or a centred line goes in a `::: 顶格` / `::: 靠右` / `::: 居中` container (see [alignment containers](forms-and-layout.md#paragraph-alignment)); never position text with spaces or empty paragraphs.
- Lists: the six written forms become native lists with the original numbers (see "Lists Numbered as Written"); other numbering (`a.`, an indented sub-item) is kept as text and reported as `unsupported_list_numbering` (`info`); a line starting with a circled number (`①`) is kept as typed text, a paragraph of its own, and not reported. A numbered line that must stay an ordinary paragraph is written `1\.`.
- Literal characters: `\*` for an asterisk (`Z\*\*\*\*\*99`), `\|` for a pipe inside a table cell; blanks of three or more underscores are written as they are. If `unparsed_inline_markdown` appears, the text has an unpaired marker: escape literal stars, or pair the markers if emphasis was intended. Never delete original characters to clear a check.
- Checks: do not add captions, references or sentences the original does not have. In ordinary documents such advice is `info` and needs no action. The exception is `caption_before_reference`, a warning in ordinary documents too: keep the original order and say in the delivery note that it follows the original. Captions are still numbered automatically; when the original's caption number differs from the generated one, `caption_number_replaced` reports it.
- Afterwards: compare the result with the original — title, paragraph order, clause numbers, every table cell, masked characters — and tell the user which comparisons you made. The tool keeps what it is given; it cannot tell whether the original was transcribed correctly.
