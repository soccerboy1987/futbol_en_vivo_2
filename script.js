document.addEventListener("DOMContentLoaded", () => {

    const manualMatches = [
        {
            title: "Leon vs America",
            competition: "Liga MX",
            thumbnail: "https://oem.com.mx/esto/img/29587529/1776693378/BASE_LANDSCAPE/1200/image.webp",
            stream: "https://aegis-cloudfront-1.tubi.video/62883227-8fc8-4992-97ff-614d283b4789/playlist576p.m3u8"
        }
    ];
    
    const streams = {
        "Switzerland vs Germany": "https://trasmisiones-tvhd.pages.dev/player?get=https%3A%2F%2Fcartelive.club%2Fplayer%2F3%2F69",
        "Argentina vs Mauritania": "https://trasmisiones-tvhd.pages.dev/player?get=https%3A%2F%2Fcartelive.club%2Fplayer%2F3%2F70",
        "England vs Uruguay": "https://trasmisiones-tvhd.pages.dev/player?get=https%3A%2F%2Fcartelive.club%2Fplayer%2F3%2F71",
        "USA vs Belgium": "https://trasmisiones-tvhd.pages.dev/player?get=https%3A%2F%2Fcartelive.club%2Fplayer%2F3%2F108",
        "Leon vs Atlas": "https://trasmisiones-tvhd.pages.dev/player?get=https%3A%2F%2Fcartelive.club%2Fplayer%2F3%2F108"
    };

    const API_KEY = null; // 👉 aquí pondrás tu key después

// 🔥 función para obtener datos reales (cuando tengas API)
async function getLiveData(home, away) {

    if (!API_KEY) {
        // 👉 fallback mientras no tienes API
        return {
            score: "0 - 0",
            status: "No disponible",
            stats: "Datos en vivo no conectados",
            lineup: "Alineaciones no disponibles"
        };
    }

    try {
        const res = await fetch("https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all", {
            method: "GET",
            headers: {
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
            }
        });

        const data = await res.json();

        const match = data.response.find(m =>
            m.teams.home.name.toLowerCase().includes(home.toLowerCase()) &&
            m.teams.away.name.toLowerCase().includes(away.toLowerCase())
        );

        if (!match) return null;

        return {
            score: `${match.goals.home} - ${match.goals.away}`,
            status: match.fixture.status.long,
            stats: "Datos disponibles",
            lineup: match.lineups?.map(t =>
                `${t.team.name}: ${t.startXI.map(p => p.player.name).join(", ")}`
            ).join("\n\n")
        };

    } catch (e) {
        console.error(e);
        return null;
    }
}

    const container = document.querySelector(".container");
    const modal = document.getElementById("modal");
    const optionsDiv = document.getElementById("options");
    const closeBtn = document.getElementById("close");
    const leagueFilter = document.getElementById("leagueFilter");

    closeBtn.addEventListener("click", () => modal.style.display = "none");
    window.addEventListener("click", (e) => {
        if(e.target === modal) modal.style.display = "none";
    });

    function matchesLeague(competition, filter){
        const comp = competition.toLowerCase();
        if(filter === "laliga") return comp.includes("spain") || comp.includes("laliga");
        if(filter === "premier") return comp.includes("england");
        if(filter === "ligamx") return comp.includes("mexico");
        if(filter === "champions") return comp.includes("champions");
        if(filter === "amistoso") return comp.includes("amistoso");
        return true;
    }

    function parseTeams(title) {
        const cleanTitle = title.replace(/\s+vs\s+/i, "|")
                                .replace(/\s+v\s+/i, "|")
                                .replace(/\s+-\s+/i, "|");

        const parts = cleanTitle.split("|").map(t => t.trim());

        return {
            home: parts[0] || "Equipo",
            away: parts[1] || "Equipo"
        };
    }

    async function loadMatches() {

        container.innerHTML = "⏳ Cargando partidos...";

        try {
            const res = await fetch("https://www.scorebat.com/video-api/v3/");
            const data = await res.json();

            container.innerHTML = "";

            const selectedLeague = leagueFilter.value || "all";
            let count = 0;

            // 🔥 MANUALES (AHORA FILTRADOS)
            manualMatches.forEach(match => {

                if(selectedLeague !== "all" && !matchesLeague(match.competition, selectedLeague)) return;

                const {home, away} = parseTeams(match.title);

                const div = document.createElement("div");

                div.innerHTML = `
                    <div class="match-card">
                        <img src="${match.thumbnail}" class="thumb">
                        
                        <div class="info">
                            <div class="teams">
                                ${home} <span class="vs">vs</span> ${away}
                            </div>

                            <div class="competition">${match.competition}</div>

                            <button class="btn">Ver opciones</button>
                        </div>
                    </div>
                `;

                div.querySelector(".btn").onclick = () => {

                    optionsDiv.innerHTML = "";

                    const opciones = [
                        {name: "🔴 Ver en vivo", url: match.stream},
                        {name: "🔎 Buscar en Google", url: `https://www.google.com/search?q=${match.title}`},
                        {name: "▶️ Buscar en YouTube", url: `https://www.youtube.com/results?search_query=${match.title}`}
                    ];

                    (async () => {

                    const {home, away} = parseTeams(match.title);

                    const live = await getLiveData(home, away);

                    if (live) {
                        const info = document.createElement("div");
                        info.className = "live-box";

                        info.innerHTML = `
                            <div>⚽ <b>${match.title}</b></div>
                            <div>📊 Marcador: ${live.score}</div>
                            <div>⏱ Estado: ${live.status}</div>
                        `;

                        optionsDiv.appendChild(info);

                        if (live.lineup) {
                            const pre = document.createElement("pre");
                            pre.textContent = "📋 Alineaciones:\n" + live.lineup;
                            pre.className = "info-extra";
                            optionsDiv.appendChild(pre);
                        }
                    }

                })();

                    opciones.forEach(opt => {
                        const a = document.createElement("a");
                        a.href = opt.url;
                        a.target = "_blank";
                        a.className = "option-btn";
                        a.textContent = opt.name;
                        a.onclick = () => modal.style.display = "none";
                        optionsDiv.appendChild(a);
                    });

                    modal.style.display = "block";
                };

                container.appendChild(div);
            });

            // 🔥 API (igual que tenías)
            data.response.forEach(match => {

                if(selectedLeague !== "all" && !matchesLeague(match.competition, selectedLeague)) return;
                if(count >= 12) return;

                count++;

                const {home, away} = parseTeams(match.title);

                const div = document.createElement("div");

                div.innerHTML = `
                    <div class="match-card">
                        <img src="${match.thumbnail}" class="thumb">
                        
                        <div class="info">
                            <div class="teams">
                                ${home} <span class="vs">vs</span> ${away}
                            </div>

                            <div class="competition">${match.competition}</div>

                            <button class="btn">Ver opciones</button>
                        </div>
                    </div>
                `;

                div.querySelector(".btn").onclick = () => {

                    optionsDiv.innerHTML = "";

                    
                    const opciones = [
                        {name: "📺 Ver resumen", url: match.matchviewUrl}
                    ];

                    let streamUrl = null;
                    const title = match.title.toLowerCase();

                    for (const key in streams) {
                        const teams = key.toLowerCase().split(" vs ");

                        if (teams.length === 2) {
                            const t1 = teams[0];
                            const t2 = teams[1];

                            if (title.includes(t1) && title.includes(t2)) {
                                streamUrl = streams[key];
                                break;
                            }
                        }
                    }

                    if (streamUrl) {
                        opciones.push({
                            name: "🔴 Ver en vivo",
                            url: streamUrl
                        });
                    }

                    opciones.push(
                        {name: "🔎 Buscar en Google", url: `https://www.google.com/search?q=${match.title}`},
                        {name: "▶️ Buscar en YouTube", url: `https://www.youtube.com/results?search_query=${match.title}`}
                    );

                    (async () => {

                    const {home, away} = parseTeams(match.title);

                    const live = await getLiveData(home, away);

                    if (live) {
                        const info = document.createElement("div");
                        info.className = "live-box";

                        info.innerHTML = `
                            <div>⚽ <b>${match.title}</b></div>
                            <div>📊 Marcador: ${live.score}</div>
                            <div>⏱ Estado: ${live.status}</div>
                        `;

                        optionsDiv.appendChild(info);

                        if (live.lineup) {
                            const pre = document.createElement("pre");
                            pre.textContent = "📋 Alineaciones:\n" + live.lineup;
                            pre.className = "info-extra";
                            optionsDiv.appendChild(pre);
                        }
                    }

                })();


                    opciones.forEach(opt => {
                        const a = document.createElement("a");
                        a.href = opt.url;
                        a.target = "_blank";
                        a.className = "option-btn";
                        a.textContent = opt.name;
                        a.onclick = () => modal.style.display = "none";
                        optionsDiv.appendChild(a);
                    });

                    modal.style.display = "block";
                };

                container.appendChild(div);
            });

        } catch(err) {
            console.error(err);
            container.innerHTML = "⚠️ Error cargando partidos";
        }
    }

    leagueFilter.addEventListener("change", loadMatches);

    loadMatches();
});