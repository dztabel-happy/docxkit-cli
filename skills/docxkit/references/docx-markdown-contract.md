# DocxKit Markdown Contract

Use this reference when writing Markdown input for `docx-kit build`, and read it before writing. The skill's `SKILL.md` gives the first decision (report or plain document), two complete inputs, the highest-frequency writing rules and the working loop; this file holds the rules behind them.

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
author: DocxKit
client: 内部验证
date: 2026-07-01
confidentiality: 内部资料
---
```

Supported keys: `title`, `subtitle`, `author`, `client`, `date`, `language`, `confidentiality`, `template`, `document_mode`, `heading_numbering`, `punctuation_mode`, `numbering_rule`, `list_of_figures`, `list_of_tables`, `cover`, `toc`, `chapter_header`, `page_numbers`, `list_numbering`, the stated-format keys `text_scale`, `<role>_font`, `<role>_latin_font`, `<role>_size`, `<role>_line_spacing` (see "Stated Formats and the Type Scale"), `margin_top`, `margin_bottom`, `margin_left`, `margin_right` (see "Page margins"), and `page_position` (see "Page position").
Unknown keys fail the build. `list_of_figures`, `list_of_tables`, `cover`, `toc` and `chapter_header` accept only `true` / `false`, `yes` / `no`, or `1` / `0`.
`language` currently accepts only `zh-CN`.

`template` defaults to `executive-cn-docx`. `executive-cn` is accepted as a ReportKit alias.

Available templates (different Chinese font pairing and layout personality):

| template id | 正文 | 章节标题 | 题注 | 封面/目录标题 | 版式 |
| --- | --- | --- | --- | --- | --- |
| `executive-cn-docx`（默认） | 楷体 | 楷体加粗 | 楷体 | 楷体（封面加粗） | 现代商务风 |
| `executive-cn-song-docx` | 宋体 | 黑体（不加粗，GB/T 9704 搭配） | 宋体 | 宋体加粗 | 正式规范风（行距 20 磅、标题段距阶梯、清北学位论文体系） |
| `executive-cn-official-docx` | 仿宋_GB2312 三号 | H1 黑体；H2 楷体_GB2312 加粗；H3 仿宋_GB2312 加粗；H4 仿宋_GB2312 | 仿宋_GB2312 小四号，表题同字号 | 方正小标宋简体（二号封面标题） | 首页副标题无前缀、无页眉、A4 默认页边距、固定 30 磅行距、公文序号“一、”“（一）”“1.”“（1）”；禁止 callout |

Body Latin text uses Times New Roman; code, equations and some template roles have their own fonts. Chinese font declarations follow the template, including code and equations. Pick a non-default template only when the user asks for the corresponding typography.

All three templates support both modes (`document_mode: report` or `document`). A mode is a ready-made set of defaults; every item in it can also be written on its own.

| Template and mode | Cover, TOC, chapter-name header | `heading_numbering` | `list_numbering` | `page_numbers` |
| --- | --- | --- | --- | --- |
| kaiti or song, `report` | all three | `auto` | `template` | `always` |
| kaiti or song, `document` (an ordinary document) | none | `none` | `author` | `auto` |
| official, `document` | none | `auto` (公文序号) | `template` | `always` |
| official, `report` | cover and TOC, no header | `auto` | `template` | `always` |

So an ordinary document on the kaiti or song template has no automatic heading numbers (the numbers the author wrote in headings are kept), keeps list numbers as written, and shows page numbers only when it runs to more than one page. Reports and the official template are as they always were. Page numbers are fields that can be updated in Word. Run `docx-kit templates` to query each mode's defaults.

### When `document_mode` Is Not Written

- Official template: `document`, whatever the content. Notices, plans, implementation schemes and ordinary official documents start with their title on page 1 and have no cover or contents. Set `document_mode: report` on the official template only when the user explicitly requests a cover or contents, or the deliverable is genuinely a long report that needs them.
- Kaiti, song, or no `template`: the block structure you wrote decides, before any title or section is inferred.
  - With no metadata `title`, a `# 标题` line that is the first content block is the document title, not a chapter.
  - Any other heading means the input has chapters: it is built as a `report`, exactly as before.
  - With no chapters it is built as a `document` with the defaults above, and that first `# 标题` is used once, as the title.

| Input without `document_mode` (kaiti, song, or no template) | Built as |
| --- | --- |
| Body text only; or a `# 标题` first and then body text | document |
| `# 文档名` first, and later a `##` or another `#` | report |
| Metadata `title`, and any heading in the body | report |
| Body text first, and a `# 事项` later | report |
| `#` inside a code or math fence | not a chapter |
| `1、事项`, `（1）事项` | not a chapter |

`effective_document.document_mode` in the receipt says which was used. When the content decided on `document`, `automatic_structure` also contains `document_mode_document_without_chapters`. Write `document_mode` whenever you know what the user wants: `report` for a short text that still needs a cover and contents, `document` for a long text with chapters that needs neither.

Two kinds of existing kaiti or song source now give a different result. A source with no `document_mode` and no chapters used to become a report with a cover, contents and one chapter made from the title; it is now an ordinary document. A source that says `document_mode: document` now gets the three defaults in the table; write `heading_numbering: auto`, `list_numbering: template` and `page_numbers: always` to keep the earlier result. Sources with chapters, the official template, and every `report.json` are unaffected (a `report.json` carries its settings; see `layout_rule` below).

`cover`, `toc`, `chapter_header` and `page_numbers` switch the outer parts one at a time, in any template and either mode. Leave them out to get the defaults above; write one only to depart from them.

| Key | Values | Effect |
| --- | --- | --- |
| `cover` | `true` / `false` | A cover page with the title, subtitle, `client · date` and `confidentiality`; it never shows a page number. Without a cover, the title and subtitle head the first page as a title block and the other three fields are not shown. |
| `toc` | `true` / `false` | The main contents. `list_of_figures` and `list_of_tables` are separate switches and no longer depend on the mode or on `toc`. If any of the three has entries, the document gets a contents section numbered i, ii, … and the body starts again at 1; otherwise there is no such section. |
| `chapter_header` | `true` / `false` | A header on body pages naming the current chapter (level-1 heading). In a document with no level-1 heading it shows the document title instead. |
| `page_numbers` | `always` / `none` / `auto` | `always` puts the page number, centred, in the footer of contents and body pages (its position and form cannot be chosen); `none` shows no page number anywhere; `auto` shows page numbers only when the whole document has more than one page. Default: `auto` for a kaiti or song ordinary document, `always` otherwise. |

`page_numbers: auto` writes a conditional field into the footer (`IF NUMPAGES > 1`, counting every page of the file). Word and WPS evaluate it as they lay the pages out: a one-page document shows no number, the numbers appear when it grows to a second page and disappear when it shrinks back, with nothing to update by hand. The receipt therefore does not say whether a number is currently shown. LibreOffice does not evaluate this footer and shows no page number at all, so `render-copy` puts a plain page number into the preview copy instead: previews of several pages are right, and the preview of a one-page document shows a "1" that the delivered file does not have. Binaries older than this feature reject `page_numbers: auto`.

`document_mode` keeps deciding everything else: title and section rules, caption numbering and check severities. Typical uses: `cover: false` for a report that starts with its title and contents; `toc: false` for a short report; `document_mode: document` with `toc: true` or `cover: true` for a long ordinary document.

These fail validation instead of producing an empty part:

- `toc: true` in an ordinary document with no chapters (`theme.toc is true but the document has no chapters…`). Add `#` headings or leave `toc` off; no chapter is created for you.
- `chapter_header: true` with neither a level-1 heading nor a title.
- `cover: true` with no title.
- An ordinary document on the kaiti or song template with no title and no content at all (`the document is empty: it has no title and no content…`). This is what an empty Markdown file, or one with only metadata and no `title`, now gives; it is not built into a blank document. A document with only a title, or only body text, is fine. The official template and `report.json` without `layout_rule` are unchanged.

`list_of_figures: true` / `list_of_tables: true` add 图目录 / 表目录 after the main contents; their entries link to the captions, and their page numbers refresh when Word updates fields. Switch them on only for figure- or table-heavy reports. A figure or table list that is switched on but has nothing to list is skipped with a warning.

`list_numbering` accepts `template` or `author` in every template and mode; the default is `author` for a kaiti or song ordinary document and `template` otherwise. `template` shows ordered lists in the template's format, each starting at 1; `author` keeps the form and numbers the author wrote. See "Lists Numbered as Written".

`heading_numbering` accepts `auto` or `none` in every template and mode; the default is `none` for a kaiti or song ordinary document and `auto` otherwise. `auto` supplies heading numbers; `none` keeps author-written clause numbers and supplies none of its own. Heading styles and outline levels remain usable. It does not disable list or caption numbering.

Put `numbering_rule: native-v1` in new Markdown that refers to tables, figures or equations by number; a text without such references does not need it. It declares that references were written against the new numbering rules; it does not choose a visual format. Do not add it to an old document before checking its reference targets. Markdown accepts only `native-v1`; legacy JSON rules are described below.

`punctuation_mode` accepts `normalize` (default for every template and mode) or `preserve`; any other value fails validation. The default can change punctuation and spaces in Chinese text. Use `preserve` when transcribing a contract, notice or letter. In JSON set `theme.punctuation_mode`. This controls text rendering, not the source stored in `report.json`; see “Punctuation and Spaces” below for the exact rules.

