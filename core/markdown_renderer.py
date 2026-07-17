#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/markdown_renderer.py

Renderizador Markdown ligero para Wiki Local.
Sin dependencias externas.
"""

import html
import re


class MarkdownRenderer:

    def __init__(self):
        self.code_languages = {
            "python": "language-python",
            "sql": "language-sql",
            "powershell": "language-powershell",
            "spl": "language-splunk",
            "json": "language-json",
            "xml": "language-xml",
            "bash": "language-bash",
        }

    def render(self, text):

        lines = text.splitlines()
        out = []

        in_code = False
        language = ""

        for line in lines:

            if line.startswith("```"):
                if not in_code:
                    language = line[3:].strip().lower()
                    css = self.code_languages.get(language, "language-text")
                    out.append(f'<pre class="{css}"><code>')
                    in_code = True
                else:
                    out.append("</code></pre>")
                    in_code = False
                continue

            if in_code:
                out.append(html.escape(line))
                continue

            if line.startswith("# "):
                out.append(f"<h1>{html.escape(line[2:])}</h1>")
            elif line.startswith("## "):
                out.append(f"<h2>{html.escape(line[3:])}</h2>")
            elif line.startswith("### "):
                out.append(f"<h3>{html.escape(line[4:])}</h3>")
            elif line.startswith("- "):
                out.append(f"<li>{self._inline(line[2:])}</li>")
            elif line.strip() == "":
                out.append("")
            else:
                out.append(f"<p>{self._inline(line)}</p>")

        return "\n".join(self._wrap_lists(out))

    def _inline(self, text):
        text = html.escape(text)

        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)

        return text

    def _wrap_lists(self, lines):
        result = []
        inside = False

        for line in lines:
            if line.startswith("<li>"):
                if not inside:
                    result.append("<ul>")
                    inside = True
                result.append(line)
            else:
                if inside:
                    result.append("</ul>")
                    inside = False
                result.append(line)

        if inside:
            result.append("</ul>")

        return result
