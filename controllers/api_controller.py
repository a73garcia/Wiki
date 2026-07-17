#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/api_controller.py

API REST interna para Wiki Local.
Devuelve estructuras Python listas para serializar a JSON.
"""

from core.page_manager import PageManager
from core.categories import CategoryManager
from core.tags import TagManager
from core.history import HistoryManager
from core.settings_manager import SettingsManager
from core.indexer import WikiIndexer


class ApiController:

    def __init__(self,
                 page_manager: PageManager,
                 category_manager: CategoryManager,
                 tag_manager: TagManager,
                 history_manager: HistoryManager,
                 settings_manager: SettingsManager,
                 indexer: WikiIndexer):
        self.pages = page_manager
        self.categories = category_manager
        self.tags = tag_manager
        self.history = history_manager
        self.settings = settings_manager
        self.indexer = indexer

    def get_pages(self):
        return self.pages.list_pages()

    def get_page(self, slug):
        return self.pages.get_page(slug)

    def search(self, query):
        return self.indexer.search(query)

    def get_categories(self):
        return self.categories.list()

    def get_tags(self):
        return self.tags.list()

    def get_history(self, page_slug=None):
        return self.history.list_history(page_slug)

    def get_settings(self):
        return self.settings.as_dict()

    def get_statistics(self):
        return {
            "index": self.indexer.statistics(),
            "pages": len(self.pages.list_pages()),
            "categories": len(self.categories.list()),
            "tags": len(self.tags.list())
        }

    def health(self):
        return {
            "status": "ok",
            "service": "Wiki Local API",
            "version": "1.0"
        }
