#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración global de Wiki Local.
"""

APP_NAME = "Wiki Local"
APP_VERSION = "1.0.0"

HOST = "127.0.0.1"
PORT = 8080

AUTO_OPEN_BROWSER = True
DEBUG = True

DATABASE_NAME = "wiki.db"

LOG_LEVEL = "INFO"

DEFAULT_PAGE = "Inicio"

SITE_TITLE = "Wiki Local"

ENABLE_BACKUPS = True
BACKUP_KEEP_DAYS = 30

ITEMS_PER_PAGE = 25

MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100 MB

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".xlsx",
    ".pptx",
    ".txt",
    ".md",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".zip",
    ".csv",
    ".json",
    ".xml",
    ".py",
    ".ps1",
    ".sql",
    ".log",
]

THEMES = [
    "light",
    "dark",
]

DEFAULT_THEME = "light"

SUPPORTED_CODE_LANGUAGES = [
    "python",
    "splunk",
    "powershell",
    "sql",
    "json",
    "xml",
    "bash",
    "cmd",
    "yaml",
]
