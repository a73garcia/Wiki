#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/attachments.py

Gestión de archivos adjuntos y enlaces para Wiki Local.
Compatible con Python estándar.
"""

from pathlib import Path
import os
import shutil
import sqlite3
from datetime import datetime


class AttachmentManager:

    def __init__(self, connection: sqlite3.Connection, attachments_path):
        self.conn = connection
        self.attachments_path = Path(attachments_path)
        self.attachments_path.mkdir(parents=True, exist_ok=True)

    def initialize(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS attachments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_slug TEXT NOT NULL,
            name TEXT NOT NULL,
            original_name TEXT NOT NULL,
            attachment_type TEXT NOT NULL,
            location TEXT NOT NULL,
            size INTEGER,
            created TEXT
        )
        """)
        self.conn.commit()

    def add_file(self, page_slug, source_file):

        source = Path(source_file)

        if not source.exists():
            raise FileNotFoundError(source)

        destination = self.attachments_path / source.name

        shutil.copy2(source, destination)

        self.conn.execute(
            """
            INSERT INTO attachments(
                page_slug,
                name,
                original_name,
                attachment_type,
                location,
                size,
                created
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                page_slug,
                destination.name,
                source.name,
                "local",
                str(destination),
                destination.stat().st_size,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()

    def add_link(self, page_slug, title, url):

        self.conn.execute(
            """
            INSERT INTO attachments(
                page_slug,
                name,
                original_name,
                attachment_type,
                location,
                size,
                created
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                page_slug,
                title,
                title,
                "link",
                url,
                0,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()

    def list(self, page_slug):

        cur = self.conn.execute(
            """
            SELECT *
            FROM attachments
            WHERE page_slug=?
            ORDER BY name
            """,
            (page_slug,)
        )

        return cur.fetchall()

    def delete(self, attachment_id):

        cur = self.conn.execute(
            "SELECT attachment_type,location FROM attachments WHERE id=?",
            (attachment_id,)
        )

        row = cur.fetchone()

        if row:

            if row[0] == "local" and os.path.exists(row[1]):
                os.remove(row[1])

            self.conn.execute(
                "DELETE FROM attachments WHERE id=?",
                (attachment_id,)
            )

            self.conn.commit()

    def get(self, attachment_id):

        cur = self.conn.execute(
            "SELECT * FROM attachments WHERE id=?",
            (attachment_id,)
        )

        return cur.fetchone()
