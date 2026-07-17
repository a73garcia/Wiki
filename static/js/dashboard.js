/*
static/js/dashboard.js
Guardar posteriormente como dashboard.js
*/

class Dashboard {

    constructor() {
        this.refreshInterval = 60000;
        this.initialize();
    }

    initialize() {
        this.loadStatistics();
        this.loadRecentActivity();
        this.bindEvents();
        this.startAutoRefresh();
    }

    bindEvents() {
        const search = document.getElementById("dashboardSearch");

        if (search) {
            search.addEventListener("keyup", (e) => {
                if (e.key === "Enter") {
                    window.location.href = "/search?q=" +
                        encodeURIComponent(search.value);
                }
            });
        }
    }

    async loadStatistics() {
        try {
            const response = await fetch("/api/statistics");
            if (!response.ok) return;

            const data = await response.json();

            this.setValue("statPages", data.pages);
            this.setValue("statCategories", data.categories);
            this.setValue("statTags", data.tags);

            if (data.index) {
                this.setValue("statIndexed", data.index.indexed || 0);
            }

        } catch (err) {
            console.error(err);
        }
    }

    async loadRecentActivity() {
        try {
            const response = await fetch("/api/history");

            if (!response.ok) return;

            const items = await response.json();

            const container = document.getElementById("recentActivity");

            if (!container) return;

            container.innerHTML = "";

            items.slice(0,10).forEach(item => {

                const div = document.createElement("div");
                div.className = "activity-item";

                div.innerHTML =
                    "<strong>" + item.page + "</strong><br>" +
                    item.date + " - " +
                    item.action;

                container.appendChild(div);

            });

        } catch(err){
            console.error(err);
        }
    }

    setValue(id,value){
        const el=document.getElementById(id);
        if(el) el.textContent=value;
    }

    startAutoRefresh(){
        setInterval(()=>{
            this.loadStatistics();
            this.loadRecentActivity();
        },this.refreshInterval);
    }

}

window.addEventListener("DOMContentLoaded",()=>{
    new Dashboard();
});
