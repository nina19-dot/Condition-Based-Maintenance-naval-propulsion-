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


# ============================================================
# FORMATO DE VALORES
# ============================================================

def _fmt(valor, dec=2):

    if valor is None:
        return "-"

    return f"{valor:.{dec}f}"


# ============================================================
# PLANTA CODLAG
# ============================================================

def esquema_planta(
    componente=None,
    valores=None,
    velocidad=None
):

    if valores is None:
        valores = {}

    # ========================================================
    # COLORES
    # ========================================================

    # Compresor
    comp_color = (
        "#E5483F"
        if componente in ["compressor", "both"]
        else "#4E9FDB"
    )

    # Turbina siempre naranja
    turb_color = (
        "#F59E0B"
        if componente in ["turbine", "both"]
        else "#D98A20"
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

    # Tp y Ts son equivalentes en el dataset
    tp = _fmt(
        valores.get(
            "Tp",
            valores.get("Ts")
        )
    )

    # ========================================================
    # HTML / SVG
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
            fill: {DIAL};
            font-size: 22px;
            font-weight: 800;
        }}

        .internal-label {{
            fill: {DIAL};
            font-size: 17px;
            font-weight: 700;
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

        .line-neutral {{
            fill: none;
            stroke: {MIST};
            stroke-width: 3;
            stroke-dasharray: 8 7;
        }}

        .line-compressor {{
            fill: none;
            stroke: {comp_color};
            stroke-width: 3;
            stroke-dasharray: 8 7;
        }}

        .line-combustion {{
            fill: none;
            stroke: {SIGNAL};
            stroke-width: 3;
            stroke-dasharray: 8 7;
        }}

        .line-turbine {{
            fill: none;
            stroke: {turb_color};
            stroke-width: 3;
            stroke-dasharray: 8 7;
        }}

    </style>

    </head>


    <body>


    <svg
        viewBox="0 0 1600 900"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- ================================================= -->
        <!-- SOMBRAS -->
        <!-- ================================================= -->

        <defs>

            <filter id="shadow">

                <feDropShadow
                    dx="0"
                    dy="4"
                    stdDeviation="6"
                    flood-color="#000000"
                    flood-opacity="0.28"
                />

            </filter>

        </defs>


        <!-- ================================================= -->
        <!-- EJES PRINCIPALES -->
        <!-- ================================================= -->

        <line
            x1="130"
            y1="285"
            x2="1480"
            y2="285"
            stroke="{DIAL}"
            stroke-width="8"
        />

        <line
            x1="130"
            y1="650"
            x2="1480"
            y2="650"
            stroke="{DIAL}"
            stroke-width="8"
        />


        <!-- ================================================= -->
        <!-- HÉLICES -->
        <!-- ================================================= -->

        <!-- Hélice estribor -->

        <ellipse
            cx="85"
            cy="285"
            rx="13"
            ry="48"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <text
            x="95"
            y="190"
            text-anchor="middle"
            class="component-label"
        >
            Hélice estribor
        </text>


        <!-- Hélice babor -->

        <ellipse
            cx="85"
            cy="650"
            rx="13"
            ry="48"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <text
            x="95"
            y="555"
            text-anchor="middle"
            class="component-label"
        >
            Hélice babor
        </text>


        <!-- ================================================= -->
        <!-- GENERADORES DIESEL -->
        <!-- ================================================= -->

        <text
            x="310"
            y="155"
            text-anchor="middle"
            class="component-label"
        >
            Generadores diesel
        </text>


        <rect
            x="195"
            y="190"
            width="235"
            height="72"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="195"
            y="560"
            width="235"
            height="72"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="195"
            y="680"
            width="235"
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
            x="600"
            y="330"
            text-anchor="middle"
            class="component-label"
        >
            Turbina de gas
        </text>


        <rect
            x="330"
            y="355"
            width="560"
            height="205"
            rx="14"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="4"
            filter="url(#shadow)"
        />


        <!-- COMPRESOR -->

        <polygon
            points="
                365,400
                560,425
                560,485
                365,510
            "
            fill="{comp_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <line
            x1="415"
            y1="406"
            x2="415"
            y2="504"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="465"
            y1="412"
            x2="465"
            y2="498"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="515"
            y1="418"
            x2="515"
            y2="492"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- COMBUSTIÓN -->

        <rect
            x="580"
            y="400"
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
                720,420
                850,395
                850,515
                720,490
            "
            fill="{turb_color}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <line
            x1="760"
            y1="414"
            x2="760"
            y2="491"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="805"
            y1="406"
            x2="805"
            y2="499"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- NOMBRES INTERNOS -->

        <text
            x="465"
            y="540"
            text-anchor="middle"
            class="internal-label"
        >
            Compresor
        </text>

        <text
            x="635"
            y="540"
            text-anchor="middle"
            class="internal-label"
        >
            Combustión
        </text>

        <text
            x="785"
            y="540"
            text-anchor="middle"
            class="internal-label"
        >
            Turbina
        </text>


        <!-- ================================================= -->
        <!-- EMBRAGUES -->
        <!-- ================================================= -->

        <text
            x="950"
            y="335"
            text-anchor="middle"
            class="component-label"
        >
            Embragues
        </text>

        <circle
            cx="950"
            cy="395"
            r="30"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />

        <circle
            cx="950"
            cy="575"
            r="30"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- CAJAS -->
        <!-- ================================================= -->

        <text
            x="1115"
            y="170"
            text-anchor="middle"
            class="component-label"
        >
            Cajas
        </text>

        <rect
            x="1080"
            y="215"
            width="72"
            height="210"
            rx="4"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <rect
            x="1080"
            y="565"
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
            x="1325"
            y="175"
            text-anchor="middle"
            class="component-label"
        >
            Motores eléctricos
        </text>

        <rect
            x="1240"
            y="225"
            width="175"
            height="95"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <rect
            x="1240"
            y="600"
            width="175"
            height="95"
            rx="7"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- ================================================= -->
        <!-- CONEXIONES MECÁNICAS -->
        <!-- ================================================= -->

        <line
            x1="890"
            y1="455"
            x2="920"
            y2="395"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="890"
            y1="455"
            x2="920"
            y2="575"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="980"
            y1="395"
            x2="1080"
            y2="320"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="980"
            y1="575"
            x2="1080"
            y2="650"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- TELEMETRÍA -->
        <!-- ================================================= -->


        <!-- TORQUE HÉLICES -->

        <g filter="url(#shadow)">

            <rect
                x="15"
                y="390"
                width="205"
                height="90"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="35"
                y="422"
                class="box-title"
            >
                Torque hélices
            </text>

            <text
                x="35"
                y="455"
                class="box-text"
            >
                Tp = {tp} kN m
            </text>

        </g>


        <!-- COMBUSTIÓN -->

        <g filter="url(#shadow)">

            <rect
                x="500"
                y="45"
                width="230"
                height="110"
                rx="8"
                fill="{HULL}"
                stroke="{SIGNAL}"
                stroke-width="2"
            />

            <text
                x="520"
                y="78"
                class="box-title"
            >
                Combustión
            </text>

            <text
                x="520"
                y="110"
                class="box-text"
            >
                mf = {mf} kg/s
            </text>

            <text
                x="520"
                y="140"
                class="box-text"
            >
                TIC = {tic} %
            </text>

        </g>


        <!-- GENERADOR DE GAS -->

        <g filter="url(#shadow)">

            <rect
                x="770"
                y="45"
                width="220"
                height="90"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="790"
                y="78"
                class="box-title"
            >
                Generador de gas
            </text>

            <text
                x="790"
                y="110"
                class="box-text"
            >
                GGn = {ggn} rpm
            </text>

        </g>


        <!-- SALIDA COMPRESOR -->

        <g filter="url(#shadow)">

            <rect
                x="330"
                y="755"
                width="230"
                height="110"
                rx="8"
                fill="{HULL}"
                stroke="{comp_color}"
                stroke-width="2"
            />

            <text
                x="350"
                y="788"
                class="box-title"
            >
                Salida compresor
            </text>

            <text
                x="350"
                y="820"
                class="box-text"
            >
                T2 = {t2} °C
            </text>

            <text
                x="350"
                y="850"
                class="box-text"
            >
                P2 = {p2} bar
            </text>

        </g>


        <!-- TURBINA / EJE -->

        <g filter="url(#shadow)">

            <rect
                x="650"
                y="750"
                width="290"
                height="135"
                rx="8"
                fill="{HULL}"
                stroke="{turb_color}"
                stroke-width="2"
            />

            <text
                x="670"
                y="783"
                class="box-title"
            >
                Turbina / eje
            </text>

            <text
                x="670"
                y="815"
                class="box-text"
            >
                GTn = {gtn} rpm
            </text>

            <text
                x="670"
                y="845"
                class="box-text"
            >
                GTT = {gtt} kN m
            </text>

            <text
                x="670"
                y="875"
                class="box-text"
            >
                T48 = {t48} °C | P48 = {p48} bar
            </text>

        </g>


        <!-- ESCAPE -->

        <g filter="url(#shadow)">

            <rect
                x="1010"
                y="415"
                width="180"
                height="80"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="1030"
                y="447"
                class="box-title"
            >
                Escape
            </text>

            <text
                x="1030"
                y="477"
                class="box-text"
            >
                Pexh = {pexh} bar
            </text>

        </g>


        <!-- OPERACIÓN -->
        <!-- Lo bajamos para separarlo de Escape -->

        <g filter="url(#shadow)">

            <rect
                x="1370"
                y="500"
                width="200"
                height="110"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="1390"
                y="533"
                class="box-title"
            >
                Operación
            </text>

            <text
                x="1390"
                y="565"
                class="box-text"
            >
                lp = {lp}
            </text>

            <text
                x="1390"
                y="595"
                class="box-text"
            >
                v = {v} knots
            </text>

        </g>


        <!-- ================================================= -->
        <!-- CONECTORES -->
        <!-- SIN FLECHAS -->
        <!-- ================================================= -->


        <!-- TORQUE HÉLICES -->
        <!-- Un tronco corto que se divide en las dos líneas -->

        <polyline
            points="
                220,435
                255,435
                255,285
                135,285
            "
            class="line-neutral"
        />

        <polyline
            points="
                255,435
                255,650
                135,650
            "
            class="line-neutral"
        />

        <circle
            cx="135"
            cy="285"
            r="5"
            fill="{MIST}"
        />

        <circle
            cx="135"
            cy="650"
            r="5"
            fill="{MIST}"
        />


        <!-- COMBUSTIÓN -->
        <!-- Solo un giro; pasa a la derecha del título -->

        <polyline
            points="
                615,155
                700,155
                700,375
                635,375
                635,400
            "
            class="line-combustion"
        />

        <circle
            cx="635"
            cy="400"
            r="5"
            fill="{SIGNAL}"
        />


        <!-- GENERADOR DE GAS -->
        <!-- Conexión corta -->

        <polyline
            points="
                880,135
                880,365
                850,365
                850,395
            "
            class="line-neutral"
        />

        <circle
            cx="850"
            cy="395"
            r="5"
            fill="{MIST}"
        />


        <!-- SALIDA COMPRESOR -->
        <!-- Vertical y directa -->

        <line
            x1="445"
            y1="755"
            x2="445"
            y2="510"
            class="line-compressor"
        />

        <circle
            cx="445"
            cy="510"
            r="5"
            fill="{comp_color}"
        />


        <!-- TURBINA / EJE -->
        <!-- Vertical prácticamente directa -->

        <polyline
            points="
                795,750
                795,570
                850,570
                850,515
            "
            class="line-turbine"
        />

        <circle
            cx="850"
            cy="515"
            r="5"
            fill="{turb_color}"
        />


        <!-- ESCAPE -->
        <!-- Conexión corta hacia la salida de la turbina -->

        <line
            x1="1010"
            y1="455"
            x2="890"
            y2="455"
            class="line-neutral"
        />

        <circle
            cx="890"
            cy="455"
            r="5"
            fill="{MIST}"
        />


        <!-- OPERACIÓN -->
        <!-- Conexión sencilla al eje inferior -->
        <!-- No se conecta al motor eléctrico -->

        <polyline
            points="
                1370,555
                1335,555
                1335,650
            "
            class="line-neutral"
        />

        <circle
            cx="1335"
            cy="650"
            r="5"
            fill="{MIST}"
        />


    </svg>

    </body>

    </html>
    """

    components.html(
        html,
        height=900,
        scrolling=False
    )
