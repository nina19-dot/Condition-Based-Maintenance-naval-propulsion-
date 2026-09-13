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
    # COLORES DE LOS COMPONENTES
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

    # Tp = Ts en este dataset.
    tp = _fmt(
        valores.get(
            "Tp",
            valores.get("Ts")
        )
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
            stroke-dasharray: 9 7;
        }}

        .line-compressor {{
            fill: none;
            stroke: {comp_color};
            stroke-width: 3;
            stroke-dasharray: 9 7;
        }}

        .line-combustion {{
            fill: none;
            stroke: {SIGNAL};
            stroke-width: 3;
            stroke-dasharray: 9 7;
        }}

        .line-turbine {{
            fill: none;
            stroke: {turb_color};
            stroke-width: 3;
            stroke-dasharray: 9 7;
        }}

    </style>

    </head>

    <body>


    <svg
        viewBox="0 0 1600 930"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- ================================================= -->
        <!-- DEFINICIONES -->
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


            <!-- Flecha neutra -->

            <marker
                id="arrow-neutral"
                markerWidth="10"
                markerHeight="10"
                refX="8"
                refY="5"
                orient="auto"
            >

                <path
                    d="M 0 0 L 10 5 L 0 10 z"
                    fill="{MIST}"
                />

            </marker>


            <!-- Flecha compresor -->

            <marker
                id="arrow-compressor"
                markerWidth="10"
                markerHeight="10"
                refX="8"
                refY="5"
                orient="auto"
            >

                <path
                    d="M 0 0 L 10 5 L 0 10 z"
                    fill="{comp_color}"
                />

            </marker>


            <!-- Flecha combustión -->

            <marker
                id="arrow-combustion"
                markerWidth="10"
                markerHeight="10"
                refX="8"
                refY="5"
                orient="auto"
            >

                <path
                    d="M 0 0 L 10 5 L 0 10 z"
                    fill="{SIGNAL}"
                />

            </marker>


            <!-- Flecha turbina -->

            <marker
                id="arrow-turbine"
                markerWidth="10"
                markerHeight="10"
                refX="8"
                refY="5"
                orient="auto"
            >

                <path
                    d="M 0 0 L 10 5 L 0 10 z"
                    fill="{turb_color}"
                />

            </marker>

        </defs>


        <!-- ================================================= -->
        <!-- EJES DE PROPULSIÓN -->
        <!-- ================================================= -->

        <line
            x1="130"
            y1="285"
            x2="1410"
            y2="285"
            stroke="{DIAL}"
            stroke-width="8"
        />

        <line
            x1="130"
            y1="650"
            x2="1410"
            y2="650"
            stroke="{DIAL}"
            stroke-width="8"
        />


        <!-- ================================================= -->
        <!-- HÉLICES -->
        <!-- ================================================= -->

        <ellipse
            cx="95"
            cy="285"
            rx="13"
            ry="48"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <ellipse
            cx="95"
            cy="650"
            rx="13"
            ry="48"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <text
            x="25"
            y="215"
            class="component-label"
        >
            Hélice estribor
        </text>

        <text
            x="25"
            y="580"
            class="component-label"
        >
            Hélice babor
        </text>


        <!-- ================================================= -->
        <!-- GENERADORES DIESEL -->
        <!-- ================================================= -->

        <text
            x="315"
            y="165"
            text-anchor="middle"
            class="component-label"
        >
            Generadores diesel
        </text>


        <rect
            x="200"
            y="195"
            width="235"
            height="72"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="200"
            y="560"
            width="235"
            height="72"
            rx="8"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <rect
            x="200"
            y="675"
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
            y="175"
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
            y="180"
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
        <!-- CAJAS DE TELEMETRÍA -->
        <!-- ================================================= -->


        <!-- TORQUE HÉLICES -->

        <g filter="url(#shadow)">

            <rect
                x="20"
                y="385"
                width="210"
                height="90"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="40"
                y="417"
                class="box-title"
            >
                Torque hélices
            </text>

            <text
                x="40"
                y="450"
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
                x="1180"
                y="390"
                width="180"
                height="80"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="1200"
                y="422"
                class="box-title"
            >
                Escape
            </text>

            <text
                x="1200"
                y="452"
                class="box-text"
            >
                Pexh = {pexh} bar
            </text>

        </g>


        <!-- OPERACIÓN -->

        <g filter="url(#shadow)">

            <rect
                x="1375"
                y="395"
                width="200"
                height="110"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="1395"
                y="428"
                class="box-title"
            >
                Operación
            </text>

            <text
                x="1395"
                y="460"
                class="box-text"
            >
                lp = {lp}
            </text>

            <text
                x="1395"
                y="490"
                class="box-text"
            >
                v = {v} knots
            </text>

        </g>


        <!-- ================================================= -->
        <!-- CONECTORES DE TELEMETRÍA -->
        <!-- Se dibujan AL FINAL para quedar por encima -->
        <!-- ================================================= -->


        <!-- TORQUE HÉLICES -->
        <!-- Caja -> bifurcación -->

        <polyline
            points="
                230,430
                270,430
                270,285
                135,285
            "
            class="line-neutral"
            marker-end="url(#arrow-neutral)"
        />

        <polyline
            points="
                270,430
                270,650
                135,650
            "
            class="line-neutral"
            marker-end="url(#arrow-neutral)"
        />

        <circle
            cx="135"
            cy="285"
            r="6"
            fill="{MIST}"
        />

        <circle
            cx="135"
            cy="650"
            r="6"
            fill="{MIST}"
        />


        <!-- ================================================= -->
        <!-- COMBUSTIÓN -->
        <!-- Rodea completamente el título Turbina de gas -->
        <!-- ================================================= -->

        <polyline
            points="
                615,155
                740,155
                740,350
                635,350
                635,395
            "
            class="line-combustion"
            marker-end="url(#arrow-combustion)"
        />

        <circle
            cx="635"
            cy="400"
            r="6"
            fill="{SIGNAL}"
        />


        <!-- ================================================= -->
        <!-- GENERADOR DE GAS -->
        <!-- ================================================= -->

        <polyline
            points="
                880,135
                880,350
                850,350
                850,395
            "
            class="line-neutral"
            marker-end="url(#arrow-neutral)"
        />

        <circle
            cx="850"
            cy="395"
            r="6"
            fill="{MIST}"
        />


        <!-- ================================================= -->
        <!-- SALIDA COMPRESOR -->
        <!-- ================================================= -->

        <polyline
            points="
                445,755
                445,590
                445,515
            "
            class="line-compressor"
            marker-end="url(#arrow-compressor)"
        />

        <circle
            cx="445"
            cy="510"
            r="6"
            fill="{comp_color}"
        />


        <!-- ================================================= -->
        <!-- TURBINA / EJE -->
        <!-- Muy visible y llega a la salida de la turbina -->
        <!-- ================================================= -->

        <polyline
            points="
                795,750
                795,705
                915,705
                915,455
                855,455
            "
            class="line-turbine"
            marker-end="url(#arrow-turbine)"
        />

        <circle
            cx="850"
            cy="455"
            r="7"
            fill="{turb_color}"
        />


        <!-- ================================================= -->
        <!-- ESCAPE -->
        <!-- ================================================= -->

        <polyline
            points="
                1180,430
                1100,430
                1000,455
                895,455
            "
            class="line-neutral"
            marker-end="url(#arrow-neutral)"
        />

        <circle
            cx="890"
            cy="455"
            r="6"
            fill="{MIST}"
        />


        <!-- ================================================= -->
        <!-- OPERACIÓN -->
        <!-- Ahora sí llega claramente a la línea principal -->
        <!-- ================================================= -->

        <polyline
            points="
                1375,450
                1340,450
                1340,340
                1435,340
                1435,285
                1415,285
            "
            class="line-neutral"
            marker-end="url(#arrow-neutral)"
        />

        <circle
            cx="1410"
            cy="285"
            r="7"
            fill="{MIST}"
        />


    </svg>

    </body>

    </html>
    """

    components.html(
        html,
        height=930,
        scrolling=False
    )
