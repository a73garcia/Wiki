/*
static/js/editor.js
Guardar posteriormente como editor.js
*/

class WikiEditor {

    constructor() {
        this.editor = document.getElementById("content");
        this.preview = document.getElementById("preview");
        this.status = document.getElementById("saveStatus");
        this.lastSaved = this.editor ? this.editor.value : "";
        this.bindEvents();
        this.startAutosave();
    }

    bindEvents() {
        if (!this.editor) return;

        this.editor.addEventListener("input", () => {
            this.updatePreview();
            this.updateCounters();
        });

        document.addEventListener("keydown", (e) => {
            if (e.ctrlKey && e.key.toLowerCase() === "s") {
                e.preventDefault();
                this.save();
            }

            if (e.ctrlKey && e.key.toLowerCase() === "b") {
                e.preventDefault();
                this.insert("```sql\n\n```");
            }

            if (e.key === "Tab") {
                e.preventDefault();
                this.insert("    ");
            }
        });

        this.configureDropZone();
    }

    updatePreview() {
        if (!this.preview) return;
        this.preview.textContent = this.editor.value;
    }

    updateCounters() {
        const words = this.editor.value.trim().split(/\s+/).filter(Boolean).length;
        const chars = this.editor.value.length;

        const w = document.getElementById("wordCount");
        const c = document.getElementById("charCount");

        if (w) w.textContent = words;
        if (c) c.textContent = chars;
    }

    insert(text) {
        const start = this.editor.selectionStart;
        const end = this.editor.selectionEnd;

        this.editor.setRangeText(text, start, end, "end");
        this.editor.focus();
        this.updatePreview();
    }

    save() {
        this.lastSaved = this.editor.value;
        if (this.status)
            this.status.textContent = "Guardado";
    }

    startAutosave() {
        setInterval(() => {
            if (!this.editor) return;
            if (this.editor.value !== this.lastSaved) {
                this.save();
            }
        }, 30000);
    }

    configureDropZone() {
        const zone = document.getElementById("dropZone");
        if (!zone) return;

        zone.addEventListener("dragover", e => e.preventDefault());

        zone.addEventListener("drop", e => {
            e.preventDefault();
            alert("Adjunte el archivo mediante el formulario correspondiente.");
        });
    }

    insertSharePoint(url) {
        this.insert(`[Documento SharePoint](${url})`);
    }

    insertLocal(path) {
        this.insert(`[Archivo local](${path})`);
    }
}

window.addEventListener("DOMContentLoaded", () => new WikiEditor());
