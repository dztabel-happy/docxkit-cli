# 示例 / Examples

示例内容均为虚构。 / All content is fictional.

| 文件 / File | 用途 / Purpose | 模板 / Template | 写了哪些设置 / Settings written |
| --- | --- | --- | --- |
| [report.md](report.md) | 分章报告：封面、目录、自动章号 / Report with cover, contents and automatic chapter numbers | 楷体 / KaiTi | `document_mode: report` 等 / and others |
| [letter.md](letter.md) | 没有标题的函件 / Letter without a title | 楷体 / KaiTi | 无 / none |
| [memo.md](memo.md) | 带章节的短备忘 / Short memo with chapters | 楷体 / KaiTi | `title`、`document_mode: document` |
| [notice.md](notice.md) | 公文模板的通知，章号由模板给 / Notice on the official template, numbered by the template | 公文 / Official | `template`、`numbering_rule` |
| [contract.md](contract.md) | 原样转录、保留条款编号的合同 / Transcribed contract keeping its clause numbers | 宋体 / SimSun | `title`、`template`、`document_mode: document`、`punctuation_mode: preserve`、`numbering_rule` |

在仓库根目录执行 / Run from the repository root:

```bash
docx-kit build examples/report.md --out ./report --filename report.docx --strict
docx-kit build examples/memo.md --out ./memo --filename memo.docx --strict
docx-kit build examples/contract.md --out ./contract --filename contract.docx --strict
docx-kit build examples/notice.md --out ./notice --filename notice.docx --strict
docx-kit build examples/letter.md --out ./letter --filename letter.docx --strict
```

函件、备忘、通知是普通文档：没有封面和目录，称呼顶格、落款靠右用 `::: 顶格`、`::: 靠右` 写；楷体、宋体的普通文档里编号照作者写的，只有一页时不显示页码。合同是原样转录，用 `punctuation_mode: preserve` 保留原文的标点和空格。 / The letter, memo and notice are plain documents: no cover or contents, a flush-left salutation and a right-aligned sign-off written with `::: 顶格` and `::: 靠右`; on the kaiti and song templates numbers stay as written and a one-page document shows no page number. The contract is a transcription and keeps its punctuation and spaces with `punctuation_mode: preserve`.