## Stated Formats and the Type Scale

Use these only when the user states a format ("正文仿宋三号，行距固定 28 磅", "标题二号小标宋", "字大一点"). They change the chosen template; they do not replace choosing one. Without them a document is built exactly as before.

```markdown
---
template: executive-cn-official-docx
title_font: 方正小标宋简体
title_size: 二号
title_line_spacing: 32pt
body_font: 仿宋_GB2312
body_latin_font: Times New Roman
body_size: 三号
body_line_spacing: 28pt
heading1_font: 黑体
heading1_size: 三号
---
```

```markdown
---
text_scale: large
---
```

**Keys.** `text_scale: normal | large`, and for each role `<role>_font`, `<role>_latin_font`, `<role>_size`, `<role>_line_spacing`. Roles: `title` (the document title; on a report, the cover title), `body`, `heading1`, `heading2`, `heading3`, and `heading4` on the official template only. Each key may be written once. There is no key for captions, tables, lists, the subtitle or the contents: they follow the body as described below. Bold, italics, character spacing, a fixed number of lines per page and a size for one paragraph cannot be stated.

**Sizes** are a Chinese size name or points with a unit, in whole or half points from 5 to 72: `16pt`, `16磅`, `10.5pt`. A bare number is refused; nothing is rounded.

| 初号 | 小初 | 一号 | 小一 | 二号 | 小二 | 三号 | 小三 | 四号 | 小四 | 五号 | 小五 | 六号 | 小六 | 七号 | 八号 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | 36 | 26 | 24 | 22 | 18 | 16 | 15 | 14 | 12 | 10.5 | 9 | 7.5 | 6.5 | 5.5 | 5 |

**Line spacing** has three forms: `28pt` or `28磅` is a fixed value; `at-least 28pt` is a minimum; `1.5x` (or `1.5倍`) is a multiple, which must be exact in Word's units (1, 1.15, 1.25, 1.5, 2 …). A bare number is refused.

**Fonts** are written into the document exactly as given, one name per key (a list is refused). `<role>_font` is the Chinese font; `<role>_latin_font` is the Latin font, and it also governs digits, list numbers, curly quotes, the dots of the contents and the page number, because Word treats those as Latin characters. On the official template the digits of the heading numbers `1.` and `（1）` (levels 3 and 4) are drawn in that heading's Latin font, like the digits in the heading text: Times New Roman unless a Latin font is in effect for the heading (stated for it or following `body_latin_font`); the full-width brackets of `（1）` stay in the heading's Chinese font. When a stated font is not installed on the building machine the build still succeeds and the document carries the name, but the check `font_not_found` (warning) names the roles and the font: the tool could not confirm how it displays, and a reader's Word or WPS that lacks the font substitutes another one without saying so. That format requirement is not met yet. Ask the user to install or supply a licensed font, or to accept another one; do not swap fonts yourself. `--strict` refuses to build with this warning. For a stated font the font table carries one alternative name, always a font Windows ships: the system twin when the stated font has one (仿宋 for 仿宋_GB2312, 楷体 for 楷体_GB2312, 宋体 for 方正小标宋简体), otherwise the chosen template's font for that role (楷体, 宋体, 黑体 or 仿宋). Word on Windows draws that font when the stated one is missing; this is not a cross-platform guarantee, and it does not make the requirement met. The official template's own fonts that Windows does not ship are written the same way, one alternative each: 仿宋 for 仿宋_GB2312, 楷体 for 楷体_GB2312, 宋体 for 方正小标宋简体, so Word on a machine without them shows 仿宋, 楷体 and 宋体 instead of 宋体 throughout.

**`text_scale: large`** is the chosen template with all text at 4/3: sizes to the nearest half point (a 12 pt body becomes 16 pt, 16 pt becomes 21.5 pt), line pitch, paragraph spacing and indents by the same factor. Fonts, bold, border widths, page margins, the header and page-number sizes and the cover's positioning distances do not change. Use it when the user wants bigger type without naming sizes; for exact sizes state them. It never shrinks text to keep a page count: a longer document simply runs to more pages.

**What follows what.** The stated values are applied in a fixed order: the template, then `text_scale`, then the roles that follow the body, then each role's own stated values. A stated value is never overridden by a derived one.

| You state | What follows | What does not |
| --- | --- | --- |
| `body_size` | Everything set from the body, by the same ratio: aligned paragraphs, lists (indents and the numbering definition together), quotes, lead and small text, table text, captions, sources, footnotes, the contents entries; and the title, subtitle, contents title and headings that are not stated themselves. First-line indent stays two characters. | Code and the cover's information lines (they follow `text_scale` only); header and page number. |
| `body_font` | Roles the template sets in the body's own font: on kaiti everything; on song the cover and contents titles, captions and tables; on official the level-3 and level-4 headings, captions and tables. | Roles the template gives their own font (the 黑体 headings of song and official, 方正小标宋简体 and 楷体_GB2312 on official); code. |
| `body_latin_font` | The whole document, including the roles above, list numbers and page numbers. | A role with its own `<role>_latin_font`; code. |
| `body_line_spacing` | Roles that use the body's line pitch: aligned paragraphs, lists, quotes. | Headings and the title (they keep their own rule, scaled by their own size); tables, captions and contents (their own ratio to their size). |
| `title_*` or `heading<n>_*` | Only that role; its spacing before and after scales with its own size. | Everything else. |

A heading size that is derived, not stated, never exceeds the level above it: with `body_size: 三号` and `heading1_size: 三号` on the kaiti template, heading 2 would follow the body to 18.5 pt and is held at 16 pt instead. Stated sizes are taken as written, even when a lower level is stated larger than a higher one; the document title is not part of this rule.

Once a size is stated or `text_scale: large` is used, tables are no longer shrunk to a compact size to make them fit: cell text wraps and the table grows. `table_consider_landscape` then says so; use `表[landscape]：` or fewer columns.

**Refused, with the field named:** a fixed line spacing smaller than the role's size (the message gives role, size and spacing and suggests `at-least`); a size outside 5–72 pt or not on a half point; a multiple that is not exact; `heading4_*` on a three-level template; a repeated key. **A tall inline formula under a stated fixed line spacing.** A fixed line does not make room for an inline formula taller than the line (a fraction, root, sum, integral, product, a limit written above or below, a matrix), and WPS cuts it off — the denominator of a fraction disappears. So the paragraph that contains one gets "at least" the stated value on that paragraph only: its lines without the formula keep the stated height, the line with the formula grows as much as the formula needs, and every other paragraph keeps the stated fixed value. The warning `fixed_line_spacing_tall_inline` names the block and the formula and says that this paragraph's line spacing is not the stated fixed value; tell the user, or make the formula a display equation if the whole text must keep one spacing. Subscripts, accents and other formulas no taller than the line change nothing. Only `\( … \)` is an inline formula (`$…$` is printed as written). This holds whenever `body_line_spacing` is stated as a fixed value, also when it equals the template's own (30pt on the official template). Where no fixed line spacing is stated, the official template's built-in 30 pt protects every paragraph with a formula or a picture the same way, without a warning.

`docx-kit templates` lists under `format.features` what this binary can do; check it before relying on any of the following with an installation you did not just update — an older binary rejects the keys and containers as unknown (one from just before page position refuses `page_position` as "not available yet"), or prints `:::` lines as text.

| You want to use | `format.features` must list |
| --- | --- |
| `<role>_font`, `<role>_latin_font` | `role_font`, `role_latin_font` |
| `<role>_size`, `<role>_line_spacing` | `role_size`, `role_line_spacing` |
| `text_scale: large` | `text_scale` |
| `margin_top` / `margin_bottom` / `margin_left` / `margin_right` | `page_margins` |
| `page_position: center` | `page_position` |
| `::: 表格` with `appearance`, `header=false`, `spacing` | `table_appearance`, `table_without_header`, `table_spacing` |
| `::: 留白` | `paragraph_spacing` |
| `::: 并排` | `parallel` |

The same output has `rule: format-v1`, the roles each template accepts (`format_roles`), the size names, and the options of the table container, the spacing directive and the side-by-side block. Plain documents decided by structure, alignment containers and lists as written are older than `format.features`: `templates` reports them as `by_structure`, and `docx-kit components` lists `alignment` on the `paragraph` component.

`redline` needs both drafts to have the same effective format, the same page margins and the same page position, and refuses otherwise, naming the differences; `三号` and `16pt`, `30mm` and `3cm`, or a value equal to the template's, count as the same. `--embed-fonts` embeds only the templates' own fonts and Times New Roman: with any other stated font it fails and says which, and the option is not dropped for you.

The build receipt reports what was applied under `effective_document.format` (see "Machine-Readable Results").

### Page margins

Use these only when the user states margins ("上边距 37 毫米，下 35，左 28，右 26", "页边距 2.5 厘米"). Without them every page keeps the template's margins and nothing changes.

```markdown
---
template: executive-cn-official-docx
margin_top: 37mm
margin_bottom: 35mm
margin_left: 28mm
margin_right: 26mm
---
```

**Keys.** `margin_top`, `margin_bottom`, `margin_left`, `margin_right`, each written once, each a length with its unit: millimetres (`30mm`, `30毫米`) or centimetres (`2.5cm`, `2.5厘米`). A bare number, inches, points and words such as 窄 or narrow are refused, and so is a negative value. Write only the edges the user named. There is no single `margin` key. Paper is always A4; gutters, mirrored margins and different odd and even pages do not exist.

