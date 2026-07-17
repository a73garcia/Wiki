#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/search_controller.py

Controlador del buscador de Wiki Local.
"""

from core.template_engine import TemplateEngine
from core.indexer import WikiIndexer


class SearchController:

    def __init__(self,
                 indexer: WikiIndexer,
                 template_engine: TemplateEngine):
        self.indexer = indexer
        self.templates = template_engine

    def search(self, query):

        if not query:
            return self.templates.render(
                "search.html",
                {
                    "query": "",
                    "results": "<p>Introduzca un texto para buscar.</p>"
                }
            )

        pages = self.indexer.search(query)

        rows = []

        for page in pages:

            title = page.get("title", "")
            slug = page.get("slug", "")
            category = page.get("category", "")

            snippet = self.indexer.highlight(
                page.get("content", "")[:250],
                query
            )

            rows.append(f"""
<div class="search-result">
    <h2><a href="/page/{slug}">{title}</a></h2>
    <div class="search-category">{category}</div>
    <p>{snippet}...</p>
</div>
""")

        if not rows:
            rows.append("<p>No se encontraron resultados.</p>")

        return self.templates.render(
            "search.html",
            {
                "query": query,
                "results": "\n".join(rows)
            }
        )

    def rebuild_index(self, pages):
        self.indexer.rebuild(pages)

    def statistics(self):
        return self.indexer.statistics()
