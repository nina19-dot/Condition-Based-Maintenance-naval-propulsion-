# ui/process_diagram.py

import streamlit.components.v1 as components

from config import (
    INK,
    HULL,
    DIAL,
    BRASS,
    SIGNAL,
    SEA,
    MIST,
    STEEL
)


def _fmt(valor, dec=2):
    if valor is None:
        return "-"
    return f"{valor:.{dec}f}"


def diagrama_proceso(valores, velocidad, kMc=None, kMt=None):

    if valores is None:
        valores = {}

    # Valores formateados
    v_txt = _fmt(velocidad, 0)
    mf_txt = _fmt(valores.get("mf"), 3)

    t2_txt = _fmt(valores.get("T2"))
    p2_txt = _fmt(valores.get("P2"))

    ggn_txt = _fmt(valores.get("GGn"))
    gtn_txt = _fmt(valores.get("GTn"))
    gtt_txt = _fmt(valores.get("GTT"))

    t48_txt = _fmt(valores.get("T48"))
    p48_txt = _fmt(valores.get("P48"))

    pexh_txt = _fmt(valores.get("Pexh"))
    ts_txt = _fmt(valores.get("Ts"))
    tic_txt = _fmt(valores.get("TIC"))

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
    </style>
    </head>

    <body>

    <svg viewBox="0 0 1200 470" xmlns="http://www.w3.org/2000/svg">

        <!-- ================================================= -->
        <!-- CUERPO PRINCIPAL -->
        <!-- ================================================= -->

        <!-- Admisión -->
        <polygon
            points="20,90 180,120 180,220 20,250"
            fill="none"
            stroke="{MIST}"
            stroke-width="3"
        />

        <!-- Flujo admisión -->
        <path d="M 30 125 C 90 125, 125 135, 170 145"
              fill="none" stroke="#4F9BD8" stroke-width="4"/>
        <path d="M 30 170 C 90 170, 125 170, 170 170"
              fill="none" stroke="#4F9BD8" stroke-width="4"/>
        <path d="M 30 215 C 90 215, 125 205, 170 195"
              fill="none" stroke="#4F9BD8" stroke-width="4"/>

        <!-- Compresor -->
        <polygon
            points="180,105 395,135 395,205 180,235"
            fill="{SIGNAL}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <!-- Etapas compresor -->
        <line x1="220" y1="110" x2="220" y2="230" stroke="{INK}" stroke-width="7"/>
        <line x1="265" y1="116" x2="265" y2="224" stroke="{INK}" stroke-width="7"/>
        <line x1="310" y1="122" x2="310" y2="218" stroke="{INK}" stroke-width="7"/>
        <line x1="355" y1="128" x2="355" y2="212" stroke="{INK}" stroke-width="7"/>

        <!-- Cámara combustión -->
        <rect
            x="405"
            y="108"
            width="260"
            height="124"
            rx="8"
            fill="{HULL}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <rect
            x="445"
            y="130"
            width="170"
            height="80"
            rx="8"
            fill="#374E52"
            stroke="{MIST}"
            stroke-width="2"
        />

        <polygon
            points="455,160 560,160 610,175 560,190 455,190"
            fill="{SIGNAL}"
        />

        <polygon
            points="450,175 480,148 472,170 505,175 472,182 480,205"
            fill="#F5C542"
        />

        <!-- Turbina -->
        <polygon
            points="675,135 850,105 850,235 675,205"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <!-- Etapas turbina -->
        <line x1="710" y1="128" x2="710" y2="212" stroke="{INK}" stroke-width="7"/>
        <line x1="750" y1="121" x2="750" y2="219" stroke="{INK}" stroke-width="7"/>
        <line x1="790" y1="114" x2="790" y2="226" stroke="{INK}" stroke-width="7"/>
        <line x1="830" y1="108" x2="830" y2="232" stroke="{INK}" stroke-width="7"/>

        <!-- Escape -->
        <polygon
            points="850,105 1180,70 1180,270 850,235"
            fill="none"
            stroke="{MIST}"
            stroke-width="3"
        />

        <path d="M 860 140 C 940 130, 1030 120, 1165 115"
              fill="none" stroke="#B44B8A" stroke-width="4"/>
        <path d="M 860 175 C 950 175, 1040 175, 1165 175"
              fill="none" stroke="#B44B8A" stroke-width="4"/>
        <path d="M 860 210 C 940 220, 1030 230, 1165 235"
              fill="none" stroke="#B44B8A" stroke-width="4"/>

        <!-- Eje -->
        <line
            x1="180"
            y1="175"
            x2="850"
            y2="175"
            stroke="#D8D8D8"
            stroke-width="7"
        />

        <!-- ================================================= -->
        <!-- ETIQUETAS PRINCIPALES -->
        <!-- ================================================= -->

        <text x="95" y="300" text-anchor="middle" fill="{MIST}" font-size="18">
            Admisión
        </text>

        <text x="288" y="300" text-anchor="middle" fill="{DIAL}" font-size="18" font-weight="bold">
            Compresor
        </text>

        <text x="535" y="300" text-anchor="middle" fill="{DIAL}" font-size="18">
            Cámara de combustión
        </text>

        <text x="760" y="300" text-anchor="middle" fill="{DIAL}" font-size="18" font-weight="bold">
            Turbina
        </text>

        <text x="1015" y="300" text-anchor="middle" fill="{MIST}" font-size="18">
            Escape
        </text>

        <!-- ================================================= -->
        <!-- CAJAS DE DATOS -->
        <!-- ================================================= -->

        <!-- Admisión -->
        <rect x="20" y="330" width="190" height="110" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="35" y="355" fill="{DIAL}" font-size="16" font-weight="bold">Admisión / operación</text>
        <text x="35" y="382" fill="{MIST}" font-size="14">v = {v_txt} knots</text>
        <text x="35" y="405" fill="{MIST}" font-size="14">mf = {mf_txt} kg/s</text>

        <!-- Compresor -->
        <rect x="240" y="330" width="190" height="110" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="255" y="355" fill="{DIAL}" font-size="16" font-weight="bold">Compresor</text>
        <text x="255" y="382" fill="{MIST}" font-size="14">T2 = {t2_txt}</text>
        <text x="255" y="405" fill="{MIST}" font-size="14">P2 = {p2_txt}</text>
        <text x="255" y="428" fill="{BRASS}" font-size="14">kMc = {kmc_txt}</text>

        <!-- Combustión / generador -->
        <rect x="460" y="330" width="220" height="110" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="475" y="355" fill="{DIAL}" font-size="16" font-weight="bold">Combustión / generador</text>
        <text x="475" y="382" fill="{MIST}" font-size="14">GGn = {ggn_txt}</text>
        <text x="475" y="405" fill="{MIST}" font-size="14">GTn = {gtn_txt}</text>
        <text x="475" y="428" fill="{MIST}" font-size="14">GTT = {gtt_txt}</text>

        <!-- Turbina -->
        <rect x="710" y="330" width="190" height="110" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="725" y="355" fill="{DIAL}" font-size="16" font-weight="bold">Turbina</text>
        <text x="725" y="382" fill="{MIST}" font-size="14">T48 = {t48_txt}</text>
        <text x="725" y="405" fill="{MIST}" font-size="14">P48 = {p48_txt}</text>
        <text x="725" y="428" fill="{BRASS}" font-size="14">kMt = {kmt_txt}</text>

        <!-- Escape / carga -->
        <rect x="930" y="330" width="250" height="110" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="945" y="355" fill="{DIAL}" font-size="16" font-weight="bold">Escape / carga</text>
        <text x="945" y="382" fill="{MIST}" font-size="14">Pexh = {pexh_txt}</text>
        <text x="945" y="405" fill="{MIST}" font-size="14">Ts = {ts_txt}</text>
        <text x="945" y="428" fill="{MIST}" font-size="14">TIC = {tic_txt}</text>

    </svg>

    </body>
    </html>
    """

    components.html(
        html,
        height=455,
        scrolling=False
    )
