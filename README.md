# DocxKit

Agent-facing CLI for exporting prepared Markdown or `report.json` into polished, editable Word `.docx` reports.

```bash
npm install @dztabel/docxkit
npx --no-install docx-kit --version
npx --no-install docx-kit build content.md --out ./report
```

Outputs:

- `report/report.docx`
- `report/report.json`
- `report/build-result.json`

The MVP ships the `executive-cn-docx` template for formal Chinese reports.

## Agent Skill

Use the Codex skill in this repository when an agent should turn uploaded materials or prepared research into a Word deliverable:

```text
skills/codex/docxkit-word-report
```

Flow:

```text
user materials / LLM research -> Markdown or report.json -> docx-kit build -> editable report.docx
```
