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
    velocidad=None,
    kMc=None,
    kMt=None
):

    if valores is None:
        valores = {}


    comp_color = (
        "#E5483F"
        if componente in [
            "compressor",
            "both"
        ]
        else "#4E9FDB"
    )


    turb_color = (
        "#F59E0B"
        if componente in [
            "turbine",
            "both"
        ]
        else "#9B5DE5"
    )


    # ========================================================
    # TELEMETRÍA
    # ========================================================

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

    gtt = _fmt(
        valores.get("GTT")
    )

    gtn = _fmt(
        valores.get("GTn")
    )

    ggn = _fmt(
        valores.get("GGn")
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
            font-size: 17px;
            font-weight: bold;
        }}

        .text {{
            fill: {MIST};
            font-size: 14px;
        }}

        .value {{
            fill: {BRASS};
            font-size: 14px;
            font-weight: bold;
        }}

    </style>

    </head>


    <body>


    <svg
        viewBox="0 0 1400 680"
        xmlns="http://www.w3.org/2000/svg"
    >


        <!-- ================================================ -->
        <!-- EJES DE PROPULSIÓN -->
        <!-- ================================================ -->

        <line
            x1="75"
            y1="170"
            x2="1280"
            y2="170"
            stroke="{DIAL}"
            stroke-width="8"
        />

        <line
            x1="75"
            y1="510"
            x2="1280"
            y2="510"
            stroke="{DIAL}"
            stroke-width="8"
        />


        <!-- Hélices -->

        <ellipse
            cx="55"
            cy="170"
            rx="12"
            ry="40"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <ellipse
            cx="55"
            cy="510"
            rx="12"
            ry="40"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================ -->
        <!-- GENERADORES DIESEL -->
        <!-- ================================================ -->

        <text
            x="260"
            y="48"
            text-anchor="middle"
            fill="{MIST}"
            font-size="19"
        >
            Generadores diesel
        </text>


        <rect
            x="160"
            y="70"
            width="200"
            height="62"
            rx="7"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="160"
            y="445"
            width="200"
            height="62"
            rx="7"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="160"
            y="535"
            width="200"
            height="62"
            rx="7"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================ -->
        <!-- TURBINA DE GAS -->
        <!-- ================================================ -->

        <text
            x="460"
            y="250"
            text-anchor="middle"
            fill="{MIST}"
            font-size="21"
        >
            Turbina de gas
        </text>


        <rect
            x="220"
            y="275"
            width="500"
            height="165"
            rx="12"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="4"
        />


        <!-- Compresor -->

        <polygon
            points="
                245,310
                415,330
                415,385
                245,405
            "
            fill="{comp_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- Combustión -->

        <rect
            x="430"
            y="315"
            width="95"
            height="85"
            fill="{SIGNAL}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- Turbina -->

        <polygon
            points="
                545,330
                680,305
                680,410
                545,385
            "
            fill="{turb_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <text
            x="330"
            y="426"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Compresor
        </text>


        <text
            x="477"
            y="426"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Combustión
        </text>


        <text
            x="610"
            y="426"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Turbina
        </text>


        <!-- ================================================ -->
        <!-- EMBRAGUES -->
        <!-- ================================================ -->

        <circle
            cx="780"
            cy="290"
            r="27"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />

        <circle
            cx="780"
            cy="455"
            r="27"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />


        <!-- ================================================ -->
        <!-- CAJAS -->
        <!-- ================================================ -->

        <rect
            x="880"
            y="100"
            width="58"
            height="185"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="880"
            y="420"
            width="58"
            height="185"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================ -->
        <!-- MOTORES ELÉCTRICOS -->
        <!-- ================================================ -->

        <rect
            x="1035"
            y="105"
            width="145"
            height="90"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="1035"
            y="475"
            width="145"
            height="90"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================ -->
        <!-- CONEXIONES TURBINA -->
        <!-- ================================================ -->

        <line
            x1="720"
            y1="355"
            x2="753"
            y2="290"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <line
            x1="720"
            y1="355"
            x2="753"
            y2="455"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <line
            x1="807"
            y1="290"
            x2="880"
            y2="195"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <line
            x1="807"
            y1="455"
            x2="880"
            y2="510"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================ -->
        <!-- TELEMETRÍA LOCAL -->
        <!-- ================================================ -->


        <!-- Condición operacional -->

        <rect
            x="45"
            y="280"
            width="145"
            height="85"
            rx="7"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="60"
            y="305"
            class="title"
        >
            Operación
        </text>

        <text
            x="60"
            y="330"
            class="text"
        >
            lp = {lp}
        </text>

        <text
            x="60"
            y="352"
            class="text"
        >
            v = {v} knots
        </text>


        <!-- Compresor -->

        <rect
            x="225"
            y="475"
            width="205"
            height="115"
            rx="7"
            fill="{HULL}"
            stroke="{comp_color}"
            stroke-width="2"
        />

        <text
            x="240"
            y="502"
            class="title"
        >
            Compresor
        </text>

        <text
            x="240"
            y="528"
            class="text"
        >
            T2 = {t2} °C
        </text>

        <text
            x="240"
            y="551"
            class="text"
        >
            P2 = {p2} bar
        </text>

        <text
            x="240"
            y="576"
            class="value"
        >
            kMc = {kmc}
        </text>


        <!-- Combustión -->

        <rect
            x="450"
            y="475"
            width="180"
            height="92"
            rx="7"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="2"
        />

        <text
            x="465"
            y="502"
            class="title"
        >
            Combustión
        </text>

        <text
            x="465"
            y="528"
            class="text"
        >
            mf = {mf} kg/s
        </text>

        <text
            x="465"
            y="551"
            class="text"
        >
            TIC = {tic} %
        </text>


        <!-- Turbina HP -->

        <rect
            x="650"
            y="480"
            width="200"
            height="115"
            rx="7"
            fill="{HULL}"
            stroke="{turb_color}"
            stroke-width="2"
        />

        <text
            x="665"
            y="507"
            class="title"
        >
            Turbina HP
        </text>

        <text
            x="665"
            y="533"
            class="text"
        >
            T48 = {t48} °C
        </text>

        <text
            x="665"
            y="556"
            class="text"
        >
            P48 = {p48} bar
        </text>

        <text
            x="665"
            y="581"
            class="value"
        >
            kMt = {kmt}
        </text>


        <!-- Eje turbina / generador -->

        <rect
            x="730"
            y="80"
            width="205"
            height="105"
            rx="7"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="745"
            y="107"
            class="title"
        >
            Eje / generador
        </text>

        <text
            x="745"
            y="132"
            class="text"
        >
            GTn = {gtn} rpm
        </text>

        <text
            x="745"
            y="154"
            class="text"
        >
            GGn = {ggn} rpm
        </text>

        <text
            x="745"
            y="176"
            class="text"
        >
            GTT = {gtt} kN m
        </text>


        <!-- Escape -->

        <rect
            x="725"
            y="205"
            width="155"
            height="60"
            rx="7"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="740"
            y="231"
            class="title"
        >
            Escape
        </text>

        <text
            x="740"
            y="253"
            class="text"
        >
            Pexh = {pexh} bar
        </text>


        <!-- Torque hélice estribor -->

        <rect
            x="1190"
            y="95"
            width="160"
            height="70"
            rx="7"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text
            x="1205"
            y="122"
            class="title"
        >
            Hélice estribor
        </text>

        <text
            x="1205"
            y="148"
            class="text"
        >
            Ts = {ts} kN m
        </text>


    </svg>

    </body>
    </html>
    """


    components.html(
        html,
        height=680,
        scrolling=False
    )
