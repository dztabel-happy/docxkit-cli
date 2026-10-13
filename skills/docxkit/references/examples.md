# DocxKit Markdown Examples

Use these patterns after deciding whether the user wants a report or a plain document (see `SKILL.md`). The examples are fictional; replace their content and illustrative source links with verified user materials. Inputs that refer to tables or figures by number declare `numbering_rule: native-v1`; a short text without such references needs no metadata at all.

## Full-Featured Formal Report

Save this as `examples/report.md` in this repository; its image is supplied at `examples/assets/migration.png`. It uses a cover and TOC, real subsections, a landscape table, a figure, native equations and source references.

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

Chapter headings would make an undeclared input a report, so `document_mode: document` is written and the title goes in the metadata. Headings carry no automatic numbers. Save as `examples/memo.md`.

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

A transcription keeps the original clause numbers and characters: `punctuation_mode: preserve` keeps punctuation and spaces, the clause headings stay as written (the default in a plain document on 楷体 and 宋体), and the numbered lines keep their numbers. Do not add sections, captions or references the original does not have. The metadata supplies the title; both `#` headings are clauses. It is set in 宋体 only because this user asked for it. Two signature blocks cannot be set side by side in this version, so they follow one another. Save as `examples/contract.md`.

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

::: 靠右
甲方（盖章）：____________

乙方（盖章）：____________

签订日期：____年____月____日
:::
```

## Build the Examples

Run from this repository's root after installing the CLI:

```bash
docx-kit build examples/report.md --out ./report --filename report.docx --strict
docx-kit build examples/memo.md --out ./memo --filename memo.docx --strict
docx-kit build examples/contract.md --out ./contract --filename contract.docx --strict
docx-kit build examples/notice.md --out ./notice --filename notice.docx --strict
docx-kit build examples/letter.md --out ./letter --filename letter.docx --strict
```

`--strict` fails on warning and error checks; `info` checks do not fail it.
