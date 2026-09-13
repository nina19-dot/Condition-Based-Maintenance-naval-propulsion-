# ui/process_diagram.py

import streamlit.components.v1 as components

from config import (
    INK,
    HULL,
    DIAL,
    BRASS,
    SIGNAL,
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

    lp_txt = _fmt(valores.get("lp"), 2)
    v_txt = _fmt(velocidad, 0)

    t1_txt = _fmt(valores.get("T1"))
    p1_txt = _fmt(valores.get("P1"))

    t2_txt = _fmt(valores.get("T2"))
    p2_txt = _fmt(valores.get("P2"))
    ggn_txt = _fmt(valores.get("GGn"))

    mf_txt = _fmt(valores.get("mf"), 3)
    tic_txt = _fmt(valores.get("TIC"))

    gtn_txt = _fmt(valores.get("GTn"))
    gtt_txt = _fmt(valores.get("GTT"))
    t48_txt = _fmt(valores.get("T48"))
    p48_txt = _fmt(valores.get("P48"))

    pexh_txt = _fmt(valores.get("Pexh"))
    ts_txt = _fmt(valores.get("Ts"))
    tp_txt = _fmt(valores.get("Tp"))

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

        .box-title {{
            fill: {DIAL};
            font-size: 15px;
            font-weight: bold;
        }}

        .box-text {{
            fill: {MIST};
            font-size: 13px;
        }}

        .box-accent {{
            fill: {BRASS};
            font-size: 13px;
            font-weight: bold;
        }}
    </style>
    </head>

    <body>

    <svg viewBox="0 0 1320 560" xmlns="http://www.w3.org/2000/svg">

        <!-- PROCESO -->
        <polygon points="20,120 180,150 180,260 20,290"
                 fill="none" stroke="{MIST}" stroke-width="3"/>

        <polygon points="180,140 390,170 390,240 180,270"
                 fill="{SIGNAL}" stroke="{DIAL}" stroke-width="4"/>

        <line x1="225" y1="146" x2="225" y2="264" stroke="{INK}" stroke-width="7"/>
        <line x1="275" y1="154" x2="275" y2="256" stroke="{INK}" stroke-width="7"/>
        <line x1="325" y1="162" x2="325" y2="248" stroke="{INK}" stroke-width="7"/>

        <rect x="410" y="145" width="260" height="120" rx="8"
              fill="{HULL}" stroke="{DIAL}" stroke-width="4"/>

        <rect x="455" y="170" width="155" height="72" rx="8"
              fill="#374E52" stroke="{MIST}" stroke-width="2"/>

        <polygon points="460,198 560,198 610,205 560,214 460,214"
                 fill="{SIGNAL}"/>

        <polygon points="455,206 485,182 477,202 510,206 477,212 485,232"
                 fill="#F5C542"/>

        <polygon points="695,170 865,140 865,270 695,240"
                 fill="{BRASS}" stroke="{DIAL}" stroke-width="4"/>

        <line x1="730" y1="162" x2="730" y2="248" stroke="{INK}" stroke-width="7"/>
        <line x1="770" y1="155" x2="770" y2="255" stroke="{INK}" stroke-width="7"/>
        <line x1="810" y1="148" x2="810" y2="262" stroke="{INK}" stroke-width="7"/>

        <polygon points="865,140 1190,105 1190,305 865,270"
                 fill="none" stroke="{MIST}" stroke-width="3"/>

        <line x1="180" y1="205" x2="865" y2="205" stroke="#D8D8D8" stroke-width="7"/>

        <!-- ETIQUETAS -->
        <text x="95" y="335" text-anchor="middle" fill="{MIST}" font-size="18">Admisión</text>
        <text x="285" y="335" text-anchor="middle" fill="{DIAL}" font-size="18" font-weight="bold">Compresor</text>
        <text x="540" y="335" text-anchor="middle" fill="{DIAL}" font-size="18">Cámara de combustión</text>
        <text x="780" y="335" text-anchor="middle" fill="{DIAL}" font-size="18" font-weight="bold">Turbina</text>
        <text x="1030" y="335" text-anchor="middle" fill="{MIST}" font-size="18">Escape</text>

        <!-- CAJAS DE DATOS -->

        <!-- Admisión -->
        <rect x="20" y="380" width="220" height="145" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="35" y="407" class="box-title">Admisión / entrada</text>
        <text x="35" y="432" class="box-text">lp = {lp_txt}</text>
        <text x="35" y="454" class="box-text">v = {v_txt} knots</text>
        <text x="35" y="476" class="box-text">T1 = {t1_txt} °C</text>
        <text x="35" y="498" class="box-text">P1 = {p1_txt} bar</text>

        <!-- Compresor -->
        <rect x="270" y="380" width="220" height="145" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="285" y="407" class="box-title">Compresor</text>
        <text x="285" y="432" class="box-text">GGn = {ggn_txt} rpm</text>
        <text x="285" y="454" class="box-text">T2 = {t2_txt} °C</text>
        <text x="285" y="476" class="box-text">P2 = {p2_txt} bar</text>
        <text x="285" y="498" class="box-accent">kMc = {kmc_txt}</text>

        <!-- Combustión -->
        <rect x="520" y="380" width="220" height="145" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="535" y="407" class="box-title">Combustión</text>
        <text x="535" y="432" class="box-text">mf = {mf_txt} kg/s</text>
        <text x="535" y="454" class="box-text">TIC = {tic_txt} %</text>

        <!-- Turbina -->
        <rect x="770" y="380" width="240" height="145" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="785" y="407" class="box-title">Turbina</text>
        <text x="785" y="432" class="box-text">GTn = {gtn_txt} rpm</text>
        <text x="785" y="454" class="box-text">GTT = {gtt_txt} kN m</text>
        <text x="785" y="476" class="box-text">T48 = {t48_txt} °C</text>
        <text x="785" y="498" class="box-text">P48 = {p48_txt} bar</text>
        <text x="785" y="520" class="box-accent">kMt = {kmt_txt}</text>

        <!-- Escape / propulsión -->
        <rect x="1040" y="380" width="250" height="145" rx="8"
              fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
        <text x="1055" y="407" class="box-title">Escape / propulsión</text>
        <text x="1055" y="432" class="box-text">Pexh = {pexh_txt} bar</text>
        <text x="1055" y="454" class="box-text">Ts = {ts_txt} kN m</text>
        <text x="1055" y="476" class="box-text">Tp = {tp_txt}</text>

    </svg>

    </body>
    </html>
    """

    components.html(
        html,
        height=560,
        scrolling=False
    )
