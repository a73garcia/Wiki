/*
editor.js
Renombrar este archivo a editor.js
*/

class WikiEditor {

    constructor() {

        this.editor = document.getElementById("editor");

        if (!this.editor) {
            return;
        }

        this.installEvents();
        this.restoreDraft();
    }

    installEvents() {

        this.editor.addEventListener(
            "keydown",
            (e) => this.shortcuts(e)
        );

        this.editor.addEventListener(
            "input",
            () => this.autoSave()
        );
    }

    shortcuts(e) {

        if (!e.ctrlKey) {
            return;
        }

        switch (e.key.toLowerCase()) {

            case "b":
                e.preventDefault();
                this.wrap("**");
                break;

            case "i":
                e.preventDefault();
                this.wrap("*");
                break;

            case "k":
                e.preventDefault();
                this.insertLink();
                break;

            case "1":
                e.preventDefault();
                this.insertHeading("# ");
                break;

            case "2":
                e.preventDefault();
                this.insertHeading("## ");
                break;

            case "3":
                e.preventDefault();
                this.insertHeading("### ");
                break;

            case "s":
                e.preventDefault();
                document.forms[0].submit();
                break;

        }

    }

    wrap(mark) {

        const start = this.editor.selectionStart;
        const end = this.editor.selectionEnd;

        const text = this.editor.value;

        const selected = text.substring(start,end);

        this.editor.value =
            text.substring(0,start)
            + mark
            + selected
            + mark
            + text.substring(end);

    }

    insertHeading(level){

        const pos=this.editor.selectionStart;

        this.editor.setRangeText(
            level,
            pos,
            pos,
            "end"
        );

    }

    insertLink(){

        const url=prompt("URL");

        if(!url){
            return;
        }

        this.editor.setRangeText(
            "[texto]("+url+")",
            this.editor.selectionStart,
            this.editor.selectionEnd,
            "end"
        );

    }

    autoSave(){

        localStorage.setItem(
            "wiki_draft",
            this.editor.value
        );

    }

    restoreDraft(){

        const value=
            localStorage.getItem("wiki_draft");

        if(
            value &&
            this.editor.value.trim()===""
        ){
            this.editor.value=value;
        }

    }

}

window.addEventListener(
    "load",
    ()=>new WikiEditor()
);
