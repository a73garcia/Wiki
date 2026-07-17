#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/backup.py

Copias de seguridad para Wiki Local.
Solo utiliza la biblioteca estándar de Python.
"""

from pathlib import Path
from datetime import datetime
import shutil
import zipfile


class BackupManager:

    def __init__(self, backup_dir):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, paths):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = self.backup_dir / f"wiki_backup_{timestamp}.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:

            for item in paths:
                p = Path(item)

                if not p.exists():
                    continue

                if p.is_file():
                    zf.write(p, arcname=p.name)
                else:
                    for f in p.rglob("*"):
                        if f.is_file():
                            zf.write(f, arcname=f.relative_to(p.parent))

        return zip_path

    def restore_backup(self, zip_file, destination):

        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_file, "r") as zf:
            zf.extractall(destination)

    def list_backups(self):

        return sorted(
            self.backup_dir.glob("wiki_backup_*.zip"),
            reverse=True
        )

    def delete_backup(self, backup_file):

        backup = Path(backup_file)

        if backup.exists():
            backup.unlink()

    def cleanup(self, keep=10):

        backups = self.list_backups()

        for old in backups[keep:]:
            old.unlink()

    def copy_database(self, database_file):

        database_file = Path(database_file)

        target = self.backup_dir / (
            database_file.stem +
            "_" +
            datetime.now().strftime("%Y%m%d_%H%M%S") +
            database_file.suffix
        )

        shutil.copy2(database_file, target)

        return target
