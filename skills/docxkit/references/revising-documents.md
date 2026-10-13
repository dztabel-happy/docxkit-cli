# Revising an Already-Generated Document

The user can continue writing directly in Word/WPS. Agent rebuilds use Markdown or `report.json`; they do not import edits from the Word file. First establish which copy contains the latest content.

## The rule

- For an agent revision, change the source and rebuild; do not patch generated Word XML.
- For a file edited by the user in Word/WPS, reconcile those edits with the source before rebuilding. Do not overwrite them with an older source.
- Preserve the document's mode, title choice, numbering rule, punctuation mode and author-written clause numbers unless the user requests a change. Transcriptions use `document` plus `none` and `punctuation_mode: preserve`; do not turn a letter into a report while revising it.

## Locating the source

1. Use the saved `content.md` if it is current.
2. Otherwise use `report.json`, which every successful build writes. Rebuild it with the same output filename.
3. If only a hand-edited `.docx` is available, reconstruct its content as source and compare it against that file. This is a new transcription, not an automatic merge.

Headings and captions retain the source text in `report.json`. Keep escapes such as `\*` and code spans that intentionally protect literal characters. JSON strings require the backslash itself to be escaped (`"text": "Z\\*\\*\\*\\*\\*99"`). Switching to JSON does not bypass inline parsing.

A `report.json` written by docx-kit 0.1.62 or earlier stored headings/captions with markers removed. If it lost protective backticks, return to the Markdown or restore the intended literal text before rebuilding. Historical JSON without `numbering_rule` retains old reference lookup; do not change it to `native-v1` without checking every affected target.

## Common revisions

| Ask | What to change |
| --- | --- |
| Reword, correct a fact or shorten prose | Edit source paragraphs; preserve original text in a transcription unless asked to change it. |
| Add, delete or move a section | Edit headings and blocks. Recheck source reference numbers against the effective policy. Word edits can update native references, but a Markdown rebuild still parses the locators written in the source. |
| Add/drop a table, figure or source | Update the block and its source references together. Uncaptioned tables consume no table number. Ordinary documents do not require adding references merely to clear `info`. |
| Change typography | Change `template:` while retaining mode. Recheck caption numbering: the 公文模板 is continuous. Remove level-4 input headings before switching to 楷体/宋体. |
| Keep the original clause numbers | Set `heading_numbering: none`; keep author numbers in headings, use line-start `1\.` for literal numbered paragraphs. |
| Add a chart | Render a local image, then add its path and a caption. Check the reference before the image in a new report. |

## Versioning

Overwrite the same output directory only when replacing the old build is intended. Otherwise use a sibling directory. For a runnable example from the repository root:

```bash
docx-kit build examples/contract.md --out ./contract --filename contract.docx --strict
docx-kit build ./contract/report.json --out ./contract_v2 --filename contract.docx --strict
```

The second command rebuilds the saved model. Edit a copy of the source before using this pattern for an actual revision.

## After every revision

Read build `errors`, `warnings`, `checks`, `effective_document` and `text_normalization`; resolve errors, review warnings, and keep legitimate `info`. Run QA on the original generated document and review the content/layout required by the task. QA checks structure only; it does not compare a transcription with its original. Return the authoritative `docx_path`, source path, and the review status.

For LibreOffice preview or conversion, create a `render-copy` after building. For a user-edited file, update fields and save in Word/WPS first. The render-only copy freezes displayed results without recomputation and is not the editable deliverable.

## Showing what changed (tracked changes)

`redline` compares two DocxKit sources (Markdown or JSON), including ordinary documents and escaped literal text. It does not compare arbitrary uploaded Word files. For example, after preparing old and new source files:

```bash
docx-kit redline --from ./old.md --to ./new.md --out ./revision
```

Both sources must resolve to the same `cover`, `toc`, `chapter_header` and `page_numbers` (and, with a chapter header, both must have level-1 headings or both must lack them). Otherwise `redline` fails with `redline needs both drafts to have the same cover, toc, chapter_header and page_numbers…`: give both sources the same settings, or build the two versions separately.

The contents section must also exist in both sources or in neither. This only matters when `toc` is off: the section then exists only while a figure or table list that is switched on has something to list, so deleting the last captioned table (or adding the first one, or switching the list on or off in one source) makes `redline` fail with `redline needs the contents section to exist in both drafts or in neither…`. Switch `toc` on in both sources, switch the lists off in both, or build the two versions separately. With `toc` on in both, the figure and table lists may differ freely.

Read `redline-result.json` and deliver its returned Word path. Accepting all revisions yields the new text; rejecting all yields the old text. Each side retains its own punctuation mode; the normalization receipt counts the emitted text from both sides. After accepting or rejecting revisions, update fields so the numbers and references match the side that was kept.

Redline compares document structure, not the bytes of external image assets. Replacing an image at the same path is visible in a rebuilt final document but is not an image-content diff. Headings/captions are compared as displayed: `**概况**` versus `概况` has the same displayed text, whereas a code-protected `A*B*C` differs from unprotected emphasis. The `added`/`removed`/`changed` summary comes from the same comparison used for the document.

Tell users that a later rebuild from source does not include changes they made in Word.
