# PDF export and figure pagination

For a requested PDF start with the export command. Use figure settling only when the user wants to reduce the gap left by a tall figure.

## PDF (`docx-kit pdf`)

```bash
docx-kit pdf ./report/report.docx --out ./report --filename 季度复盘.pdf
```

When the user wants a PDF, make it with `docx-kit pdf`; never run LibreOffice on the delivered file directly. It never changes the input. On Windows with Microsoft Word installed it exports through Word: its own invisible instance, a copy of the document, repaginated first; the user's open documents are not touched. Everywhere else it exports with LibreOffice from an internal render copy, so captions, references and the page-number footer come out as Word shows them (a one-page document of `page_numbers: auto` has no page number, as in Word), and the page numbers in the contents and in the lists of figures and tables are those of the pages LibreOffice lays out. `DOCXKIT_SOFFICE` names LibreOffice; `DOCXKIT_PDF_WITH=libreoffice` forces it.

It prints one JSON object (exit code 0 on success, 1 otherwise; the JSON is plain ASCII, non-ASCII characters as `\uXXXX`):

```json
{"ok": true, "command": "pdf", "pdf_path": "/abs/report/季度复盘.pdf", "engine": "libreoffice", "engine_version": "26.2.3.2",
 "notes": ["Exported with LibreOffice 26.2.3.2 from an internal render copy (...)", "This PDF was laid out by LibreOffice, not Word: ..."],
 "errors": [], "substituted_fonts": []}
```

An existing target is kept by default. `output_exists` gives its absolute path. Choose a new `--filename`, or pass `--overwrite` when the user wants to replace that PDF. CLIs through 0.2.5 silently replace an existing target, so use a fresh filename with those versions.

On macOS, a volume such as exFAT may lack the operation needed to create a completed PDF exclusively. If `export_failed` reports this limitation, export to a local APFS folder. Use `--overwrite` on the requested volume only with permission to replace the target.

`engine` is `word` or `libreoffice`. On failure `pdf_path`, `engine` and `engine_version` are null, `substituted_fonts` is empty and `errors` holds `{code, message}`. Besides `output_exists`, codes include `invalid_arguments`, `input_not_found`, `not_a_docx`, `export_failed`, and `no_pdf_engine`. With `no_pdf_engine`, neither Word nor LibreOffice is available here. Its message says so plainly: this computer cannot make a PDF; do not install anything, do not look for another converter and do not make the PDF with another tool; deliver the Word file and tell the user they can open it in Word or WPS and save it as PDF.

`substituted_fonts` lists the fonts the document uses to show text that the exporting program does not have on this computer, by the names the document writes; in the PDF those characters are in another font. Fonts embedded in the document count as present; with LibreOffice, fonts that only Microsoft Office can use (its own font folder on macOS) count as missing and LibreOffice's own fonts as present. A font that is only set somewhere but shows no character (a Latin font of a paragraph with only Chinese text) is not listed.

Read `notes`: they name the engine and say when Word failed and LibreOffice was used instead. With LibreOffice a note says the PDF was laid out by LibreOffice, not Word — line and page breaks can differ by a line or two, contents page numbers with them, fonts the computer lacks are substituted (it repeats `substituted_fonts`) — and that a PDF exactly like Word comes from saving it as PDF in Word or WPS; tell the user this when you deliver such a PDF. When `substituted_fonts` is not empty a note says so and asks you to tell the user. A note also says when the document centres its pages (`page_position: center`) — LibreOffice does not, so that PDF starts every page at the top; export it from Word or WPS to keep the centring. Deliver the PDF beside the Word file, never instead of it unless the user asked only for a PDF.

## Render-only copies

```bash
docx-kit render-copy ./report/report.docx --out ./report/copy --filename report.render-only.docx
```

`render-copy` is for other programs that read the file and for troubleshooting, not a check before delivery. LibreOffice and similar renderers recalculate Word caption and reference fields incorrectly. For a PDF use `docx-kit pdf` (above), which does this internally. `render-copy` writes a copy in which those fields are replaced by what they currently show; the original is never changed. A table of contents, and each list of figures or tables, loses only its outer TOC field: the entries stay as they are and their page-number fields are left for the renderer to compute, so the copy shows the real page numbers instead of the `1` that Word replaces when it opens the file. Page numbers, headers and footers keep their fields — with one exception: the conditional footer of `page_numbers: auto`, which LibreOffice does not display, becomes a plain page number in the copy (see `page_numbers` under "Metadata"). Latin text marked as Chinese — DocxKit marks it so, because Word then breaks English only between words and never hyphenates it — is marked English in the copy, with automatic hyphenation off: LibreOffice breaks Latin text marked Chinese inside a word (`error_code` as `e` / `rror_code`). A freshly built document can be copied directly; for a file edited in Word or WPS, update fields and save first. The default output is `<input-stem>.render-only.docx` beside the input. Use the copy for other programs only; deliver the original.

