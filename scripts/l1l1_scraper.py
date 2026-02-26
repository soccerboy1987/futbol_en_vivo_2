import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

PLAYER_PREFIX = "https://5bcda32c.player-dwk.pages.dev/?get="

URL = "https://l1l1.link/"
OUTPUT_FILE = "eventos_l1l1.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
    "Referer": "https://l1l1.link/",
    "Connection": "keep-alive"
}

MEXICO_TZ = ZoneInfo("America/Mexico_City")


def fetch():
    print("📡 Descargando eventos...")
    r = requests.get(URL, headers=HEADERS, timeout=40)
    r.raise_for_status()
    return r.text


def detect_liga(texto):
    t = texto.lower()

    if "hockey" in t:
        return "nhl", "logos/nhl.png"
    if "nba" in t:
        return "nba", "logos/nba.png"
    if "soccer" in t or "league" in t:
        return "soccer", "logos/soccer.png"

    return "soccer", "logos/soccer.png"

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    eventos = []

    for li in soup.find_all("li"):

        # Nombre del partido
        titulo_div = li.select_one("div.text-sm")
        if not titulo_div:
            continue

        textos = list(titulo_div.stripped_strings)

        # Filtrar basura
        textos_limpios = [
            t for t in textos
            if t.lower() != "football" and t != "--:--"
        ]

        # Nombre del partido (equipos)
        info_container = li.find("div", class_="flex-1")

        nombre_partido = ""
        liga = ""

        if info_container:
            # Equipos
            equipos_div = info_container.find("div", class_="text-sm")
            if equipos_div:
                nombre_partido = equipos_div.get_text(strip=True)

            # Liga
            liga_div = info_container.find("div", class_=lambda x: x and "muted" in x)
            if liga_div:
                liga = liga_div.get_text(strip=True).split("·")[0].strip()

        if nombre_partido and liga:
            nombre_evento = f"{liga} · {nombre_partido}"
        elif nombre_partido:
            nombre_evento = nombre_partido
        elif liga:
            nombre_evento = liga
        else:
            nombre_evento = ""

        # Liga
        liga_div = li.find("div", class_="text-[12px] muted")
        liga_texto = liga_div.get_text(strip=True) if liga_div else ""

        # Hora GMT
        time_div = li.find("div", attrs={"data-gmt-time": True})
        if not time_div:
            continue

        timestamp = int(time_div["data-gmt-time"])
        from datetime import datetime, timedelta, timezone

        dt_utc = datetime.fromtimestamp(timestamp, timezone.utc)
        dt_mex = dt_utc.astimezone(MEXICO_TZ)

        liga_detectada, logo = detect_liga(liga_texto)

        embeds = []

        # 🔥 CORRECTO: loops bien anidados
        bloques = li.select("div.r3")

        for bloque in bloques:
            inputs = bloque.find_all("input")

            for inp in inputs:
                val = inp.get("value", "").strip()

                if val.startswith("https://l1l1.link/ch?id="):
                    canal_tag = bloque.find("span", class_="badge-tv")
                    canal_nombre = canal_tag.get_text(strip=True) if canal_tag else "Canal"

                    

                    embeds.append({
                        "nombre": canal_nombre,
                        "url": f"{PLAYER_PREFIX}{val}"
                    })

        # 👇 ESTE if debe estar dentro del for li
        if embeds:
            eventos.append({
                "nombre": nombre_evento,
                "hora": dt_mex.strftime("%H:%M"),
                "liga": liga_detectada,
                "logo": logo,
                "fecha": dt_mex.strftime("%Y-%m-%d"),
                "embeds": embeds
            })
    eventos.sort(key=lambda x: (x["fecha"], x["hora"]))
    return eventos


def save(eventos):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(eventos)} eventos guardados en {OUTPUT_FILE}")


from datetime import datetime, timedelta

def main():
    hoy = datetime.now().strftime("%Y-%m-%d")
    manana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    urls = [
        f"https://l1l1.link/?date={hoy}&sport=&q=&chid=&sort=time_asc",
        f"https://l1l1.link/?date={manana}&sport=&q=&chid=&sort=time_asc"
    ]

    todos_eventos = []

    for url in urls:
        print(f"📡 Descargando {url}")
        r = requests.get(url, headers=HEADERS, timeout=40)
        r.raise_for_status()
        html = r.text

        eventos = parse(html)
        todos_eventos.extend(eventos)

    # Ordenar por fecha y hora
    todos_eventos.sort(key=lambda x: (x["fecha"], x["hora"]))

    save(todos_eventos)


if __name__ == "__main__":
    main()