**What the values mean.** They name the physical edges of every page: cover, contents, body, landscape table pages and the portrait pages after them. A landscape page does not rotate them: `margin_top` is the top of that page as it is read. An edge that is not written keeps what the page had: the template's margin on portrait pages (kaiti 18 mm top and bottom, 25 mm left and right; song 25 mm all round; official 25.4 mm all round) and 18 mm on landscape pages. The header and the page number stay 12.7 mm from the edge of the paper.

**What follows the margins.** Everything laid out to the text width follows the new text area: body text and lists; the page numbers at the right edge of the contents and of the lists of figures and tables (also after "update entire table" in Word); every table — plain pipe tables, the table looks, side-by-side blocks, landscape tables; callouts and code blocks; display equations and their numbers; figures. A figure without a width fills the text width, a percentage is of the new text width, and the tallest a figure may be moves with the height of the text area. Type sizes, indents and line spacing do not change.

**Equal to the template is the same as not written.** When every written value equals the template's own, the Word file and the bookmark names are exactly those of a document without margins. `30mm` and `3cm` are the same value. As soon as one edge differs, every written edge counts on every page: with `margin_top: 30mm` and `margin_bottom: 25mm` on the song template, landscape pages get a 25 mm bottom margin instead of their own 18 mm.

**Refused, with the reason and what to change.** DocxKit does not move a stated margin and does not shrink a figure whose width is stated.

- Left and right margins that leave a text area narrower than the template's deepest list indent plus ten characters, or top and bottom margins that leave fewer than ten body lines; the message gives the widths in millimetres. Landscape pages are checked only when the document has one.
- With a cover, top and bottom margins that leave a text area shorter than the cover needs (about 150 mm): the cover would run onto a second page. Reduce them, or set `cover: false`.
- A top margin under 16.9 mm while the chapter header is on, or a bottom margin under 17.6 mm while page numbers are on: the header and the page number each take one line 12.7 mm from the paper edge. State a larger margin, or `chapter_header: false` / `page_numbers: none`.
- In JSON, a figure whose `width` is given in millimetres and is wider than the text area. Use a smaller width or a percentage.
- `--settle-figures` together with stated margins: figure settling does not measure the new geometry yet.

When the longest chapter title may not fit in one header line of the new text width, the build succeeds with the warning `chapter_header_may_not_fit`. This is an estimate: if the header does wrap in Word, Word pushes the text of that page down, so the top margin is no longer the stated one. Look at the page in Word; raise `margin_top` to the value the message gives, shorten the heading, or set `chapter_header: false`.

The build receipt gives the margins and the text area in effect under `effective_document.format.page`.

### Page position

Use it only when the user wants a short text in the middle of the sheet: an oath, an invitation, a certificate, a notice meant to stand alone on one page. Without it every page starts at the top margin, as before.

```markdown
---
title: 入党誓词
text_scale: large
page_position: center
---
```

**Key.** `page_position: top | center`, written once. `top` is the original layout and the default: writing it is the same as not writing it (the Word file and the bookmark names are those of a document without it). Any other value is refused.

**What `center` does.** Every body page is centred between its own top and bottom margins: portrait pages, landscape table pages and the portrait pages after them, in normal and redline builds. Everything on the page moves together as one block — title, text, list, table, sign-off — and keeps its spacing; no line inside is centred by this (that is `::: 居中`). It is the page setting Word calls vertical alignment, written into each body section, so it stays when the user types, saves and reopens the file, and Word and WPS both honour it.

**Every page, the last one too.** When the text runs past one page, every page is still centred, a short last page after an automatic page break included: its first line sits lower by half of what is left empty, and a page that is nearly full moves down by half of its unused foot. So `center` is meant for a document that should stand on one page; on a longer one the top edge of the text differs from page to page. DocxKit does not count pages and does not switch to `top` for you: if the text may not fit on one page, leave `page_position` out or tell the user.

**What counts as content.** Word centres everything in the section, structural empty paragraphs included: the empty paragraph after a table that ends the document (where the user goes on writing) or the one that carries the section break after a landscape table. A page that ends that way shows its text about 8–17 pt above the exact centre. Do not add or delete paragraphs or change margins to correct it.

**What does not change.** The cover and the contents pages keep their own layout; without a cover, a document with contents has its title on the contents page, which is not centred either. Header, footer and page numbers stay where they are, numbering does not restart, and no section or page is added. With `page_numbers: auto` the number appears once the text reaches a second page, as before.

**Previews.** LibreOffice (and so the preview of a render copy, and the built-in preview of some desktop apps) does not apply vertical alignment: it shows a centred page from the top. Check the position in Word or WPS, or trust the receipt.

**Refused.** `--settle-figures` together with `center` (it judges a page by the space under its last line). `redline` between drafts whose page positions differ.

The receipt has `page_position: center` under `effective_document.format` when the body pages are centred; without it they start at the top.

## Titles and Sections

Ordinary documents (`document_mode: document`) have three title cases:

| Input | Result |
| --- | --- |
| Metadata has `title` | One title block; every `#` is a real section, even if its text matches the title |
| No title, first nonblank body block is `# ...` | That heading becomes the document title and is consumed; later headings remain sections |
| No title, body starts with anything else | No title block; body starts immediately. No standalone subtitle is emitted |

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

For transcriptions with `heading_numbering: none`, retain `# 第一条 整理范围` or `## 1.1 核对时间` exactly. This turns off `manual_numbering_in_title`, but not unpaired-marker checks. See the skill's transcription workflow and the complete contract/notice/letter examples.

## Numbering and References

| Effective policy | Captions / equations | Body reference |
| --- | --- | --- |
| 楷体/宋体, automatic numbered chapters | 表 2.1、图 2.1、（2.1） | 见表 2.1、如图 2.1、式 2.1 |
| 公文, any mode or heading policy | 表 1、图 1、（1） throughout the document | 见表 1、如图 1、式 1 |
| Any template with `heading_numbering: none`, without chapters, or with captions before the first ordinary-document chapter | Continuous integers throughout the document | 见表 1、如图 1、式 1 |

Each numbered level-1 section counts as a chapter, including an opening summary: an opening `# 执行摘要` or `# 导论` is chapter 1 and pushes the later chapters up. When `dangling_caption_reference` fires, its message lists the numbers that exist — copy from there instead of guessing, or write the skeleton first, build once, then fill in the references. Tables, figures and equations have separate sequences. **An uncaptioned table consumes no table number.** Captions and their body references display a space between label and number, even when the source omits it. Captions/equation numbers use native Word fields; body table/figure/equation/source references are clickable, updatable fields. Editing in Word requires updating fields; rebuilding Markdown requires updating the source's reference locators as well.

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

These items are set like body paragraphs, the convention for notices, contracts and official-style text: the numbered line is indented two characters like the first line of a body paragraph, wrapped lines return to the left edge, and there is no hanging indent. Spacing, line pitch and alignment are the body's. After `1.` comes one space; the other forms run straight into the text, so the text after a wider number (9 → 10) simply starts further right. On the kaiti and song templates, template lists (`list_numbering: template`) keep their hanging-indent look. On the official template every list is set like this, the template's own lists included: its `（1）` numbers run straight into the text, and `1.`, `a.` and the bullet `•` are followed by one space.

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

- letters and roman numerals (`a.`, `A、`, `(b)`, `iv.`, `Ⅳ、`), circled or parenthesised number symbols (`①`, `⑴`), full-width digits (`１.`);
- leading zeros and zero (`01.`, `0、`), a lone closing bracket or mixed brackets (`1)`, `1）`, `（1)`);
- Chinese numerals outside 一…九十九 or not in the usual spelling (`一百、`, `一十、`), and Chinese numerals in other shapes (`(一)`, `一.`);
- any numbered line that is indented. Below a list item that is a nested list, and multi-level import is not supported, so it is not flattened into the parent list or changed to another form: write the lower level flush left in another form, as in the example above. (Indented bullets are unchanged.)

Like every paragraph, a kept line follows `punctuation_mode`: under `normalize` an ASCII `. ` next to Chinese becomes `。`, except a single letter and its period at the start of the line (`A. 继续工作` stays; the `B.` after it does not); transcriptions use `preserve`. Dates, decimals, version numbers and ordinary sentences (`2026.10.13`, `1.5 倍`, `v1.2.3`, `A、B 两栋`, numbers above 32767) are not numbering and are not reported.

Unaffected by the option: `# 资料来源` sections (`1.` entries there are still the `[n]` source list; the other forms there are paragraphs), quotes, callouts, table cells, code blocks, `:::` alignment containers (numbered lines inside them stay text) and bullet lists.

In `report.json` an `ordered_list` block carries `list_format` (one of the six names above; `template`, the default, is omitted) and `list_start`, the number its numbering instance starts from (default 1, omitted). Blocks with the same `list_id` are one instance: they must have the same `list_format` and the same `list_start`, and a later block continues counting after the items of the earlier ones, so its own first number is not stored. An author `list_format` needs `theme.list_numbering: author`; a `list_start` other than 1 needs an author format; a `chinese-comma` or `chinese-full-paren` list must stay within 一…九十九. These rules fail validation with a message that names the block. JSON has no line numbers, so `unsupported_list_numbering` is reported only for Markdown.

