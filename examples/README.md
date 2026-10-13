# 示例 / Examples

示例内容均为虚构。 / All content is fictional.

| 文件 / File | 用途 / Purpose | 模板 / Template | 模式、标题编号 / Mode, headings |
| --- | --- | --- | --- |
| [report.md](report.md) | 分章报告 / Report | 楷体 / KaiTi | report, auto |
| [memo.md](memo.md) | 短备忘 / Memo | 楷体 / KaiTi | document, auto |
| [contract.md](contract.md) | 保留条款编号的合同 / Contract keeping its clause numbers | 宋体 / SimSun | document, none |
| [notice.md](notice.md) | 第一个标题作文档标题的通知 / Notice titled by its first heading | 公文 / Official | document, none |
| [letter.md](letter.md) | 没有标题的函件 / Letter without a title | 楷体 / KaiTi | document, none |

在仓库根目录执行 / Run from the repository root:

```bash
docx-kit build examples/report.md --out ./report --filename report.docx --strict
docx-kit build examples/memo.md --out ./memo --filename memo.docx --strict
docx-kit build examples/contract.md --out ./contract --filename contract.docx --strict
docx-kit build examples/notice.md --out ./notice --filename notice.docx --strict
docx-kit build examples/letter.md --out ./letter --filename letter.docx --strict
```

合同、通知、函件用 `punctuation_mode: preserve` 保留原文的标点和空格；报告和备忘用默认的标点规范化。 / The contract, notice and letter keep their punctuation and spaces with `punctuation_mode: preserve`; the report and memo use the default normalization.
