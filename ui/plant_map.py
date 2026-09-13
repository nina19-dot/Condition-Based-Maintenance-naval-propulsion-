# ui/plant_map.py

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


def esquema_planta(
    componente=None,
    valores=None,
    velocidad=None
):

    if valores is None:
        valores = {}

    # ========================================================
    # COLORES DE RESALTADO
    # ========================================================

    comp_color = (
        "#E5483F"
        if componente in ["compressor", "both"]
        else "#4E9FDB"
    )

    turb_color = (
        "#F59E0B"
        if componente in ["turbine", "both"]
        else "#9B5DE5"
    )

    # ========================================================
    # VARIABLES A MOSTRAR EN LA PLANTA
    # ========================================================

    lp = _fmt(valores.get("lp"), 3)
    v = _fmt(velocidad, 0)

    t2 = _fmt(valores.get("T2"))
    p2 = _fmt(valores.get("P2"))

    mf = _fmt(valores.get("mf"), 3)
    tic = _fmt(valores.get("TIC"))

    t48 = _fmt(valores.get("T48"))
    p48 = _fmt(valores.get("P48"))

    gtn = _fmt(valores.get("GTn"))
    ggn = _fmt(valores.get("GGn"))
    gtt = _fmt(valores.get("GTT"))

    pexh = _fmt(valores.get("Pexh"))

    ts = _fmt(valores.get("Ts"))
    tp = _fmt(valores.get("Tp", valores.get("Ts")))  # si no existe Tp, usa Ts

    # ========================================================
    # SVG
    # ========================================================

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

        .component-label {{
            fill: {MIST};
            font-size: 17px;
            font-weight: bold;
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
    </style>
    </head>

    <body>

    <svg
        viewBox="0 0 1500 800"
        xmlns="http://www.w3.org/2000/svg"
    >

        <defs>
            <filter id="shadow">
                <feDropShadow
                    dx="0"
                    dy="4"
                    stdDeviation="6"
                    flood-color="#000000"
                    flood-opacity="0.25"
                />
            </filter>
        </defs>

        <!-- ================================================= -->
        <!-- EJES PRINCIPALES -->
        <!-- ================================================= -->

        <line x1="95" y1="185" x2="1370" y2="185" stroke="{DIAL}" stroke-width="8"/>
        <line x1="95" y1="605" x2="1370" y2="605" stroke="{DIAL}" stroke-width="8"/>

        <!-- Hélices -->
        <ellipse cx="65" cy="185" rx="12" ry="46" fill="none" stroke="{DIAL}" stroke-width="6"/>
        <ellipse cx="65" cy="605" rx="12" ry="46" fill="none" stroke="{DIAL}" stroke-width="6"/>

        <text x="20" y="120" class="component-label">Hélice</text>
        <text x="20" y="540" class="component-label">Hélice</text>

        <!-- ================================================= -->
        <!-- GENERADORES DIESEL -->
        <!-- ================================================= -->

        <text x="265" y="45" text-anchor="middle" class="component-label">
            Generadores diesel
        </text>

        <rect x="165" y="75" width="230" height="72" rx="8"
              fill="#7138A8" stroke="{DIAL}" stroke-width="4"/>

        <rect x="165" y="500" width="230" height="72" rx="8"
              fill="#7138A8" stroke="{DIAL}" stroke-width="4"/>

        <rect x="165" y="615" width="230" height="72" rx="8"
              fill="#7138A8" stroke="{DIAL}" stroke-width="4"/>

        <!-- ================================================= -->
        <!-- TURBINA DE GAS -->
        <!-- ================================================= -->

        <text x="485" y="280" text-anchor="middle" class="component-label">
            Turbina de gas
        </text>

        <rect x="230" y="305" width="560" height="195" rx="14"
              fill="{HULL}" stroke="{STEEL}" stroke-width="4" filter="url(#shadow)"/>

        <!-- Compresor -->
        <polygon
            points="265,350 470,375 470,430 265,455"
            fill="{comp_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <line x1="315" y1="355" x2="315" y2="450" stroke="{INK}" stroke-width="7"/>
        <line x1="365" y1="361" x2="365" y2="444" stroke="{INK}" stroke-width="7"/>
        <line x1="415" y1="367" x2="415" y2="438" stroke="{INK}" stroke-width="7"/>

        <!-- Cámara de combustión -->
        <rect x="490" y="350" width="110" height="110" rx="6"
              fill="{SIGNAL}" stroke="{DIAL}" stroke-width="4"/>

        <!-- Turbina -->
        <polygon
            points="625,370 765,345 765,465 625,440"
            fill="{turb_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <line x1="665" y1="364" x2="665" y2="441" stroke="{INK}" stroke-width="7"/>
        <line x1="715" y1="356" x2="715" y2="449" stroke="{INK}" stroke-width="7"/>

        <!-- Etiquetas internas -->
        <text x="370" y="482" text-anchor="middle" fill="{DIAL}" font-size="15">Compresor</text>
        <text x="545" y="482" text-anchor="middle" fill="{DIAL}" font-size="15">Combustión</text>
        <text x="695" y="482" text-anchor="middle" fill="{DIAL}" font-size="15">Turbina</text>

        <!-- ================================================= -->
        <!-- EMBRAGUES -->
        <!-- ================================================= -->

        <text x="850" y="330" class="component-label">Embragues</text>

        <circle cx="865" cy="315" r="30" fill="{HULL}" stroke="{SIGNAL}" stroke-width="6"/>
        <circle cx="865" cy="505" r="30" fill="{HULL}" stroke="{SIGNAL}" stroke-width="6"/>

        <!-- ================================================= -->
        <!-- CAJAS -->
        <!-- ================================================= -->

        <text x="980" y="55" class="component-label">Cajas</text>

        <rect x="990" y="95" width="72" height="205" rx="4"
              fill="{SEA}" stroke="{DIAL}" stroke-width="4"/>

        <rect x="990" y="470" width="72" height="205" rx="4"
              fill="{SEA}" stroke="{DIAL}" stroke-width="4"/>

        <!-- ================================================= -->
        <!-- MOTORES ELÉCTRICOS -->
        <!-- ================================================= -->

        <text x="1180" y="65" class="component-label">Motores eléctricos</text>

        <rect x="1130" y="115" width="170" height="95" rx="7"
              fill="{BRASS}" stroke="{DIAL}" stroke-width="4"/>

        <rect x="1130" y="555" width="170" height="95" rx="7"
              fill="{BRASS}" stroke="{DIAL}" stroke-width="4"/>

        <!-- ================================================= -->
        <!-- CONEXIONES -->
        <!-- ================================================= -->

        <line x1="790" y1="405" x2="835" y2="315" stroke="{DIAL}" stroke-width="6"/>
        <line x1="790" y1="405" x2="835" y2="505" stroke="{DIAL}" stroke-width="6"/>

        <line x1="895" y1="315" x2="990" y2="195" stroke="{DIAL}" stroke-width="6"/>
        <line x1="895" y1="505" x2="990" y2="605" stroke="{DIAL}" stroke-width="6"/>

        <!-- ================================================= -->
        <!-- BLOQUES DE TELEMETRÍA -->
        <!-- ================================================= -->

        <!-- Operación -->
        <g filter="url(#shadow)">
            <rect x="20" y="355" width="175" height="100" rx="8"
                  fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
            <text x="38" y="385" class="box-title">Operación</text>
            <text x="38" y="415" class="box-text">lp = {lp}</text>
            <text x="38" y="442" class="box-text">v = {v} knots</text>
        </g>

        <line x1="195" y1="405" x2="230" y2="405"
              stroke="{STEEL}" stroke-width="2" stroke-dasharray="5 4"/>

        <!-- Salida compresor -->
        <g filter="url(#shadow)">
            <rect x="250" y="545" width="225" height="110" rx="8"
                  fill="{HULL}" stroke="{comp_color}" stroke-width="2"/>
            <text x="268" y="575" class="box-title">Salida compresor</text>
            <text x="268" y="603" class="box-text">T2 = {t2} °C</text>
            <text x="268" y="630" class="box-text">P2 = {p2} bar</text>
        </g>

        <line x1="380" y1="545" x2="380" y2="500"
              stroke="{comp_color}" stroke-width="2" stroke-dasharray="5 4"/>

        <!-- Combustión -->
        <g filter="url(#shadow)">
            <rect x="470" y="165" width="200" height="105" rx="8"
                  fill="{HULL}" stroke="{SIGNAL}" stroke-width="2"/>
            <text x="488" y="195" class="box-title">Combustión</text>
            <text x="488" y="223" class="box-text">mf = {mf} kg/s</text>
            <text x="488" y="250" class="box-text">TIC = {tic} %</text>
        </g>

        <line x1="545" y1="270" x2="545" y2="350"
              stroke="{SIGNAL}" stroke-width="2" stroke-dasharray="5 4"/>

        <!-- Generador de gas -->
        <g filter="url(#shadow)">
            <rect x="690" y="130" width="205" height="80" rx="8"
                  fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
            <text x="708" y="160" class="box-title">Generador de gas</text>
            <text x="708" y="188" class="box-text">GGn = {ggn} rpm</text>
        </g>

        <line x1="790" y1="210" x2="790" y2="345"
              stroke="{STEEL}" stroke-width="2" stroke-dasharray="5 4"/>

        <!-- Turbina / eje -->
        <g filter="url(#shadow)">
            <rect x="705" y="545" width="235" height="115" rx="8"
                  fill="{HULL}" stroke="{turb_color}" stroke-width="2"/>
            <text x="723" y="575" class="box-title">Turbina / eje</text>
            <text x="723" y="603" class="box-text">GTn = {gtn} rpm</text>
            <text x="723" y="630" class="box-text">GTT = {gtt} kN m</text>
            <text x="723" y="657" class="box-text">T48 = {t48} °C | P48 = {p48} bar</text>
        </g>

        <line x1="790" y1="545" x2="790" y2="470"
              stroke="{turb_color}" stroke-width="2" stroke-dasharray="5 4"/>

        <!-- Escape -->
        <g filter="url(#shadow)">
            <rect x="860" y="385" width="170" height="75" rx="8"
                  fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
            <text x="878" y="415" class="box-title">Escape</text>
            <text x="878" y="442" class="box-text">Pexh = {pexh} bar</text>
        </g>

        <line x1="860" y1="422" x2="765" y2="422"
              stroke="{STEEL}" stroke-width="2" stroke-dasharray="5 4"/>

        <!-- Hélice superior -->
        <g filter="url(#shadow)">
            <rect x="1290" y="105" width="170" height="75" rx="8"
                  fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
            <text x="1308" y="135" class="box-title">Hélice estribor</text>
            <text x="1308" y="162" class="box-text">Ts = {ts} kN m</text>
        </g>

        <line x1="1290" y1="145" x2="1260" y2="145"
              stroke="{STEEL}" stroke-width="2" stroke-dasharray="5 4"/>

        <!-- Hélice inferior -->
        <g filter="url(#shadow)">
            <rect x="1290" y="565" width="170" height="75" rx="8"
                  fill="{HULL}" stroke="{STEEL}" stroke-width="2"/>
            <text x="1308" y="595" class="box-title">Hélice babor</text>
            <text x="1308" y="622" class="box-text">Tp = {tp} kN m</text>
        </g>

        <line x1="1290" y1="605" x2="1260" y2="605"
              stroke="{STEEL}" stroke-width="2" stroke-dasharray="5 4"/>

    </svg>

    </body>
    </html>
    """

    components.html(
        html,
        height=800,
        scrolling=False
    )
