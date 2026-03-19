import requests
import re
import json
from datetime import datetime, timedelta

# ================= CONFIG =================

BOLALOCA_URL = "https://bolaloca.my/"
OUTPUT_FILE = "eventos_bolaca.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

UTC_OFFSET_MEXICO = -7  # horas

# Mapa CH -> nombre canal
CHANNEL_MAP = {
    1: "beIN 1",
    2: "beIN 2",
    3: "beIN 3",
    4: "beIN max 4",
    5: "beIN max 5",
    6: "beIN max 6",
    7: "beIN max 7",
    8: "beIN max 8",
    9: "beIN max 9",
    10: "beIN max 10",
    11: "canal+",
    12: "canal+ foot",
    13: "canal+ sport",
    14: "canal+ sport360",
    15: "eurosport1",
    16: "eurosport2",
    17: "rmc sport1",
    18: "rmc sport2",
    19: "equipe",
    20: "LIGUE 1 FR",
    21: "LIGUE 1 FR",
    22: "LIGUE 1 FR",
    23: "automoto",
    24: "tf1",
    25: "tmc",
    26: "m6",
    27: "w9",
    28: "france2",
    29: "france3",
    30: "france4",
    31: "C+Live 1",
    32: "C+Live 2",
    33: "C+Live 3",
    34: "C+Live 4",
    35: "C+Live 5",
    36: "C+Live 6",
    37: "C+Live 7",
    38: "C+Live 8",
    39: "C+Live 9",
    40: "C+Live 10",
    41: "C+Live 11",
    42: "C+Live 12",
    43: "C+Live 13",
    44: "C+Live 14",
    45: "C+Live 15",
    46: "C+Live 16",
    47: "C+Live 17",
    48: "C+Live 18",
    49: "ES m.laliga",
    50: "ES m.laliga2",
    51: "ES DAZN liga",
    52: "ES DAZN liga2",
    53: "ES LALIGA HYPERMOTION",
    54: "ES LALIGA HYPERMOTION2",
    55: "ES Vamos",
    56: "ES DAZN 1",
    57: "ES DAZN 2",
    58: "ES DAZN 3",
    59: "ES DAZN 4",
    60: "ES DAZN F1",
    61: "ES M+ Liga de Campeones",
    62: "ES M+ Deportes",
    63: "ES M+ Deportes2",
    64: "ES M+ Deportes3",
    65: "ES M+ Deportes4",
    66: "ES M+ Deportes5",
    67: "ES M+ Deportes6",
    68: "TUDN USA",
    69: "beIN En español",
    70: "FOX Deportes",
    71: "ESPN Deportes",
    72: "NBC UNIVERSO",
    73: "Telemundo",
    74: "GOL español",
    75: "TNT sport arg",
    76: "ESPN Premium",
    77: "TyC Sports",
    78: "FOXsport1 arg",
    79: "FOXsport2 arg",
    80: "FOXsport3 arg",
    81: "WINsport+",
    82: "WINsport",
    83: "TNTCHILE Premium",
    84: "Liga1MAX",
    85: "GOLPERU",
    86: "Zapping sports",
    87: "ESPN1",
    88: "ESPN2",
    89: "ESPN3",
    90: "ESPN4",
    91: "ESPN5",
    92: "ESPN6",
    93: "ESPN7",
    94: "directv",
    95: "directv2",
    96: "directv+",
    97: "ESPN1MX",
    98: "ESPN2MX",
    99: "ESPN3MX",
    100: "ESPN4MX",
    101: "FOXsport1MX",
    102: "FOXsport2MX",
    103: "FOXsport3MX",
    104: "FOX SPORTS PREMIUM",
    105: "TVC Deportes",
    106: "TUDNMX",
    107: "CANAL5",
    108: "Azteca 7",
    109: "VTV plus",
    110: "DE bundliga10",
    111: "DE bundliga1",
    112: "DE bundliga2",
    113: "DE bundliga3",
    114: "DE bundliga4",
    115: "DE bundliga5",
    116: "DE bundliga6",
    117: "DE bundliga7",
    118: "DE bundliga8",
    119: "DE bundliga9 (mix)",
    120: "DE skyde PL",
    121: "DE skyde f1",
    122: "DE skyde tennis",
    123: "DE dazn 1",
    124: "DE dazn 2",
    125: "DE Sportdigital Fussball",
    126: "UK TNT SPORT",
    127: "UK SKY MAIN",
    128: "UK SKY FOOT",
    129: "UK EPL 3PM",
    130: "UK EPL 3PM",
    131: "UK EPL 3PM",
    132: "UK EPL 3PM",
    133: "UK EPL 3PM",
    134: "UK F1",
    135: "UK SPFL",
    136: "UK SPFL",
    137: "IT DAZN",
    138: "IT SKYCALCIO",
    139: "IT FEED",
    140: "IT FEED",
    141: "NL ESPN 1",
    142: "NL ESPN 2",
    143: "NL ESPN 3",
    144: "PT SPORT 1",
    145: "PT SPORT 2",
    146: "PT SPORT 3",
    147: "PT BTV",
    148: "GR SPORT 1",
    149: "GR SPORT 2",
    150: "GR SPORT 3",
    151: "TR BeIN sport 1",
    152: "TR BeIN sport 2",
    153: "BE channel1",
    154: "BE channel2",
    155: "EXTRA SPORT1",
    156: "EXTRA SPORT2",
    157: "EXTRA SPORT3",
    158: "EXTRA SPORT4",
    159: "EXTRA SPORT5",
    160: "EXTRA SPORT6",
    161: "EXTRA SPORT7",
    162: "EXTRA SPORT8",
    163: "EXTRA SPORT9",
    164: "EXTRA SPORT10",
    165: "EXTRA SPORT11",
    166: "EXTRA SPORT12",
    167: "EXTRA SPORT13",
    168: "EXTRA SPORT14",
    169: "EXTRA SPORT15",
    170: "EXTRA SPORT16",
    171: "EXTRA SPORT17",
    172: "EXTRA SPORT18",
    173: "EXTRA SPORT19",
    174: "EXTRA SPORT20",
    175: "EXTRA SPORT21",
    176: "EXTRA SPORT22",
    177: "EXTRA SPORT23",
    178: "EXTRA SPORT24",
    179: "EXTRA SPORT25",
    180: "EXTRA SPORT26",
    181: "EXTRA SPORT27",
    182: "EXTRA SPORT28",
    183: "EXTRA SPORT30",
    184: "EXTRA SPORT31",
    185: "EXTRA SPORT32",
    186: "EXTRA SPORT33",
    187: "EXTRA SPORT34",
    188: "EXTRA SPORT35",
    189: "EXTRA SPORT36",
    190: "EXTRA SPORT37",
    191: "EXTRA SPORT38",
    192: "EXTRA SPORT39",
    193: "EXTRA SPORT40",
    194: "EXTRA SPORT41",
    195: "EXTRA SPORT42",
    196: "EXTRA SPORT43",
    197: "EXTRA SPORT44",
    198: "EXTRA SPORT45",
    199: "EXTRA SPORT46",
    200: "EXTRA SPORT47",
}