`docx-kit redline` compares the form and the displayed numbers, not `list_id`. The parts of a list whose form or displayed numbers changed (renumbered, another form, continued differently) are shown as deleted and inserted, and accepting or rejecting all changes leaves each draft's own numbering.

Binaries older than this feature reject `list_numbering: author` (or the key itself). Check `docx-kit components`: the `ordered_list` component lists `list_format` and `list_start`.

## Paragraph Alignment

Body paragraphs are justified with a first-line indent. Three block containers change that for the paragraphs inside them: `::: 顶格` (flush left, no indent), `::: 靠右` (right-aligned) and `::: 居中` (centred). A container starts with that line and ends with a line containing only `:::`.

```markdown
::: 顶格
各有关单位：
:::

正文内容。

::: 靠右
某某单位

2026 年 10 月 13 日
:::
```

- Inside a container the ordinary paragraph rules apply: a blank line separates paragraphs, and adjacent non-blank lines join into one paragraph (see "Punctuation and Spaces" for the space at the join). **A two-line sign-off therefore needs a blank line between the organisation and the date**, as above; without it the two lines become one paragraph.
- Adjacent right-aligned paragraphs sit directly under each other, and the group keeps one line of space from what precedes it. Do not add empty paragraphs or spaces to position text.
- Only ordinary paragraphs are allowed inside, with the usual inline markers. A heading, table, list, quote, callout, code block, image, page break or another container inside one is an error — also when it stands directly under a line of text, where it is not read as a continuation of that paragraph — as are an unknown name (`::: 落款`), a container that is never closed, an empty container and a stray closing `:::`. Each error names the line number; nothing is printed as text. Inside a code fence `:::` stays literal.
- The names describe the shape only (flush left / right / centre); there are no "salutation" or "signature" components, and no trailing-attribute syntax.
- In `report.json` the same thing is `"alignment": "left" | "right" | "center"` on a `paragraph` block (`normal`, the default, is omitted). An aligned paragraph must keep `emphasis: normal`; combining it with `lead` or `small` fails validation.
- Binaries older than this feature print the `:::` lines as text. Check `docx-kit components` (the `paragraph` component lists `alignment`) before relying on it.

## Space Before a Paragraph (`::: 留白`)

When the user wants room left on the page, for a stamp, a signature, or simply air before a sign-off, write a one-line directive in front of the paragraph that should stand lower:

```markdown
特此证明。

::: 留白 三行
::: 靠右
青原科技有限公司（盖章）

2026 年 10 月 13 日
:::
```

- The directive is `::: 留白 一行`, `::: 留白 两行` or `::: 留白 三行`, alone on its line. It has no closing `:::` and produces no text. There are only these three levels: one, two or three body lines (22.2 pt each on the default template, 30 pt on the official one; with a stated body line spacing, that value). Numbers, millimetres and words such as 盖章 are refused. "留出盖章的位置" is three lines (about 2.3 cm on the default template, 3.2 cm on the official one): that is the most there is, and it is the usual answer, because a seal is stamped over the sign-off rather than in a free box. When the height must be exact, or larger, tell the user.
- It moves the next ordinary paragraph down: an indented paragraph, a paragraph in `::: 顶格` or `::: 居中`, or a whole `::: 靠右` group (the group stays together, with no gap inside it). In front of an alignment container, write it above the container line.
- When what follows is not a paragraph (a table, a list, a side-by-side block), the space is attached after the ordinary paragraph directly above instead. After a `::: 靠右` group it belongs to the whole group: the group stays together and the space appears once, below its last line. With no ordinary paragraph on either side there is nothing to attach it to, and the build fails.
- It is the larger of the paragraph's own spacing and the stated lines, never the sum: a `::: 靠右` group already stands one line below the text, so `一行` in front of it changes nothing and `三行` gives three. Between two paragraphs Word also uses the larger of "space after" and "space before".
- It is spacing in a paragraph style (named, for example, 正文·段前三行), not empty paragraphs. Pressing Enter after such a paragraph in Word gives an ordinary paragraph without the extra space. Never add blank lines, empty paragraphs or spaces to make room.
- **At the top of a page the space is gone.** Word does not keep the space before a body paragraph that lands first on a page, after an automatic page break or a `---PAGE---`; inside a side-by-side block the space is always kept, also at the top of a page. So room for a stamp is dependable inside `::: 并排`, and in the body only away from a page boundary. For a box that must keep its height wherever it lands, use a table with `spacing=roomy` or `extra`.

Errors, each with the line number, never silently dropped: a value other than the three levels; two directives in a row (use `三行`; levels do not add up); a directive at the end of the file, before a heading, next to `---PAGE---`, between two tables or two other blocks that are not paragraphs, at the end of a pane, or inside an alignment container.

## Side by Side (`::: 并排`)

Two blocks of text next to each other, tops aligned: the two parties of a contract, or a line with a date at the right margin.

```markdown
::: 并排 widths=1,1
甲方（盖章）：青原科技有限公司

::: 留白 三行
代表人（签字）：____________

日期：____年____月____日
---COLUMN---
乙方（盖章）：北辰数据服务有限公司

::: 留白 三行
代表人（签字）：____________

日期：____年____月____日
:::
```

A résumé row, two thirds for the text and one third for the date, which stays at the right margin when the text on the left wraps:

```markdown
::: 并排 widths=2,1
**青原科技有限公司　产品经理**
---COLUMN---
::: 靠右
2021.03—至今
:::
:::
```

- `::: 并排` opens the block, one line `---COLUMN---` separates exactly two panes, a line `:::` closes it. `widths=左,右` gives the relative widths (two positive numbers); without it the panes are equal. The block is as wide as the text area; between the panes there is a gap of one body character. Text, size and line spacing are the body's.
- A pane holds ordinary paragraphs, flush left with no first-line indent. Inside a pane you may use `::: 顶格`, `::: 居中` and `::: 靠右` (each closed by its own `:::`) and the `::: 留白` directive before a paragraph of the same pane. A `::: 靠右` group inside a pane does not get the one line of space that it has in the body.
- Nothing else goes inside: no headings, lists (a line starting with `1.` or `- ` is a list), tables, figures, display equations, code, quotes, page breaks, another `::: 并排` or `::: 表格`. Every line is checked, so an image line directly under a line of text is refused with its own line number; it is never joined to that paragraph. Write those outside the block. There are two panes, not three, and this is not a multi-column page: text does not flow from one pane into the other.
- **Staying together.** A short block is never split across pages: when it does not fit at the foot of a page it moves to the next page as a whole, so a stamp line and its signature line are not separated. "Short" means the taller pane comes to at most 10 body lines, counting each paragraph by the lines its visible text wraps to in its pane (a link counts by its label, not its address; inline markers do not count) and adding the lines of space written in front of paragraphs (the signature block above is 6). A longer block may break at the foot of a page and continue on the next, each pane where it stopped. If a block of more than 10 lines must stay whole, put `---PAGE---` before it.
- Several `::: 并排` blocks in a row are laid out as rows of one table with nothing between them (that is how the résumé rows above stack). Put a paragraph between two blocks to separate them, and use `::: 留白` for more distance.
- In Word the block is a borderless one-row table. Pressing Enter inside a pane continues in that pane.

Errors, each with the line number: no `---COLUMN---`, or more than one; an empty pane; an option other than `widths`, or not two positive numbers; anything in a pane that is not an ordinary paragraph; a block that is not closed; `---COLUMN---` outside a block.

Both features make the document `format-v1` (the tool writes `format_rule` into `report.json`), and an older binary rejects them: check `docx-kit templates` → `format.features` for `paragraph_spacing` and `parallel`. `redline` refuses when a side-by-side block differs between the two drafts in any way, or when a paragraph's spacing level changed; unchanged blocks pass through and the rest of the document is compared as usual.

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
| `\( … \)` | native inline equation (see Equations) |

Markers must be paired and hug their content (`**9.1%**`, not `** 9.1% **`); unpaired markers stay literal and trigger the `unparsed_inline_markdown` warning. Underscores are read by run length: only a run of exactly two, with no further underscore touching it, is a bold marker; a run of three or more is literal text wherever inline markers are read (body, table cells, headings, captions) and never warns, so fill-in blanks such as `姓名：______` are written as they are; a single `_` is literal. There is no `\_` escape: a lone `__` stays literal with the warning — pair it for bold, or use three or more underscores for a blank. Only three escapes are interpreted: `\*` for a literal star, `\|` in a table cell, and line-start `1\.` (any digits, followed by whitespace) for a literal numbered paragraph. Other backslash behavior is unchanged. Code spans/blocks, math and URL targets do not decode these escapes. A masked value such as `Z*****99` is written `Z\*\*\*\*\*99`. Unpaired stars intended as literal characters should be escaped, never deleted to clear a warning. Inline markers inside section headings and table/figure/equation captions are not styled: the document shows the text with the markers removed (headings and captions already carry their own uniform style), while `report.json` keeps the heading or caption exactly as you wrote it. To keep literal `*` or `~` characters in a heading or caption, use `\*` for a star, or a code span for literal text — `` 表：`电量*电价` 测算 `` is shown as `电量*电价 测算`.

### Punctuation and Spaces

**The default is `punctuation_mode: normalize`.** In text that contains Chinese characters, the ASCII punctuation `, ; : ? ! .` becomes `，；：？！。`, and ASCII spaces between that punctuation and Chinese characters are removed. For example, `甲,  乙: 丙.` becomes `甲，乙：丙。`.

