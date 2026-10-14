# 示例 / Examples

示例内容均为虚构。 / All content is fictional.

| 文件 / File | 用途 / Purpose | 模板 / Template | 写了哪些设置 / Settings written |
| --- | --- | --- | --- |
| [report.md](report.md) | 分章报告：封面、目录、自动章号 / Report with cover, contents and automatic chapter numbers | 楷体 / KaiTi | `document_mode: report` 等 / and others |
| [letter.md](letter.md) | 没有标题的函件 / Letter without a title | 楷体 / KaiTi | 无 / none |
| [memo.md](memo.md) | 带章节的短备忘 / Short memo with chapters | 楷体 / KaiTi | `title`、`document_mode: document` |
| [notice.md](notice.md) | 公文模板的通知，章号由模板给 / Notice on the official template, numbered by the template | 公文 / Official | `template`、`numbering_rule` |
| [contract.md](contract.md) | 原样转录、保留条款编号的合同，结尾是左右并排、留出盖章位置的签署栏 / Transcribed contract keeping its clause numbers, ending in a side-by-side signature block with room for stamps | 宋体 / SimSun | `title`、`template`、`document_mode: document`、`punctuation_mode: preserve`、`numbering_rule` |
| [form.md](form.md) | 手填的表单：全框线、没有表头、留高的格子 / Form to fill in by hand: all lines, no header row, roomy cells | 楷体 / KaiTi | 无 / none |
| [certificate.md](certificate.md) | 落款前留出盖章位置的证明 / Certificate with room for the stamp above the sign-off | 楷体 / KaiTi | 无 / none |
| [stated-format.md](stated-format.md) | 明说了字号、行距和四边页边距的通知 / Notice with stated sizes, line spacing and four margins | 公文 / Official | `template`、`title_size`、`body_size`、`body_line_spacing`、`margin_*` |

在仓库根目录执行 / Run from the repository root:

```bash
docx-kit build examples/report.md --out ./report --filename report.docx --strict
docx-kit build examples/memo.md --out ./memo --filename memo.docx --strict
docx-kit build examples/contract.md --out ./contract --filename contract.docx --strict
docx-kit build examples/notice.md --out ./notice --filename notice.docx --strict
docx-kit build examples/letter.md --out ./letter --filename letter.docx --strict
docx-kit build examples/form.md --out ./form --filename form.docx --strict
docx-kit build examples/certificate.md --out ./certificate --filename certificate.docx --strict
docx-kit build examples/stated-format.md --out ./stated-format --filename stated-format.docx --strict
```

后四份（合同的签署栏、表单、证明、明说格式的通知）用到 `docx-kit templates` 在 `format.features` 里列出的能力，旧版本不认。 / The last four (the contract's signature block, the form, the certificate and the stated-format notice) use features listed by `docx-kit templates` under `format.features`; older binaries reject them.

函件、备忘、通知是普通文档：没有封面和目录，称呼顶格、落款靠右用 `::: 顶格`、`::: 靠右` 写；楷体、宋体的普通文档里编号照作者写的，只有一页时不显示页码。合同是原样转录，用 `punctuation_mode: preserve` 保留原文的标点和空格。 / The letter, memo and notice are plain documents: no cover or contents, a flush-left salutation and a right-aligned sign-off written with `::: 顶格` and `::: 靠右`; on the kaiti and song templates numbers stay as written and a one-page document shows no page number. The contract is a transcription and keeps its punctuation and spaces with `punctuation_mode: preserve`.