# ================= FUNCIONES =================

LIGAS_MAP = {

    # Inglaterra
    "premier league": ("soccer", "logos/liga_premier.png"),

    # Inglaterra
    "fa cup": ("soccer", "logos/liga_premier.png"),

    "championship": ("soccer", "logos/liga_premier.png"),  # puedes cambiar si tienes logo propio

    # Escocia
    "premiership": ("soccer", "logos/liga_premier.png"),  # no tienes escocia, usa premier de momento

    # Alemania
    "dfb pokal": ("soccer", "logos/liga_bundesliga.png"),  # no tienes logo alemán aún

    # Alemania
    "bundesliga": ("soccer", "logos/liga_bundesliga.png"),  # no tienes logo alemán aún

    # Italia
    "coppa italia": ("soccer", "logos/liga_italia.png"),  # no tienes logo italia aún
    
    # Italia
    "serie": ("soccer", "logos/liga_italia.png"),  # no tienes logo italia aún

    # España
    "coupe du roi": ("soccer", "logos/liga_española.png"),

    # España
    "laliga": ("soccer", "logos/liga_española.png"),

    # España
    "laliga 2": ("soccer", "logos/liga_española.png"),

    # Bélgica
    "coupe de belgique": ("soccer", "logos/soccer.png"),  # no tienes logo belga aún

    # Holanda
    "eredivisie": ("soccer", "logos/liga_holanda.png"),

    # Holanda
    "liga portugal": ("soccer", "logos/liga_portugal.png"),

    # Champions
    "ligue des champions femmes": ("soccer", "logos/liga_champions.png"),

      # Champions
    "liga 1": ("soccer", "logos/liga_peru.png"),

    # Argentina
    "copa argentina": ("soccer", "logos/liga_argentina.png"),

    # Argentina
    "torneo lpf": ("soccer", "logos/liga_argentina.png"),

     # Uruguay
    "liga auf uruguaya": ("soccer", "logos/liga_uruguay.png"),

    # Italia
    "serie a ": ("soccer", "logos/liga_italia.png"),
    
    # Brasil
    "serie a bresil": ("soccer", "logos/liga_brasil.png"),

    # Colombia
    "liga betplay": ("soccer", "logos/liga_colombia.png"),

    # Libertadores
    "copa libertadores": ("soccer", "logos/liga_libertadores.png"),  # puedes cambiar luego

    # Concacaf
    "concacaf champions cup": ("soccer", "logos/liga_concachampions.png"),

    # Arabia
    "saudi pro league": ("soccer", "logos/liga_arabiasaudita.png"),

    # Francia
    "ligue 1": ("soccer", "logos/liga_francia.png"),

    # Mexicana
    "liga mx": ("soccer", "logos/liga_mx.png"),

    # Mexicana
    "liga de expansion mx": ("soccer", "logos/liga_mx.png"),

    # Mexicana
    "liga mx women": ("soccer", "logos/liga_mx.png"),

    # liga endesa NBA
    "liga endesa": ("nba", "logos/nba.png"),

    # liga AFC CHAMPIONS
    "afc champions league": ("soccer", "logos/liga_afc.png"),

    # liga UEFA CHAMPIONS
    "uefa champions league": ("soccer", "logos/liga_uefa.png"),

    # CONFERENCE League
    "conference league": ("soccer", "logos/liga_conference.png"),

    # EUROPA League
    "ligue europa": ("soccer", "logos/liga_europaleague.png"),

    # Liga MLS
    "mls": ("soccer", "logos/liga_mls.png"),

    # formula 1
    "formula 1": ("soccer", "logos/formula1.png"),

}