Left alone in either mode: bare `http(s)` URLs and email addresses, link targets, code spans and code blocks, native equations, and colons, commas and dots inside Latin or numeric text such as `10:00`, `1,000` and `Node.js`. A Windows drive colon next to Chinese text is not protected: `C:\资料` can become `C：\资料`.

**A letter enumerator at the start keeps its period.** When a paragraph or a list item starts with one Latin letter, a period, and then a space or Chinese text (`A. 继续工作`, `b.核对材料`), that period stays a half-width `.`. Only this shape: two letters (`AB.`, `IV.`), a digit (`1.` is list syntax), an `A.` later in the paragraph, a period followed by something else (`A.1`), and the start of a quote, callout, table cell, heading or caption follow the rule above.

**Lines joined into one paragraph.** Adjacent lines of a paragraph (also in alignment containers and side-by-side panes) are joined with no space where the characters on both sides are Chinese — characters, kana, Chinese punctuation, and a curly quote, dash or ellipsis next to them — because a line break in Chinese is not a space: `第一，先切断电源。` + line break + `第二，……` gives `第一，先切断电源。第二，……`. Where both sides are Latin, or one side is Latin, the lines are joined with one space as before. This holds in both punctuation modes.

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

Do not paste naked long URLs into prose or tables. A paragraph that still contains a bare URL or a very long Latin string (an identifier, a path) is written to allow line breaks inside words, and a justified one is set flush left, so the string wraps instead of running off the line; Word shows this as "允许西文在单词中间换行". This is deliberate: say so if the user asks why an English word was broken. Use `[来源名称](URL)` in the source list. Inline `[1]` / `[2]` citations become clickable superscript Word REF fields. Adjacent `[1][2]` citations work; range forms such as `[1–3]` are not expanded. After adding a source in Word, update the reference fields. New references inserted through “交叉引用 → 编号项” need the “来源引用” character style.

## Tables

Keep tables as real row/column data. If cells become long paragraphs, move the explanation into surrounding prose or split the table.

DocxKit infers column widths for normal Markdown tables. For another look, stated widths or a table without a header, use the table container below.

### Table looks (`::: 表格`)

A pipe table on its own is the template's three-line table with a bold, repeating header, as before. To give one table another look, put it in a container: a line `::: 表格` with options, the table, and a line `:::`. A caption, when there is one, goes inside, on the line directly above the table. The options apply to that table only.

A grid table with a header and a caption, columns 3 : 1 : 1.5, first column left-aligned:

```markdown
见表 1。

::: 表格 appearance=grid widths=3,1,1.5 alignments=left,center,center
表：待办事项
| 事项 | 责任人 | 完成时间 |
| --- | --- | --- |
| 重点客户回款计划 | 陈默 | 10 月 31 日 |
| 投放预算草案 | 林晓 | 11 月 10 日 |
:::
```

A form to fill in by hand: grid, no header, more room in every cell, narrow label columns:

```markdown
::: 表格 appearance=grid header=false spacing=roomy widths=1,2,1,2
| 姓名 |  | 部门 |  |
| --- | --- | --- | --- |
| 岗位 |  | 联系电话 |  |
| 报名课程 |  | 期望时间 |  |
:::
```

| Option | Values | Meaning |
| --- | --- | --- |
| `appearance` | `three-line` (default), `grid`, `borderless` | `grid` draws every line (0.5 pt); `borderless` draws none, for option lists or aligned blocks; `three-line` is the template's table |
| `header` | `true` (default), `false` | `false`: the table has no header. The line above the `---` separator line is then data like every other row: it is not bold, nothing repeats across pages, nothing is dropped, and you do not invent column names. The separator line is still required syntax |
| `spacing` | `normal` (default), `roomy`, `extra` | Room above and below the text in every cell: 5, 12 or 24 pt (rows about 9.5, 14.5 and 23 mm high on the default template). Use `roomy` or `extra` for cells to be written in by hand. Rows still grow with their text; there is no fixed row height |
| `widths` | positive numbers, one per column | Relative column widths, `widths=1,2,1,2`. Without it the columns are equal |
| `alignments` | `left`, `center`, `right`, one per column | Per-column alignment of the cell text. Default is centred |
| `layout` | `normal` (default), `landscape` | `landscape` puts the table on a landscape page, like `表[landscape]：`. If the caption bracket and this option are both written they must agree |

Rules for a table that uses `appearance`, `header=false` or a `spacing` other than `normal`:

- Columns are equal, or follow `widths`, across the full text width. Widths are not guessed from the content, and the text is never shrunk to make a table fit: a long cell wraps and the row grows. A column of long English identifiers, codes or URLs needs more weight in `widths` (for example `widths=3,1,1,4`); otherwise such a word is broken inside wherever the column ends. A column too narrow for one character is an error that names the table and the column; give it more weight, use `layout=landscape`, or split the table.
- Every row must have the same number of cells; write an empty cell as `|  |`. An empty cell stays empty, a place to write.
- A three-line table with `header=false` has only its top and bottom rules. A grid or borderless table with a header still has a bold header that repeats on every page.
- **Merged cells are not supported.** A form row such as "参训理由" spanning the rest of the line is written with the cells it has; say so to the user rather than imitating a merge.

Errors, each with the line number: an empty container; a caption without a table; more than one table, or anything other than the table and its caption, in one container; an unknown, repeated or badly formed option (`key=value`, no spaces around `=`); a wrong number of `widths` or `alignments`; rows of unequal length; a caption written above the container instead of inside it; a container that is not closed. Inside a code fence `:::` stays literal.

A document that uses the container is read under `format-v1` like the stated formats: the tool writes `format_rule` into `report.json`, and an older binary rejects the container; check `docx-kit templates` → `format.features` (`table_appearance`, `table_without_header`, `table_spacing`). `redline` refuses when the same table has a different `appearance`, `header` or `spacing` in the two drafts; with equal settings a changed table is shown as before.

## Figures

Image paths are resolved relative to the Markdown file. Keep alt text short and different from the formal `图：` caption.
A figure whose file is missing fails validation. When the user asked for a figure that does not exist, do not draw, generate or borrow one: build without that figure, tell the user which file was missing, and write a placeholder paragraph in its place (for example `［此处插入时序图］`) only if the user agrees to one.
The generated `report.json` rebases relative figure paths to its own output directory, so `docx-kit build report/report.json --out report --filename 目标文件名.docx` remains reproducible.

PNG, JPEG, GIF, and BMP files are embedded directly. PDF figures use the first page and require `pdftoppm` on `PATH` (macOS can fall back to `sips`); otherwise convert the figure to PNG/JPEG before building.
Unsupported extensions, mismatched file signatures, and corrupt bitmap files fail validation instead of producing a broken Word image.

### Chart manifests (ChartKit)

If `<image>-manifest.json` sits next to a figure image (e.g. `assets/chart.png` + `assets/chart-manifest.json`), Markdown import reads `layout.recommended_insert_width_mm` (falling back to `layout.rendered_width_mm`) to size the figure. Discovery is fail-soft: a sidecar that is not valid JSON or has no usable width is treated as absent and never blocks or changes a build. An explicit `width` on the figure always wins over the manifest.

In direct `report.json`, `chart_manifest` on a figure block is a strict reference: the file must exist and parse, otherwise the build fails with a structured error.

### Tall figures and blank page bottoms (`--settle-figures`, opt-in)

Word cannot split a figure across pages. A figure taller than the space left on the page moves to the next page as a whole and leaves the bottom of the previous page empty — often a third to two thirds of it.

`docx-kit build <input> --out <dir> --filename <name.docx> --settle-figures` measures the real pagination after the normal build and, **in the delivered `.docx` only**, lets such a figure fall back by one or two of the ordinary paragraphs that follow it, so those paragraphs fill the page and the figure opens the next one. The paragraphs keep their order and wording; only the figure's position among them changes. The input and `report.json` keep the author's order, and every build starts again from that order.

