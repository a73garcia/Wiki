#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/history.py

Gestión del historial de versiones de las páginas.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime


class HistoryManager:

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def initialize(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS page_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_slug TEXT NOT NULL,
            title TEXT,
            category TEXT,
            content TEXT,
            action TEXT,
            author TEXT,
            comment TEXT,
            created TEXT
        )
        """)
        self.conn.commit()

    def add_version(
        self,
        page_slug,
        title,
        category,
        content,
        action="Edición",
        author="Sistema",
        comment=""
    ):

        self.conn.execute(
            """
            INSERT INTO page_history(
                page_slug,
                title,
                category,
                content,
                action,
                author,
                comment,
                created
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                page_slug,
                title,
                category,
                content,
                action,
                author,
                comment,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()

    def list_history(self, page_slug=None):

        if page_slug:

            cur = self.conn.execute(
                """
                SELECT *
                FROM page_history
                WHERE page_slug=?
                ORDER BY created DESC
                """,
                (page_slug,)
            )

        else:

            cur = self.conn.execute(
                """
                SELECT *
                FROM page_history
                ORDER BY created DESC
                """
            )

        return cur.fetchall()

    def get_version(self, version_id):

        cur = self.conn.execute(
            """
            SELECT *
            FROM page_history
            WHERE id=?
            """,
            (version_id,)
        )

        return cur.fetchone()

    def delete_history(self, page_slug):

        self.conn.execute(
            """
            DELETE FROM page_history
            WHERE page_slug=?
            """,
            (page_slug,)
        )

        self.conn.commit()
