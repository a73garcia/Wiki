#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/indexer.py

Índice interno y motor de búsqueda para Wiki Local.
"""

import re
from collections import defaultdict


class WikiIndexer:

    def __init__(self):
        self.index = defaultdict(set)
        self.pages = {}

    def clear(self):
        self.index.clear()
        self.pages.clear()

    def add_page(self, page):

        slug = page["slug"]
        self.pages[slug] = page

        text = " ".join([
            page.get("title", ""),
            page.get("content", ""),
            page.get("category", ""),
            page.get("tags", "")
        ])

        for token in self._tokenize(text):
            self.index[token].add(slug)

    def remove_page(self, slug):

        if slug not in self.pages:
            return

        del self.pages[slug]

        for token in list(self.index.keys()):
            self.index[token].discard(slug)

            if not self.index[token]:
                del self.index[token]

    def rebuild(self, pages):

        self.clear()

        for page in pages:
            self.add_page(page)

    def search(self, query, limit=20):

        scores = defaultdict(int)

        for token in self._tokenize(query):

            for slug in self.index.get(token, set()):
                scores[slug] += 1

        results = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        return [
            self.pages[slug]
            for slug, _ in results
        ]

    def highlight(self, text, query):

        for token in self._tokenize(query):

            text = re.sub(
                rf"(?i)\b({re.escape(token)})\b",
                r"<mark>\1</mark>",
                text
            )

        return text

    def statistics(self):

        return {
            "pages": len(self.pages),
            "terms": len(self.index),
            "relations": sum(
                len(v)
                for v in self.index.values()
            )
        }

    @staticmethod
    def _tokenize(text):

        return re.findall(
            r"[A-Za-zÀ-ÿ0-9_]+",
            text.lower()
        )
