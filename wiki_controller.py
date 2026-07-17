#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/wiki_controller.py

Controlador principal de páginas de la Wiki.
"""

from core.page_manager import PageManager
from core.markdown_renderer import MarkdownRenderer
from core.template_engine import TemplateEngine


class WikiController:

    def __init__(self, page_manager: PageManager,
                 template_engine: TemplateEngine):
        self.page_manager = page_manager
        self.templates = template_engine
        self.renderer = MarkdownRenderer()

    def index(self):

        pages = self.page_manager.list_pages()

        items = []

        for page in pages:
            items.append(
                f'<li><a href="/page/{page[1]}">{page[0]}</a></li>'
            )

        return self.templates.render(
            "index.html",
            {
                "recent_pages": "\n".join(items),
                "activity": "",
                "total_pages": len(pages),
                "total_categories": "",
                "total_favorites": ""
            }
        )

    def view(self, slug):

        page = self.page_manager.get_page(slug)

        if page is None:
            return self.templates.render(
                "page.html",
                {
                    "title": "Página no encontrada",
                    "content": "<p>La página solicitada no existe.</p>"
                }
            )

        html = self.renderer.render(
            page["content"]
        )

        return self.templates.render(
            "page.html",
            {
                "title": page["title"],
                "content": html,
                "category": page.get("category", ""),
                "tags": page.get("tags", "")
            }
        )

    def create(self, data):

        self.page_manager.create_page(
            title=data["title"],
            slug=data["slug"],
            content=data["content"],
            category=data.get("category", ""),
            tags=data.get("tags", "")
        )

    def update(self, slug, data):

        self.page_manager.update_page(
            slug=slug,
            title=data["title"],
            content=data["content"],
            category=data.get("category", ""),
            tags=data.get("tags", ""),
            comment=data.get("comment", "")
        )

    def delete(self, slug):
        return self.page_manager.delete_page(slug)
