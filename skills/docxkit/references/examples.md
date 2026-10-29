# DocxKit Markdown Examples

Use these examples as patterns, after deciding whether the user wants a report or a plain document (see `SKILL.md`). The examples are fictional: replace their content with the user's prepared material and their illustrative source links with verified ones; do not invent sources. Inputs that refer to tables or figures by number declare `numbering_rule: native-v1`; a short text without such references needs no metadata at all.

## Full-Featured Formal Report

This is the shape a serious deliverable should take: a `##` subsection hierarchy, prose-led sections, captioned tables (including a landscape one) and a figure introduced by number before they appear, numbered block equations cited from the prose, inline math, and inline `[n]` citations tied to the source chapter. Save it as `examples/report.md` in this repository; its image is supplied at `examples/assets/migration.png`.

````markdown
---
title: 华东区渠道效能季度评估
template: executive-cn-docx
document_mode: report
heading_numbering: auto
numbering_rule: native-v1
subtitle: 2026 年第二季度
author: 咨询项目组
client: 示例集团
date: 2026-07-05
confidentiality: 内部资料
list_of_tables: true
---

# 执行摘要

以下内容与数据均为虚构演示，不作为业务结论。本季度华东区渠道整体效能稳中有升，线索质量改善但转化节奏放缓[1]。核心判断是：预算应从泛投放转向高意向渠道，配套调整销售承接节奏。

# 渠道效能分析

## 效率指标走势

渠道效率的核心指标是单位成本产出比，记为 \(E_c\)，其季度综合值由式 2.1 给出：

```math title=渠道效率综合值
E = \frac{1}{n} \sum_{i=1}^{n} \frac{R_i}{C_i}
```

由式 2.1 可见，效率提升主要来自高意向渠道占比上升。具体对比见表 2.1。

表：核心渠道效率对比
| 渠道 | 效率值 | 环比 | 判断 |
| --- | --- | --- | --- |
| 伙伴推荐 | 3.2 | +0.4 | 继续加码 |
| 内容获客 | 2.1 | +0.1 | 维持 |
| 信息流投放 | 0.9 | -0.3 | 收缩 |

## 区域结构变化

区域间差异扩大：核心城市依靠置换需求保持稳定，非核心城市对价格与售后更敏感[2]。跨区域的完整变量跟踪见表 2.2。

表[landscape]：区域渠道变量季度跟踪
| 区域 | 主力渠道 | 线索量环比 | 转化率 | 客单价变化 | 售后评分 | 主要风险 | 建议动作 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 上海 | 伙伴推荐 | +12% | 8.3% | 持平 | 4.6 | 承接容量不足 | 扩充售前编制 |
| 杭州 | 内容获客 | +6% | 6.1% | 略降 | 4.4 | 内容同质化 | 建立行业案例库 |
| 苏州 | 信息流投放 | -9% | 3.2% | 下降 | 4.1 | 获客成本上行 | 预算转移至伙伴渠道 |

# 执行建议

如图 3.1 所示，预算迁移路径分三步落地，先收缩低效投放，再扩充承接能力，最后建立复盘节奏。

图：预算迁移路径
![预算迁移三步路径](assets/migration.png)

> [!risk] 预算风险
> 若只调整投放而不同步调整销售承接，效率改善将在执行层被抵消。建议预算调整与承接扩容绑定审批。

落地顺序如下：

1. 两周内完成信息流预算下调与伙伴渠道加码。
2. 一个月内完成售前团队扩充与话术更新。
3. 季度末按式 2.1 复算效率值并复盘。

# 资料来源

