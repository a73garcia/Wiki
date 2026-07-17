#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/file_manager.py

Utilidades para la gestión segura de archivos y directorios.
Compatible con Python estándar.
"""

from pathlib import Path
import hashlib
import shutil
from datetime import datetime


class FileManager:

    def __init__(self, root_path):
        self.root = Path(root_path).resolve()

    def ensure_directory(self, path):
        p = self._safe_path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def read_text(self, path, encoding="utf-8"):
        return self._safe_path(path).read_text(encoding=encoding)

    def write_text(self, path, content, encoding="utf-8"):
        p = self._safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding=encoding)
        return p

    def copy(self, source, destination):
        src = self._safe_path(source)
        dst = self._safe_path(destination)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return dst

    def move(self, source, destination):
        src = self._safe_path(source)
        dst = self._safe_path(destination)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return dst

    def delete(self, path):
        p = self._safe_path(path)
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            shutil.rmtree(p)

    def exists(self, path):
        return self._safe_path(path).exists()

    def list_files(self, path=".", pattern="*"):
        return sorted(self._safe_path(path).glob(pattern))

    def checksum(self, path, algorithm="sha256"):
        h = hashlib.new(algorithm)
        with self._safe_path(path).open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    def info(self, path):
        p = self._safe_path(path)
        s = p.stat()
        return {
            "name": p.name,
            "path": str(p),
            "size": s.st_size,
            "modified": datetime.fromtimestamp(s.st_mtime).isoformat(),
            "is_file": p.is_file(),
            "is_dir": p.is_dir(),
        }

    def _safe_path(self, relative_path):
        p = (self.root / relative_path).resolve()
        if not str(p).startswith(str(self.root)):
            raise ValueError("Ruta fuera del directorio permitido.")
        return p
