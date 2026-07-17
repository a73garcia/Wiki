#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/router.py

Router principal de Wiki Local.
"""

from __future__ import annotations

from urllib.parse import parse_qs


class Router:

    def __init__(self):
        self.routes = {}

    def add(self, method: str, path: str, handler):
        key = (method.upper(), path)
        self.routes[key] = handler

    def resolve(self, method: str, path: str):
        key = (method.upper(), path)
        return self.routes.get(key)

    def dispatch(self, handler):

        route = self.resolve(handler.command, handler.path.split("?")[0])

        if route:
            return route(handler)

        self.not_found(handler)

    @staticmethod
    def query(handler):
        if "?" not in handler.path:
            return {}
        return parse_qs(handler.path.split("?", 1)[1])

    @staticmethod
    def send_html(handler, html, status=200):

        body = html.encode("utf-8")

        handler.send_response(status)
        handler.send_header("Content-Type", "text/html; charset=utf-8")
        handler.send_header("Content-Length", str(len(body)))
        handler.end_headers()

        handler.wfile.write(body)

    @staticmethod
    def redirect(handler, location):

        handler.send_response(302)
        handler.send_header("Location", location)
        handler.end_headers()

    @staticmethod
    def not_found(handler):

        html = """
        <html>
        <head><title>404</title></head>
        <body>
            <h1>404 - Página no encontrada</h1>
        </body>
        </html>
        """

        Router.send_html(handler, html, 404)


if __name__ == "__main__":

    router = Router()

    def index(handler):
        Router.send_html(
            handler,
            "<h1>Wiki Local funcionando</h1>"
        )

    router.add("GET", "/", index)

    print("Router inicializado correctamente.")
