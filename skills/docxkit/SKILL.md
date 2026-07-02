---
name: docxkit
description: Use when prepared report content, uploaded user materials, Markdown, or report.json should be delivered as a polished editable Word .docx through the local docx-kit CLI. Use at the final report-export step after content is available, when a task naturally needs a formal Chinese Word deliverable, or when the user explicitly asks to use DocxKit. This skill formats and exports reports; it does not gather sources by itself.
---

# DocxKit

Use this skill when the next deliverable is a polished, editable Word report. The user may have uploaded materials for the agent to organize, the current task may naturally end in a report, or the user may explicitly ask to use DocxKit.

This skill drives the local CLI. It does not research, gather facts, or decide source material by itself.

## Principle

- Keep the editable source as Markdown or `report.json`.
- Use the CLI to generate `report.docx`, `report.json`, and diagnostics.
- Return both the Word `.docx` path and editable `report.json` path.
- Default to the `executive-cn-docx` Chinese report template.
- Keep the default embedded font subsets; do not add `--no-embed-fonts` unless the user explicitly asks for a compatibility escape hatch.
- Do not edit the embedded Word template for ordinary report generation.
- Default to the current project/workspace directory for artifacts.

## Output Location

Unless the user gives an explicit output path, write artifacts under `./output_docx` in the current project/workspace directory.

Use a stable file name for the editable source, such as `./output_docx/content.md`, and run the CLI with `--out ./output_docx`. If `./output_docx` already contains a report that should be preserved, use a versioned sibling such as `./output_docx_v2`.

## Input Contract

For Markdown input, follow `references/docx-markdown-contract.md`. If the task needs examples, read `references/examples.md`.

Minimum rules:

- Put frontmatter at the top for title, subtitle, author, client, date, language, and confidentiality when available.
- Use unnumbered headings such as `# 研究背景`; do not write `# 一、研究背景`, `# 1. 研究背景`, or `## （一）研究方法`.
- Put `表：` before every Markdown table.
- Use `表[compact]：标题` only for dense numeric/status/checklist tables with many short cells; use normal `表：标题` for narrative or comparison tables.
- Use `表[landscape]：标题` only when a wide table must remain intact.
- Introduce each table or figure in the preceding prose before the `表：` or `图：` caption; do not place `如图1.1所示` or `见表1.1` after the referenced object.
- Put `图：` before every image, with image alt text kept short and not identical to the formal figure caption; image paths are resolved relative to the Markdown file.
- Use fenced code blocks for JSON/config/code; put the optional display title after the language, for example ```` ```json renderer_contract ````. If no title is provided, DocxKit shows the language label.
- Use callouts sparingly: `> [!note]`, `> [!insight]`, `> [!risk]`, `> [!warning]`.
- Do not rely on `---PAGE---` for normal pagination. Use it only when the user explicitly wants a hard page break.

Keep analysis conclusions, recommendations, field explanations, status notes, and action items as paragraphs, tables, or normal lists. Do not create glossary/checklist-style blocks in Markdown unless the user provides an existing `report.json` that already uses them.

## Delivery Gate

`ok: true` only means the build completed. It is not enough to return success.

Before returning the final Word path:

1. Read the JSON result printed by the CLI.
2. Verify `report.docx`, `report.json`, and `build-result.json` exist.
3. Confirm `build-result.json` exactly matches stdout.
4. Inspect `warnings` and `errors`; revise the Markdown/report JSON and rebuild if any issue is reported.
5. Return the `.docx` path, editable `report.json` path, and any remaining intentional warning.

Avoid these common LLM habits:

- manual heading numbers: `# 一、背景`, `# 1. 背景`, `## （一）方法`;
- sections made only of tables or figures with no explanatory prose;
- excessive callouts for ordinary conclusions or risks;
- decorative horizontal rules instead of natural document flow;
- missing `表：` or `图：` captions.

## CLI Commands

Use these commands in the normal workflow:

```bash
docx-kit build ./output_docx/content.md --out ./output_docx
docx-kit build ./output_docx/report.json --out ./output_docx
```

Use these only when validating or debugging:

```bash
docx-kit --version
docx-kit validate ./output_docx/report.json
```

If `docx-kit` is not installed but npm is available, install the public package in the current workspace before building:

```bash
npm install @dztabel/docxkit
npx --no-install docx-kit build ./output_docx/content.md --out ./output_docx
```

## Visual QA

When rendering the `.docx` to PNG/PDF for visual QA, use DocxKit's QA wrapper. It only calls the Documents skill renderer and patches a temporary TOC cache for PNG/PDF review:

```bash
python3 <docxkit-skill>/tools/render_docxkit.py ./output_docx/report.docx --report-json ./output_docx/report.json --renderer <documents-skill>/render_docx.py --output-dir ./output_docx/rendered --emit-pdf
```

Do not hand-write or run direct `soffice`, `libreoffice`, `pdftoppm`, `qlmanage`, or custom conversion commands. If the DocxKit QA wrapper or Documents skill renderer is unavailable, report that visual QA is unavailable instead of using a substitute renderer.

## Workflow

1. Prepare the final report content from the materials already available in the conversation, uploaded files, or an existing Markdown / `report.json` input.
2. Save the draft as `./output_docx/content.md`, or use an existing `report.json` when editing a prior build.
3. Run `docx-kit build <input> --out ./output_docx` unless the user asked for another path.
4. Save stdout as `stdout.json` when verifying parity.
5. Verify the returned `report_path`, `docx_path`, and `artifacts.build_result` exist.
6. Compare stdout JSON with `build-result.json`.
7. If warnings or errors are present, revise the Markdown/report JSON and rebuild once before returning final output.
8. Return the Word path and editable `report.json` path.

## Revision Workflow

When the user asks for changes:

1. Edit Markdown if the source was Markdown, or edit `report.json` if that is the active editable artifact.
2. Re-run `build` for Markdown or `build <report.json>` for JSON.
3. Keep the same output directory only if overwriting is intended; otherwise use a versioned folder such as `./output_docx_v2`.
4. Return the new `.docx` path and the edited source path.

## Guardrails

- Do not search the web or invent sources as part of this skill.
- Use the local CLI or binary command shown above for Word export.
- Do not hand-write OpenXML for ordinary reports.
- Do not edit `template.docx` for ordinary reports.
- If CLI validation fails, inspect structured errors, fix the Markdown or JSON, and rerun.
