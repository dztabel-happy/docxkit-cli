# DocxKit Markdown Contract

Use this reference when writing Markdown input for `docx-kit build`.

## Metadata

```markdown
---
title: 项目复盘报告
subtitle: v0.1
author: DocxKit
client: 内部验证
date: 2026-07-01
confidentiality: 内部资料
---
```

Supported keys: `title`, `subtitle`, `author`, `client`, `date`, `language`, `confidentiality`, `template`.

`template` defaults to `executive-cn-docx`. `executive-cn` is accepted as a ReportKit alias.

## Sections

- If frontmatter has `title`, `#` is a level-1 report section.
- If frontmatter has no `title`, the first `#` becomes the cover title.
- Use `##` and `###` for lower levels.
- Do not manually number headings. Write `# 研究背景与方法论`, not `# 一、研究背景与方法论`; write `## 资料来源`, not `## （一）资料来源`.

## Blocks

```markdown
普通段落会变成 paragraph。

- 无序列表会变成 bullet_list。

1. 有序列表会变成 ordered_list。

> 普通引用会变成 quote。
```

Prefer paragraphs, bullet lists, ordered lists, tables, figures, and code blocks for normal report content. Use callouts only for rare high-signal emphasis.

## Captions

Place captions directly before every table and figure.

```markdown
表：渠道效率对比
| 渠道 | 状态 | 说明 |
| --- | --- | --- |
| Partner Program | 继续投入 | 线索质量稳定。 |

图：结算瀑布图
![瀑布图](assets/waterfall.png)
```

Use `表[compact]：标题` for dense tables and `表[landscape]：标题` for wide tables that must remain intact.

## Tables

Keep tables as real row/column data. If cells become long paragraphs, move the explanation into surrounding prose or split the table.

DocxKit infers column widths for normal Markdown tables. Use direct `report.json` with `widths` only when a table needs exact control.

## Figures

Image paths are resolved relative to the Markdown file. Keep alt text short and different from the formal `图：` caption.

## Callouts

```markdown
> [!note] 关键说明
> 这句话必须从正文中被快速扫到。

> [!risk] 风险提示
> 只在用户明确需要视觉风险框时使用。
```

Supported kinds: `note`, `insight`, `risk`, `warning`. `tip` is normalized to `note`.

## Code Blocks

````markdown
```json renderer_contract
{
  "renderer": "docx-kit",
  "template": "executive-cn-docx"
}
```
````

The first word after the opening fence is the language. The remaining text becomes the optional code-block title.

## Page Breaks

Use `---PAGE---` only when the user explicitly asks for a hard page break. Normal reports should rely on automatic Word/WPS pagination.

## Direct report.json

Use direct `report.json` only when Markdown cannot express the required structure or exact table widths. Supported first-stage block types are:

```text
paragraph
table
figure
ordered_list
bullet_list
quote
code_block
callout
page_break
```

Compatibility blocks can exist in explicit JSON, but Markdown should not generate them for ordinary reports:

```text
definition_list
checklist
metric_grid
equation
inline_math
```