1. [季度渠道数据看板](https://example.com/dashboard)，内部经营分析系统，2026-07-05 访问。
2. [区域消费行为调研](https://example.com/survey)，第三方调研机构，2026-06-28 访问。
````

## Plain Documents

A plain document has no cover, no contents and no header. On the default 楷体 template (and on 宋体) headings and list numbers are kept as written and the page number appears only when there is a second page.

### Letter — no settings at all

No metadata: the content has no chapter headings, so it is built as a plain document, and with no first-line `# 标题` it has no title block. The salutation and the sign-off use alignment containers; the numbered lines are a native list numbered as written; the table has no caption, so it takes no table number. Save as `examples/letter.md`.

```markdown
::: 顶格
青原资料室：
:::

来函收悉。现就资料交接事项答复如下。

1. 交接时间定于 10 月 28 日上午。
2. 经办人电话：139\*\*\*\*2468。

| 核对项 | 内容 |
| --- | --- |
| 交接方式 | 现场\|邮寄 |
| 资料编号 | Z\*\*\*\*\*99 |

::: 靠右
松溪档案服务组

2026 年 10 月 13 日
:::
```

### Memo — a plain document with chapters

For short deliverables a flat structure is fine; keep prose first and sources real. Chapter headings would make an undeclared input a report, so `document_mode: document` is written and the title goes in the metadata. Headings carry no automatic numbers. Save as `examples/memo.md`.

```markdown
---
title: 项目复盘备忘
document_mode: document
---

# 本阶段结论

项目已形成从内容准备到 Word 交付的闭环，本阶段重点验证了交付质量门禁的有效性。

> [!note] 关键说明
> Word 输出保持完全可编辑，收件人可以直接修改后回传。

# 后续计划

1. 扩充真实交付样例。
2. 将质量门禁纳入例行验收。
```

### Notice on the 公文模板

Only the template is chosen. On the 公文模板 an undeclared input is always a plain document, the first `#` is its title, and the template supplies its own heading numbers (一、二、) and list numbers, so headings are written without numbers. The page number always shows. Save as `examples/notice.md`.

```markdown
---
template: executive-cn-official-docx
numbering_rule: native-v1
---

# 关于开展年度档案清点的通知

::: 顶格
各部门：
:::

为做好年度归档工作，现就档案清点有关事项通知如下。

# 清点安排

1. 清点时间为 10 月 20 日至 24 日。
2. 各部门联系人工号按 A\*\*\*\*07 的形式登记。

# 提交材料

需提交的材料见表 1。

表：材料清单
| 名称 | 份数 |
| --- | --- |
| 档案清点表 | 2 |

::: 靠右
松溪档案服务组

2026 年 10 月 13 日
:::
```

## Transcription — Contract

A transcription keeps the original clause numbers and characters: `punctuation_mode: preserve` keeps punctuation and spaces, the clause headings stay as written (the default in a plain document on 楷体 and 宋体), and the numbered lines keep their numbers. Do not add sections, captions or references the original does not have. The metadata supplies the title; both `#` headings are clauses. It is set in 宋体 only because this user asked for it. The two parties sign side by side: one `::: 并排` block, each pane with three lines of room for the stamp (inside a pane the room is kept wherever the block lands on the page). Save as `examples/contract.md`.

```markdown
---
title: 资料整理服务协议
template: executive-cn-song-docx
document_mode: document
punctuation_mode: preserve
numbering_rule: native-v1
---

::: 顶格
甲方：青原资料室

乙方：松溪档案服务组
:::

# 第一条 服务内容

1. 乙方按甲方提供的清单整理纸质资料，保持原有卷次顺序。
2. 甲方联系人电话：138\*\*\*\*5678。

# 第二条 交接

交接物品见表 1。

表：交接清单
| 项目 | 说明 |
| --- | --- |
| 资料编号 | Z\*\*\*\*\*99 |
| 交付形式 | 纸质\|电子 |

::: 并排 widths=1,1
甲方（盖章）：

::: 留白 三行
签订日期：____年____月____日
---COLUMN---
乙方（盖章）：

::: 留白 三行
签订日期：____年____月____日
:::
```

## Forms, Room for a Stamp, a Stated Format

These use what `docx-kit templates` lists under `format.features`; check it first on an installation you did not just update.

### Form to be filled in by hand

A form that is printed and filled in with a pen. The 宋体 template; every part is a grid with no header row (`header=false`: the first row is data too), labels in bold, and a minimum row height of 8–10 mm so there is room to write. The part title is the first row of its table, merged across the whole width, so each part is a table of its own and the parts stand apart. The photo box is the last column merged down four rows with `^` (4 × 9 mm holds a 35 mm photo); its width is in millimetres, the weights of each table adding up to the 160 mm text width, and the label columns of the three tables line up. The declaration and the signatures come last, in a table with a taller row height. Save as `examples/form.md`.

```markdown
---
template: executive-cn-song-docx
---

# 实习生报名登记表

::: 表格 appearance=grid header=false row_height=9mm widths=26,39,26,39,30
| **一、个人信息** | < | < | < | < |
| --- | --- | --- | --- | --- |
| **姓名** |  | **性别** |  | 贴一寸照片处 |
| **出生日期** |  | **民族** |  | ^ |
| **学校** |  | **专业** |  | ^ |
| **联系电话** |  | **电子邮箱** |  | ^ |
| **通讯地址** |  | < | < | < |
:::

::: 表格 appearance=grid header=false row_height=9mm widths=26,39,26,69
| **二、实习意向** | < | < | < |
| --- | --- | --- | --- |
| **意向部门** |  | **到岗日期** |  |
| **每周天数** |  | **实习期限** |  |
| **特长说明** |  | < | < |
:::

::: 表格 appearance=grid header=false row_height=12mm widths=26,39,26,69
| **三、声明与签字** | < | < | < |
| --- | --- | --- | --- |
| 本人保证以上信息真实有效。 | < | < | < |
| **本人签字** |  | **日期** |  |
| **审核人签字** |  | **日期** |  |
:::
```

- A row whose columns differ from the rest — an 18-box ID number under a form of five columns — is a table of its own directly below, with one column per box (`widths=26,` then eighteen equal weights making up the rest); an empty line separates the two tables.
- When one page is tight, put each part title in a left column merged down instead of a row of its own (`| **一、个人信息** | **姓名** |  | … |`, then `| ^ | **出生日期** |  | … |`): it saves a row per part, and the parts can share one table when their columns agree.
- The user wants one page of A4: run `docx-kit pdf` on the result and check the page count before delivery. A second page that is blank means the last table ends right at the foot of the page and the empty paragraph Word keeps after a final table moved over: make a row height or a part a little smaller.

### Certificate with room for the stamp

`::: 留白 三行` stands on the line above the `::: 靠右` container, so the whole sign-off moves down together. Save as `examples/certificate.md`.

```markdown
# 在职证明

兹证明林晓（工号 A\*\*\*\*07）自 2021 年 3 月起在我公司工作，现任市场部经理。

特此证明。

::: 留白 三行
::: 靠右
青原科技有限公司（盖章）

2026 年 10 月 14 日
:::
```

### Notice in a stated format

The user named sizes, a fixed line spacing and the four margins; only those are written, and the receipt's `effective_document.format` shows what took effect. Fonts the user names go in the same way (`title_font: 方正小标宋简体`, `body_font: 仿宋_GB2312`) and should be written; this example leaves them out only so that it builds with `--strict` on any machine — on one that lacks a stated font the build warns with `font_not_found`. As in the other 公文 notice, the template numbers the headings. Save as `examples/stated-format.md`.

```markdown
---
template: executive-cn-official-docx
title_size: 二号
body_size: 三号
body_line_spacing: 28pt
margin_top: 3.7cm
margin_bottom: 3.5cm
margin_left: 2.8cm
margin_right: 2.6cm
---

# 关于调整办公时间的通知

::: 顶格
各部门：
:::

根据季节变化，经研究决定，自 11 月 1 日起调整办公时间，现将有关事项通知如下。

# 办公时间

上午 8:30 至 12:00，下午 13:30 至 17:30。

# 有关要求

各部门要提前安排好值班和对外服务窗口，确保工作衔接。

特此通知。

::: 靠右
青原科技有限公司综合管理部

2026 年 10 月 14 日
:::
```

### A line with its date at the right (résumé)

One side-by-side block per line; consecutive blocks stack as rows with nothing between them.

```markdown
::: 并排 widths=2,1
**青原科技有限公司　市场部经理**
---COLUMN---
::: 靠右
2021.03 — 至今
:::
:::

::: 并排 widths=2,1
**松溪档案服务组　项目助理**
---COLUMN---
::: 靠右
2018.07 — 2021.02
:::
:::
```

## Build the Examples

Run from this repository's root after installing the CLI:

```bash
docx-kit build examples/report.md --out ./report --filename report.docx
docx-kit build examples/memo.md --out ./memo --filename memo.docx
docx-kit build examples/contract.md --out ./contract --filename contract.docx
docx-kit build examples/notice.md --out ./notice --filename notice.docx
docx-kit build examples/letter.md --out ./letter --filename letter.docx
docx-kit build examples/form.md --out ./form --filename form.docx
docx-kit build examples/certificate.md --out ./certificate --filename certificate.docx
docx-kit build examples/stated-format.md --out ./stated-format --filename stated-format.docx
```

Each builds with no error and no warning. `--strict`, which fails on warning-level checks (never on `info`), is for CI and batch pipelines; when you deliver, build without it and iterate until `checks` and `warnings` are clean.
