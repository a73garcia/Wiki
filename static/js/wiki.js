#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
static/js/wiki.js

Lógica principal de la interfaz de Wiki Local.
Guardar con extensión .js
"""

class WikiApp {

    constructor() {
        this.init();
    }

    init() {
        this.configureNavigation();
        this.configureSearch();
        this.configureShortcuts();
        this.configureConfirmations();
        this.highlightCurrentMenu();
    }

    configureNavigation() {
        document.querySelectorAll("[data-link]").forEach(item => {
            item.addEventListener("click", e => {
                const url = item.dataset.link;
                if (url) {
                    window.location.href = url;
                }
            });
        });
    }

    configureSearch() {
        const box = document.getElementById("searchBox");
        if (!box) return;

        box.addEventListener("keydown", e => {
            if (e.key === "Enter") {
                const value = box.value.trim();
                if (value.length > 0) {
                    window.location.href = "/search?q=" + encodeURIComponent(value);
                }
            }
        });
    }

    configureShortcuts() {
        document.addEventListener("keydown", e => {

            if (e.ctrlKey && e.key.toLowerCase() === "k") {
                e.preventDefault();
                const box = document.getElementById("searchBox");
                if (box) box.focus();
            }

            if (e.ctrlKey && e.key.toLowerCase() == "n") {
                e.preventDefault();
                window.location.href="/editor";
            }

        });
    }

    configureConfirmations() {
        document.querySelectorAll("[data-confirm]").forEach(btn => {
            btn.addEventListener("click", e => {
                const msg = btn.dataset.confirm || "¿Continuar?";
                if (!confirm(msg)) {
                    e.preventDefault();
                }
            });
        });
    }

    highlightCurrentMenu() {
        document.querySelectorAll("nav a").forEach(a => {
            if (a.href === window.location.href) {
                a.classList.add("active");
            }
        });
    }

}

window.addEventListener("DOMContentLoaded", () => {
    new WikiApp();
});
