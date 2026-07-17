#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/database.py
Gestión de la base de datos SQLite.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime


class Database:

    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

    def initialize(self):
        conn = self.connect()

        conn.execute("""
        CREATE TABLE IF NOT EXISTS pages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category TEXT,
            content TEXT,
            created TEXT,
            modified TEXT
        )
        """)

        conn.commit()

    def get_pages(self):
        cur = self.connection.execute(
            "SELECT * FROM pages ORDER BY title"
        )
        return cur.fetchall()

    def get_page(self, slug):
        cur = self.connection.execute(
            "SELECT * FROM pages WHERE slug=?",
            (slug,)
        )
        return cur.fetchone()

    def add_page(self, title, slug, category, content):

        now = datetime.now().isoformat()

        self.connection.execute(
            """
            INSERT INTO pages
            (
                title,
                slug,
                category,
                content,
                created,
                modified
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                title,
                slug,
                category,
                content,
                now,
                now,
            )
        )

        self.connection.commit()

    def update_page(
        self,
        slug,
        title,
        category,
        content
    ):

        now = datetime.now().isoformat()

        self.connection.execute(
            """
            UPDATE pages
            SET
                title=?,
                category=?,
                content=?,
                modified=?
            WHERE slug=?
            """,
            (
                title,
                category,
                content,
                now,
                slug
            )
        )

        self.connection.commit()

    def delete_page(self, slug):

        self.connection.execute(
            "DELETE FROM pages WHERE slug=?",
            (slug,)
        )

        self.connection.commit()
