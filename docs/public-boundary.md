# DocxKit Public Boundary

`docxkit-cli` 是对外 npm 入口仓库，不承载核心渲染能力。

## 仓库职责

本仓库包含：

- `package.json`
- npm wrapper：`npm/docx-kit.cjs`
- 平台包 metadata：`npm/platform-packages/*/package.json`
- 用户 README
- Codex skill：`skills/codex/docxkit-word-report`
- 公开示例和截图

本仓库不包含：

- `.NET` / OpenXML renderer 源码；
- Word 模板源码；
- schemas；
- 测试；
- release preflight；
- 私有产品说明；
- npm token。

主包不包含二进制。平台包目录在发布前会放入当前平台 self-contained binary。
public 仓库必须通过 `.gitignore` 忽略平台二进制：

```gitignore
npm/platform-packages/*/docx-kit
npm/platform-packages/*/docx-kit.exe
```

## npm 包结构

```text
@dztabel/docxkit
  public npm wrapper
  - bin: docx-kit, docxkit
  - optionalDependencies 指向平台包

@dztabel/docxkit-darwin-arm64
  platform packages
  - 只包含当前平台 self-contained binary
```

MVP 只发布 `@dztabel/docxkit-darwin-arm64`。Linux 和 Windows 平台包是跨平台构建阶段的后续项。

## Agent skill

```text
skills/codex/docxkit-word-report
```

该 skill 负责指导 Agent 把用户上传材料、LLM 调研内容、Markdown 或 `report.json` 整理后调用 `docx-kit` 导出 Word。

边界：

- skill 不负责自行调研或编造来源；
- skill 不修改 core 模板或 OpenXML；
- skill 输出 `report.docx` 和可继续编辑的 `report.json`；
- 正常分页交给 Word/WPS，`---PAGE---` 只作为显式分页逃生口。

## 产品验收

产品验收以 npm 安装态为准：

```bash
npm install @dztabel/docxkit
npx --no-install docx-kit --version
npx --no-install docx-kit build content.md --out ./report
```

验收通过条件：

- 用户无需安装 Python、.NET SDK、Typst 或 Microsoft Word；
- stdout 是单个 JSON；
- `build-result.json` 与 stdout 完全一致；
- 输出包含 `report.docx`、`report.json`、`build-result.json`；
- `report.docx` 完整复刻 ReportKit 默认 `executive-cn` 格式；
- 主包 tarball 不包含 core 源码、模板源码、schemas、tests 或二进制；
- 平台包 tarball 只包含当前平台二进制和 package metadata。

## 发布凭证和发布方式

npm 已在本机用户级配置中登录。后续 LLM / Agent 发布前只需要验证当前登录态：

```bash
npm whoami
npm ping
```

禁止读取、打印或提交任何 npm / GitHub token；禁止把 token 写入仓库、README、脚本、日志样例或构建产物。

本机 GitHub 已验证可用：`gh auth status` 通过，账号 `dztabel-happy`，具备 `repo`、`workflow` 权限，可推送 GitHub。

完整发布步骤见：

```text
/Users/dztmacmini/project/zhiyun/docxkit-cli-core/docs/release-runbook.md
```
