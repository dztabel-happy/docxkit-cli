# Forms, stated formats and page layout

For a handwritten form start with a Song-template document and a headerless grid. The separator row is required even when the first row contains data. The minimum row height applies to every body row.

```markdown
::: 表格 appearance=grid header=false row_height=11.7mm
| **姓名** | |
| --- | --- |
| **电话** | |
| **签字** | |
:::
```

Use the table options below for merges and column widths, the alignment and spacing sections for seals or signatures, and the role settings for specified fonts, sizes and margins.

## Table options

A pipe table on its own has a bold, repeating header. When `appearance` is not written, a table's look follows its structure on every template, the 公文模板 included: a table with a header row is a three-line table, a table without one (`header=false`) is a grid; a written `appearance` always wins. Write `appearance=grid` for a form to be filled in, and `appearance=borderless` for aligned blocks and signature areas. To give one table another look, put it in a container: a line `::: 表格` with options, the table, and a line `:::`. A caption, when there is one, goes inside, on the line directly above the table. The options apply to that table only.

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

A form with merged cells and a minimum row height. A cell that is exactly `<` joins the cell on its left, a cell that is exactly `^` joins the cell above; the top-left cell of the merged region holds the text (it may be empty). Here the photo box spans three rows of the last column — 25 mm wide and 3 × 11.7 mm, about 35.6 mm, high — and the address and remark values span the rest of their lines:

```markdown
::: 表格 appearance=grid header=false row_height=11.7mm widths=26,41,26,42,25
| **姓名** |  | **性别** |  | 贴照片处 |
| --- | --- | --- | --- | --- |
| **出生日期** |  | **民族** |  | ^ |
| **联系电话** |  | **邮箱** |  | ^ |
| **现住址** |  | < | < | < |
| **备注** |  | < | < | < |
:::
```

| Option | Values | Meaning |
| --- | --- | --- |
| `appearance` | `three-line`, `grid`, `borderless`; not written: by structure | `grid` draws every line (0.5 pt); `borderless` draws none, for option lists or aligned blocks; `three-line` draws the top and bottom rules and the header rule (without a header only the top and bottom rules). Without `appearance`: three-line with a header row, grid with `header=false`, on every template |
| `header` | `true` (default), `false` | `false`: the table has no header. The line above the `---` separator line is then data like every other row: it is not bold, nothing repeats across pages, nothing is dropped, and you do not invent column names. The separator line is still required syntax |
| `spacing` | `normal` (default), `roomy`, `extra` | Room above and below the text in every cell: 5, 12 or 24 pt (rows about 9.5, 14.5 and 23 mm high on the default template in Word; on `normal` about 10.3 mm in LibreOffice). Use `roomy` or `extra` for cells to be written in by hand. Rows still grow with their text; for a minimum height use `row_height` |
| `row_height` | `5mm` to `100mm`, or in `cm`, written like a page margin | Every body row (not the header row) is at least this tall, the `spacing` room included; the text stays centred vertically, and a row whose text needs more still grows, so nothing is cut. A value below the row's natural height (one line on `normal` spacing: about 9.5 mm in Word, 10.3 mm in LibreOffice) changes nothing, and a row comes out about 0.2 mm taller than the value (its line). Usually 11.7–14 mm for a line written by hand, 15–17 mm for a signature. A cell merged down n rows is as tall as those rows: three rows of `11.7mm` make a 35 mm photo box. One value per table: there is no height for a single row and no exact height, so a taller signature row is a table of its own |
| `widths` | positive numbers, one per column | Relative column widths, `widths=1,2,1,2`. Without it the columns are equal. Weights that add up to the text width in millimetres are exact widths (see below). Units are refused (`widths=30mm,50mm`, `40%`): the error says they are relative weights and gives the numbers without units |
| `alignments` | `left`, `center`, `right`, one per column | Per-column alignment of the cell text. Default is centred |
| `layout` | `normal` (default), `landscape` | `landscape` puts the table on a landscape page, like `表[landscape]：`. If the caption bracket and this option are both written they must agree |

Rules for a table that uses `appearance`, `header=false`, a `spacing` other than `normal`, merged cells or `row_height`:

