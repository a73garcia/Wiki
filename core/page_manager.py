#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/page_manager.py

Gestión centralizada de páginas de la Wiki.
"""

from datetime import datetime


class PageManager:

    def __init__(self, database, history):
        self.db = database
        self.history = history

    def create_page(self, title, slug, content,
                    category="", tags="", author="Sistema"):

        now = datetime.now().isoformat()

        self.db.execute(
            """
            INSERT INTO pages
            (title, slug, content, category, tags, created, modified)
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                title,
                slug,
                content,
                category,
                tags,
                now,
                now,
            ),
        )

        self.db.commit()

        self.history.add_version(
            slug,
            title,
            category,
            content,
            action="Creación",
            author=author,
        )

    def update_page(self, slug, title, content,
                    category="", tags="", author="Sistema",
                    comment=""):

        now = datetime.now().isoformat()

        self.db.execute(
            """
            UPDATE pages
            SET
                title=?,
                content=?,
                category=?,
                tags=?,
                modified=?
            WHERE slug=?
            """,
            (
                title,
                content,
                category,
                tags,
                now,
                slug,
            ),
        )

        self.db.commit()

        self.history.add_version(
            slug,
            title,
            category,
            content,
            action="Edición",
            author=author,
            comment=comment,
        )

    def delete_page(self, slug):

        page = self.get_page(slug)

        if not page:
            return False

        self.history.add_version(
            slug,
            page["title"],
            page["category"],
            page["content"],
            action="Eliminación",
        )

        self.db.execute(
            "DELETE FROM pages WHERE slug=?",
            (slug,),
        )

        self.db.commit()
        return True

    def get_page(self, slug):

        cur = self.db.execute(
            "SELECT * FROM pages WHERE slug=?",
            (slug,),
        )

        row = cur.fetchone()

        if row is None:
            return None

        columns = [c[0] for c in cur.description]

        return dict(zip(columns, row))

    def list_pages(self):

        cur = self.db.execute(
            """
            SELECT *
            FROM pages
            ORDER BY title
            """
        )

        return cur.fetchall()

    def search(self, text):

        pattern = f"%{text}%"

        cur = self.db.execute(
            """
            SELECT *
            FROM pages
            WHERE
                title LIKE ?
                OR content LIKE ?
                OR tags LIKE ?
            ORDER BY modified DESC
            """,
            (
                pattern,
                pattern,
                pattern,
            ),
        )

        return cur.fetchall()

    def page_exists(self, slug):

        cur = self.db.execute(
            """
            SELECT COUNT(*)
            FROM pages
            WHERE slug=?
            """,
            (slug,),
        )

        return cur.fetchone()[0] > 0
