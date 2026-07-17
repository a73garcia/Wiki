#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/search.py

Motor de búsqueda para Wiki Local.
"""

from __future__ import annotations

import re


class SearchEngine:

    def __init__(self):
        pass

    @staticmethod
    def normalize(text: str) -> str:
        if text is None:
            return ""
        return text.lower().strip()

    def contains(self, query: str, text: str) -> bool:
        query = self.normalize(query)
        text = self.normalize(text)
        return query in text

    def score(self, query: str, title: str, content: str) -> int:
        score = 0

        query = self.normalize(query)
        title = self.normalize(title)
        content = self.normalize(content)

        if query in title:
            score += 100

        score += content.count(query) * 5

        return score

    def search(self, query: str, pages):

        results = []

        for page in pages:

            title = page["title"]
            content = page["content"]

            if self.contains(query, title) or self.contains(query, content):

                results.append({
                    "id": page["id"],
                    "title": title,
                    "slug": page["slug"],
                    "category": page["category"],
                    "score": self.score(query, title, content)
                })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    def highlight(self, query: str, text: str):

        if not query:
            return text

        regex = re.compile(
            re.escape(query),
            re.IGNORECASE
        )

        return regex.sub(
            lambda m: "<mark>%s</mark>" % m.group(0),
            text
        )


if __name__ == "__main__":

    pages = [
        {
            "id": 1,
            "title": "Splunk",
            "slug": "splunk",
            "category": "SIEM",
            "content": "Consultas SPL para Splunk Enterprise."
        },
        {
            "id": 2,
            "title": "Proofpoint",
            "slug": "proofpoint",
            "category": "Email",
            "content": "Administración de Proofpoint."
        }
    ]

    engine = SearchEngine()

    for item in engine.search("splunk", pages):
        print(item)
