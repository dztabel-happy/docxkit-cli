---
name: docxkit
description: Export prepared Chinese-language content, Markdown or report.json as an editable Word document with DocxKit. Use for reports, notices, letters, forms, transcriptions and tracked changes between DocxKit drafts, in a template or the user's stated format.
---

# DocxKit

Build the editable Word file from Markdown or `report.json`. Make corrections in the source and regenerate with DocxKit. Keep the source for future revisions. Reconcile any edits made in Word or WPS before rebuilding.

## Requirements

This skill matches `@dztabel/docxkit >= 0.2.5`. Once at session start, refresh the CLI and skill. If the refresh fails, continue with the installed version. Use the same binary throughout a build or revision.

```bash
npm install @dztabel/docxkit@latest
npx --no-install docx-kit --version
npx --no-install docx-kit sync-skill
```

The refreshed skill takes effect next session. In the examples below, invoke the local CLI with `npx --no-install docx-kit`.

## Write the source

For a short notice, letter or certificate, start with its title and write the text. Save this as `./output_docx/content.md`, replacing the example details with the user's:

```markdown
# 关于召开经营分析会的通知

::: 顶格
各部门：
:::

请于 11 月 20 日上午 9 时到三楼会议室参加经营分析会，并携带本月月报。

::: 靠右
综合管理部
:::
```

- A short document with only an initial title needs no frontmatter. For a plain document with chapter headings, set `title:` and `document_mode: document` in YAML frontmatter. For a report with a cover and contents, set `title:` and `document_mode: report` and start chapters at `#`. In reports the template numbers headings.
- The default `executive-cn-docx` uses 楷体. Choose `executive-cn-song-docx` for 宋体正文、黑体标题, or `executive-cn-official-docx` for 公文格式. The official template defaults to plain-document mode.
- A basic table uses pipe rows and a Markdown separator row. In reports, introduce it by number in the prose (e.g. `见表 1.1`), then put `表：标题` immediately before the table. Declare `numbering_rule: native-v1` in new sources using numbered exhibit references. For citations place `[1]` after the claim and list the source under `# 资料来源`.
- For a transcription set `punctuation_mode: preserve` and compare the result with the original. Keep the author's wording, numbers and blank fields.

## Build and check

Use one directory per document and give the Word file a descriptive name. Substitute the intended filename in both commands.

```bash
npx --no-install docx-kit validate ./output_docx/content.md
npx --no-install docx-kit build ./output_docx/content.md --out ./output_docx --filename 经营分析会通知.docx
npx --no-install docx-kit qa ./output_docx/经营分析会通知.docx --report-json ./output_docx/report.json --out ./output_docx/qa
```

Read the receipt's errors, warnings and checks. Fix the source and rebuild if needed. Check `effective_document` against the requested mode and numbering, and `text_normalization` if the wording must be exact. Compare the generated model and content with the request. Explain any warning retained for an intentional layout.

Deliver the single file at `docx_path` and identify its editable source. Tell the recipient they can keep writing in Word or WPS; for a later rebuild, ask for any edits made there. At handoff, identify any unmet requirements and any fields left blank because source information was missing. Report the checks actually performed. Structural QA inspects the DOCX package. Visual appearance, source fidelity and accepting or rejecting tracked changes each require their own check.

## When the task needs more

| Task | Read or run |
| --- | --- |
| A grid form, merged cells, handwritten rows, signature space, prescribed fonts, type sizes, margins or side-by-side blocks | [Forms and page layout](references/forms-and-layout.md) |
| Heading or list numbering, template defaults, punctuation or faithful transcription | [Markdown structure and numbering](references/docx-markdown-contract.md) |
| Captioned or landscape tables, images, equations, citations and numbered cross-references | [Figures, tables and sources](references/figures-tables-and-sources.md) |
| Find a component or its fields | Run `docx-kit components --list`, then query one by name, e.g. `docx-kit components checklist`. For JSON-only blocks and saved-model compatibility, see [Authoring report.json](references/report-json.md). |
| Revise an existing source or compare two drafts with independent Word revisions | [Revising documents](references/revising-documents.md) gives the redline and receipt-based QA commands. |
| Export a requested PDF or reduce space left by a tall figure | [PDF and figure pagination](references/pdf-and-pagination.md) |
| Interpret a specific check code, failure or receipt field | [Diagnostics](references/diagnostics.md) |
| A complete report, 公文, contract or printable form to adapt | [Worked examples](references/examples.md) |
| Help a recipient continue editing styles, lists, captions, references or contents in Word/WPS | [Editing in Word or WPS](references/word-editing.md) |