The result is JSON on stdout with `command: render-copy`, `input_sha256`, `docx_path` and `artifacts.render_copy`; `template_id` is `not-applicable`, and no `report.json` is created.

## Tall figures and blank page bottoms (`--settle-figures`, opt-in)

Word cannot split a figure across pages. A figure taller than the space left on the page moves to the next page as a whole and leaves the bottom of the previous page empty — often a third to two thirds of it.

`docx-kit build <input> --out <dir> --filename <name.docx> --settle-figures` measures the real pagination after the normal build and, **in the delivered `.docx` only**, lets such a figure fall back by one or two of the ordinary paragraphs that follow it, so those paragraphs fill the page and the figure opens the next one. The paragraphs keep their order and wording; only the figure's position among them changes. The input and `report.json` keep the author's order, and every build starts again from that order.

- **Use it only on request**: when the user asks to reduce the blank space before a figure. It is not a default and it does not replace sizing a figure sensibly.
- **What it measures with**: on Windows with Microsoft Word installed, Word itself (the reader's pagination). Otherwise LibreOffice (`soffice` on `PATH`, `DOCXKIT_SOFFICE`, or the standard install location) plus poppler's `pdftotext`; LibreOffice measures a render-only copy. `DOCXKIT_SETTLE_WITH=libreoffice` skips Word; `DOCXKIT_DOCX2PDF=<executable>` uses your own converter (`<it> <input.docx> <output.pdf>`), on the original document unless `DOCXKIT_DOCX2PDF_RENDER_COPY=1` is set.
- **LibreOffice is not the reader's Word**: the two paginate these documents a line or two apart per page. A LibreOffice-measured arrangement is re-checked with the page one or two lines taller and shorter and is delivered only if it is no worse than the draft both ways; even so, in our sample roughly one changed document in nine came out worse in real Word. For a document that matters, measure with Word.
- **A figure never moves past** a paragraph that points at it (“上图”“图中”“如上所示”), its note or source line (“注：”“资料来源：”), a paragraph describing what is on it (“右上区域”“虚线”“箭头”), a lead-in sentence (ends with a colon, “如下”“以下”), a salutation, sign-off or centred line (a `::: 顶格`, `::: 靠右` or `::: 居中` paragraph), or a paragraph directly followed by a table, figure, list, equation or other non-paragraph block (it is most likely that block's lead-in; a hard page break after it does not count); it never leaves a preceding sentence that points down at it (“如下图所示：”), and a figure placed directly after another figure stays with it. These word lists only stop a move — they do not prove a paragraph is position-independent. Referring to figures by number (`见图 2.1`) is what makes a move safe.
- **Read the result**: with the flag, `build-result.json` gains `figure_settling` — `requested`, `measured`, `moved_paragraphs`, `improved`, `renderer` / `renderer_version`, `rounds`, `before_page_count` / `after_page_count`, `before_pages` / `after_pages` (pages whose bottom is ≥ 25% blank: `page`, `bottom_whitespace`, `figure`), `measurements` (`round`, `figure`, `score`, `page_count`, `outcome`: `draft` / `kept` / `undone`), `figures` (`figure`, `paragraph_count`, `paragraph_starts`, `blank_before`, `blank_after`), `held` (`figure`, `why` — figures still preceded by a blank page bottom and the reason they were not moved), `notes`, `reason`, `message`. When `moved_paragraphs > 0`, **check that the paragraphs listed in `figures[].paragraph_starts` still read naturally ahead of their figure** before delivering; if one does not, rebuild without the flag. Without the flag the field is absent.
- **It never fails a build**: with missing tools or a probe error the document is still delivered — the normal one, or the best arrangement already measured — and one entry is added to `warnings` (`图位置整理未执行: …` / `图位置整理中止: …`). That entry is not a content problem: leave it, tell the user, and note that `--strict` does not fail on it. The whole pass has a time budget of about three minutes; when it runs out, the best arrangement measured so far is delivered and `figure_settling.notes` says so. Do not promise that the option removes every gap.
- **Refused before building**: together with stated page margins (it still measures pages with the template's own margins) and together with `page_position: center` (it judges a page by the space under its last line, which a centred page splits above and below). Build without one of the two.
- It cannot help when the figure is followed by a table, another figure, a list, or the end of the section: there is no paragraph to bring forward. Shrink the figure, move it, or accept the blank.
