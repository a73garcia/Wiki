#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/import_export.py

Importación y exportación de contenidos para Wiki Local.
Solo usa la biblioteca estándar.
"""

from pathlib import Path
import json
import shutil
import zipfile


class ImportExportManager:

    def export_page_markdown(self, page, output_file):

        output = Path(output_file)

        metadata = [
            "---",
            f"title: {page.get('title','')}",
            f"slug: {page.get('slug','')}",
            f"category: {page.get('category','')}",
            f"tags: {page.get('tags','')}",
            "---",
            "",
        ]

        output.write_text(
            "\n".join(metadata) + page.get("content", ""),
            encoding="utf-8"
        )

        return output

    def import_page_markdown(self, markdown_file):

        text = Path(markdown_file).read_text(encoding="utf-8")

        page = {
            "title": "",
            "slug": "",
            "category": "",
            "tags": "",
            "content": ""
        }

        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) == 3:
                for line in parts[1].splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        page[k.strip()] = v.strip()
                page["content"] = parts[2].strip()
        else:
            page["content"] = text

        return page

    def export_json(self, data, output_file):

        output = Path(output_file)
        output.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        return output

    def import_json(self, json_file):

        return json.loads(
            Path(json_file).read_text(encoding="utf-8")
        )

    def export_zip(self, source_dirs, output_zip):

        output = Path(output_zip)

        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
            for item in source_dirs:
                p = Path(item)
                if not p.exists():
                    continue
                if p.is_file():
                    zf.write(p, arcname=p.name)
                else:
                    for f in p.rglob("*"):
                        if f.is_file():
                            zf.write(f, arcname=f.relative_to(p.parent))

        return output

    def import_zip(self, zip_file, destination):

        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_file, "r") as zf:
            zf.extractall(destination)

        return destination

    def copy_tree(self, source, destination):

        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=True
        )
