#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/syntax_highlighter.py

Resaltado de sintaxis ligero mediante expresiones regulares.
No requiere librerías externas.
"""

import html
import re


class SyntaxHighlighter:

    PATTERNS = {
        "python": [
            (r"\b(def|class|import|from|return|if|elif|else|for|while|try|except|with|as|pass|break|continue|lambda|yield|True|False|None)\b", "kw"),
            (r'".*?"|\'.*?\'', "str"),
            (r"#.*$", "com"),
        ],
        "sql": [
            (r"\b(SELECT|FROM|WHERE|GROUP BY|ORDER BY|INSERT|UPDATE|DELETE|JOIN|LEFT|RIGHT|INNER|OUTER|AND|OR|NOT|IN|LIKE|AS|COUNT|SUM|AVG|MIN|MAX)\b", "kw"),
            (r"'[^']*'", "str"),
        ],
        "powershell": [
            (r"\b(Get|Set|New|Remove|Write)-[A-Za-z]+\b", "kw"),
            (r"\$[A-Za-z_][A-Za-z0-9_]*", "var"),
            (r"#.*$", "com"),
        ],
        "spl": [
            (r"\b(search|index|stats|table|chart|timechart|eval|rex|spath|lookup|fields|sort|dedup|where)\b", "kw"),
            (r'"[^"]*"', "str"),
        ],
        "json": [
            (r'"[^"]*"\s*:', "key"),
            (r':\s*"[^"]*"', "str"),
        ],
        "xml": [
            (r"</?[^>]+?>", "tag"),
            (r'\b\w+="[^"]*"', "attr"),
        ],
    }

    def highlight(self, code, language="text"):
        text = html.escape(code)
        patterns = self.PATTERNS.get(language.lower(), [])

        for pattern, css in patterns:
            text = re.sub(
                pattern,
                lambda m: f'<span class="{css}">{m.group(0)}</span>',
                text,
                flags=re.MULTILINE | re.IGNORECASE,
            )
        return text
