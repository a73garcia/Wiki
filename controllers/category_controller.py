#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/category_controller.py

Controlador de categorías para Wiki Local.
"""

from core.categories import CategoryManager
from core.template_engine import TemplateEngine


class CategoryController:

    def __init__(self,
                 category_manager: CategoryManager,
                 template_engine: TemplateEngine,
                 page_manager=None):
        self.categories = category_manager
        self.templates = template_engine
        self.page_manager = page_manager

    def list(self):

        rows = []

        for cat in self.categories.list():
            rows.append(f"""
<tr>
<td>{cat[5]}</td>
<td>{cat[1]}</td>
<td>{cat[4]}</td>
<td>{cat[7]}</td>
<td>{cat[8]}</td>
</tr>
""")

        return self.templates.render(
            "categories.html",
            {
                "categories": "\n".join(rows)
            }
        )

    def create(self, data):
        self.categories.create(
            name=data["name"],
            slug=data["slug"],
            parent=data.get("parent"),
            color=data.get("color", "#4A90E2"),
            icon=data.get("icon", "📁"),
            description=data.get("description", "")
        )

    def update(self, category_id, data):
        self.categories.update(
            category_id,
            data["name"],
            data.get("parent"),
            data.get("color", "#4A90E2"),
            data.get("icon", "📁"),
            data.get("description", "")
        )

    def delete(self, category_id):
        self.categories.delete(category_id)

    def pages(self, category_slug):
        if self.page_manager is None:
            return []

        return [
            page for page in self.page_manager.list_pages()
            if page[3] == category_slug
        ]

    def children(self, parent_slug):
        return self.categories.children(parent_slug)
