# Revising an Already-Generated Document

When the user is not satisfied with a `.docx` DocxKit produced and asks for changes — or wants a Word file with tracked changes showing what changed — this is fast and safe, **because the source of truth is the Markdown / `report.json`, not the `.docx`.** You never edit the Word file or its OOXML. You edit the source and rebuild; the gate loop re-validates automatically.

The user can also continue writing directly in Word/WPS. Agent rebuilds use Markdown or `report.json`; they do not import edits from the Word file. First establish which copy contains the latest content.

## The rule

- **Never hand-edit the generated `.docx`.** It is a derived artifact: a change made in its XML is lost on the next rebuild and cannot be merged back. For an agent revision, change the source and rebuild.
- For a file edited by the user in Word/WPS, reconcile those edits with the source before rebuilding. Do not overwrite them with an older source.
- Preserve the document's mode, title choice, numbering rule, punctuation mode and author-written clause numbers unless the user requests a change. A source that was built as a plain document stays one: if a revision adds chapter headings to a text that had none and declared no `document_mode`, write `document_mode: document`, or the rebuild becomes a report with a cover. Transcriptions keep `punctuation_mode: preserve`. A `report.json` already states every setting, so rebuilding it never changes the kind of document.

## Locating the source

1. Use the saved `content.md` if it is current.
2. Otherwise use `report.json`, which every successful build writes. Rebuild it with the same output filename.
3. If only a hand-edited `.docx` is available, reconstruct its content as source and compare it against that file. This is a new transcription, not an automatic merge — say so plainly to the user.

Headings and captions retain the source text in `report.json`. Keep escapes such as `\*` and code spans that intentionally protect literal characters. JSON strings require the backslash itself to be escaped (`"text": "Z\\*\\*\\*\\*\\*99"`). Switching to JSON does not bypass inline parsing.

A `report.json` written by docx-kit 0.1.62 or earlier stored headings/captions with markers removed. If it lost protective backticks, return to the Markdown or restore the intended literal text before rebuilding. Historical JSON without `numbering_rule` retains old reference lookup; do not change it to `native-v1` without checking every affected target.

## Common revisions

| Ask | What to change |
| --- | --- |
| Reword, correct a fact or shorten prose | Edit source paragraphs; preserve original text in a transcription unless asked to change it. |
| Add, delete or move a section | Edit headings and blocks. Recheck source reference numbers against the effective policy. Word edits can update native references, but a Markdown rebuild still parses the locators written in the source. |
| Add/drop a table, figure or source | Update the block and its prose reference together. In a report keep every captioned exhibit referenced in the text (avoids `unreferenced_caption`). Uncaptioned tables consume no table number. Ordinary documents do not require adding references merely to clear `info`. |
| Switch typography (楷体 / 宋体 + 黑体 / 公文模板) | Change `template:` while retaining the mode; the content is untouched. Recheck caption numbering: the 公文模板 numbers continuously, and a document without `document_mode` becomes a plain document there. Remove `####` headings before switching away from the 公文模板. |
| Keep the original clause numbers | In a plain document on the 楷体 or 宋体 template they are kept as written, in headings and in numbered lines (native lists). On the 公文模板 or in a report, set `heading_numbering: none` and `list_numbering: author`. Line-start `1\.` keeps a numbered line as an ordinary paragraph. |
| Add a chart | If ChartKit is installed, render the figure to `assets/*.png` (its `-manifest.json` beside the image sizes it), then reference it with `图：` — DocxKit places, numbers and cross-references it. Otherwise render a local image the same way. In a report, introduce it by number before the image. |

## Versioning

- **Overwrite** the same `--out ./output_docx`, with the same `--filename`, when the user wants the previous build replaced (the default).
- **Keep both** by building into a versioned sibling when the user may want to compare or revert, or wants the changes shown as tracked changes (`redline` needs the old source as well as the new one): copy the source into `./output_docx_v2/`, edit the copy, and build it with `docx-kit build ./output_docx_v2/content.md --out ./output_docx_v2 --filename 原交付文件名.docx`; the old folder keeps the old source and build.
- **Never overwrite a file the user has edited** in Word or WPS: reconcile their edits with the source first (see "The rule"), and build the result beside it rather than over it.

For a runnable example from the repository root:

```bash
docx-kit build examples/contract.md --out ./contract --filename contract.docx
docx-kit build ./contract/report.json --out ./contract_v2 --filename contract.docx
```

The second command rebuilds the saved model into a sibling folder. Edit a copy of the source before using this pattern for an actual revision.

## After every revision

Re-run the same gate loop as a first build: read build `errors`, `warnings`, `checks`, `effective_document` and `text_normalization`, fix at the reported `path` and rebuild until errors and warnings are clean (leave a warning only when the user explicitly wants that shape, or it is a `table_consider_landscape` whose table reads well as built, and say so); keep legitimate `info`. Run QA on the original generated document — for a redline document with the new draft's `report.json`, see below — and review the content/layout required by the task. QA checks structure only; it does not compare a transcription with its original. Return the authoritative `docx_path`, source path, and the review status.

