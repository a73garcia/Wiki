#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/wiki_links.py

Gestión de enlaces internos tipo Wiki.

Sintaxis soportada:

[[Página]]
[[Página|Texto mostrado]]
"""

import html
import re


class WikiLinks:

    LINK_PATTERN = re.compile(r"\[\[(.+?)\]\]")

    def __init__(self, page_exists_callback=None):
        """
        page_exists_callback(slug)->bool
        """
        self.page_exists = page_exists_callback

    def render(self, text):

        def replace(match):

            value = match.group(1)

            if "|" in value:
                page, alias = value.split("|", 1)
            else:
                page = value
                alias = value

            slug = self.slugify(page)

            exists = True
            if self.page_exists:
                exists = self.page_exists(slug)

            css = "wiki-link" if exists else "wiki-link missing"

            return (
                f'<a class="{css}" '
                f'href="/page/{slug}">'
                f'{html.escape(alias)}</a>'
            )

        return self.LINK_PATTERN.sub(replace, text)

    def extract_links(self, text):

        links = []

        for match in self.LINK_PATTERN.finditer(text):

            value = match.group(1)

            if "|" in value:
                page = value.split("|", 1)[0]
            else:
                page = value

            links.append(self.slugify(page))

        return sorted(set(links))

    def backlinks(self, target_slug, pages):

        result = []

        for page in pages:

            slug = page.get("slug", "")

            if slug == target_slug:
                continue

            links = self.extract_links(
                page.get("content", "")
            )

            if target_slug in links:
                result.append(page)

        return result

    def orphan_pages(self, pages):

        linked = set()

        for page in pages:
            linked.update(
                self.extract_links(
                    page.get("content", "")
                )
            )

        return [
            page
            for page in pages
            if page.get("slug") not in linked
        ]

    @staticmethod
    def slugify(title):

        title = title.lower()

        table = str.maketrans({
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "ü": "u",
            "ñ": "n"
        })

        title = title.translate(table)

        title = re.sub(r"[^a-z0-9\s-]", "", title)
        title = re.sub(r"\s+", "-", title.strip())
        title = re.sub(r"-+", "-", title)

        return title
