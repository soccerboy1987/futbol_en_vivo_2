import json
import re
from datetime import datetime

# Archivos
input_file = "input.txt"        # Tu lista de partidos tal cual
canales_file = "canales.json"   # Mapeo de CH -> nombre
output_file = "../partidos.json"   # Salida para la web


# Cargar canales
with open(canales_file, "r", encoding="utf-8") as f:
    canales = json.load(f)

partidos = []

with open(input_file, "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()
        if not linea:
            continue

        # Extraer fecha, hora, liga, partido y posibles embeds
        m = re.match(r"(\d{2}-\d{2}-\d{4}) \((\d{2}:\d{2})\) (.+?) : (.+?)\s*(\(.+\))?$", linea)
        if not m:
            print(f"Formato inválido: {linea}")
            continue

        fecha_str, hora_str, liga_larga, partido_texto, embeds_str = m.groups()

        # Procesar embeds (puede haber múltiples)
        embed_codes = re.findall(r"CH\d+[a-z]*", embeds_str or "", re.IGNORECASE)
        embeds = []
        for code in embed_codes:
            nombre_ch = canales.get(code.upper(), code)  # Si no está en canales.json, dejar el código
            numero = re.findall(r"CH(\d+)", code)[0]      # Extraer solo el número
            url = f"https://5bcda32c.player-dwk.pages.dev/?get=https://bolaloca.my/player/3/{numero}"
            embeds.append({"nombre": nombre_ch, "url": url})

        # Convertir fecha + hora SIN CAMBIO DE ZONA HORARIA
        dt = datetime.strptime(f"{fecha_str} {hora_str}", "%d-%m-%Y %H:%M")

        fecha_iso = dt.strftime("%Y-%m-%d")
        hora_evento = dt.strftime("%H:%M")

        # Detectar tipo de liga para tu web (soccer, nba, nhl, nfl)
        liga = liga_larga.lower()
        if "nba" in liga:
            tipo_liga = "nba"
        elif "nhl" in liga:
            tipo_liga = "nhl"
        elif "nfl" in liga:
            tipo_liga = "nfl"
        else:
            tipo_liga = "soccer"

        # Logo según liga
        logo = f"logos/{tipo_liga}.png"

        # Armar el objeto partido
        partidos.append({
            "nombre": f"{liga_larga}: {partido_texto}",
            "hora": hora_evento,  # Hora convertida a México
            "liga": tipo_liga,
            "logo": logo,
            "fecha": fecha_iso,
            "embeds": embeds
        })

# Guardar JSON listo para la web
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(partidos, f, ensure_ascii=False, indent=2)

print(f"Se generó {output_file} con {len(partidos)} partidos en hora México")
