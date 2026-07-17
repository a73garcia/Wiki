#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/navigation.py

Componentes de navegación para Wiki Local.
"""

from collections import defaultdict


class NavigationManager:

    def breadcrumbs(self, page):
        """
        page = {
            "title": "...",
            "category": "...",
            "slug": "..."
        }
        """
        items = [("Inicio", "/")]

        if page.get("category"):
            items.append(
                (
                    page["category"],
                    f"/category/{page['category']}"
                )
            )

        items.append(
            (
                page.get("title", ""),
                f"/page/{page.get('slug','')}"
            )
        )

        return items

    def recent_pages(self, pages, limit=10):

        return sorted(
            pages,
            key=lambda p: p.get("modified", ""),
            reverse=True
        )[:limit]

    def related_pages(self, page, pages, limit=10):

        category = page.get("category")
        tags = set(page.get("tags", "").split(","))

        related = []

        for other in pages:

            if other.get("slug") == page.get("slug"):
                continue

            score = 0

            if other.get("category") == category:
                score += 5

            other_tags = set(other.get("tags", "").split(","))

            score += len(tags & other_tags)

            if score:
                related.append((score, other))

        related.sort(reverse=True, key=lambda x: x[0])

        return [p for _, p in related[:limit]]

    def category_tree(self, categories):

        tree = defaultdict(list)

        roots = []

        for c in categories:

            parent = c.get("parent")

            if parent:
                tree[parent].append(c)
            else:
                roots.append(c)

        return roots, tree

    def previous_next(self, pages, slug):

        ordered = sorted(
            pages,
            key=lambda p: p.get("title", "").lower()
        )

        for i, page in enumerate(ordered):

            if page.get("slug") != slug:
                continue

            previous = ordered[i - 1] if i > 0 else None
            nxt = ordered[i + 1] if i < len(ordered) - 1 else None

            return previous, nxt

        return None, None

    def most_viewed(self, pages, limit=10):

        return sorted(
            pages,
            key=lambda p: p.get("views", 0),
            reverse=True
        )[:limit]
