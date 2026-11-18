# Authoring components in report.json

For a component index run `docx-kit components --list`. For its fields, item schema and example, query it by name, e.g. `docx-kit components checklist`.

## Direct report.json

Use direct `report.json` only when Markdown cannot express the required structure — the compatibility blocks listed below, a figure width — or when you are revising a `report.json` that already exists. Column widths no longer need it: write them with `::: 表格 widths=…` (in JSON, `widths` holds the same relative weights).

`report.json` is a strict contract: unknown properties, invalid enum values, null object/array fields, and non-empty `appendices` fail validation instead of being ignored.

The `report.json` that `build` persists alongside the named Word deliverable omits content fields equal to their defaults (empty strings/arrays, `emphasis: "normal"`, `language: "zh-CN"`, …) — a paragraph is just `{"type": "paragraph", "text": "…"}`. Layout settings are the exception: `layout_rule`, `numbering_rule` and a complete `theme` (`template`, `document_mode`, `cover`, `toc`, `chapter_header`, `page_numbers`, `heading_numbering`, `list_numbering`, `list_of_figures`, `list_of_tables`, `punctuation_mode`) are always written with the values the build actually used, including `false`, `none` and the default template, so a later rebuild does not depend on defaults. Reading is unchanged: omitted fields deserialize to the same defaults, and the slim form round-trips losslessly — section titles and table/figure/equation captions are stored as written, inline markers included, so rebuilding from `report.json` any number of times gives the same content and formatting. Selective inline emphasis inside a paragraph is expressed with the [inline markers](docx-markdown-contract.md#inline-formatting) (e.g. `"text": "弃电率为 **16.6%**。"`), not a separate runs structure.

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
- Top-level `layout_rule`: `layout-v1` or `legacy-v0`, independent of `numbering_rule`. It records which generation of layout defaults fills in theme settings that are not written out. JSON without it is read as `legacy-v0` and saved back with an explicit `legacy-v0`; Markdown builds persist `layout-v1`. The two differ only for what is not written: under `legacy-v0` a missing `theme.document_mode` means `report` (`document` on the official template) and every mode has `heading_numbering: auto`, `list_numbering: template`, `page_numbers: always`; under `layout-v1` a missing `theme.document_mode` is decided by the content (`report` if any section is a chapter, i.e. `kind: section`; `document` if there are only `kind: body` containers; still `document` on the official template) and a kaiti or song `document` defaults to `none`, `author`, `auto` as in the [metadata defaults](docx-markdown-contract.md#metadata). A file that `build` wrote spells out every setting, so it rebuilds the same under either rule. Do not add or change this marker in an existing file; hand-written JSON that wants the new defaults must say `"layout_rule": "layout-v1"`.
- `theme.document_mode`, `theme.heading_numbering` and `theme.punctuation_mode` match the Markdown options. Omitted `punctuation_mode` means `normalize`; use `preserve` for transcription.
- `theme.cover`, `theme.toc`, `theme.chapter_header`, `theme.page_numbers` and `theme.list_numbering` match the Markdown options and follow the same rules. Hand-written JSON may omit them to get the defaults of its `layout_rule` and mode.
- `paragraph.space_before` and `paragraph.space_after` (0–3, body lines) are what `::: 留白` compiles to; the directive itself is not stored. Right-aligned paragraphs that follow one another form a group (Word sets them without space between them only while they share one style), so every paragraph of a group carries the same `space_before` and the same `space_after`: a level on only part of a group is a validation error. A following right-aligned paragraph with another non-zero `space_before` starts a new group. A `parallel` block has `panes`, exactly two, each `{"blocks": [...]}` holding `paragraph` blocks only (with optional `alignment` and `space_before`), and an optional `widths` of two relative weights. All of them need top-level `format_rule`; default values are omitted and do not rename bookmarks. Build receipts count the paragraphs inside panes as paragraphs; there is no separate count for parallel blocks.
- `table.appearance` (`three-line` / `grid` / `borderless`), `table.header` (boolean) and `table.spacing` (`normal` / `roomy` / `extra`) match the container options; a table that uses any of them needs top-level `format_rule`. Without `appearance` the look follows the structure (three-line with a header row, grid with `header: false`) on every template, and report.json leaves it out; a written `three-line` is drawn as three-line on every template and, like a missing one, does not rename bookmarks. With `header: false`, `columns` is an empty array and `rows` holds every line, the first included, all of equal length. `widths` and `alignments` are the existing fields. `table.merges` lists the merged regions as `{"row": 0, "column": 4, "row_span": 4, "column_span": 1}`, counted from 0 in `rows` (never the header `columns`); the spans are positive and not both 1. A region must lie inside the table and not overlap another, and every cell it covers except its top-left one must be `""` or `null` — text is never dropped silently; the errors give the JSON path and the cells in conflict. Markdown writes the `<` and `^` cells as `""`. `table.row_height_mm` is the minimum body-row height in millimetres, 5–100, stored as written (`1cm` as `10`). Both need `format_rule` like the other looks. Default values are omitted and do not rename bookmarks.
- Top-level `format_rule: format-v1` and `theme.format` exist only when a format is stated. Markdown authors never write `format_rule`; a build writes it together with the normalised settings as soon as one stated-format key is used. `theme.format` holds `text_scale` and, per role, `font`, `latin_font`, `size_pt` (points) and `line_spacing` (`{"rule": "exact" | "at_least" | "multiple", "value": …}`); only what was stated is stored, and the derived values are recomputed by the fixed `format-v1` table on every build. JSON with `theme.format` but no `format_rule` is rejected. A document that states no format has neither key, and its report.json, Word file, receipt and bookmark names are what they were before these settings existed. Stating a value equal to the template's, or `三号` instead of `16pt`, does not rename bookmarks; an actual change of format does.
- `theme.format.page_position` is `top` or `center`, as written; it needs `format_rule` like the rest of `theme.format`. `top` is stored when written and changes neither the Word file nor the bookmark names; `center` renames bookmarks, like any real change of format.
- `theme.format.margins` holds the stated page margins in millimetres: `top_mm`, `bottom_mm`, `left_mm`, `right_mm`, each from 0 to 150, only the edges that were stated. It needs `format_rule` like the rest of `theme.format`. The values are what the author wrote (`2.5cm` is stored as `25`); margins equal to the template's are stored too, and change neither the Word file nor the bookmark names. With stated margins a `figure.width` in millimetres may be as wide as the text area and is an error beyond it; without them it is limited to 160 mm as before (on the 公文模板 to its text width, 159.2 mm).
- `sections[0].kind: body` stores ordinary-document content before any section, without creating a heading. It is allowed only as the first container in document mode, with an empty title and level 1. Other containers are `section` (default). A title-only ordinary document may have an empty sections array; on the kaiti and song templates under `layout-v1` a document with no title and no content is an error.
- `table`/`figure` blocks may carry `caption_number`, recording the supplied number without overriding automatic numbering.
- `ordered_list.list_id`: equal nonempty IDs continue one instance, different IDs restart at 1; an omitted/empty ID retains historical document-wide list numbering. Markdown supplies these IDs automatically.
- `ordered_list.list_format` and `ordered_list.list_start`: the written form and the start number of a list kept as the author wrote it; only under `theme.list_numbering: author`. Omitted means the template's numbering from 1. See [lists numbered as written](docx-markdown-contract.md).

Documents generated from different inputs never share bookmark names, so a chapter copied from one into another keeps its own references. Copies of the same document share names, as copies of any Word document do. Saving the layout settings explicitly does not rename anything: a rebuild from the persisted `report.json` has the same bookmark names as the build that wrote it.
