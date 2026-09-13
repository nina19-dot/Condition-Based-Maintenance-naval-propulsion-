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

    # Tp fue eliminado del modelo porque es idéntico a Ts.
    # Para visualización usamos el mismo valor.
    tp = _fmt(
        valores.get(
            "Tp",
            valores.get("Ts")
        )
    )

    # ========================================================
    # DIAGRAMA SVG
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
        <!-- EJES -->
        <!-- ================================================= -->

        <line
            x1="95"
            y1="185"
            x2="1370"
            y2="185"
            stroke="{DIAL}"
            stroke-width="8"
        />

        <line
            x1="95"
            y1="605"
            x2="1370"
            y2="605"
            stroke="{DIAL}"
            stroke-width="8"
        />


        <!-- ================================================= -->
        <!-- HÉLICES DEL LADO IZQUIERDO -->
        <!-- ================================================= -->

        <ellipse
            cx="65"
            cy="185"
            rx="12"
            ry="46"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <ellipse
            cx="65"
            cy="605"
            rx="12"
            ry="46"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <text
            x="22"
            y="120"
            class="component-label"
        >
            Hélice estribor
        </text>


        <text
            x="22"
            y="540"
            class="component-label"
        >
            Hélice babor
        </text>


        <!-- Torque conjunto de hélices -->

        <g filter="url(#shadow)">

            <rect
                x="20"
                y="335"
                width="175"
                height="82"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="38"
                y="365"
                class="box-title"
            >
                Torque hélices
            </text>

            <text
                x="38"
                y="395"
                class="box-text"
            >
                Tp = {tp} kN m
            </text>

        </g>


        <!-- ================================================= -->
        <!-- GENERADORES DIESEL -->
        <!-- ================================================= -->

        <text
            x="270"
            y="45"
            text-anchor="middle"
            class="component-label"
        >
            Generadores diesel
        </text>


        <rect
            x="165"
            y="75"
            width="230"
            height="72"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="165"
            y="500"
            width="230"
            height="72"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="165"
            y="615"
            width="230"
            height="72"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================= -->
        <!-- TURBINA DE GAS -->
        <!-- ================================================= -->

        <text
            x="500"
            y="290"
            text-anchor="middle"
            class="component-label"
        >
            Turbina de gas
        </text>


        <rect
            x="235"
            y="315"
            width="555"
            height="195"
            rx="14"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="4"
            filter="url(#shadow)"
        />


        <!-- COMPRESOR -->

        <polygon
            points="
                270,360
                475,385
                475,440
                270,465
            "
            fill="{comp_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="320"
            y1="366"
            x2="320"
            y2="459"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="370"
            y1="372"
            x2="370"
            y2="453"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="420"
            y1="378"
            x2="420"
            y2="447"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- COMBUSTIÓN -->

        <rect
            x="495"
            y="360"
            width="110"
            height="110"
            rx="6"
            fill="{SIGNAL}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- TURBINA -->

        <polygon
            points="
                630,380
                765,355
                765,475
                630,450
            "
            fill="{turb_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="670"
            y1="374"
            x2="670"
            y2="451"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="715"
            y1="366"
            x2="715"
            y2="459"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- Nombres internos -->

        <text
            x="370"
            y="492"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Compresor
        </text>

        <text
            x="550"
            y="492"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Combustión
        </text>

        <text
            x="695"
            y="492"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Turbina
        </text>


        <!-- ================================================= -->
        <!-- EMBRAGUES -->
        <!-- ================================================= -->

        <text
            x="865"
            y="245"
            text-anchor="middle"
            class="component-label"
        >
            Embragues
        </text>


        <circle
            cx="865"
            cy="315"
            r="30"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />


        <circle
            cx="865"
            cy="505"
            r="30"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- CAJAS -->
        <!-- ================================================= -->

        <text
            x="1030"
            y="50"
            text-anchor="middle"
            class="component-label"
        >
            Cajas
        </text>


        <rect
            x="995"
            y="90"
            width="72"
            height="210"
            rx="4"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="995"
            y="470"
            width="72"
            height="210"
            rx="4"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================= -->
        <!-- MOTORES ELÉCTRICOS -->
        <!-- ================================================= -->

        <text
            x="1210"
            y="60"
            text-anchor="middle"
            class="component-label"
        >
            Motores eléctricos
        </text>


        <rect
            x="1130"
            y="110"
            width="170"
            height="95"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="1130"
            y="555"
            width="170"
            height="95"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================= -->
        <!-- CONEXIONES -->
        <!-- ================================================= -->

        <line
            x1="790"
            y1="415"
            x2="835"
            y2="315"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="790"
            y1="415"
            x2="835"
            y2="505"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="895"
            y1="315"
            x2="995"
            y2="195"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="895"
            y1="505"
            x2="995"
            y2="605"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- TELEMETRÍA: COMBUSTIÓN MÁS ARRIBA -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="455"
                y="110"
                width="210"
                height="105"
                rx="8"
                fill="{HULL}"
                stroke="{SIGNAL}"
                stroke-width="2"
            />

            <text
                x="473"
                y="140"
                class="box-title"
            >
                Combustión
            </text>

            <text
                x="473"
                y="170"
                class="box-text"
            >
                mf = {mf} kg/s
            </text>

            <text
                x="473"
                y="198"
                class="box-text"
            >
                TIC = {tic} %
            </text>

        </g>


        <line
            x1="550"
            y1="215"
            x2="550"
            y2="360"
            stroke="{SIGNAL}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- ================================================= -->
        <!-- GENERADOR DE GAS -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="690"
                y="125"
                width="200"
                height="80"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="708"
                y="155"
                class="box-title"
            >
                Generador de gas
            </text>

            <text
                x="708"
                y="184"
                class="box-text"
            >
                GGn = {ggn} rpm
            </text>

        </g>


        <line
            x1="790"
            y1="205"
            x2="790"
            y2="355"
            stroke="{STEEL}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- ================================================= -->
        <!-- SALIDA COMPRESOR -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="265"
                y="545"
                width="215"
                height="105"
                rx="8"
                fill="{HULL}"
                stroke="{comp_color}"
                stroke-width="2"
            />

            <text
                x="283"
                y="575"
                class="box-title"
            >
                Salida compresor
            </text>

            <text
                x="283"
                y="604"
                class="box-text"
            >
                T2 = {t2} °C
            </text>

            <text
                x="283"
                y="631"
                class="box-text"
            >
                P2 = {p2} bar
            </text>

        </g>


        <line
            x1="370"
            y1="545"
            x2="370"
            y2="510"
            stroke="{comp_color}"
            stroke-width="2"
            stroke-dasharray="5 4"
        />


        <!-- ================================================= -->
        <!-- TURBINA / EJE -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="625"
                y="545"
                width="250"
                height="130"
                rx="8"
                fill="{HULL}"
                stroke="{turb_color}"
                stroke-width="2"
            />

            <text
                x="643"
                y="575"
                class="box-title"
            >
                Turbina / eje
            </text>

            <text
                x="643"
                y="603"
                class="box-text"
            >
                GTn = {gtn} rpm
            </text>

            <text
                x="643"
                y="630"
                class="box-text"
            >
                GTT = {gtt} kN m
            </text>

            <text
                x="643"
                y="657"
                class="box-text"
            >
                T48 = {t48} °C | P48 = {p48} bar
            </text>

        </g>


        <!-- ================================================= -->
        <!-- ESCAPE -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="805"
                y="390"
                width="165"
                height="75"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="823"
                y="420"
                class="box-title"
            >
                Escape
            </text>

            <text
                x="823"
                y="448"
                class="box-text"
            >
                Pexh = {pexh} bar
            </text>

        </g>


        <!-- ================================================= -->
        <!-- OPERACIÓN HASTA LA DERECHA -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="1310"
                y="335"
                width="170"
                height="105"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="1328"
                y="365"
                class="box-title"
            >
                Operación
            </text>

            <text
                x="1328"
                y="395"
                class="box-text"
            >
                lp = {lp}
            </text>

            <text
                x="1328"
                y="423"
                class="box-text"
            >
                v = {v} knots
            </text>

        </g>

    </svg>

    </body>
    </html>
    """

    components.html(
        html,
        height=800,
        scrolling=False
    )
