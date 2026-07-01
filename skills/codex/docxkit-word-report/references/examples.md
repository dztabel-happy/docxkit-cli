# DocxKit Markdown Examples

Use these examples as patterns. Replace content with the user's prepared material; do not invent sources.

## Uploaded Materials To Word Report

```markdown
---
title: 用户资料整理报告
subtitle: 基于已上传材料
author: DocxKit
date: 2026-07-01
confidentiality: 内部资料
---

# 执行摘要

本报告基于用户上传材料整理，目标是把分散信息合并为可交付、可编辑的 Word 报告。阶段判断是：当前材料已经足够形成第一版报告，后续重点是补充数据来源和结论边界。

# 关键发现

- 需求集中在稳定导出和审美一致性。
- 用户希望 Agent 在最终交付阶段自动调用 Word 导出能力。
- 后续需要继续扩展跨平台安装体验。

表：交付重点
| 维度 | 当前判断 | 后续动作 |
| --- | --- | --- |
| 内容 | 已具备基础结构 | 补充更多真实案例 |
| 样式 | 已形成第一版模板 | 持续视觉回归 |
| 分发 | npm 可安装 | 扩展平台包 |
```

## Direct Skill Invocation

```markdown
---
title: 项目复盘报告
subtitle: 阶段交付复盘
author: DocxKit
date: 2026-07-01
---

# 本阶段结论

项目已经形成从 Agent 准备内容到 CLI 输出 Word 的基础闭环。

> [!note] 关键说明
> Word 输出应保持可编辑，而不是把内容固化成图片。

# 后续计划

1. 扩展真实样例。
2. 完善跨平台二进制。
3. 继续优化模板组件。
```

## Figure And Code

````markdown
---
title: 渲染能力验证
author: DocxKit
date: 2026-07-01
---

# 执行摘要

这份样张用于验证表格、图片、代码块和提示块的基础组合。

图：示例架构图
![架构图](assets/architecture.png)

```json renderer_contract
{
  "renderer": "docx-kit",
  "template": "executive-cn-docx"
}
```
````
