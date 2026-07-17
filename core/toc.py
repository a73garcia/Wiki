#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/toc.py

Generador automático de Tabla de Contenidos (TOC)
a partir de encabezados Markdown.
"""

import html
import re


class TableOfContents:

    def __init__(self):
        self._heading = re.compile(r"^(#{1,6})\s+(.*)$")

    def generate(self, markdown_text):
        toc = []
        processed = []

        for line in markdown_text.splitlines():
            m = self._heading.match(line)
            if not m:
                processed.append(line)
                continue

            level = len(m.group(1))
            title = m.group(2).strip()
            anchor = self._slugify(title)

            toc.append({
                "level": level,
                "title": title,
                "anchor": anchor
            })

            processed.append(
                f"{'#' * level} <a id=\"{anchor}\"></a>{title}"
            )

        return toc, "\n".join(processed)

    def render_html(self, toc):

        if not toc:
            return ""

        html_out = [
            '<nav class="wiki-toc">',
            '<div class="wiki-toc-title">Contenido</div>',
            "<ul>"
        ]

        current = 1

        for item in toc:

            while current < item["level"]:
                html_out.append("<ul>")
                current += 1

            while current > item["level"]:
                html_out.append("</ul>")
                current -= 1

            html_out.append(
                f'<li><a href="#{item["anchor"]}">'
                f'{html.escape(item["title"])}</a></li>'
            )

        while current > 1:
            html_out.append("</ul>")
            current -= 1

        html_out.extend([
            "</ul>",
            "</nav>"
        ])

        return "\n".join(html_out)

    def _slugify(self, text):

        text = text.lower()

        replacements = {
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "ü": "u",
            "ñ": "n"
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = re.sub(r"[^a-z0-9\s-]", "", text)
        text = re.sub(r"\s+", "-", text.strip())
        text = re.sub(r"-+", "-", text)

        return text
