#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/history_controller.py

Controlador del historial de versiones.
"""

from core.history import HistoryManager
from core.template_engine import TemplateEngine


class HistoryController:

    def __init__(self,
                 history_manager: HistoryManager,
                 template_engine: TemplateEngine,
                 page_manager=None):
        self.history = history_manager
        self.templates = template_engine
        self.page_manager = page_manager

    def list(self, page_slug=None):

        rows = []

        for item in self.history.list_history(page_slug):
            rows.append(f"""
<tr>
<td>{item[1]}</td>
<td>{item[5]}</td>
<td>{item[6]}</td>
<td>{item[8]}</td>
<td>
<a href="/history/view/{item[0]}">Ver</a>
</td>
</tr>
""")

        return self.templates.render(
            "history.html",
            {
                "history_rows": "\n".join(rows)
            }
        )

    def view(self, version_id):
        return self.history.get_version(version_id)

    def restore(self, version_id):

        if self.page_manager is None:
            raise RuntimeError("PageManager no configurado.")

        version = self.history.get_version(version_id)

        if version is None:
            return False

        page_slug = version[1]
        title = version[2]
        category = version[3]
        content = version[4]

        self.page_manager.update_page(
            slug=page_slug,
            title=title,
            content=content,
            category=category,
            comment=f"Restaurada versión {version_id}"
        )

        return True

    def filter(self, page_slug=None,
               author=None,
               action=None):

        history = self.history.list_history(page_slug)

        result = []

        for item in history:

            if author and item[6] != author:
                continue

            if action and item[5] != action:
                continue

            result.append(item)

        return result
