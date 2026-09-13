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


def diagrama_proceso(
    valores,
    velocidad,
    kMc=None,
    kMt=None
):

    lp = _fmt(
        valores.get("lp"),
        3
    )

    v = _fmt(
        velocidad,
        0
    )

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

    gtn = _fmt(
        valores.get("GTn")
    )

    ggn = _fmt(
        valores.get("GGn")
    )

    gtt = _fmt(
        valores.get("GTT")
    )

    pexh = _fmt(
        valores.get("Pexh")
    )

    ts = _fmt(
        valores.get("Ts")
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

        .title {{
            fill: {DIAL};
            font-size: 15px;
            font-weight: bold;
        }}

        .text {{
            fill: {MIST};
            font-size: 13px;
        }}

        .accent {{
            fill: {BRASS};
            font-size: 13px;
            font-weight: bold;
        }}

    </style>

    </head>


    <body>


    <svg
        viewBox="0 0 1300 520"
        xmlns="http://www.w3.org/2000/svg"
    >


        <!-- ================================================ -->
        <!-- ADMISIÓN -->
        <!-- ================================================ -->

        <polygon
            points="
                20,100
                185,135
                185,235
                20,270
            "
            fill="none"
            stroke="{MIST}"
            stroke-width="3"
        />


        <!-- flujo azul -->

        <path
            d="M30 130 C80 130 125 145 175 155"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="4"
        />

        <path
            d="M30 185 C90 185 125 185 175 185"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="4"
        />

        <path
            d="M30 240 C80 240 125 225 175 215"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="4"
        />


        <!-- ================================================ -->
        <!-- COMPRESOR -->
        <!-- ================================================ -->

        <polygon
            points="
                185,115
                420,145
                420,225
                185,255
            "
            fill="#4E9FDB"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="230"
            y1="121"
            x2="230"
            y2="249"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="280"
            y1="128"
            x2="280"
            y2="242"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="330"
            y1="134"
            x2="330"
            y2="236"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="380"
            y1="140"
            x2="380"
            y2="230"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- ================================================ -->
        <!-- COMBUSTIÓN -->
        <!-- ================================================ -->

        <rect
            x="430"
            y="118"
            width="270"
            height="135"
            rx="8"
            fill="{HULL}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="475"
            y="145"
            width="170"
            height="82"
            rx="8"
            fill="#374E52"
            stroke="{MIST}"
            stroke-width="2"
        />


        <polygon
            points="
                480,175
                585,175
                640,185
                585,195
                480,195
            "
            fill="{SIGNAL}"
        />


        <polygon
            points="
                475,185
                505,160
                497,181
                530,185
                497,192
                505,215
            "
            fill="#F5C542"
        />


        <!-- ================================================ -->
        <!-- TURBINA -->
        <!-- ================================================ -->

        <polygon
            points="
                720,145
                920,110
                920,260
                720,225
            "
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="760"
            y1="138"
            x2="760"
            y2="232"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="810"
            y1="130"
            x2="810"
            y2="240"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="860"
            y1="120"
            x2="860"
            y2="250"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- ================================================ -->
        <!-- ESCAPE -->
        <!-- ================================================ -->

        <polygon
            points="
                920,110
                1280,70
                1280,300
                920,260
            "
            fill="none"
            stroke="{MIST}"
            stroke-width="3"
        />


        <path
            d="M935 150 C1010 140 1110 125 1260 120"
            fill="none"
            stroke="#B44B8A"
            stroke-width="4"
        />

        <path
            d="M935 185 C1050 185 1150 185 1260 185"
            fill="none"
            stroke="#B44B8A"
            stroke-width="4"
        />

        <path
            d="M935 220 C1010 230 1110 245 1260 250"
            fill="none"
            stroke="#B44B8A"
            stroke-width="4"
        />


        <!-- EJE -->

        <line
            x1="185"
            y1="185"
            x2="920"
            y2="185"
            stroke="#D8D8D8"
            stroke-width="7"
        />


        <!-- ================================================ -->
        <!-- NOMBRES -->
        <!-- ================================================ -->

        <text
            x="100"
            y="335"
            text-anchor="middle"
            fill="{MIST}"
            font-size="18"
        >
            Admisión
        </text>


        <text
            x="300"
            y="335"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="18"
            font-weight="bold"
        >
            Compresor
        </text>


        <text
            x="565"
            y="335"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="18"
        >
            Cámara de combustión
        </text>


        <text
            x="820"
            y="335"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="18"
            font-weight="bold"
        >
            Turbina
        </text>


        <text
            x="1090"
            y="335"
            text-anchor="middle"
            fill="{MIST}"
            font-size="18"
        >
            Escape
        </text>


        <!-- ================================================ -->
        <!-- TELEMETRÍA DEL PROCESO -->
        <!-- ================================================ -->


        <!-- Condición operacional -->

        <rect
            x="20"
            y="370"
            width="190"
            height="105"
            rx="8"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="35"
            y="397"
            class="title"
        >
            Operación
        </text>

        <text
            x="35"
            y="424"
            class="text"
        >
            lp = {lp}
        </text>

        <text
            x="35"
            y="449"
            class="text"
        >
            v = {v} knots
        </text>


        <!-- Compresor -->

        <rect
            x="235"
            y="370"
            width="210"
            height="120"
            rx="8"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="250"
            y="397"
            class="title"
        >
            Salida compresor
        </text>

        <text
            x="250"
            y="424"
            class="text"
        >
            T2 = {t2} °C
        </text>

        <text
            x="250"
            y="449"
            class="text"
        >
            P2 = {p2} bar
        </text>

        <text
            x="250"
            y="474"
            class="accent"
        >
            kMc = {kmc}
        </text>


        <!-- Combustión -->

        <rect
            x="470"
            y="370"
            width="190"
            height="105"
            rx="8"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="485"
            y="397"
            class="title"
        >
            Combustión
        </text>

        <text
            x="485"
            y="424"
            class="text"
        >
            mf = {mf} kg/s
        </text>

        <text
            x="485"
            y="449"
            class="text"
        >
            TIC = {tic} %
        </text>


        <!-- Eje generador -->

        <rect
            x="685"
            y="370"
            width="200"
            height="120"
            rx="8"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="700"
            y="397"
            class="title"
        >
            Eje / generador
        </text>

        <text
            x="700"
            y="424"
            class="text"
        >
            GGn = {ggn} rpm
        </text>

        <text
            x="700"
            y="449"
            class="text"
        >
            GTn = {gtn} rpm
        </text>

        <text
            x="700"
            y="474"
            class="text"
        >
            GTT = {gtt} kN m
        </text>


        <!-- Turbina -->

        <rect
            x="910"
            y="370"
            width="195"
            height="120"
            rx="8"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="925"
            y="397"
            class="title"
        >
            Salida turbina HP
        </text>

        <text
            x="925"
            y="424"
            class="text"
        >
            T48 = {t48} °C
        </text>

        <text
            x="925"
            y="449"
            class="text"
        >
            P48 = {p48} bar
        </text>

        <text
            x="925"
            y="474"
            class="accent"
        >
            kMt = {kmt}
        </text>


        <!-- Escape -->

        <rect
            x="1130"
            y="370"
            width="150"
            height="105"
            rx="8"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="1145"
            y="397"
            class="title"
        >
            Escape
        </text>

        <text
            x="1145"
            y="424"
            class="text"
        >
            Pexh = {pexh}
        </text>

        <text
            x="1145"
            y="449"
            class="text"
        >
            Ts = {ts}
        </text>


    </svg>

    </body>

    </html>
    """


    components.html(
        html,
        height=520,
        scrolling=False
    )
