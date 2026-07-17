#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/markdown_parser.py

Parser Markdown ligero sin dependencias externas.
"""

from __future__ import annotations

import html
import re


class MarkdownParser:

    def __init__(self):
        self.rules = [
            (r"^### (.*)$", r"<h3>\1</h3>"),
            (r"^## (.*)$", r"<h2>\1</h2>"),
            (r"^# (.*)$", r"<h1>\1</h1>"),
            (r"\*\*(.*?)\*\*", r"<strong>\1</strong>"),
            (r"\*(.*?)\*", r"<em>\1</em>"),
            (r"`([^`]*)`", r"<code>\1</code>"),
            (r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>')
        ]

    def parse(self, text: str) -> str:

        text = html.escape(text)

        lines = []

        for line in text.splitlines():

            converted = line

            for pattern, replacement in self.rules:
                converted = re.sub(pattern, replacement, converted)

            if converted.strip():

                if not converted.startswith("<h"):
                    converted = f"<p>{converted}</p>"

            lines.append(converted)

        return "\n".join(lines)


def markdown_to_html(text: str) -> str:
    return MarkdownParser().parse(text)


if __name__ == "__main__":

    sample = """
# Wiki Local

## Primera página

Este es un **texto** con *cursiva*.

Visita [OpenAI](https://openai.com)

`print("Hola")`
"""

    print(markdown_to_html(sample))
