#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/settings_manager.py

Gestión de configuración de Wiki Local.
Compatible con Python estándar.
"""

import json
from pathlib import Path


DEFAULT_SETTINGS = {
    "site_title": "Wiki Local",
    "default_page": "Inicio",
    "language": "es",
    "theme": "light",
    "compact_mode": False,
    "autosave": True,
    "preview": True,
    "syntax_highlighting": True,
    "attachments_path": "attachments",
    "backup_path": "backups",
    "max_upload_mb": 100,
    "backup_days": 30,
    "items_per_page": 20
}


class SettingsManager:

    def __init__(self, config_file):
        self.config_file = Path(config_file)
        self.settings = DEFAULT_SETTINGS.copy()

    def load(self):

        if self.config_file.exists():
            data = json.loads(
                self.config_file.read_text(
                    encoding="utf-8"
                )
            )
            self.settings.update(data)

        return self.settings

    def save(self):

        self.config_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.config_file.write_text(
            json.dumps(
                self.settings,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value

    def update(self, values):
        self.settings.update(values)

    def reset(self):
        self.settings = DEFAULT_SETTINGS.copy()

    def reload(self):
        self.settings = DEFAULT_SETTINGS.copy()
        return self.load()

    def as_dict(self):
        return dict(self.settings)
