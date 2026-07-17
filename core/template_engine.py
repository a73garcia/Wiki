#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/template_engine.py

Motor de plantillas muy ligero para Wiki Local.
Compatible con Python estándar.
"""

from pathlib import Path
import re


class TemplateEngine:

    def __init__(self, templates_path):
        self.templates_path = Path(templates_path)

    def load(self, template_name):

        template_file = self.templates_path / template_name

        if not template_file.exists():
            raise FileNotFoundError(template_file)

        return template_file.read_text(
            encoding="utf-8"
        )

    def render(self, template_name, context=None):

        if context is None:
            context = {}

        html = self.load(template_name)

        html = self.replace_variables(
            html,
            context
        )

        return html

    def replace_variables(
        self,
        html,
        context
    ):

        pattern = re.compile(
            r"\{\{\s*(.*?)\s*\}\}"
        )

        def replace(match):

            key = match.group(1)

            return str(
                context.get(
                    key,
                    ""
                )
            )

        return pattern.sub(
            replace,
            html
        )


if __name__ == "__main__":

    engine = TemplateEngine("../templates")

    print(
        engine.render(
            "index.html",
            {
                "total_pages": 12,
                "total_categories": 4,
                "total_favorites": 7,
                "recent_pages": "<li>Inicio</li>",
                "activity": ""
            }
        )
    )
