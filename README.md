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
