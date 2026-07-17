#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Wiki Local - app.py (Parte 1)"""

from __future__ import annotations

import logging
import sqlite3
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

APP_NAME="Wiki Local"
APP_VERSION="1.0.0"
HOST="127.0.0.1"
PORT=8080

ROOT_DIR=Path(__file__).resolve().parent
CORE_DIR=ROOT_DIR/'core'
DATABASE_DIR=ROOT_DIR/'database'
STATIC_DIR=ROOT_DIR/'static'
TEMPLATES_DIR=ROOT_DIR/'templates'
PAGES_DIR=ROOT_DIR/'pages'
ATTACHMENTS_DIR=ROOT_DIR/'attachments'
BACKUPS_DIR=ROOT_DIR/'backups'
LOGS_DIR=ROOT_DIR/'logs'
DB_FILE=DATABASE_DIR/'wiki.db'
LOG_FILE=LOGS_DIR/'wiki.log'