def detect_liga(texto):
    t = texto.lower()

    # NBA y NHL primero (prioridad)
    if "nba" in t:
        return "nba", "logos/nba.png"
    if "nhl" in t:
        return "nhl", "logos/nhl.png"
        

    # Buscar coincidencia en mapa
    for key, value in LIGAS_MAP.items():
        if key in t:
            return value

    # Default
    return "soccer", "logos/soccer.png"



def fetch_bolaloca():
    print("📡 Descargando eventos de Bolaloca...")
    r = requests.get(BOLALOCA_URL, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.text


def parse_events(html):
    eventos = []

    pattern = re.compile(
        r"(\d{2}-\d{2}-\d{4}).*?\((\d{2}:\d{2})\)\s*(.+?)\s*:\s*(.+?)\s*-\s*(.+?)\s*((?:\(CH\d+.*?\)\s*)+)",
        re.IGNORECASE
    )

    for date_str, hour_str, liga_txt, local, visitante, chs_raw in pattern.findall(html):

        # Fecha + hora original
        dt_original = datetime.strptime(
            f"{date_str} {hour_str}", "%d-%m-%Y %H:%M"
        )

        # Ajuste horario México
        dt_mexico = dt_original + timedelta(hours=UTC_OFFSET_MEXICO)

        # Detectar liga y logo
        liga, logo = detect_liga(liga_txt)

        # Extraer TODOS los CH
        chs = [int(x) for x in re.findall(r"CH(\d+)", chs_raw)]

        embeds = []
        for ch in chs:
            embeds.append({
                "nombre": CHANNEL_MAP.get(ch, f"CH{ch}"),
                "url": f"https://5bcda32c.player-dwk.pages.dev/?get=https%3A%2F%2Fbolaloca.my%2Fplayer%2F3%2F{ch}"
            })

        eventos.append({
            "nombre": f"{liga_txt.strip()}: {local.strip()} - {visitante.strip()}",
            "hora": dt_mexico.strftime("%H:%M"),
            "liga": liga,
            "logo": logo,
            "fecha": dt_mexico.strftime("%Y-%m-%d"),
            "embeds": embeds
        })

    return eventos


def save_events(eventos):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(eventos)} eventos guardados en {OUTPUT_FILE}")


# ================= MAIN =================

def main():
    html = fetch_bolaloca()
    eventos = parse_events(html)
    save_events(eventos)


if __name__ == "__main__":
    main()
