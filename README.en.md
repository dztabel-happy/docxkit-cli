<h1 align="center">DocxKit</h1>

<p align="center">Word report export for agents</p>

<p align="center">
  <a href="README.zh-CN.md">中文</a>
  ·
  <a href="#install">Install</a>
  ·
  <a href="#quick-start">Quick Start</a>
  ·
  <a href="#preview">Preview</a>
</p>

<p align="center">
  <img alt="npm" src="https://img.shields.io/npm/v/@dztabel/docxkit?label=npm">
  <img alt="platforms" src="https://img.shields.io/badge/platform-macOS%20arm64-blue">
</p>

---

Users provide source material or a report goal. The agent organizes the content, and DocxKit exports the final result as a polished, editable Word `.docx` report.

Users can provide any material the agent can read and understand, such as:

- Documents, spreadsheets, web pages, screenshots, or existing reports.
- Project materials, research notes, meeting notes, or data summaries.
- A clear report topic for the agent to research and organize.

## Preview

These screenshots show DocxKit's default Word report output.

| | |
|:---:|:---:|
| <sub><strong>Cover</strong></sub> | <sub><strong>Table of contents</strong></sub> |
| <img src="examples/showcase/reference/01-cover.png" alt="DocxKit cover" width="320"> | <img src="examples/showcase/reference/02-toc.png" alt="DocxKit table of contents" width="320"> |
| <sub><strong>Body and visual blocks</strong></sub> | <sub><strong>Continuation page</strong></sub> |
| <img src="examples/showcase/reference/03-body.png" alt="DocxKit body and visual blocks" width="320"> | <img src="examples/showcase/reference/04-continuation.png" alt="DocxKit continuation page" width="320"> |

## Install

### 1. Install the CLI

```bash
npm install -g @dztabel/docxkit
docx-kit --version
```

Output like this means the CLI is installed:

```text
docx-kit 0.1.16
```

### 2. Install one agent skill

#### 2.1 Codex

```bash
node -e "const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process');const root=cp.execSync('npm root -g',{encoding:'utf8'}).trim();const src=path.join(root,'@dztabel','docxkit','skills','docxkit');const dest=path.join(os.homedir(),'.agents','skills','docxkit');fs.rmSync(dest,{recursive:true,force:true});fs.mkdirSync(path.dirname(dest),{recursive:true});fs.cpSync(src,dest,{recursive:true});console.log('Codex skill installed');"
```

Check the Codex skill in your terminal:

```bash
node -e "const fs=require('fs'),os=require('os'),path=require('path');const p=path.join(os.homedir(),'.agents','skills','docxkit','SKILL.md');if(!fs.existsSync(p))process.exit(1);console.log('Codex skill installed');"
```

This output means the skill is installed:

```text
Codex skill installed
```

Open Codex and type `$docxkit`. If you can select the skill with `Tab`, it is ready. If it does not appear, press `Cmd+K` / `Ctrl+K`, choose `Force Reload Skills`, or reopen Codex.

#### 2.2 Claude Code

```bash
node -e "const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process');const root=cp.execSync('npm root -g',{encoding:'utf8'}).trim();const src=path.join(root,'@dztabel','docxkit','skills','docxkit');const dest=path.join(os.homedir(),'.claude','skills','docxkit');fs.rmSync(dest,{recursive:true,force:true});fs.mkdirSync(path.dirname(dest),{recursive:true});fs.cpSync(src,dest,{recursive:true});console.log('Claude Code skill installed');"
```

Check the Claude Code skill in your terminal:

```bash
node -e "const fs=require('fs'),os=require('os'),path=require('path');const p=path.join(os.homedir(),'.claude','skills','docxkit','SKILL.md');if(!fs.existsSync(p))process.exit(1);console.log('Claude Code skill installed');"
```

This output means the skill is installed:

```text
Claude Code skill installed
```

Open Claude Code and type `/docxkit`. If you can select the skill, it is ready. If it does not appear, run `/reload-skills` and try again. Older Claude Code versions may need a new window.

## Quick Start

### 1. Generate a Word report from provided material

```text
$docxkit Read my uploaded Excel, PDF, and meeting notes, then turn them into a formal project review report and export it as Word.
/docxkit Read my uploaded Excel, PDF, and meeting notes, then turn them into a formal project review report and export it as Word.
```

### 2. Research a topic and generate a Word report

```text
$docxkit Research recent developments in China's energy storage industry, organize the findings into an industry report, and export it as Word.
/docxkit Research recent developments in China's energy storage industry, organize the findings into an industry report, and export it as Word.
```

### 3. Turn a rough draft into a deliverable report

```text
$docxkit Rewrite this rough draft into a clear formal analysis report and export it as Word.
/docxkit Rewrite this rough draft into a clear formal analysis report and export it as Word.
```

### 4. Revise a generated report from feedback

```text
$docxkit Compress the report you just generated to 8 pages, rewrite chapter 2 for management readers, and export a new Word document.
/docxkit Compress the report you just generated to 8 pages, rewrite chapter 2 for management readers, and export a new Word document.
```

The agent handles source reading, research, writing, formatting, and Word export.

## Technical Details

The agent turns the material into DocxKit-ready intermediate content and runs:

```bash
docx-kit build prepared-report.md --out ./report
```

DocxKit outputs:

```text
report/report.docx
report/report.json
report/build-result.json
```

## Troubleshooting

The public beta supports macOS Apple Silicon.

If global npm install skips optional dependencies, install the matching platform package explicitly:

```bash
npm install -g @dztabel/docxkit @dztabel/docxkit-darwin-arm64
```

When reporting a build failure, include:

- `docx-kit --version`
- `report/build-result.json`
- A minimal `content.md` that reproduces the issue

## Repository Scope

This public repository contains npm wrapper metadata, the command shim, public skills, documentation, and lightweight preview assets.

Renderer source, private templates, schemas, visual regression samples, and platform binaries are not included here. Platform binaries are distributed through npm platform packages.

## License

DocxKit is distributed through npm as a proprietary CLI binary. This repository provides the public wrapper, skills, and documentation for installing and using the CLI.