- **Use it only on request**: when the user asks to reduce the blank space before a figure, or you can see that problem in the delivered file. It is not a default and it does not replace sizing a figure sensibly.
- **What it measures with**: on Windows with Microsoft Word installed, Word itself (the reader's pagination). Otherwise LibreOffice (`soffice` on `PATH`, `DOCXKIT_SOFFICE`, or the standard install location) plus poppler's `pdftotext`; LibreOffice measures a render-only copy. `DOCXKIT_SETTLE_WITH=libreoffice` skips Word; `DOCXKIT_DOCX2PDF=<executable>` uses your own converter (`<it> <input.docx> <output.pdf>`), on the original document unless `DOCXKIT_DOCX2PDF_RENDER_COPY=1` is set.
- **LibreOffice is not the reader's Word**: the two paginate these documents a line or two apart per page. A LibreOffice-measured arrangement is re-checked with the page one or two lines taller and shorter and is delivered only if it is no worse than the draft both ways; even so, in our sample roughly one changed document in nine came out worse in real Word. For a document that matters, measure with Word.
- **A figure never moves past** a paragraph that points at it (“上图”“图中”“如上所示”), its note or source line (“注：”“资料来源：”), a paragraph describing what is on it (“右上区域”“虚线”“箭头”), a lead-in sentence (ends with a colon, “如下”“以下”), a salutation, sign-off or centred line (a `::: 顶格`, `::: 靠右` or `::: 居中` paragraph), or a paragraph directly followed by a table, figure, list, equation or other non-paragraph block (it is most likely that block's lead-in; a hard page break after it does not count); it never leaves a preceding sentence that points down at it (“如下图所示：”), and a figure placed directly after another figure stays with it. These word lists only stop a move — they do not prove a paragraph is position-independent. Referring to figures by number (`见图 2.1`) is what makes a move safe.
- **Read the result**: with the flag, `build-result.json` gains `figure_settling` — `requested`, `measured`, `moved_paragraphs`, `improved`, `renderer` / `renderer_version`, `rounds`, `before_page_count` / `after_page_count`, `before_pages` / `after_pages` (pages whose bottom is ≥ 25% blank: `page`, `bottom_whitespace`, `figure`), `measurements` (`round`, `figure`, `score`, `page_count`, `outcome`: `draft` / `kept` / `undone`), `figures` (`figure`, `paragraph_count`, `paragraph_starts`, `blank_before`, `blank_after`), `held` (`figure`, `why` — figures still preceded by a blank page bottom and the reason they were not moved), `notes`, `reason`, `message`. When `moved_paragraphs > 0`, **check that the paragraphs listed in `figures[].paragraph_starts` still read naturally ahead of their figure** before delivering; if one does not, rebuild without the flag. Without the flag the field is absent.
- **It never fails a build**: with missing tools or a probe error the document is still delivered — the normal one, or the best arrangement already measured — and one entry is added to `warnings` (`图位置整理未执行: …` / `图位置整理中止: …`). That entry is not a content problem: leave it, tell the user, and note that `--strict` does not fail on it. The whole pass has a time budget of about three minutes; when it runs out, the best arrangement measured so far is delivered and `figure_settling.notes` says so. Do not promise that the option removes every gap.
- **Refused before building**: together with stated page margins (it still measures pages with the template's own margins) and together with `page_position: center` (it judges a page by the space under its last line, which a centred page splits above and below). Build without one of the two.
- It cannot help when the figure is followed by a table, another figure, a list, or the end of the section: there is no paragraph to bring forward. Shrink the figure, move it, or accept the blank.

### PDF (`docx-kit pdf`)

```bash
docx-kit pdf ./report/report.docx --out ./report --filename 季度复盘.pdf
```

When the user wants a PDF, make it with `docx-kit pdf`; never run LibreOffice on the delivered file directly. It never changes the input. On Windows with Microsoft Word installed it exports through Word: its own invisible instance, a copy of the document, repaginated first; the user's open documents are not touched. Everywhere else it exports with LibreOffice from an internal render copy, so captions, references and the page-number footer come out as Word shows them (a one-page document of `page_numbers: auto` has no page number, as in Word). `DOCXKIT_SOFFICE` names LibreOffice; `DOCXKIT_PDF_WITH=libreoffice` forces it.

It prints one JSON object (exit code 0 on success, 1 otherwise; the JSON is plain ASCII, non-ASCII characters as `\uXXXX`):

```json
{"ok": true, "command": "pdf", "pdf_path": "/abs/report/季度复盘.pdf", "engine": "libreoffice", "engine_version": "26.2.3.2",
 "notes": ["Exported with LibreOffice 26.2.3.2 from an internal render copy (...)"], "errors": []}
```

`engine` is `word` or `libreoffice`. On failure `pdf_path`, `engine` and `engine_version` are null and `errors` holds `{code, message}`: `invalid_arguments`, `input_not_found`, `not_a_docx`, `export_failed`, or `no_pdf_engine` — neither Word nor LibreOffice is available here; tell the user to open the file in Word or WPS and export it as PDF. Read `notes`: they name the engine, say when Word failed and LibreOffice was used instead, and say when the document centres its pages (`page_position: center`) — LibreOffice does not, so that PDF starts every page at the top; export it from Word or WPS to keep the centring. Fonts the machine lacks are substituted by the engine. Deliver the PDF beside the Word file, never instead of it unless the user asked only for a PDF.

### Render-only copies

```bash
docx-kit render-copy ./report/report.docx --out ./report/preview --filename report.render-only.docx
```

LibreOffice and similar renderers recalculate Word caption and reference fields incorrectly. For a PDF use `docx-kit pdf` (above), which does this internally. `render-copy` writes a copy in which those fields are replaced by what they currently show; the original is never changed, and tables of contents, page numbers, headers and footers keep their fields — with one exception: the conditional footer of `page_numbers: auto`, which LibreOffice does not display, becomes a plain page number in the copy (see `page_numbers` under "Metadata"). A freshly built document can be copied directly; for a file edited in Word or WPS, update fields and save first. The default output is `<input-stem>.render-only.docx` beside the input. Use the copy for preview and conversion only; deliver the original.

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

Use `---PAGE---` only when the user explicitly asks for a hard page break, or before a side-by-side block of more than 10 lines that must stay whole (see "Side by Side"). Normal documents rely on automatic Word/WPS pagination.

## Transcribing an Existing Document

A transcription keeps the original's wording, clause numbers, masks and order. Nothing in this contract is permission to rewrite it.

- Settings: `punctuation_mode: preserve` always. On the kaiti and song templates an ordinary document already keeps heading numbers and list numbers as written; on the 公文模板 add `heading_numbering: none` and `list_numbering: author`. Write `document_mode: document` when the original has headings, and do not switch to the 公文模板 just to remove a cover.
- Position: a flush-left salutation, a right-aligned sign-off or a centred line goes in a `::: 顶格` / `::: 靠右` / `::: 居中` container (see "Paragraph Alignment"); never position text with spaces or empty paragraphs.
- Lists: the six written forms become native lists with the original numbers (see "Lists Numbered as Written"); other numbering (`a.`, `①`, an indented sub-item) is kept as text and reported as `unsupported_list_numbering` (`info`). A numbered line that must stay an ordinary paragraph is written `1\.`.
- Literal characters: `\*` for an asterisk (`Z\*\*\*\*\*99`), `\|` for a pipe inside a table cell; blanks of three or more underscores are written as they are. If `unparsed_inline_markdown` appears, the text has an unpaired marker: escape literal stars, or pair the markers if emphasis was intended. Never delete original characters to clear a check.
- Checks: do not add captions, references or sentences the original does not have. In ordinary documents such advice is `info` and needs no action. The exception is `caption_before_reference`, a warning in ordinary documents too: keep the original order and say in the delivery note that it follows the original. Captions are still numbered automatically; when the original's caption number differs from the generated one, `caption_number_replaced` reports it.
- Afterwards: compare the result with the original — title, paragraph order, clause numbers, every table cell, masked characters — and tell the user which comparisons you made. The tool keeps what it is given; it cannot tell whether the original was transcribed correctly.

## Content Checks

`build` and `validate` return structured `checks` (`{code, severity, path, message}`). Error-level checks fail the build:

| code | report | document | Meaning and action |
| --- | --- | --- | --- |
| `dangling_caption_reference` | error | error | Reference target does not exist; use the available reference locators listed in the message, which may include legacy locators different from the displayed numbers |
| `dangling_source_reference` | error | error | `[n]` exceeds the source list; correct the reference or source |
| `table_row_wider_than_columns` | error | error | Extra cells would be lost; repair the table |
| `table_row_narrower_than_columns` | warning | warning | Missing cells render blank; check original data |
| `table_consider_landscape` | warning | warning | Table cannot fit at normal portrait size; consider landscape. With a stated size or `text_scale: large` the table is not shrunk either, so cells wrap |
| `font_not_found` | warning | warning | A stated font is not installed on this machine: the name is written as given, its display is unconfirmed and readers without it get a silent substitute. Ask the user for the font or for permission to use another |
| `fixed_line_spacing_tall_inline` | warning | warning | A paragraph under a stated fixed line spacing holds an inline formula taller than the line; to keep it whole (WPS cuts it off) that paragraph was given "at least" the stated value, the other paragraphs keep the fixed value. Tell the user, or make the formula a display equation |
| `chapter_header_may_not_fit` | warning | warning | With the stated margins the longest chapter title may wrap to a second header line and reach past the top margin; Word then pushes that page's text down. Check the page in Word; raise `margin_top`, shorten the heading or turn the header off |
| `table_compact_layout_ignored` | warning | warning | Obsolete compact flag; remove it, sizing is automatic |
| `manual_numbering_in_title` | warning | warning | Author numbering conflicts with `auto`; use `none` when it belongs to the original |
| `unparsed_inline_markdown` | warning | warning | Unpaired markers remain literal, or a link has an unsupported target; preserve original characters, escape literal stars or repair intended formatting; a lone `__` needs its pair for bold, while three or more underscores are a literal fill-in blank and never warn; use current display numbers such as 表 1 / 表 1.1 for exhibit references |
| `unsupported_list_numbering` | info | info | Under `list_numbering: author`, a Markdown line looks like list numbering but is not one of the six supported forms, or is indented; it is kept as a paragraph without native numbering and will not renumber in Word. Rewrite it flush left in a supported form if it should renumber; leave it if it is not a list or the original must be kept. Never fails `--strict` |
| `caption_reference_renumbered` | warning | warning | Undeclared Markdown's table reference changes target under new counting; inspect both targets before declaring the rule |
| `legacy_official_reference` | info | info | A legacy chapter locator was resolved to the intended object and displayed with its new number |
| `caption_number_replaced` | info | info | Supplied caption number differs from generated number; check fidelity |
| `table_missing_caption` | warning | info | Uncaptioned table consumes no number, enters no table list and cannot be referenced by table number; add a separate caption only if those functions are needed |
| `figure_missing_caption` | warning | info | Figure has neither caption nor alt text |
| `unreferenced_caption` | warning | info | Captioned table/figure has no body reference; introduce it in the prose with “见表/图 x.x” or a sentence that leads to it |
| `caption_before_reference` | warning | warning | Table/figure occurs before its first numbered introduction. A warning in ordinary documents too; when transcribing an existing document, do not move or rewrite the original to clear it — say in your delivery note that the order follows the original |
| `positional_caption_reference` | warning | info | Position-based exhibit wording such as 上图/下表/如下表所示/见上表: it points at the wrong exhibit as soon as one moves to another page or is added or removed. New reports reference the displayed number instead (“见图 x.x”“表 x.x 中”, or 表 1). Only clear phrases are matched, and a document with no table and no figure is not checked |
| `checklist_like_bullet_items` | warning | info | Three or more bullet items start with status labels |
| `section_reads_like_checklist` | warning | info | Many list items with no explanatory prose |
| `flat_section_structure` | warning | info | Large chapters without subsections; the TOC follows heading levels, while numbering depends on `heading_numbering` |
| `mechanical_section_nesting` | warning | info | Most level-1 chapters hold a single level-2 section, as if spread out to fill pages; merge them into fewer chapters, each with several level-2 sections |

`manual_numbering_in_title` is suppressed by `heading_numbering: none`; unpaired-marker warnings are not. For new reports, resolve errors and warnings before delivery. In ordinary-document transcription, do not add or rewrite original text to clear `info`. It remains useful evidence when comparing with the original.

`build --strict` fails on warning-level checks and rendering warnings, including formula fallback or a requested figure/table list with no entries; `info` never fails it. It is intended for CI and batch pipelines; the default for a delivery is to iterate until `checks` and `warnings` are clean. An interrupted or skipped figure-settling pass puts a warning in top-level `warnings` without failing strict mode. Read both `checks` and `warnings`, not just `ok`.

`qa` is separate: it checks package structure, fields, links, styles and font declarations. Its output explicitly says `check_scope: structure_only`, `original_content_consistency: not_checked`, and `original_layout_consistency: not_checked`; read `scope_notice`. Passing QA does not mean the text matches an original, the layout matches an original, or the document is ready to deliver. It does not cancel build checks.

`docx-kit components` prints the full machine-readable component contract.

`docx-kit sync-skill` mirrors the packaged skill into the machine-installed copies (`~/.claude/skills/docxkit`, `~/.agents/skills/docxkit`; only roots that already exist) and prints `{ok, command: "sync-skill", source, synced, skipped, errors}`. Updated skill files take effect in the next session; do not re-read the skill or upgrade the CLI in the middle of a build and revision loop.

## When a Build or Check Fails

| Situation | Action |
| --- | --- |
| Validation or build errors | Fix the named field, line or missing asset in the source. Do not patch the generated Word file. |
| `the document is empty…` | The input has no title and no content; write at least a title or some text. |
| The receipt shows a report where a plain document was meant (or the reverse) | The text has chapter headings and no `document_mode`, or none and you wanted a cover: write `document_mode` explicitly. |
| `dangling_caption_reference` | Check the available reference locators listed in the message and the effective numbering policy. Some locators support old input and differ from the displayed number. Opening sections count as chapters when chapter numbering applies. |
| `caption_reference_renumbered` | Compare the old and new target named at each location. Correct the source reference to the intended object before declaring `native-v1`. |
| `… is not available yet` / `这一版还不能用` | The setting or container belongs to a later version than the installed binary (a binary from before page position says this for `page_position`). Update the binary, or remove it and tell the user that this part cannot be done with this installation; do not imitate it. |
| `theme.format.page_position must be top or center` | Only `top` and `center` exist; there is no third position (a third of the way down, half a page). |
| `页边距写带单位的毫米或厘米` / `theme.format.margins…` | A margin without a unit or in another unit; or margins that leave too small a text area, or that collide with the chapter header or the page number. The message names the edge and the smallest value that works. Tell the user when the margin they asked for cannot be built; do not pick another margin for them silently. |
| `…width: … is wider than the text area` | A figure width stated in millimetres does not fit between the stated margins. Use the width the message gives, or a percentage. |
| `--settle-figures is not available together with stated page margins yet` | Build without `--settle-figures`, or without the margin keys. |
| `chapter_header_may_not_fit` | Open the page in Word. If the header wraps, raise `margin_top` to the value in the message, shorten the heading, or set `chapter_header: false`. |
| `redline needs both drafts to have the same page margins` | Build the two drafts separately, or give both drafts the same margins. |
| `fixed line spacing … is smaller than the … size` | Use a fixed value of at least the size, or write the spacing as `at-least …`. Do not change the user's size. |
| `font_not_found` | The stated font is missing here. The document names it anyway. Ask the user to install or supply it, or to accept another font; say so in the hand-over if you deliver. |
| `--embed-fonts cannot embed the stated font …` | Only the templates' own fonts can be embedded. Tell the user; do not drop the option or change the font on your own. |
| `留白要写在…` / `…留白没有东西可以附着` | The `::: 留白` directive is not in front of an ordinary paragraph (or between an ordinary paragraph and the table after it). Move it; do not replace it with blank lines. |
| `…的栏里只能放普通段落` | A `::: 并排` pane contains a heading, list, table, figure or another container. Move that content outside the block. |
| `redline cannot show a changed side-by-side block yet` / `… a change of paragraph spacing yet` | Build the two drafts separately, or keep that block and that spacing identical in both drafts. |
| `unsupported_list_numbering` | Only under `list_numbering: author` (the default for a kaiti or song ordinary document). The named line looks like numbering but is not a supported form, or is indented; it was kept as text and will not renumber in Word. It is `info` and does not block a strict build. In new writing, rewrite it flush left as `1.`, `（1）`, `1、`, `一、`, `(1)` or `（一）` if it is a list; if it is not one (exam options `A. … B. …`) or a transcription must keep the original numbering, leave it. |
| `legacy_official_reference` / `caption_number_replaced` | Informational compatibility and renumbering notices; read them, but do not change an original merely to clear them. |
| Punctuation or spaces changed unexpectedly (`text_normalization.applied: true`) | Add `punctuation_mode: preserve`. |
| Formula rendered as plain text | Correct the LaTeX or use valid native OMML from the source. Check top-level `warnings` as well as `checks`. |
| Figure settling skipped or stopped | Inspect `figure_settling` and warn the user; this warning alone does not fail strict builds. A moved figure still needs a reading-order review. |
| QA fails | Rebuild from source. If it still fails, report the QA result as a tool issue. |
| A command or option is absent | The installed binary is older than this contract. The CLI is updated once at session start (`npm install @dztabel/docxkit@latest`, fail-soft, see `SKILL.md`), never in the middle of a build and redline loop; if it is still missing, report the local capability gap. Do not silently produce a report when a plain document was requested, and do not fall back to generating the Word file another way. |

`docx-kit build` takes `--embed-fonts` when recipients lack the template's fonts and the locally available fonts allow embedding; fonts are otherwise not embedded.

## Machine-Readable Results (cli-contract 0.2)

`build-result.json`, `redline-result.json`, and `qa-result.json` carry `contract_version: "0.2"`; stdout matches the persisted result file for these commands. `render-copy` instead returns its receipt only on stdout.

- All paths in results (`input_path`, `output_dir`, `report_path`, `docx_path`, `artifacts.*`) are absolute. Pass `--filename <name.docx>` to `build`; it accepts a file name only, not a path. `docx_path` is the single authoritative Word deliverable and must not be copied or renamed by the agent.
- `build` and `validate` results carry `input_sha256`: the SHA-256 of the exact input bytes that were parsed (a successful result always has a real 64-hex digest; an unreadable input leaves it empty). `redline` and `error` results keep it empty instead of fabricating one.
- `docx-kit pdf` prints its own object (see "PDF"), described by `schemas/cli-pdf-result.schema.json` in the CLI repository; it carries no `contract_version`.
- `qa` results carry `docx_sha256` and `report_sha256`, computed from the same bytes the structural checks inspected; a passing QA always has both digests.

- `effective_document` on build/validate/redline describes the actual `template`, `document_mode`, `title_block`, `cover`, `toc`, `chapter_header`, `page_numbers`, `heading_numbering`, `list_numbering`, `caption_numbering` (`chapter` or `continuous`), and `punctuation_mode` (`normalize` or `preserve`). `page_numbers` is `always`, `none` or `auto` (`auto` does not say whether a number is currently shown); `list_numbering` is `template` or `author`. These are the values the build used, whether written or defaulted. It is null when no usable model is available; on redline it describes the new side.
- `effective_document.format` is present when the document is `format-v1`: when it states a format, margins or a page position, or uses the `::: 表格` options, `::: 留白` or `::: 并排`. It carries `format_rule` (`format-v1`), `text_scale`, and per role (`title`, `body`, `heading1` …) the `requested` values as normalised and the values in effect: `font`, `latin_font`, `size_pt`, `line_spacing` (`rule` `exact` / `at_least` / `multiple`, `value`), each with a `*_source`: `stated`, `template`, `text_scale`, `body_size`, `text_scale+body_size`, `body_font`, `body_latin_font`, `role_size` (a heading's line pitch derived from its own stated size), or `higher_heading` (a derived heading size held down to the size of the level above it). `font_installed` / `latin_font_installed` appear for stated fonts; `false` means this machine could not confirm the display. `derived` gives the values that follow the body: `first_line_indent_pt`, `small_text_size_pt`, `table_text_size_pt`, `caption_size_pt`, `code_size_pt`, `toc_entry_line_pt`, and `tables_shrink_to_fit` (true only when a table was actually set in the compact size because it did not fit at the normal size; always false for the table looks, which never shrink, and once a size is stated). `page` appears only when stated margins differ from the template's: `margin_top_mm` / `margin_bottom_mm` / `margin_left_mm` / `margin_right_mm` with a `*_source` each (`stated` or `template`), the text area of portrait pages (`text_width_mm`, `text_height_mm`) and of landscape pages (`landscape_text_width_mm`, `landscape_text_height_mm`), and `figure_max_width_mm` / `figure_max_height_mm` — a figure without a width is drawn `figure_max_width_mm` wide, and no figure is taller than `figure_max_height_mm`. `page_position` appears only when the body pages are centred, with the value `center`. It is a snapshot for checking; the settings themselves live in `report.json` under `theme.format`.
- `docx-kit templates` reports under `format` the stated-format capabilities of this binary: `rule`, `features` (only what is built), `text_scale`, `role_settings`, `size_names` and `line_spacing` forms, `table` (the container name, its options and their values), `spacing` (the directive and its three levels), `parallel` (container, column separator, options, and `keep_together_lines`, the limit under which a block is not split), `margins` (the four keys and the units) and `page_position` (the key, its two values and the default); each template lists its `format_roles`.
- `automatic_structure` records this import's changes: `document_title_from_first_h1` consumes the first ordinary-document heading as its title; `section_from_document_title_or_body` and `document_title_from_section_or_default` describe report-mode fallback structure; `document_mode_document_without_chapters` says that `document_mode` was not written and the content has no chapters, so it was built as an ordinary document (a source with chapters built as a report records nothing). It is empty when none was added, including JSON rebuilds that already contain the resolved model. Ordinary documents never gain a synthetic chapter.

- `text_normalization` reports actual emitted-text changes: `mode`, `applied`, `changed_characters`, `punctuation_replacements`, `removed_spaces`, and `scope: emitted_text_including_field_caches_and_revisions`. Every replaced punctuation character and every removed ASCII space counts as one; `changed_characters` is their sum. `applied` is true only when something changed. Repeated text in a TOC cache is counted again; redline includes both sides using each side's own policy. Discarded layout attempts do not inflate the counts. Pure `validate`, `render-copy` and failures before rendering return null. Counts cover generated text, not future Word field updates.
- With only the paragraph `甲,  乙: 丙.`, the default receipt reports 3 punctuation replacements, 3 removed spaces, and 6 changed characters. Preserve mode reports zero changes and `applied: false`.

Any upstream system can verify what was built by comparing these digests against its own copy of the input and artifacts.

## Direct report.json

Use direct `report.json` only when Markdown cannot express the required structure — the compatibility blocks listed below, a figure width — or when you are revising a `report.json` that already exists. Column widths no longer need it: write them with `::: 表格 widths=…` (in JSON, `widths` holds the same relative weights). Run `components` for component fields and usage guidance.

`report.json` is a strict contract: unknown properties, invalid enum values, null object/array fields, and non-empty `appendices` fail validation instead of being ignored.

The `report.json` that `build` persists alongside the named Word deliverable omits content fields equal to their defaults (empty strings/arrays, `emphasis: "normal"`, `language: "zh-CN"`, …) — a paragraph is just `{"type": "paragraph", "text": "…"}`. Layout settings are the exception: `layout_rule`, `numbering_rule` and a complete `theme` (`template`, `document_mode`, `cover`, `toc`, `chapter_header`, `page_numbers`, `heading_numbering`, `list_numbering`, `list_of_figures`, `list_of_tables`, `punctuation_mode`) are always written with the values the build actually used, including `false`, `none` and the default template, so a later rebuild does not depend on defaults. Reading is unchanged: omitted fields deserialize to the same defaults, and the slim form round-trips losslessly — section titles and table/figure/equation captions are stored as written, inline markers included, so rebuilding from `report.json` any number of times gives the same content and formatting. Selective inline emphasis inside a paragraph is expressed with the inline markers above (e.g. `"text": "弃电率为 **16.6%**。"`), not a separate runs structure.

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
- Top-level `layout_rule`: `layout-v1` or `legacy-v0`, independent of `numbering_rule`. It records which generation of layout defaults fills in theme settings that are not written out. JSON without it is read as `legacy-v0` and saved back with an explicit `legacy-v0`; Markdown builds persist `layout-v1`. The two differ only for what is not written: under `legacy-v0` a missing `theme.document_mode` means `report` (`document` on the official template) and every mode has `heading_numbering: auto`, `list_numbering: template`, `page_numbers: always`; under `layout-v1` a missing `theme.document_mode` is decided by the content (`report` if any section is a chapter, i.e. `kind: section`; `document` if there are only `kind: body` containers; still `document` on the official template) and a kaiti or song `document` defaults to `none`, `author`, `auto` as in the table under "Metadata". A file that `build` wrote spells out every setting, so it rebuilds the same under either rule. Do not add or change this marker in an existing file; hand-written JSON that wants the new defaults must say `"layout_rule": "layout-v1"`.
- `theme.document_mode`, `theme.heading_numbering` and `theme.punctuation_mode` match the Markdown options. Omitted `punctuation_mode` means `normalize`; use `preserve` for transcription.
- `theme.cover`, `theme.toc`, `theme.chapter_header`, `theme.page_numbers` and `theme.list_numbering` match the Markdown options and follow the same rules. Hand-written JSON may omit them to get the defaults of its `layout_rule` and mode.
- `paragraph.space_before` and `paragraph.space_after` (0–3, body lines) are what `::: 留白` compiles to; the directive itself is not stored. Right-aligned paragraphs that follow one another form a group (Word sets them without space between them only while they share one style), so every paragraph of a group carries the same `space_before` and the same `space_after`: a level on only part of a group is a validation error. A following right-aligned paragraph with another non-zero `space_before` starts a new group. A `parallel` block has `panes`, exactly two, each `{"blocks": [...]}` holding `paragraph` blocks only (with optional `alignment` and `space_before`), and an optional `widths` of two relative weights. All of them need top-level `format_rule`; default values are omitted and do not rename bookmarks. Build receipts count the paragraphs inside panes as paragraphs; there is no separate count for parallel blocks.
- `table.appearance` (`three-line` / `grid` / `borderless`), `table.header` (boolean) and `table.spacing` (`normal` / `roomy` / `extra`) match the container options; a table that uses any of them needs top-level `format_rule`. With `header: false`, `columns` is an empty array and `rows` holds every line, the first included, all of equal length. `widths` and `alignments` are the existing fields. Default values are omitted and do not rename bookmarks.
- Top-level `format_rule: format-v1` and `theme.format` exist only when a format is stated. Markdown authors never write `format_rule`; a build writes it together with the normalised settings as soon as one stated-format key is used. `theme.format` holds `text_scale` and, per role, `font`, `latin_font`, `size_pt` (points) and `line_spacing` (`{"rule": "exact" | "at_least" | "multiple", "value": …}`); only what was stated is stored, and the derived values are recomputed by the fixed `format-v1` table on every build. JSON with `theme.format` but no `format_rule` is rejected. A document that states no format has neither key, and its report.json, Word file, receipt and bookmark names are what they were before these settings existed. Stating a value equal to the template's, or `三号` instead of `16pt`, does not rename bookmarks; an actual change of format does.
- `theme.format.page_position` is `top` or `center`, as written; it needs `format_rule` like the rest of `theme.format`. `top` is stored when written and changes neither the Word file nor the bookmark names; `center` renames bookmarks, like any real change of format.
- `theme.format.margins` holds the stated page margins in millimetres: `top_mm`, `bottom_mm`, `left_mm`, `right_mm`, each from 0 to 150, only the edges that were stated. It needs `format_rule` like the rest of `theme.format`. The values are what the author wrote (`2.5cm` is stored as `25`); margins equal to the template's are stored too, and change neither the Word file nor the bookmark names. With stated margins a `figure.width` in millimetres may be as wide as the text area and is an error beyond it; without them it is limited to 160 mm as before.
- `sections[0].kind: body` stores ordinary-document content before any section, without creating a heading. It is allowed only as the first container in document mode, with an empty title and level 1. Other containers are `section` (default). A title-only ordinary document may have an empty sections array; on the kaiti and song templates under `layout-v1` a document with no title and no content is an error.
- `table`/`figure` blocks may carry `caption_number`, recording the supplied number without overriding automatic numbering.
- `ordered_list.list_id`: equal nonempty IDs continue one instance, different IDs restart at 1; an omitted/empty ID retains historical document-wide list numbering. Markdown supplies these IDs automatically.
- `ordered_list.list_format` and `ordered_list.list_start`: the written form and the start number of a list kept as the author wrote it; only under `theme.list_numbering: author`. Omitted means the template's numbering from 1. See "Lists Numbered as Written".

Documents generated from different inputs never share bookmark names, so a chapter copied from one into another keeps its own references. Copies of the same document share names, as copies of any Word document do. Saving the layout settings explicitly does not rename anything: a rebuild from the persisted `report.json` has the same bookmark names as the build that wrote it.
