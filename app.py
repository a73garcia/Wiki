#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wiki Local - app.py
Versión inicial del proyecto.
"""
from __future__ import annotations
import logging, sqlite3, sys
from pathlib import Path

APP_NAME="Wiki Local"
APP_VERSION="1.0.0"
HOST="127.0.0.1"
PORT=8080

ROOT_DIR=Path(__file__).resolve().parent
CORE_DIR=ROOT_DIR/"core"
DATABASE_DIR=ROOT_DIR/"database"
STATIC_DIR=ROOT_DIR/"static"
TEMPLATES_DIR=ROOT_DIR/"templates"
PAGES_DIR=ROOT_DIR/"pages"
ATTACHMENTS_DIR=ROOT_DIR/"attachments"
BACKUPS_DIR=ROOT_DIR/"backups"
LOGS_DIR=ROOT_DIR/"logs"
DB_FILE=DATABASE_DIR/"wiki.db"
LOG_FILE=LOGS_DIR/"wiki.log"

DIRECTORIES=(CORE_DIR,DATABASE_DIR,STATIC_DIR,TEMPLATES_DIR,PAGES_DIR,ATTACHMENTS_DIR,BACKUPS_DIR,LOGS_DIR)

def create_directories():
    for d in DIRECTORIES:
        d.mkdir(parents=True,exist_ok=True)

def configure_logger():
    LOGS_DIR.mkdir(parents=True,exist_ok=True)
    logger=logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt=logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
        fh=logging.FileHandler(LOG_FILE,encoding="utf-8")
        fh.setFormatter(fmt)
        ch=logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger

def initialize_database(logger):
    DATABASE_DIR.mkdir(parents=True,exist_ok=True)
    if DB_FILE.exists():
        logger.info("Base de datos existente.")
        return
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute("""CREATE TABLE pages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        category TEXT,
        content TEXT,
        created TEXT,
        modified TEXT)""")
    conn.commit()
    conn.close()
    logger.info("Base de datos creada.")

def main():
    print("="*60)
    print(f"{APP_NAME} {APP_VERSION}")
    print("="*60)
    create_directories()
    logger=configure_logger()
    initialize_database(logger)
    logger.info("Proyecto inicializado.")

if __name__=="__main__":
    main()
