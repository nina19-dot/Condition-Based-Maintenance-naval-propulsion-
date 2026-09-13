# ui/plant_map.py

import streamlit.components.v1 as components

from config import (
    INK,
    HULL,
    DIAL,
    BRASS,
    SIGNAL,
    SEA,
    MIST
)


def _fmt(valor, dec=2):
    if valor is None:
        return "-"
    return f"{valor:.{dec}f}"


def esquema_planta(componente=None, valores=None, velocidad=None, kMc=None, kMt=None):

    if valores is None:
        valores = {}

    compresor = "#E5483F" if componente in ["compressor", "both"] else "#4E9FDB"
    turbina = "#F59E0B" if componente in ["turbine", "both"] else "#9B5DE5"

    t1_txt = _fmt(valores.get("T1"))
    p1_txt = _fmt(valores.get("P1"))
    t2_txt = _fmt(valores.get("T2"))
    p2_txt = _fmt(valores.get("P2"))
    mf_txt = _fmt(valores.get("mf"), 3)
    tic_txt = _fmt(valores.get("TIC"))
    gtt_txt = _fmt(valores.get("GTT"))
    gtn_txt = _fmt(valores.get("GTn"))
    ggn_txt = _fmt(valores.get("GGn"))
    t48_txt = _fmt(valores.get("T48"))
    p48_txt = _fmt(valores.get("P48"))
    pexh_txt = _fmt(valores.get("Pexh"))
    ts_txt = _fmt(valores.get("Ts"))
    tp_txt = _fmt(valores.get("Tp"))
    v_txt = _fmt(velocidad, 0)
    lp_txt = _fmt(valores.get("lp"))

    kmc_txt = "-" if kMc is None else f"{kMc:.4f}"
    kmt_txt = "-" if kMt is None else f"{kMt:.4f}"

    html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: {INK};
            font-family: Arial, sans-serif;
        }}

        svg {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .small {{
            fill: {MIST};
            font-size: 13px;
        }}

        .label {{
            fill: {DIAL};
            font-size: 14px;
            font-weight: bold;
        }}

        .accent {{
            fill: {BRASS};
            font-size: 13px;
            font-weight: bold;
        }}
    </style>
    </head>

    <body>

    <svg viewBox="0 0 1380 650" xmlns="http://www.w3.org/2000/svg">

        <!-- Ejes -->
        <line x1="70" y1="165" x2="1120" y2="165" stroke="{DIAL}" stroke-width="8"/>
        <line x1="70" y1="455" x2="1120" y2="455" stroke="{DIAL}" stroke-width="8"/>

        <!-- Hélices -->
        <ellipse cx="50" cy="165" rx="12" ry="38" fill="none" stroke="{DIAL}" stroke-width="6"/>
        <ellipse cx="50" cy="455" rx="12" ry="38" fill="none" stroke="{DIAL}" stroke-width="6"/>

        <!-- Generadores diesel -->
        <rect x="150" y="70" width="210" height="60" rx="6"
              fill="#7138A8" stroke="{DIAL}" stroke-width="4"/>

        <rect x="150" y="360" width="210" height="60" rx="6"
              fill="#7138A8" stroke="{DIAL}" stroke-width="4"/>

        <rect x="150" y="445" width="210" height="60" rx="6"
              fill="#7138A8" stroke="{DIAL}" stroke-width="4"/>

        <text x="255" y="50" text-anchor="middle" fill="{MIST}" font-size="18">
            Generadores diesel
        </text>

        <!-- Turbina de gas -->
        <rect x="180" y="250" width="440" height="135" rx="10"
              fill="{HULL}" stroke="#2C5155" stroke-width="4"/>

        <polygon points="205,275 370,295 370,340 205,360"
                 fill="{compresor}" stroke="{DIAL}" stroke-width="4"/>

        <rect x="380" y="280" width="80" height="75"
              fill="{SIGNAL}" stroke="{DIAL}" stroke-width="4"/>

        <polygon points="475,290 595,270 595,365 475,345"
                 fill="{turbina}" stroke="{DIAL}" stroke-width="4"/>

        <text x="400" y="230" text-anchor="middle" fill="{MIST}" font-size="20">
            Turbina de gas
        </text>

        <!-- Embragues -->
        <circle cx="690" cy="260" r="25" fill="{HULL}" stroke="{SIGNAL}" stroke-width="5"/>
        <circle cx="690" cy="405" r="25" fill="{HULL}" stroke="{SIGNAL}" stroke-width="5"/>

        <!-- Cajas -->
        <rect x="765" y="100" width="55" height="170" fill="{SEA}" stroke="{DIAL}" stroke-width="4"/>
        <rect x="765" y="350" width="55" height="170" fill="{SEA}" stroke="{DIAL}" stroke-width="4"/>

        <!-- Motores eléctricos -->
        <rect x="875" y="100" width="130" height="80" rx="5" fill="{BRASS}" stroke="{DIAL}" stroke-width="4"/>
        <rect x="875" y="390" width="130" height="80" rx="5" fill="{BRASS}" stroke="{DIAL}" stroke-width="4"/>

        <!-- Conexiones -->
        <line x1="620" y1="317" x2="665" y2="260" stroke="{DIAL}" stroke-width="6"/>
        <line x1="620" y1="317" x2="665" y2="405" stroke="{DIAL}" stroke-width="6"/>
        <line x1="715" y1="260" x2="765" y2="185" stroke="{DIAL}" stroke-width="6"/>
        <line x1="715" y1="405" x2="765" y2="435" stroke="{DIAL}" stroke-width="6"/>

        <!-- Títulos internos -->
        <text x="285" y="378" text-anchor="middle" fill="{DIAL}" font-size="15">Compresor</text>
        <text x="420" y="378" text-anchor="middle" fill="{DIAL}" font-size="15">Combustión</text>
        <text x="535" y="378" text-anchor="middle" fill="{DIAL}" font-size="15">Turbina</text>

        <!-- TELEMETRÍA -->
        <rect x="1080" y="70" width="260" height="520" rx="10"
              fill="{HULL}" stroke="#2C5155" stroke-width="3"/>

        <text x="1100" y="100" class="label">Telemetría seleccionada</text>

        <text x="1100" y="130" class="small">lp = {lp_txt}</text>
        <text x="1100" y="152" class="small">v = {v_txt} knots</text>

        <text x="1100" y="190" class="label">Entrada compresor</text>
        <text x="1100" y="214" class="small">T1 = {t1_txt} °C</text>
        <text x="1100" y="236" class="small">P1 = {p1_txt} bar</text>

        <text x="1100" y="274" class="label">Salida compresor</text>
        <text x="1100" y="298" class="small">T2 = {t2_txt} °C</text>
        <text x="1100" y="320" class="small">P2 = {p2_txt} bar</text>
        <text x="1100" y="342" class="accent">kMc = {kmc_txt}</text>

        <text x="1100" y="380" class="label">Combustión</text>
        <text x="1100" y="404" class="small">mf = {mf_txt} kg/s</text>
        <text x="1100" y="426" class="small">TIC = {tic_txt} %</text>

        <text x="1100" y="464" class="label">Turbina / eje</text>
        <text x="1100" y="488" class="small">GGn = {ggn_txt} rpm</text>
        <text x="1100" y="510" class="small">GTn = {gtn_txt} rpm</text>
        <text x="1100" y="532" class="small">GTT = {gtt_txt} kN m</text>
        <text x="1100" y="554" class="small">T48 = {t48_txt} °C</text>
        <text x="1100" y="576" class="small">P48 = {p48_txt} bar</text>
        <text x="1100" y="598" class="accent">kMt = {kmt_txt}</text>

        <!-- Etiquetas locales -->
        <text x="200" y="240" class="small">T1={t1_txt} | P1={p1_txt}</text>
        <text x="330" y="285" class="small">T2={t2_txt} | P2={p2_txt}</text>
        <text x="397" y="270" class="small">mf={mf_txt} | TIC={tic_txt}</text>
        <text x="510" y="285" class="small">T48={t48_txt} | P48={p48_txt}</text>
        <text x="605" y="300" class="small">GTn={gtn_txt} | GTT={gtt_txt}</text>
        <text x="610" y="320" class="small">GGn={ggn_txt}</text>
        <text x="880" y="250" class="small">Pexh={pexh_txt}</text>
        <text x="860" y="150" class="small">Ts={ts_txt}</text>
        <text x="860" y="445" class="small">Tp={tp_txt}</text>

    </svg>

    </body>
    </html>
    """

    components.html(
        html,
        height=650,
        scrolling=False
    )
