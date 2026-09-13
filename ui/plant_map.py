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
# FUNCIÓN PARA FORMATEAR VALORES
# ============================================================

def _fmt(valor, dec=2):

    if valor is None:
        return "-"

    return f"{valor:.{dec}f}"


# ============================================================
# DIAGRAMA DE LA PLANTA CODLAG
# ============================================================

def esquema_planta(
    componente=None,
    valores=None,
    velocidad=None
):

    if valores is None:
        valores = {}

    # ========================================================
    # COLORES SEGÚN EL COMPONENTE ANALIZADO
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
    # VARIABLES DE TELEMETRÍA
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

    # Tp fue eliminado del modelo porque es igual a Ts.
    # Para mostrarlo en el diagrama usamos el valor de Ts
    # cuando Tp no está disponible.
    tp = _fmt(
        valores.get(
            "Tp",
            valores.get("Ts")
        )
    )

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

        /* Títulos principales de la planta */
        .component-label {{
            fill: {DIAL};
            font-size: 22px;
            font-weight: 800;
        }}

        /* Nombres internos de la turbina de gas */
        .internal-label {{
            fill: {DIAL};
            font-size: 17px;
            font-weight: 700;
        }}

        /* Título de las cajas de telemetría */
        .box-title {{
            fill: {DIAL};
            font-size: 16px;
            font-weight: 700;
        }}

        /* Valores de telemetría */
        .box-text {{
            fill: {MIST};
            font-size: 14px;
        }}

        /* Líneas punteadas normales */
        .connector {{
            stroke: {MIST};
            stroke-width: 3;
            stroke-dasharray: 8 6;
            fill: none;
        }}

        /* Línea de combustión */
        .connector-signal {{
            stroke: {SIGNAL};
            stroke-width: 3;
            stroke-dasharray: 8 6;
            fill: none;
        }}

        /* Línea de compresor */
        .connector-compressor {{
            stroke: {comp_color};
            stroke-width: 3;
            stroke-dasharray: 8 6;
            fill: none;
        }}

        /* Línea de turbina */
        .connector-turbine {{
            stroke: {turb_color};
            stroke-width: 3;
            stroke-dasharray: 8 6;
            fill: none;
        }}

    </style>

    </head>


    <body>


    <svg
        viewBox="0 0 1600 920"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- ================================================= -->
        <!-- SOMBRA PARA CAJAS -->
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

        <!-- Hélice estribor -->

        <ellipse
            cx="95"
            cy="285"
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


        <!-- Hélice babor -->

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


        <!-- ================================================= -->
        <!-- COMPRESOR -->
        <!-- ================================================= -->

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


        <!-- ================================================= -->
        <!-- CÁMARA DE COMBUSTIÓN -->
        <!-- ================================================= -->

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


        <!-- ================================================= -->
        <!-- TURBINA -->
        <!-- ================================================= -->

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


        <!-- ================================================= -->
        <!-- NOMBRES INTERNOS -->
        <!-- ================================================= -->

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
        <!-- TELEMETRÍA FUERA DEL DIAGRAMA -->
        <!-- ================================================= -->


        <!-- ================================================= -->
        <!-- TORQUE HÉLICES -->
        <!-- ================================================= -->

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


        <!-- Sale de la caja -->

        <path
            d="
                M 230 430
                L 265 430
            "
            class="connector"
        />


        <!-- Rama hacia eje superior -->

        <path
            d="
                M 265 430
                L 265 285
                L 130 285
            "
            class="connector"
        />


        <!-- Rama hacia eje inferior -->

        <path
            d="
                M 265 430
                L 265 650
                L 130 650
            "
            class="connector"
        />


        <!-- puntos de referencia -->

        <circle
            cx="130"
            cy="285"
            r="5"
            fill="{MIST}"
        />

        <circle
            cx="130"
            cy="650"
            r="5"
            fill="{MIST}"
        />


        <!-- ================================================= -->
        <!-- COMBUSTIÓN -->
        <!-- ================================================= -->

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


        <!--
        La línea primero se mueve hacia la derecha,
        después baja por fuera del título "Turbina de gas"
        y finalmente regresa a la cámara de combustión.
        -->

        <path
            d="
                M 615 155
                L 700 155
                L 700 365
                L 635 365
                L 635 400
            "
            class="connector-signal"
        />


        <circle
            cx="635"
            cy="400"
            r="5"
            fill="{SIGNAL}"
        />


        <!-- ================================================= -->
        <!-- GENERADOR DE GAS -->
        <!-- ================================================= -->

        <g filter="url(#shadow)">

            <rect
                x="760"
                y="45"
                width="220"
                height="90"
                rx="8"
                fill="{HULL}"
                stroke="{STEEL}"
                stroke-width="2"
            />

            <text
                x="780"
                y="78"
                class="box-title"
            >
                Generador de gas
            </text>

            <text
                x="780"
                y="110"
                class="box-text"
            >
                GGn = {ggn} rpm
            </text>

        </g>


        <path
            d="
                M 870 135
                L 870 365
                L 850 365
                L 850 395
            "
            class="connector"
        />


        <circle
            cx="850"
            cy="395"
            r="5"
            fill="{MIST}"
        />


        <!-- ================================================= -->
        <!-- SALIDA COMPRESOR -->
        <!-- ================================================= -->

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


        <path
            d="
                M 445 755
                L 445 560
                L 445 510
            "
            class="connector-compressor"
        />


        <circle
            cx="445"
            cy="510"
            r="5"
            fill="{comp_color}"
        />


        <!-- ================================================= -->
        <!-- TURBINA / EJE -->
        <!-- ================================================= -->

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


        <!--
        Sale por arriba de la caja,
        se desplaza a la derecha y llega
        al eje de salida de la turbina.
        -->

        <path
            d="
                M 795 750
                L 795 705
                L 900 705
                L 900 455
                L 850 455
            "
            class="connector-turbine"
        />


        <circle
            cx="850"
            cy="455"
            r="5"
            fill="{turb_color}"
        />


        <!-- ================================================= -->
        <!-- ESCAPE -->
        <!-- ================================================= -->

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


        <path
            d="
                M 1180 430
                L 1040 430
                L 890 455
            "
            class="connector"
        />


        <circle
            cx="890"
            cy="455"
            r="5"
            fill="{MIST}"
        />


        <!-- ================================================= -->
        <!-- OPERACIÓN -->
        <!-- ================================================= -->

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


        <!--
        Conexión desde Operación
        hasta la línea de propulsión superior.
        -->

        <path
            d="
                M 1375 450
                L 1340 450
                L 1340 330
                L 1410 330
                L 1410 285
            "
            class="connector"
        />


        <circle
            cx="1410"
            cy="285"
            r="5"
            fill="{MIST}"
        />


    </svg>

    </body>

    </html>
    """

    # ========================================================
    # MOSTRAR EN STREAMLIT
    # ========================================================

    components.html(
        html,
        height=920,
        scrolling=False
    )
