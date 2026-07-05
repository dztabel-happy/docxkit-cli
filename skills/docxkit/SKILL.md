---
name: docxkit
description: Use when prepared report content, uploaded user materials, Markdown, or report.json should be delivered as a polished editable Word .docx through the local docx-kit CLI. Use at the final report-export step after content is available, when a task naturally needs a formal Chinese Word deliverable, or when the user explicitly asks to use DocxKit. This skill formats and exports reports; it does not gather sources by itself.
---

# DocxKit

Use this skill when the next deliverable is a polished, editable Word report. The user may have uploaded materials for the agent to organize, the current task may naturally end in a report, or the user may explicitly ask to use DocxKit.

This skill drives the local CLI after the agent has prepared content, sources, Markdown, or `report.json`. It does not replace the agent's normal research or source-reading work.

## Requirements

This skill matches `@dztabel/docxkit >= 0.1.48`. Ensure the latest CLI before building:

```bash
npm install @dztabel/docxkit          # install or upgrade in the workspace
npx --no-install docx-kit --version
```

## Principles

- Keep the editable source as Markdown (`./output_docx/content.md`) or `report.json`; the CLI generates `report.docx` plus diagnostics into the same `--out` directory (default `./output_docx`; use a versioned sibling like `./output_docx_v2` when the old build must be preserved).
- Default template is `executive-cn-docx` (楷体 body and headings). Switch to `executive-cn-song-docx` (宋体 body + 黑体 bold headings, GB/T 9704 pairing) only when the user asks for 宋体/黑体 styling, via `template: executive-cn-song-docx` frontmatter.
- Keep the default font behavior (no embedding): fonts map across Windows/macOS Word/WPS via alt-name chains, so files stay small and fully editable. Add `--embed-fonts` only when recipients may lack Chinese fonts (for example overseas readers on non-Chinese systems).
- Never hand-edit the generated `.docx` or write OpenXML directly; all changes go through the Markdown/`report.json` source and a rebuild.

## Writing the Input

`references/docx-markdown-contract.md` is the single authoritative writing contract — read it before writing. `references/examples.md` shows a full-featured report to imitate. When unsure which component fits, run `docx-kit components` for the machine-readable component contract (purpose, use/avoid, fields, visual behavior).

The highest-frequency rules:

1. Headings are unnumbered (`# 研究背景`, never `# 一、背景`), and long chapters get real `##` subsections — a report where every chapter is a flat `#` reads like an outline.
2. Every table gets `表：标题` on the line before it (`表[landscape]：` for wide tables, `表[compact]：` for dense numeric ones); every image gets `图：题注`.
3. Introduce each table/figure in the prose before it appears, referencing it as `见表 x.x` / `如图 x.x` — these become clickable cross-references.
4. Cite sources inline as `[1]` after the supported claim and list them in a final `# 资料来源` chapter as ordered `[名称](url)，出处，日期。` items — never invent sources, never paste naked URLs.
5. Block formulas go in ```` ```math ```` fences (LaTeX, auto-numbered, cite as `式 x.x` in prose); inline math uses `\( ... \)` spans inside body text.
6. Prose first: conclusions and explanations are paragraphs; lists support them. Use callouts (`> [!note]` / `> [!risk]`) sparingly, avoid `---PAGE---`, and never fabricate glossary/checklist blocks in Markdown.

## Workflow

1. Prepare content per the contract and save it as `./output_docx/content.md` (or edit the active `report.json`).
2. Ensure the CLI is current (see Requirements).
3. Build, capturing stdout:

   ```bash
   npx --no-install docx-kit build ./output_docx/content.md --out ./output_docx | tee ./output_docx/stdout.json
   ```

4. **Gate loop** — `ok: true` is not enough; read `errors`, `warnings`, and `checks` (a list of `{code, severity, path, message}`):
   - `severity: error` fails the build (dangling `表/图/式 x.x` references, `[n]` beyond the source list, table rows wider than the header). Fix the content at the reported `path` and rebuild — never work around the gate.
   - `severity: warning` and formula-fallback `warnings` should be fixed too; iterate until `checks` and `warnings` are clean. Leave a warning only when the user explicitly wants that shape, and say so when delivering.
5. Run structural QA (package structure, Word fields, internal link anchors, style names, font declarations):

   ```bash
   npx --no-install docx-kit qa ./output_docx/report.docx --report-json ./output_docx/report.json --out ./output_docx/qa
   ```

6. Verify `report.docx`, `report.json`, and `build-result.json` exist and `build-result.json` matches the captured stdout.
7. Deliver the `.docx` path, the editable source path, and any intentionally remaining warning.

For user-requested revisions: edit the same editable source, rebuild into the same directory (or a versioned sibling if the old build must survive), and rerun the gate loop.

## Failure Playbook

| Situation | Action |
| --- | --- |
| `errors` from validate/build (missing fields, unknown template, missing image) | Fix the structure at the reported path; each message names the field. |
| `checks` with `severity: error` | Fix the content at `path`; the code table in the contract explains every code. |
| `warnings` like `formula rendered as plain text` | Repair the LaTeX (subset listed in the contract) or switch that formula to an ```` ```omml ```` fence. |
| `qa` fails | Do not hand-edit the docx; rebuild, and if QA still fails report the QA JSON to the user as a tool issue. |
| `docx-kit` not found | `npm install @dztabel/docxkit`, then use `npx --no-install docx-kit ...`. |
