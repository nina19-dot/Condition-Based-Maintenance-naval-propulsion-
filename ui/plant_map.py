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

    # ========================================================
    # COLORES SEGÚN COMPONENTE ANALIZADO
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
    # TELEMETRÍA QUE SÍ QUEREMOS MOSTRAR
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

        .section-label {{
            fill: {MIST};
            font-size: 18px;
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

        .box-value {{
            fill: {BRASS};
            font-size: 13px;
            font-weight: bold;
        }}

    </style>

    </head>


    <body>


    <svg
        viewBox="0 0 1400 720"
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
        <!-- PROPULSIÓN SUPERIOR -->
        <!-- ================================================= -->

        <line
            x1="70"
            y1="155"
            x2="1260"
            y2="155"
            stroke="{DIAL}"
            stroke-width="8"
        />

        <ellipse
            cx="48"
            cy="155"
            rx="12"
            ry="42"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- PROPULSIÓN INFERIOR -->
        <!-- ================================================= -->

        <line
            x1="70"
            y1="565"
            x2="1260"
            y2="565"
            stroke="{DIAL}"
            stroke-width="8"
        />

        <ellipse
            cx="48"
            cy="565"
            rx="12"
            ry="42"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- GENERADORES DIESEL -->
        <!-- ================================================= -->

        <text
            x="255"
            y="40"
            text-anchor="middle"
            class="section-label"
        >
            Generadores diesel
        </text>


        <rect
            x="145"
            y="65"
            width="220"
            height="65"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="145"
            y="480"
            width="220"
            height="65"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="145"
            y="590"
            width="220"
            height="65"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================= -->
        <!-- TURBINA DE GAS -->
        <!-- ================================================= -->

        <text
            x="480"
            y="260"
            text-anchor="middle"
            class="section-label"
        >
            Turbina de gas
        </text>


        <rect
            x="210"
            y="285"
            width="545"
            height="185"
            rx="14"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="4"
            filter="url(#shadow)"
        />


        <!-- COMPRESOR -->

        <polygon
            points="
                240,325
                430,348
                430,407
                240,430
            "
            fill="{comp_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="280"
            y1="330"
            x2="280"
            y2="425"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="325"
            y1="336"
            x2="325"
            y2="419"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="370"
            y1="341"
            x2="370"
            y2="414"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- COMBUSTIÓN -->

        <rect
            x="445"
            y="325"
            width="105"
            height="105"
            rx="5"
            fill="{SIGNAL}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- TURBINA -->

        <polygon
            points="
                575,345
                720,320
                720,435
                575,410
            "
            fill="{turb_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="610"
            y1="339"
            x2="610"
            y2="416"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="655"
            y1="331"
            x2="655"
            y2="424"
            stroke="{INK}"
            stroke-width="7"
        />


        <text
            x="335"
            y="455"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Compresor
        </text>


        <text
            x="497"
            y="455"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Combustión
        </text>


        <text
            x="650"
            y="455"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Turbina
        </text>


        <!-- ================================================= -->
        <!-- EMBRAGUES -->
        <!-- ================================================= -->

        <circle
            cx="820"
            cy="295"
            r="28"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />

        <circle
            cx="820"
            cy="495"
            r="28"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- CAJAS -->
        <!-- ================================================= -->

        <rect
            x="930"
            y="85"
            width="65"
            height="195"
            rx="4"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <rect
            x="930"
            y="470"
            width="65"
            height="195"
            rx="4"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================= -->
        <!-- MOTORES ELÉCTRICOS -->
        <!-- ================================================= -->

        <rect
            x="1070"
            y="95"
            width="155"
            height="90"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <rect
            x="1070"
            y="520"
            width="155"
            height="90"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================= -->
        <!-- CONEXIONES DE TURBINA -->
        <!-- ================================================= -->

        <line
            x1="755"
            y1="375"
            x2="792"
            y2="295"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="755"
            y1="375"
            x2="792"
            y2="495"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="848"
            y1="295"
            x2="930"
            y2="185"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="848"
            y1="495"
            x2="930"
            y2="565"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- TELEMETRÍA LOCALIZADA -->
        <!-- ================================================= -->


        <!-- OPERACIÓN -->

        <g filter="url(#shadow)">

            <rect
                x="20"
                y="300"
                width="160"
                height="95"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="35"
                y="328"
                class="box-title"
            >
                Operación
            </text>

            <text
                x="35"
                y="355"
                class="box-text"
            >
                lp = {lp}
            </text>

            <text
                x="35"
                y="380"
                class="box-text"
            >
                v = {v} knots
            </text>

        </g>


        <!-- Línea hacia planta -->

        <line
            x1="180"
            y1="350"
            x2="210"
            y2="350"
            stroke="{STEEL}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- COMPRESOR -->

        <g filter="url(#shadow)">

            <rect
                x="225"
                y="505"
                width="210"
                height="115"
                rx="8"
                fill="{HULL}"
                stroke="{comp_color}"
                stroke-width="2"
            />

            <text
                x="240"
                y="532"
                class="box-title"
            >
                Salida compresor
            </text>

            <text
                x="240"
                y="558"
                class="box-text"
            >
                T2 = {t2} °C
            </text>

            <text
                x="240"
                y="582"
                class="box-text"
            >
                P2 = {p2} bar
            </text>

            <text
                x="240"
                y="607"
                class="box-value"
            >
                kMc = {kmc}
            </text>

        </g>


        <line
            x1="335"
            y1="505"
            x2="335"
            y2="470"
            stroke="{comp_color}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- COMBUSTIÓN -->

        <g filter="url(#shadow)">

            <rect
                x="430"
                y="160"
                width="185"
                height="100"
                rx="8"
                fill="{HULL}"
                stroke="{SIGNAL}"
                stroke-width="2"
            />

            <text
                x="445"
                y="188"
                class="box-title"
            >
                Combustión
            </text>

            <text
                x="445"
                y="215"
                class="box-text"
            >
                mf = {mf} kg/s
            </text>

            <text
                x="445"
                y="240"
                class="box-text"
            >
                TIC = {tic} %
            </text>

        </g>


        <line
            x1="500"
            y1="260"
            x2="500"
            y2="325"
            stroke="{SIGNAL}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- TURBINA HP -->

        <g filter="url(#shadow)">

            <rect
                x="570"
                y="510"
                width="205"
                height="115"
                rx="8"
                fill="{HULL}"
                stroke="{turb_color}"
                stroke-width="2"
            />

            <text
                x="585"
                y="537"
                class="box-title"
            >
                Turbina HP
            </text>

            <text
                x="585"
                y="563"
                class="box-text"
            >
                T48 = {t48} °C
            </text>

            <text
                x="585"
                y="587"
                class="box-text"
            >
                P48 = {p48} bar
            </text>

            <text
                x="585"
                y="612"
                class="box-value"
            >
                kMt = {kmt}
            </text>

        </g>


        <line
            x1="650"
            y1="510"
            x2="650"
            y2="470"
            stroke="{turb_color}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- GAS GENERATOR / SHAFT -->

        <g filter="url(#shadow)">

            <rect
                x="680"
                y="135"
                width="210"
                height="115"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="695"
                y="162"
                class="box-title"
            >
                Eje / generador
            </text>

            <text
                x="695"
                y="188"
                class="box-text"
            >
                GGn = {ggn} rpm
            </text>

            <text
                x="695"
                y="212"
                class="box-text"
            >
                GTn = {gtn} rpm
            </text>

            <text
                x="695"
                y="236"
                class="box-text"
            >
                GTT = {gtt} kN m
            </text>

        </g>


        <line
            x1="760"
            y1="250"
            x2="760"
            y2="320"
            stroke="{STEEL}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- ESCAPE -->

        <g filter="url(#shadow)">

            <rect
                x="790"
                y="370"
                width="165"
                height="72"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="805"
                y="398"
                class="box-title"
            >
                Escape
            </text>

            <text
                x="805"
                y="425"
                class="box-text"
            >
                Pexh = {pexh} bar
            </text>

        </g>


        <line
            x1="790"
            y1="405"
            x2="720"
            y2="405"
            stroke="{STEEL}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


    </svg>

    </body>

    </html>
    """

    components.html(
        html,
        height=720,
        scrolling=False
    )
