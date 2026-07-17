#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/editor_controller.py

Controlador del editor de Wiki Local.
"""

from core.template_engine import TemplateEngine
from core.page_manager import PageManager


class EditorController:

    def __init__(self,
                 page_manager: PageManager,
                 template_engine: TemplateEngine):
        self.page_manager = page_manager
        self.templates = template_engine

    def new(self):
        return self.templates.render(
            "editor.html",
            {
                "title": "",
                "slug": "",
                "category": "",
                "tags": "",
                "content": "",
                "comment": ""
            }
        )

    def edit(self, slug):
        page = self.page_manager.get_page(slug)

        if page is None:
            return None

        return self.templates.render(
            "editor.html",
            {
                "title": page.get("title", ""),
                "slug": page.get("slug", ""),
                "category": page.get("category", ""),
                "tags": page.get("tags", ""),
                "content": page.get("content", ""),
                "comment": ""
            }
        )

    def save(self, data):

        required = ("title", "slug", "content")

        for field in required:
            if not data.get(field, "").strip():
                raise ValueError(f"Campo obligatorio: {field}")

        if self.page_manager.page_exists(data["slug"]):
            self.page_manager.update_page(
                slug=data["slug"],
                title=data["title"],
                content=data["content"],
                category=data.get("category", ""),
                tags=data.get("tags", ""),
                comment=data.get("comment", "")
            )
            return "updated"

        self.page_manager.create_page(
            title=data["title"],
            slug=data["slug"],
            content=data["content"],
            category=data.get("category", ""),
            tags=data.get("tags", "")
        )

        return "created"

    def preview(self, markdown_renderer, markdown_text):
        return markdown_renderer.render(markdown_text)
