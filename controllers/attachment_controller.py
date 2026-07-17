#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controllers/attachment_controller.py

Controlador para la gestión de adjuntos.
"""

from core.attachments import AttachmentManager
from core.template_engine import TemplateEngine


class AttachmentController:

    def __init__(self,
                 attachment_manager: AttachmentManager,
                 template_engine: TemplateEngine):
        self.manager = attachment_manager
        self.templates = template_engine

    def list(self, page_slug):

        rows = []

        for item in self.manager.list(page_slug):
            attachment_id = item[0]
            name = item[2]
            kind = item[4]
            size = item[6]

            rows.append(f"""
<tr>
<td>{name}</td>
<td>{kind}</td>
<td>{size}</td>
<td>
<a href="/attachment/download/{attachment_id}">Abrir</a> |
<a href="/attachment/delete/{attachment_id}">Eliminar</a>
</td>
</tr>
""")

        return self.templates.render(
            "attachments.html",
            {
                "attachments": "\n".join(rows)
            }
        )

    def upload(self, page_slug, source_file):
        self.manager.add_file(page_slug, source_file)

    def add_link(self, page_slug, title, url):
        self.manager.add_link(page_slug, title, url)

    def delete(self, attachment_id):
        self.manager.delete(attachment_id)

    def get(self, attachment_id):
        return self.manager.get(attachment_id)

    @staticmethod
    def validate(filename, size_bytes,
                 allowed_extensions=None,
                 max_size_mb=100):

        if allowed_extensions is None:
            allowed_extensions = {
                ".pdf", ".doc", ".docx",
                ".xls", ".xlsx",
                ".ppt", ".pptx",
                ".txt", ".log",
                ".py", ".sql", ".json",
                ".xml", ".zip"
            }

        extension = "." + filename.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            raise ValueError(f"Tipo de archivo no permitido: {extension}")

        if size_bytes > max_size_mb * 1024 * 1024:
            raise ValueError("El archivo supera el tamaño máximo permitido.")

        return True