For LibreOffice preview or conversion, create a `render-copy` after building. For a user-edited file, update fields and save in Word/WPS first. The render-only copy freezes displayed results without recomputation (only the page numbers of the contents are left for the renderer to compute) and is not the editable deliverable.

## Showing what changed (tracked changes)

To hand the user a Word file with tracked-changes markup of what changed between two versions you generated, use `redline`: it renders the new version with insertions and deletions marked, reviewable and acceptable in Word/WPS. It compares two DocxKit sources (Markdown or JSON), including ordinary documents and escaped literal text, so both versions' sources must be at hand; it is not for redlining an arbitrary uploaded `.docx`. For example, after preparing old and new source files:

```bash
docx-kit redline --from ./old.md --to ./new.md --out ./revision
```

`redline` always writes `redline.docx` and `redline-result.json` into `--out`: the names are fixed (`--filename` is refused), a redline already in that folder is overwritten, and no `report.json` is written. Give each redline its own folder. To run `qa` on it, pass the `report.json` that building the new draft wrote — the draft given as `--to`:

```bash
docx-kit build ./new.md --out ./output_docx_v2 --filename 原交付文件名.docx
docx-kit qa ./revision/redline.docx --report-json ./output_docx_v2/report.json --out ./revision/qa
```

Without `--report-json`, `qa` looks for a `report.json` beside the redline, finds none, says so and runs no other check.

Both sources must resolve to the same `cover`, `toc`, `chapter_header` and `page_numbers` (and, with a chapter header, both must have level-1 headings or both must lack them). Otherwise `redline` fails with `redline needs both drafts to have the same cover, toc, chapter_header and page_numbers…`: give both sources the same settings, or build the two versions separately. This also applies across versions: a 楷体 or 宋体 ordinary document saved as `report.json` by an earlier release has `page_numbers: always`, while a new Markdown draft of it defaults to `auto`; write `page_numbers: always` (and `heading_numbering: auto`, `list_numbering: template` if the old draft used them) in the new draft before comparing.

The contents section must also exist in both sources or in neither. This only matters when `toc` is off: the section then exists only while a figure or table list that is switched on has something to list, so deleting the last captioned table (or adding the first one, or switching the list on or off in one source) makes `redline` fail with `redline needs the contents section to exist in both drafts or in neither…`. Switch `toc` on in both sources, switch the lists off in both, or build the two versions separately. With `toc` on in both, the figure and table lists may differ freely.

Both sources must also have the same layout in effect, and `redline` refuses, naming the difference, when they do not: a different stated format (fonts, sizes, line spacing, `text_scale`) or different page margins — `三号` and `16pt`, `30mm` and `3cm`, or a value equal to the template's count as the same; a table whose `appearance`, `header` or `spacing` differs between the drafts; a side-by-side block (`::: 并排`) that changed in any way; a paragraph whose `::: 留白` level changed. Unchanged side-by-side blocks and spaced paragraphs pass, and text changes elsewhere are shown as usual. For those changes build the two versions separately and send both.

Landscape tables keep their landscape pages in the redline document, and the other page settings (margins, page position) are those of both drafts. When one draft has landscape table pages that the other lacks, Word restarts the page numbers at 1 in the section after those pages once all revisions are accepted or rejected — or, when those landscape pages end the kept draft, on the landscape pages themselves; Word cannot record taking a page-number restart away as a revision. To keep that file, set the page numbering of that section (the one that follows the landscape pages, or the landscape pages at the end) to continue from the previous section (Insert → Page Number → Format Page Numbers → Continue from previous section); that one setting is enough. Otherwise use the document rebuilt from the kept draft's source. Read `redline-result.json` and deliver its returned Word path. Accepting all revisions yields the new text; rejecting all yields the old text. Each side retains its own punctuation mode; the normalization receipt counts the emitted text from both sides. After accepting or rejecting revisions, update fields so the numbers and references match the side that was kept.

Redline compares document structure, not the bytes of external image assets. Replacing an image at the same path is visible in a rebuilt final document but is not an image-content diff. Headings/captions are compared as displayed: `**概况**` versus `概况` has the same displayed text, whereas a code-protected `A*B*C` differs from unprotected emphasis. A changed body paragraph is compared as shown too, character by character with its formatting: inserted and deleted text keeps its bold, italic, strikethrough or code look, a word that only became bold (or stopped being bold) is shown deleted and inserted again, and no `**` or other marker is printed. A paragraph with a link, a cross-reference, a citation or an inline formula is deleted and inserted whole, and so is a list, quote, callout or table whose text changed. The `added`/`removed`/`changed` summary comes from the same comparison used for the document.

Tell users that a later rebuild from source does not include changes they made in Word.
