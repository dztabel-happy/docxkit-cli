---
name: docxkit
description: Use when prepared report content, uploaded user materials, Markdown, or report.json should be delivered as a polished editable Word .docx through the local docx-kit CLI. Use at the final report-export step after content is available, when a task naturally needs a formal Chinese Word deliverable, or when the user explicitly asks to use DocxKit. This skill formats and exports reports; it does not gather sources by itself.
---

# DocxKit

Use this skill when the next deliverable is a polished, editable Word report. The user may have uploaded materials for the agent to organize, the current task may naturally end in a report, or the user may explicitly ask to use DocxKit.

This skill drives the local CLI after the agent has prepared content, sources, Markdown, or `report.json`. It does not replace the agent's normal research or source-reading work.

## Requirements

This skill matches `@dztabel/docxkit >= 0.1.61`. At session start (once, before the first build), refresh the CLI and the installed skill copies. Every step is fail-soft: if offline or a step errors, keep going with the local versions — never block the build on updating.

```bash
npm install @dztabel/docxkit@latest   # session-start upgrade; on failure keep the local install
npx --no-install docx-kit --version
npx --no-install docx-kit sync-skill  # mirrors the packaged skill into ~/.claude/skills and ~/.agents/skills
```

`sync-skill` refreshes the machine-installed skill copies from the npm package (only into skills roots that already exist); an updated skill takes effect in the next session — do not re-read it mid-session. Skip the command silently if the local CLI predates it. Do not run `npm install` again mid-session: the CLI version must stay stable across a build/redline loop.

## Principles

- Keep the editable source as Markdown (`./output_docx/content.md`) or `report.json`; the CLI generates one user-facing Word file plus diagnostics into the same `--out` directory (default `./output_docx`; use a versioned sibling like `./output_docx_v2` when the old build must be preserved).
- Always pass `--filename <descriptive-name.docx>` on `build`. Use a concise name derived from the report title, with no directory components. The returned `docx_path` is the only Word deliverable: never copy or rename it, and never expose a second `.docx` from the same build.
- Default template is `executive-cn-docx` (楷体 body and headings). Use `executive-cn-song-docx` for 宋体正文 + 黑体标题. Use `executive-cn-official-docx` only for a 公文范式 request: 方正小标宋简体 title, no-prefix 楷体_GB2312 subtitle, 仿宋_GB2312 三号 body, bold H2/H3, 小四 tables and table captions, no header, four official heading levels and fixed 30 pt line spacing.
- `executive-cn-official-docx` defaults to `document`: notices, plans, implementation schemes and ordinary official documents start with an inline title/subtitle and have no separate cover or TOC. Set `document_mode: report` only when the user explicitly requests a cover or TOC, or the deliverable is genuinely a long report that needs them.
- Keep the default font behavior (no embedding): fonts map across Windows/macOS Word/WPS via alt-name chains, so files stay small and fully editable. Add `--embed-fonts` only when recipients may lack Chinese fonts (for example overseas readers on non-Chinese systems).
- Never hand-edit the generated `.docx` or write OpenXML directly; all changes go through the Markdown/`report.json` source and a rebuild.

## Writing the Input

`references/docx-markdown-contract.md` is the single authoritative writing contract — read it before writing. `references/examples.md` shows a full-featured report to imitate. When unsure which component fits, run `docx-kit components` for the machine-readable component contract (purpose, use/avoid, fields, visual behavior).

The highest-frequency rules:

1. Headings are unnumbered (`# 研究背景`, never `# 一、背景`), and long chapters get real `##` subsections. `####` is reserved for `executive-cn-official-docx`; the two legacy templates accept only `#` through `###`.
2. Every table gets `表：标题` on the line before it (`表[landscape]：` for wide tables that must stay intact); every image gets `图：题注`. Table font size is automatic — never try to control it.
3. Introduce each table/figure in the prose before it appears, referencing it as `见表 x.x` / `如图 x.x` — these become clickable cross-references.
4. Cite sources inline as `[1]` after the supported claim and list them in a final `# 资料来源` chapter as ordered `[名称](url)，出处，日期。` items — never invent sources, never paste naked URLs.
5. Block formulas go in ```` ```math ```` fences (LaTeX, auto-numbered, cite as `式 x.x` in prose); inline math uses `\( ... \)` spans inside body text.
6. Prose first: conclusions and explanations are paragraphs; lists support them. `executive-cn-official-docx` forbids callouts; with the other templates use callouts (`> [!note]` / `> [!risk]`) sparingly. Avoid `---PAGE---`, and never fabricate glossary/checklist blocks in Markdown.

## Workflow

1. Prepare content per the contract and save it as `./output_docx/content.md` (or edit the active `report.json`).
2. Ensure the CLI is current (see Requirements).
3. Build:

   ```bash
   npx --no-install docx-kit build ./output_docx/content.md --out ./output_docx --filename 项目复盘报告.docx
   ```

   The full result JSON is also written to `./output_docx/build-result.json` — read that file; no `tee` needed.

4. **Gate loop** — `ok: true` is not enough; read `errors`, `warnings`, and `checks` (a list of `{code, severity, path, message}`):
   - `severity: error` fails the build (dangling `表/图/式 x.x` references, `[n]` beyond the source list, table rows wider than the header). Fix the content at the reported `path` and rebuild — never work around the gate.
   - `severity: warning` and formula-fallback `warnings` should be fixed too; iterate until `checks` and `warnings` are clean. Leave a warning only when the user explicitly wants that shape, and say so when delivering.
5. Run structural QA (package structure, Word fields, internal link anchors, style names, font declarations):

   ```bash
   npx --no-install docx-kit qa ./output_docx/项目复盘报告.docx --report-json ./output_docx/report.json --out ./output_docx/qa
   ```

6. Verify the single `.docx` at `docx_path`, plus `report.json` and `build-result.json`, exist.
7. Deliver only `docx_path` as the Word file, together with the editable source path and any intentionally remaining warning.

When the user wants changes to an already-generated report — including asking for tracked-changes markup of what changed — read `references/revising-documents.md`. The short version: edit the same editable source (`content.md` or the always-written `report.json`), never the `.docx`, then rebuild and rerun the gate loop.

## Failure Playbook

| Situation | Action |
| --- | --- |
| `errors` from validate/build (missing fields, unknown template, missing image) | Fix the structure at the reported path; each message names the field. |
| `checks` with `severity: error` | Fix the content at `path`; the code table in the contract explains every code. `dangling_caption_reference` messages list the document's actual auto-generated numbers — use those instead of guessing (执行摘要/导论 also counts as chapter 1). |
| `warnings` like `formula rendered as plain text` | Repair the LaTeX (subset listed in the contract) or switch that formula to an ```` ```omml ```` fence. |
| `qa` fails | Do not hand-edit the docx; rebuild, and if QA still fails report the QA JSON to the user as a tool issue. |
| `docx-kit` not found | `npm install @dztabel/docxkit`, then use `npx --no-install docx-kit ...`. |
