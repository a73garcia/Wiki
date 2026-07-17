#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/settings_controller.py

Controlador de configuración para Wiki Local.
"""

from core.settings_manager import SettingsManager
from core.template_engine import TemplateEngine


class SettingsController:

    def __init__(self,
                 settings_manager: SettingsManager,
                 template_engine: TemplateEngine):
        self.settings = settings_manager
        self.templates = template_engine

    def view(self):
        config = self.settings.load()
        return self.templates.render(
            "settings.html",
            config
        )

    def save(self, data):
        self.settings.update(data)
        self.settings.save()
        return True

    def reset(self):
        self.settings.reset()
        self.settings.save()
        return self.view()

    def reload(self):
        self.settings.reload()
        return self.view()

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def export(self):
        return self.settings.as_dict()
