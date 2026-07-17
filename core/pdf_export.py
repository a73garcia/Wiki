#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/pdf_export.py

Exportación de páginas de la Wiki a PDF.
Requiere únicamente reportlab.
"""

from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


class PDFExporter:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title = self.styles["Heading1"]
        self.title.alignment = TA_CENTER
        self.heading = self.styles["Heading2"]
        self.body = self.styles["BodyText"]
        self.code = self.styles["Code"] if "Code" in self.styles else self.styles["BodyText"]

    def export_page(self, title, content, output_file):

        doc = SimpleDocTemplate(str(output_file))
        story = [
            Paragraph(title, self.title),
            Paragraph("<br/>", self.body)
        ]

        in_code = False
        buffer = []

        for line in content.splitlines():
            if line.strip().startswith("```"):
                if in_code:
                    story.append(Preformatted("\n".join(buffer), self.code))
                    buffer = []
                    in_code = False
                else:
                    in_code = True
                continue

            if in_code:
                buffer.append(line)
            elif line.startswith("# "):
                story.append(Paragraph(line[2:], self.heading))
            elif line.strip():
                story.append(Paragraph(line, self.body))

        if buffer:
            story.append(Preformatted("\n".join(buffer), self.code))

        doc.build(story)
        return Path(output_file)

    def export_multiple(self, pages, output_file):
        doc = SimpleDocTemplate(str(output_file))
        story = []

        for page in pages:
            story.append(Paragraph(page["title"], self.title))
            story.append(Paragraph("<br/>", self.body))
            story.append(Paragraph(page["content"], self.body))
            story.append(Paragraph("<br/><br/>", self.body))

        doc.build(story)
        return Path(output_file)
