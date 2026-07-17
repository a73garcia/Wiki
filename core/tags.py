#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/tags.py

Gestión de etiquetas para Wiki Local.
"""

import sqlite3


class TagManager:

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def initialize(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#6c757d'
        );

        CREATE TABLE IF NOT EXISTS page_tags(
            page_slug TEXT NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY(page_slug, tag_id)
        );
        """)
        self.conn.commit()

    def create(self, name, color="#6c757d"):
        self.conn.execute(
            "INSERT OR IGNORE INTO tags(name,color) VALUES(?,?)",
            (name, color)
        )
        self.conn.commit()

    def assign(self, page_slug, tag_name):
        cur = self.conn.execute(
            "SELECT id FROM tags WHERE name=?",
            (tag_name,)
        )
        row = cur.fetchone()
        if row is None:
            self.create(tag_name)
            cur = self.conn.execute(
                "SELECT id FROM tags WHERE name=?",
                (tag_name,)
            )
            row = cur.fetchone()

        self.conn.execute(
            "INSERT OR IGNORE INTO page_tags(page_slug,tag_id) VALUES(?,?)",
            (page_slug, row[0])
        )
        self.conn.commit()

    def remove(self, page_slug, tag_name):
        self.conn.execute(
            """
            DELETE FROM page_tags
            WHERE page_slug=?
            AND tag_id=(SELECT id FROM tags WHERE name=?)
            """,
            (page_slug, tag_name)
        )
        self.conn.commit()

    def list(self):
        cur = self.conn.execute("""
        SELECT
            t.id,
            t.name,
            t.color,
            COUNT(pt.page_slug) AS usage_count
        FROM tags t
        LEFT JOIN page_tags pt
            ON t.id=pt.tag_id
        GROUP BY t.id,t.name,t.color
        ORDER BY t.name
        """)
        return cur.fetchall()

    def tags_for_page(self, page_slug):
        cur = self.conn.execute("""
        SELECT t.name,t.color
        FROM tags t
        JOIN page_tags pt
            ON pt.tag_id=t.id
        WHERE pt.page_slug=?
        ORDER BY t.name
        """, (page_slug,))
        return cur.fetchall()

    def search(self, tag_name):
        cur = self.conn.execute("""
        SELECT page_slug
        FROM page_tags
        WHERE tag_id=(SELECT id FROM tags WHERE name=?)
        ORDER BY page_slug
        """, (tag_name,))
        return cur.fetchall()
