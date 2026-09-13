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

        .stage {{
            fill: {DIAL};
            font-size: 18px;
            font-weight: bold;
        }}

        .data-title {{
            fill: {DIAL};
            font-size: 14px;
            font-weight: bold;
        }}

        .data {{
            fill: {MIST};
            font-size: 13px;
        }}

        .value {{
            fill: {BRASS};
            font-size: 13px;
            font-weight: bold;
        }}

    </style>

    </head>


    <body>


    <svg
        viewBox="0 0 1400 570"
        xmlns="http://www.w3.org/2000/svg"
    >


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
                    stop-color="#E2AD47"
                />

                <stop
                    offset="100%"
                    stop-color="#A76918"
                />

            </linearGradient>


            <filter id="shadow">

                <feDropShadow
                    dx="0"
                    dy="5"
                    stdDeviation="7"
                    flood-color="#000"
                    flood-opacity="0.28"
                />

            </filter>

        </defs>


        <!-- ================================================ -->
        <!-- ADMISIÓN -->
        <!-- ================================================ -->

        <polygon
            points="
                20,105
                190,145
                190,255
                20,295
            "
            fill="#142F33"
            stroke="{MIST}"
            stroke-width="3"
        />


        <path
            d="M35 145 C90 145 130 155 180 170"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="5"
        />

        <path
            d="M35 200 C95 200 130 200 180 200"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="5"
        />

        <path
            d="M35 255 C90 255 130 245 180 230"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="5"
        />


        <!-- ================================================ -->
        <!-- COMPRESOR -->
        <!-- ================================================ -->

        <polygon
            points="
                190,120
                440,155
                440,245
                190,280
            "
            fill="url(#compressorGradient)"
            stroke="{DIAL}"
            stroke-width="4"
            filter="url(#shadow)"
        />


        <line x1="235" y1="126" x2="235" y2="274"
              stroke="{INK}" stroke-width="8"/>

        <line x1="290" y1="134" x2="290" y2="266"
              stroke="{INK}" stroke-width="8"/>

        <line x1="345" y1="142" x2="345" y2="258"
              stroke="{INK}" stroke-width="8"/>

        <line x1="400" y1="150" x2="400" y2="250"
              stroke="{INK}" stroke-width="8"/>


        <!-- ================================================ -->
        <!-- COMBUSTIÓN -->
        <!-- ================================================ -->

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


        <polygon
            points="
                515,190
                625,190
                680,200
                625,210
                515,210
            "
            fill="{SIGNAL}"
        />


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


        <!-- ================================================ -->
        <!-- TURBINA -->
        <!-- ================================================ -->

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


        <line x1="805" y1="147" x2="805" y2="253"
              stroke="{INK}" stroke-width="8"/>

        <line x1="855" y1="137" x2="855" y2="263"
              stroke="{INK}" stroke-width="8"/>

        <line x1="905" y1="128" x2="905" y2="272"
              stroke="{INK}" stroke-width="8"/>

        <line x1="945" y1="120" x2="945" y2="280"
              stroke="{INK}" stroke-width="8"/>


        <!-- ================================================ -->
        <!-- ESCAPE -->
        <!-- ================================================ -->

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


        <!-- EJE -->

        <line
            x1="190"
            y1="200"
            x2="970"
            y2="200"
            stroke="#D8D8D8"
            stroke-width="8"
        />


        <!-- ================================================ -->
        <!-- ETIQUETAS -->
        <!-- ================================================ -->

        <text
            x="100"
            y="365"
            text-anchor="middle"
            class="stage"
        >
            Admisión
        </text>


        <text
            x="315"
            y="365"
            text-anchor="middle"
            class="stage"
        >
            Compresor
        </text>


        <text
            x="595"
            y="365"
            text-anchor="middle"
            class="stage"
        >
            Cámara de combustión
        </text>


        <text
            x="865"
            y="365"
            text-anchor="middle"
            class="stage"
        >
            Turbina
        </text>


        <text
            x="1180"
            y="365"
            text-anchor="middle"
            class="stage"
        >
            Escape
        </text>


        <!-- ================================================ -->
        <!-- DATOS POR ETAPA -->
        <!-- ================================================ -->


        <!-- OPERACIÓN -->

        <rect
            x="20"
            y="400"
            width="190"
            height="115"
            rx="10"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text x="35" y="428" class="data-title">
            Operación
        </text>

        <text x="35" y="456" class="data">
            lp = {lp}
        </text>

        <text x="35" y="483" class="data">
            v = {v} knots
        </text>


        <!-- COMPRESOR -->

        <rect
            x="235"
            y="400"
            width="220"
            height="130"
            rx="10"
            fill="{HULL}"
            stroke="#4E9FDB"
            stroke-width="2"
        />

        <text x="250" y="428" class="data-title">
            Salida compresor
        </text>

        <text x="250" y="456" class="data">
            T2 = {t2} °C
        </text>

        <text x="250" y="483" class="data">
            P2 = {p2} bar
        </text>

        <text x="250" y="512" class="value">
            kMc = {kmc}
        </text>


        <!-- COMBUSTIÓN -->

        <rect
            x="480"
            y="400"
            width="220"
            height="115"
            rx="10"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="2"
        />

        <text x="495" y="428" class="data-title">
            Combustión
        </text>

        <text x="495" y="456" class="data">
            mf = {mf} kg/s
        </text>

        <text x="495" y="483" class="data">
            TIC = {tic} %
        </text>


        <!-- GENERADOR -->

        <rect
            x="725"
            y="400"
            width="225"
            height="130"
            rx="10"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text x="740" y="428" class="data-title">
            Eje / generador
        </text>

        <text x="740" y="456" class="data">
            GGn = {ggn} rpm
        </text>

        <text x="740" y="483" class="data">
            GTn = {gtn} rpm
        </text>

        <text x="740" y="510" class="data">
            GTT = {gtt} kN m
        </text>


        <!-- TURBINA -->

        <rect
            x="975"
            y="400"
            width="215"
            height="130"
            rx="10"
            fill="{HULL}"
            stroke="{BRASS}"
            stroke-width="2"
        />

        <text x="990" y="428" class="data-title">
            Salida turbina HP
        </text>

        <text x="990" y="456" class="data">
            T48 = {t48} °C
        </text>

        <text x="990" y="483" class="data">
            P48 = {p48} bar
        </text>

        <text x="990" y="512" class="value">
            kMt = {kmt}
        </text>


        <!-- ESCAPE -->

        <rect
            x="1215"
            y="400"
            width="165"
            height="115"
            rx="10"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="2"
        />

        <text x="1230" y="428" class="data-title">
            Escape
        </text>

        <text x="1230" y="456" class="data">
            Pexh = {pexh} bar
        </text>


    </svg>

    </body>

    </html>
    """


    components.html(
        html,
        height=570,
        scrolling=False
    )