- Columns are equal, or follow `widths`, across the full text width. Widths are not guessed from the content, and the text is never shrunk to make a table fit: a long cell wraps and the row grows. A column of long English identifiers, codes or URLs needs more weight in `widths` (for example `widths=3,1,1,4`); otherwise such a word is broken inside wherever the column ends. A column too narrow for one character is an error that names the table and the column; give it more weight, use `layout=landscape`, or split the table.
- Every row must have the same number of cells; write an empty cell as `|  |`. An empty cell stays empty, a place to write.
- A three-line table with `header=false` has only its top and bottom rules. A grid or borderless table with a header still has a bold header that repeats on every page.
- `widths` are weights that fill the text width, so millimetres adding up to the text width give exact column widths: 160 mm on the kaiti and song templates, 159.2 mm on the 公文模板, and with stated margins 210 minus the left and right margins (the receipt's `effective_document.format.page.text_width_mm`). A 25 mm photo column on the song template: `widths=22,35,22,35,21,25` (sum 160).
- Merged cells: a region w columns wide and h rows high is written one way only — its top-left cell (the anchor), then w−1 cells of `<` in the same row, and in each of the h−1 rows below, `^` in all w of its columns. Regions are rectangles and do not overlap. The first cell of a row cannot be `<` and the first row cannot have `^`.
- The header row takes no part in merging: with a header, the header row has no `<` and the row below it no `^`. A form is written with `header=false`, its labels in `**粗体**`.
- Merged text takes the alignment of the anchor's column; a merged cell is as wide as the columns it spans. The rows joined by a vertical merge are kept on one page (not guaranteed for a region taller than a page).
- A cell that is exactly `\<` or `\^` prints a literal `<` or `^`; these escapes apply only to a whole cell inside the container. Outside a container a cell of `<` or `^` is printed as written, nothing is merged, and the warning `merge_marker_outside_table_container` says so.
- One table has one column structure. A row that needs other columns — an 18-box ID number under a six-column form, a signature block — is a table of its own directly after, with its own `widths` and `row_height`; an empty line separates the two tables.
- Merged header cells and slanted header cells cannot be made.

Errors, each with the line number: an empty container; a caption without a table; more than one table, or anything other than the table and its caption, in one container; an unknown, repeated or badly formed option (`key=value`, no spaces around `=`); a wrong number of `widths` or `alignments`; rows of unequal length; a `row_height` without a unit or outside 5–100 mm; a caption written above the container instead of inside it; a container that is not closed. Merge errors also name the cell (counted from 1), the rule broken and how to fix it: a `<` in the first cell of a row; a `^` in the first row or directly under the header; a `<` or `^` in the header row; a `<` or `^` that does not join a rectangle (for example `第 14 行第 6 格：这里应该是 ^，上面第 11 行起的合并区域占第 5–6 格…`). Inside a code fence `:::` stays literal.

A document that uses the container is read under `format-v1` like the stated formats: the tool writes `format_rule` into `report.json`, and an older binary rejects the container; check `docx-kit templates` → `format.features` (`table_appearance`, `table_without_header`, `table_spacing`, and `table_merges`, `table_row_height` for merged cells and `row_height`). `redline` refuses when the same table has a different `appearance`, `header`, `spacing`, merged cells or `row_height` in the two drafts; with equal settings a changed table is shown as before.

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

- Inside a container the ordinary paragraph rules apply: a blank line separates paragraphs, and adjacent non-blank lines join into one paragraph (see [punctuation and spaces](docx-markdown-contract.md#punctuation-and-spaces) for the space at the join). **A two-line sign-off therefore needs a blank line between the organisation and the date**, as above; without it the two lines become one paragraph.
- Adjacent right-aligned paragraphs sit directly under each other, and the group keeps one line of space from what precedes it. Do not add empty paragraphs or spaces to position text.
- **A right-aligned group of up to a third of the page is not split across pages, and it stays on the page of the paragraph before it** (as built, a sign-off does not stand alone at the top of a page): every paragraph of the group except the last keeps with the next, each is kept in one piece, and when the block before the group is a paragraph or a list, its last paragraph keeps with the group too. For keeping together, right-aligned paragraphs that follow one another count as one group even where a `::: 留白` of another level stands between them (which starts a new spacing group, see below). After a table nothing is tied (a table's last row never keeps with what follows); inside a `::: 并排` pane nothing is tied either. Only paragraphs written right-aligned (`::: 靠右`, `"alignment": "right"`) form a group; nothing is guessed from the wording.
  The keep is Word's "Keep with next" (与下段同页): inside the group it is set on the paragraphs; the paragraph before the group gets it from a style of its own, its style plus "·与下段同页" (body text: `正文·与下段同页`), based on that style and followed by it — so a paragraph the user starts with Enter at its end is ordinary body text, and what is written before the sign-off in Word or WPS does not pile up into a block that jumps to the next page; the paragraphs added that way are not tied to the group, so the group can then start a page on its own, still in one piece.
  The limit is the one for short tables: the group's estimated height — its lines (wrapped lines counted) times the body line, plus its space before and after, `::: 留白` included — is at most a third of the text height of the page. That is ten one-line paragraphs with no space between them in `executive-cn-docx` and `executive-cn-song-docx`, six in `executive-cn-official-docx` (the line of space above the group counts); a sign-off of an organisation, three lines of space for a seal and a date fits in all three. A taller group (a long list of signatories, say) is not tied at all: like body text it continues at the foot of the page and runs on to the next, so its last lines may start that page; each of its paragraphs is still kept in one piece, and the paragraph before it does not keep with it.
- Only ordinary paragraphs are allowed inside, with the usual inline markers. A heading, table, list, quote, callout, code block, image, page break or another container inside one is an error — also when it stands directly under a line of text, where it is not read as a continuation of that paragraph — as are an unknown name (`::: 落款`), a container that is never closed, an empty container and a stray closing `:::`. Each error names the line number; nothing is printed as text. Inside a code fence `:::` stays literal.
- The names describe the shape only (flush left / right / centre); there are no "salutation" or "signature" components, and no trailing-attribute syntax.
- In `report.json` the same thing is `"alignment": "left" | "right" | "center"` on a `paragraph` block (`normal`, the default, is omitted). An aligned paragraph must keep `emphasis: normal`; combining it with `lead` or `small` fails validation.
- Binaries older than this feature print the `:::` lines as text. Use `docx-kit components paragraph` to check for `alignment`.

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

Errors, each with the line number, never silently dropped: a value other than the three levels; two directives in a row (use `三行`; levels do not add up); a directive at the end of the file, before a heading, next to `---PAGE---`, between two tables or two other blocks that are not paragraphs, at the end of a pane, or inside an alignment container. A directive standing between two `::: 靠右` paragraphs at the level the group above already has (also `一行` after a right-aligned group with no directive, since such a group already stands one line lower) is an error too: adjacent right-aligned paragraphs form one group with no space inside it, so the directive would do nothing — to leave room under each of several signature or seal lines, write them as a borderless table with a row height (`::: 表格 appearance=borderless header=false alignments=right row_height=16mm`, one line per row), as a `::: 并排` block, or put each line in its own `::: 顶格` with its own directive; a directive of another level starts a new group and is kept.

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

## Stated Formats and the Type Scale

Use these only when the user states a format ("正文仿宋三号，行距固定 28 磅", "标题二号小标宋", "字大一点"). A paragraph style of its own, a size or line spacing for one paragraph, character spacing, paper other than A4, gutters and mirrored margins cannot be stated. They change the chosen template; they do not replace choosing one. Without them a document is built exactly as before.

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
| `body_latin_font` | The whole document, including the roles above, list numbers and page numbers. | A role with its own `<role>_latin_font`; code; the 公文模板's page numbers (宋体, GB/T 9704). |
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
| `<` and `^` cells, `row_height` in `::: 表格` | `table_merges`, `table_row_height` |
| `::: 留白` | `paragraph_spacing` |
| `::: 并排` | `parallel` |

The same output has `rule: format-v1`, the roles each template accepts (`format_roles`), the size names, and the options of the table container, the spacing directive and the side-by-side block. Plain documents decided by structure, alignment containers and lists as written are older than `format.features`: `templates` reports them as `by_structure`, and `docx-kit components` lists `alignment` on the `paragraph` component.

`redline` needs both drafts to have the same effective format, the same page margins and the same page position, and refuses otherwise, naming the differences; `三号` and `16pt`, `30mm` and `3cm`, or a value equal to the template's, count as the same. When one draft has landscape table pages that the other lacks, Word restarts the page numbers at 1 in the section after those pages once all revisions are accepted or rejected — or, when those landscape pages end the kept draft, on the landscape pages themselves; Word cannot record taking a page-number restart away as a revision. To keep that file, set the page numbering of that section (the one that follows the landscape pages, or the landscape pages at the end) to continue from the previous section (Insert → Page Number → Format Page Numbers → Continue from previous section); that one setting is enough. Otherwise use the document rebuilt from the kept draft's source. `--embed-fonts` embeds only the templates' own fonts and Times New Roman: with any other stated font it fails and says which, and the option is not dropped for you.

The build receipt reports what was applied under `effective_document.format` (see [receipt fields](diagnostics.md)).

## Page margins

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

**What the values mean.** They name the physical edges of every page: cover, contents, body, landscape table pages and the portrait pages after them. A landscape page does not rotate them: `margin_top` is the top of that page as it is read. An edge that is not written keeps what the page had: the template's margin on portrait pages (kaiti 18 mm top and bottom, 25 mm left and right; song 25 mm all round; official 25.4 mm all round) and 18 mm on landscape pages. The header and the page number stay 12.7 mm from the edge of the paper (on the 公文模板 the page number follows the bottom margin instead, see below).

**What follows the margins.** Everything laid out to the text width follows the new text area: body text and lists; the page numbers at the right edge of the contents and of the lists of figures and tables (also after "update entire table" in Word); every table — plain pipe tables, the table looks, side-by-side blocks, landscape tables; callouts and code blocks; display equations and their numbers; figures. A figure without a width fills the text width, a percentage is of the new text width, and the tallest a figure may be moves with the height of the text area. On the 公文模板 the page number moves with the bottom margin: its line stays 7 mm below the text area. Type sizes, indents and line spacing do not change.

**Equal to the template is the same as not written.** When every written value equals the template's own, the Word file and the bookmark names are exactly those of a document without margins. `30mm` and `3cm` are the same value. As soon as one edge differs, every written edge counts on every page: with `margin_top: 30mm` and `margin_bottom: 25mm` on the song template, landscape pages get a 25 mm bottom margin instead of their own 18 mm.

**Refused, with the reason and what to change.** DocxKit does not move a stated margin and does not shrink a figure whose width is stated.

- Left and right margins that leave a text area narrower than the template's deepest list indent plus ten characters, or top and bottom margins that leave fewer than ten body lines; the message gives the widths in millimetres. Landscape pages are checked only when the document has one.
- With a cover, top and bottom margins that leave a text area shorter than the cover needs (about 150 mm): the cover would run onto a second page. Reduce them, or set `cover: false`.
- A top margin under 16.9 mm while the chapter header is on, or a bottom margin under 17.6 mm while page numbers are on: the header and the page number each take one line 12.7 mm from the paper edge. On the 公文模板 the page number follows the text area instead (its line 7 mm below it), so the bottom margin must be at least 17 mm: 7 mm, one line, and 5 mm below it. State a larger margin, or `chapter_header: false` / `page_numbers: none`.
- In JSON, a figure whose `width` is given in millimetres and is wider than the text area. Use a smaller width or a percentage.
- `--settle-figures` together with stated margins: figure settling does not measure the new geometry yet.

When the longest chapter title may not fit in one header line of the new text width, the build succeeds with the warning `chapter_header_may_not_fit`. This is an estimate: if the header does wrap in Word, Word pushes the text of that page down, so the top margin is no longer the stated one. Raise `margin_top` to the value the message gives, shorten the heading, or set `chapter_header: false`.

The build receipt gives the margins and the text area in effect under `effective_document.format.page`.

## Page position

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

**Refused.** `--settle-figures` together with `center` (it judges a page by the space under its last line). `redline` between drafts whose page positions differ.

The receipt has `page_position: center` under `effective_document.format` when the body pages are centred; without it they start at the top.

## Layout limits

- **Merged header cells, slanted headers, a height for one row, two column structures in one table.** A slanted header is not drawn: tell the user it can be added in Word or WPS.
- **More than two panes side by side, text flowing from one column into the next, and anything but paragraphs in a pane** (no list, table or figure).
- **Other spacing**: an amount in millimetres, more than three lines, space at the end of the file. **Keeping two blocks on one page**: a side-by-side block of up to 10 lines, a short table and a `::: 靠右` sign-off of up to about a third of a page stay whole by themselves (the sign-off on the page of the paragraph before it); anything else only with a `---PAGE---` before it.
- **Decoration and special looks**: rules between résumé sections, a sealing line, a page border; a clause lead-in (`第一条`) in a style of its own — write `**第一条**` if bold is wanted.
- **Pictures as page decoration, and pictures without a number**: a logo or picture in the header or footer, a watermark, a page background, a picture on the cover, a picture that must carry no number (a logo, a QR code, an ID photo). Tell the user, and suggest inserting such pictures in Word or WPS; do not fake them with python or another tool.
