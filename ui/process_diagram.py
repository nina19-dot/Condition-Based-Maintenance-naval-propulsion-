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


# ============================================================
# FORMATO DE VALORES
# ============================================================

def _fmt(valor, dec=2):

    if valor is None:
        return "-"

    return f"{valor:.{dec}f}"


# ============================================================
# DIAGRAMA DEL PROCESO DE LA TURBINA DE GAS
# ============================================================

def diagrama_proceso(
    valores,
    velocidad=None,
    kMc=None,
    kMt=None
):

    if valores is None:
        valores = {}

    # ========================================================
    # VARIABLES
    # ========================================================

    t2 = _fmt(
        valores.get("T2")
    )

    p2 = _fmt(
        valores.get("P2")
    )

    mf = _fmt(
        valores.get("mf"),
        3
    )

    tic = _fmt(
        valores.get("TIC")
    )

    t48 = _fmt(
        valores.get("T48")
    )

    p48 = _fmt(
        valores.get("P48")
    )

    pexh = _fmt(
        valores.get("Pexh")
    )

    kmc = (
        "-"
        if kMc is None
        else f"{kMc:.4f}"
    )

    kmt = (
        "-"
        if kMt is None
        else f"{kMt:.4f}"
    )

    # ========================================================
    # COLORES ESPECÍFICOS
    # ========================================================

    BLUE = "#4E9FDB"
    HOT = "#C0402C"
    TURBINE = "#F59E0B"
    PINK = "#D16BA5"

    # ========================================================
    # HTML + SVG
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

        .stage-title {{
            fill: {DIAL};
            font-size: 21px;
            font-weight: 800;
        }}

        .stage-subtitle {{
            fill: {MIST};
            font-size: 14px;
            font-weight: 600;
        }}

        .sensor-blue {{
            fill: {BLUE};
            font-size: 17px;
            font-weight: 800;
        }}

        .box-title {{
            fill: {DIAL};
            font-size: 16px;
            font-weight: 700;
        }}

        .box-text {{
            fill: {MIST};
            font-size: 14px;
        }}

        .box-value {{
            fill: {BRASS};
            font-size: 14px;
            font-weight: 700;
        }}

    </style>

    </head>

    <body>


    <svg
        viewBox="0 0 1400 570"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- ================================================= -->
        <!-- DEFINICIONES -->
        <!-- ================================================= -->

        <defs>

            <linearGradient
                id="compressorGradient"
                x1="0%"
                x2="100%"
            >

                <stop
                    offset="0%"
                    stop-color="#68B7E8"
                />

                <stop
                    offset="100%"
                    stop-color="#367EAE"
                />

            </linearGradient>


            <linearGradient
                id="turbineGradient"
                x1="0%"
                x2="100%"
            >

                <stop
                    offset="0%"
                    stop-color="#F6AF28"
                />

                <stop
                    offset="100%"
                    stop-color="#CE7913"
                />

            </linearGradient>


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
        <!-- ADMISIÓN -->
        <!-- ================================================= -->

        <polygon
            points="
                20,105
                185,145
                185,255
                20,295
            "
            fill="#142F33"
            stroke="{MIST}"
            stroke-width="3"
        />


        <!-- Líneas de flujo de aire -->

        <path
            d="M35 145 C90 145 130 155 175 170"
            fill="none"
            stroke="{BLUE}"
            stroke-width="5"
        />

        <path
            d="M35 200 C95 200 130 200 175 200"
            fill="none"
            stroke="{BLUE}"
            stroke-width="5"
        />

        <path
            d="M35 255 C90 255 130 245 175 230"
            fill="none"
            stroke="{BLUE}"
            stroke-width="5"
        />


        <!-- Solo nombres T1 y P2 -->
        <!-- Sin valores y sin recuadro -->

        <text
            x="75"
            y="120"
            class="sensor-blue"
        >
            T1
        </text>

        <text
            x="150"
            y="290"
            class="sensor-blue"
        >
            P1
        </text>


        <!-- ================================================= -->
        <!-- COMPRESOR -->
        <!-- ================================================= -->

        <polygon
            points="
                185,120
                440,155
                440,245
                185,280
            "
            fill="url(#compressorGradient)"
            stroke="{DIAL}"
            stroke-width="4"
            filter="url(#shadow)"
        />


        <!-- Álabes -->

        <line
            x1="235"
            y1="126"
            x2="235"
            y2="274"
            stroke="{INK}"
            stroke-width="8"
        />

        <line
            x1="290"
            y1="134"
            x2="290"
            y2="266"
            stroke="{INK}"
            stroke-width="8"
        />

        <line
            x1="345"
            y1="142"
            x2="345"
            y2="258"
            stroke="{INK}"
            stroke-width="8"
        />

        <line
            x1="400"
            y1="150"
            x2="400"
            y2="250"
            stroke="{INK}"
            stroke-width="8"
        />


        <!-- ================================================= -->
        <!-- CÁMARA DE COMBUSTIÓN -->
        <!-- ================================================= -->

        <rect
            x="455"
            y="120"
            width="285"
            height="160"
            rx="10"
            fill="{HULL}"
            stroke="{DIAL}"
            stroke-width="4"
            filter="url(#shadow)"
        />


        <rect
            x="505"
            y="150"
            width="180"
            height="100"
            rx="12"
            fill="#334D51"
            stroke="{MIST}"
            stroke-width="2"
        />


        <!-- Gases calientes -->

        <polygon
            points="
                515,190
                625,190
                680,200
                625,210
                515,210
            "
            fill="{HOT}"
        />


        <!-- Llama -->

        <polygon
            points="
                510,200
                545,170
                535,194
                572,200
                535,207
                545,235
            "
            fill="#FFC94A"
        />


        <!-- ================================================= -->
        <!-- TURBINA -->
        <!-- ================================================= -->

        <polygon
            points="
                765,155
                970,115
                970,285
                765,245
            "
            fill="url(#turbineGradient)"
            stroke="{DIAL}"
            stroke-width="4"
            filter="url(#shadow)"
        />


        <!-- Álabes -->

        <line
            x1="805"
            y1="147"
            x2="805"
            y2="253"
            stroke="{INK}"
            stroke-width="8"
        />

        <line
            x1="855"
            y1="137"
            x2="855"
            y2="263"
            stroke="{INK}"
            stroke-width="8"
        />

        <line
            x1="905"
            y1="128"
            x2="905"
            y2="272"
            stroke="{INK}"
            stroke-width="8"
        />

        <line
            x1="945"
            y1="120"
            x2="945"
            y2="280"
            stroke="{INK}"
            stroke-width="8"
        />


        <!-- ================================================= -->
        <!-- ESCAPE -->
        <!-- ================================================= -->

        <polygon
            points="
                970,115
                1380,65
                1380,335
                970,285
            "
            fill="#142F33"
            stroke="{MIST}"
            stroke-width="3"
        />


        <!-- Flujo de gases -->

        <path
            d="M990 160 C1090 145 1210 125 1360 120"
            fill="none"
            stroke="#B44B8A"
            stroke-width="5"
        />

        <path
            d="M990 200 C1110 200 1230 200 1360 200"
            fill="none"
            stroke="#B44B8A"
            stroke-width="5"
        />

        <path
            d="M990 240 C1090 255 1210 275 1360 280"
            fill="none"
            stroke="#B44B8A"
            stroke-width="5"
        />


        <!-- ================================================= -->
        <!-- EJE -->
        <!-- ================================================= -->

        <line
            x1="185"
            y1="200"
            x2="970"
            y2="200"
            stroke="#D8D8D8"
            stroke-width="8"
        />


        <!-- ================================================= -->
        <!-- NOMBRES PRINCIPALES -->
        <!-- ================================================= -->

        <text
            x="100"
            y="365"
            text-anchor="middle"
            class="stage-title"
        >
            Admisión
        </text>


        <text
            x="315"
            y="365"
            text-anchor="middle"
            class="stage-title"
        >
            Compresor
        </text>


        <text
            x="595"
            y="365"
            text-anchor="middle"
            class="stage-title"
        >
            Cámara de combustión
        </text>


        <text
            x="865"
            y="365"
            text-anchor="middle"
            class="stage-title"
        >
            Turbina
        </text>

        <text
            x="1180"
            y="365"
            text-anchor="middle"
            class="stage-title"
        >
            Escape
        </text>


        <!-- ================================================= -->
        <!-- TELEMETRÍA COMPRESOR -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="235"
                y="420"
                width="225"
                height="125"
                rx="10"
                fill="{HULL}"
                stroke="{BLUE}"
                stroke-width="2"
            />

            <text
                x="253"
                y="452"
                class="box-title"
            >
                Salida compresor
            </text>

            <text
                x="253"
                y="482"
                class="box-text"
            >
                T2 = {t2} °C
            </text>

            <text
                x="253"
                y="510"
                class="box-text"
            >
                P2 = {p2} bar
            </text>

            <text
                x="253"
                y="535"
                class="box-value"
            >
                kMc = {kmc}
            </text>

        </g>


        <!-- ================================================= -->
        <!-- TELEMETRÍA COMBUSTIÓN -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="485"
                y="420"
                width="220"
                height="105"
                rx="10"
                fill="{HULL}"
                stroke="{SIGNAL}"
                stroke-width="2"
            />

            <text
                x="503"
                y="452"
                class="box-title"
            >
                Combustión
            </text>

            <text
                x="503"
                y="482"
                class="box-text"
            >
                mf = {mf} kg/s
            </text>

            <text
                x="503"
                y="510"
                class="box-text"
            >
                TIC = {tic} %
            </text>

        </g>


        <!-- ================================================= -->
        <!-- TELEMETRÍA TURBINA -->
        <!-- Debajo del nombre Turbina -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="755"
                y="420"
                width="235"
                height="125"
                rx="10"
                fill="{HULL}"
                stroke="{TURBINE}"
                stroke-width="2"
            />

            <text
                x="773"
                y="452"
                class="box-title"
            >
                Salida turbina HP
            </text>

            <text
                x="773"
                y="482"
                class="box-text"
            >
                T48 = {t48} °C
            </text>

            <text
                x="773"
                y="510"
                class="box-text"
            >
                P48 = {p48} bar
            </text>

            <text
                x="773"
                y="535"
                class="box-value"
            >
                kMt = {kmt}
            </text>

        </g>


        <!-- ================================================= -->
        <!-- TELEMETRÍA ESCAPE -->
        <!-- Único recuadro rosa -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="1080"
                y="420"
                width="220"
                height="95"
                rx="10"
                fill="{HULL}"
                stroke="{PINK}"
                stroke-width="3"
            />

            <text
                x="1098"
                y="452"
                class="box-title"
            >
                Escape
            </text>

            <text
                x="1098"
                y="485"
                class="box-text"
            >
                Pexh = {pexh} bar
            </text>

        </g>


    </svg>

    </body>

    </html>
    """

    components.html(
        html,
        height=570,
        scrolling=False
    )
