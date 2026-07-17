#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/categories.py

Gestión de categorías para Wiki Local.
"""

from datetime import datetime
import sqlite3


class CategoryManager:

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def initialize(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            parent TEXT,
            color TEXT DEFAULT '#4A90E2',
            icon TEXT DEFAULT '📁',
            description TEXT,
            created TEXT
        )
        """)
        self.conn.commit()

    def create(self, name, slug,
               parent=None,
               color="#4A90E2",
               icon="📁",
               description=""):

        self.conn.execute(
            """
            INSERT INTO categories(
                name,
                slug,
                parent,
                color,
                icon,
                description,
                created
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                name,
                slug,
                parent,
                color,
                icon,
                description,
                datetime.now().isoformat()
            )
        )
        self.conn.commit()

    def update(self, category_id,
               name,
               parent,
               color,
               icon,
               description):

        self.conn.execute(
            """
            UPDATE categories
            SET
                name=?,
                parent=?,
                color=?,
                icon=?,
                description=?
            WHERE id=?
            """,
            (
                name,
                parent,
                color,
                icon,
                description,
                category_id
            )
        )
        self.conn.commit()

    def delete(self, category_id):

        self.conn.execute(
            "DELETE FROM categories WHERE id=?",
            (category_id,)
        )
        self.conn.commit()

    def list(self):

        cur = self.conn.execute(
            """
            SELECT
                c.*,
                (
                    SELECT COUNT(*)
                    FROM pages p
                    WHERE p.category=c.slug
                ) AS page_count
            FROM categories c
            ORDER BY name
            """
        )

        return cur.fetchall()

    def get(self, slug):

        cur = self.conn.execute(
            """
            SELECT *
            FROM categories
            WHERE slug=?
            """,
            (slug,)
        )

        return cur.fetchone()

    def children(self, parent_slug):

        cur = self.conn.execute(
            """
            SELECT *
            FROM categories
            WHERE parent=?
            ORDER BY name
            """,
            (parent_slug,)
        )

        return cur.fetchall()
