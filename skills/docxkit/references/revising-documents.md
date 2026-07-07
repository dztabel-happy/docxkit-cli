# Revising an Already-Generated Report

When the user is not satisfied with a `.docx` DocxKit produced and asks for changes, this is fast and safe — **because the source of truth is the Markdown / `report.json`, not the `.docx`.** You never edit the Word file or its OOXML. You edit the source and rebuild; the gate loop re-validates automatically.

## The rule

- **Never hand-edit the generated `.docx`.** It is a derived artifact. Any change made directly in Word/WPS is lost on the next rebuild and cannot be merged back.
- **Always change the editable source, then rebuild.** The source is `./output_docx/content.md` (if you kept the Markdown) or `./output_docx/report.json` (always written by every build, and fully round-trippable — you can rebuild straight from it).

## Locating the source

1. If `content.md` is still in the output directory, edit that.
2. Otherwise edit `report.json` — it is the canonical editable artifact and `docx-kit build ./output_docx/report.json --out ./output_docx` regenerates everything.
3. If neither is available (the user only has the `.docx` and it was hand-edited outside DocxKit), you cannot cleanly merge. Reconstruct the content as Markdown and treat it as a fresh build — say so plainly to the user.

## Common revisions

| Ask | What to change |
| --- | --- |
| Reword / fix a fact / tighten prose | Edit the paragraph text in the source. |
| Add / remove / reorder a section | Add, delete, or move the `#`/`##` heading and its blocks. Table/figure/equation numbers renumber automatically; re-check any `见表/图/式 x.x` references (the `dangling_caption_reference` error lists the new numbers). |
| Add or drop a table / figure / source | Edit the block and its prose reference together; keep every captioned exhibit referenced (avoids `unreferenced_caption`). |
| Switch typography (楷体 ↔ 宋体+黑体) | Change `template:` in the frontmatter; content is untouched. |
| Add a chart | If ChartKit is installed, render the figure to `assets/*.png`, then reference it with `图：` — DocxKit places, numbers, and cross-references it. |

## Versioning

- **Overwrite** the same `--out ./output_docx` when the user wants the previous build replaced (the default).
- **Keep both** by building into a versioned sibling: `docx-kit build ./output_docx/content.md --out ./output_docx_v2`. Use this when the user may want to compare or revert.

## After every revision

Re-run the same gate loop as a first build: read `errors` / `warnings` / `checks` in the result, fix at the reported `path`, and rebuild until clean. Then return the new `.docx` path and the edited source path.

## Showing what changed (tracked changes)

To hand the user a Word file with tracked-changes markup of what changed between two versions you generated, use `docx-kit redline --from <old.report.json> --to <new.report.json> --out <dir>` — it renders the new report with insertions/deletions marked, reviewable and acceptable in Word/WPS. This works only between DocxKit-generated versions (both sources available); it is not for redlining an arbitrary uploaded `.docx`.
