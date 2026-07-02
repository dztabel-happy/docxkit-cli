#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def run(cmd):
    subprocess.run([str(part) for part in cmd], check=True)


def render_python():
    configured = os.environ.get("DOCXKIT_RENDER_PYTHON")
    if configured and Path(configured).exists():
        return Path(configured)
    bundled = Path("/Users/dztmacmini/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3")
    if bundled.exists():
        return bundled
    return Path(sys.executable)


def numbered_sections(sections):
    numbers = [0, 0, 0]
    result = []
    for index, section in enumerate(sections, start=1):
        level = max(1, min(3, int(section.get("level") or 1)))
        numbers[level - 1] += 1
        for reset in range(level, 3):
            numbers[reset] = 0
        if level > 1 and numbers[0] == 0:
            numbers[0] = 1
        result.append((index, ".".join(str(value) for value in numbers[:level]), section["title"]))
    return result


def pdf_pages(pdf_path):
    text = subprocess.check_output(["pdftotext", str(pdf_path), "-"], text=True)
    return [page for page in text.split("\f") if page.strip()]


def toc_page_numbers(report_json, pdf_path):
    sections = numbered_sections(json.loads(report_json.read_text())["sections"])
    pages = pdf_pages(pdf_path)
    if not sections or not pages:
        return {}

    first_number, first_title = sections[0][1], sections[0][2]
    first_section = re.compile(rf"(^|\n)\s*{re.escape(first_number)}\s+{re.escape(first_title)}\s*(\n|$)")
    body_start = next((i for i, page in enumerate(pages) if first_section.search(page)), 2)
    mapped = {}
    for index, number, title in sections:
        pattern = re.compile(rf"(^|\n)\s*{re.escape(number)}\s+{re.escape(title)}\s*(\n|$)")
        for page_index, page in enumerate(pages[body_start:], start=body_start):
            if pattern.search(page):
                mapped[index] = str(page_index - body_start + 1)
                break
    return mapped


def patch_toc_cache(input_docx, output_docx, page_numbers):
    with zipfile.ZipFile(input_docx) as zin:
        document_xml = zin.read("word/document.xml").decode("utf-8")

    for index, page in page_numbers.items():
        pattern = re.compile(
            rf"(<w:instrText[^>]*>\s*PAGEREF\s+DocxKitSection{index}\s+\\h\s*</w:instrText>.*?"
            rf"<w:fldChar[^>]*w:fldCharType=\"separate\"[^>]*/>)(.*?)(<w:fldChar[^>]*w:fldCharType=\"end\"[^>]*/>)",
            re.S,
        )

        def replace(match):
            result = re.sub(r"<w:t[^>]*>.*?</w:t>", f"<w:t>{page}</w:t>", match.group(2), count=1)
            return match.group(1) + result + match.group(3)

        document_xml = pattern.sub(replace, document_xml, count=1)

    with zipfile.ZipFile(input_docx) as zin, zipfile.ZipFile(output_docx, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = document_xml.encode("utf-8") if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)


def render(renderer, docx, output_dir, emit_pdf):
    cmd = [render_python(), renderer, docx, "--output_dir", output_dir]
    if emit_pdf:
        cmd.append("--emit_pdf")
    run(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docx")
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--renderer", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--emit-pdf", action="store_true")
    args = parser.parse_args()

    docx = Path(args.docx)
    report_json = Path(args.report_json)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not shutil.which("pdftotext"):
        render(args.renderer, docx, output_dir, args.emit_pdf)
        return

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        first_render = tmp_dir / "first-render"
        patched_docx = tmp_dir / "report-toc-cache.docx"

        render(args.renderer, docx, first_render, True)
        pdf_path = first_render / f"{docx.stem}.pdf"
        page_numbers = toc_page_numbers(report_json, pdf_path)
        if not page_numbers:
            render(args.renderer, docx, output_dir, args.emit_pdf)
            return

        patch_toc_cache(docx, patched_docx, page_numbers)
        render(args.renderer, patched_docx, output_dir, args.emit_pdf)


if __name__ == "__main__":
    main()
