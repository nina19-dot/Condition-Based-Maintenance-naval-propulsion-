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


def esquema_planta(
    componente=None
):

    compresor = (
        "#E5483F"
        if componente in [
            "compressor",
            "both"
        ]
        else "#4E9FDB"
    )

    turbina = (
        "#F59E0B"
        if componente in [
            "turbine",
            "both"
        ]
        else "#9B5DE5"
    )

    html = f"""
    <style>

        body {{
            margin: 0;
            padding: 0;
            background: {INK};
        }}

        svg {{
            width: 100%;
            display: block;
        }}

    </style>


    <svg
        viewBox="0 0 1200 520"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- ================================================= -->
        <!-- HÉLICES -->
        <!-- ================================================= -->

        <line
            x1="70"
            y1="145"
            x2="1040"
            y2="145"
            stroke="{DIAL}"
            stroke-width="8"
        />

        <line
            x1="70"
            y1="385"
            x2="1040"
            y2="385"
            stroke="{DIAL}"
            stroke-width="8"
        />


        <!-- Hélice superior -->

        <ellipse
            cx="50"
            cy="145"
            rx="12"
            ry="38"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="50"
            y1="107"
            x2="25"
            y2="75"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="50"
            y1="183"
            x2="25"
            y2="215"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- Hélice inferior -->

        <ellipse
            cx="50"
            cy="385"
            rx="12"
            ry="38"
            fill="none"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="50"
            y1="347"
            x2="25"
            y2="315"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="50"
            y1="423"
            x2="25"
            y2="455"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- GENERADORES DIÉSEL -->
        <!-- ================================================= -->

        <text
            x="250"
            y="45"
            text-anchor="middle"
            fill="{MIST}"
            font-size="18"
        >
            Generadores diesel
        </text>


        <rect
            x="150"
            y="65"
            width="200"
            height="60"
            rx="6"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <circle cx="180" cy="95" r="13"
            fill="{INK}" stroke="{DIAL}" stroke-width="3"/>

        <circle cx="220" cy="95" r="13"
            fill="{INK}" stroke="{DIAL}" stroke-width="3"/>

        <circle cx="260" cy="95" r="13"
            fill="{INK}" stroke="{DIAL}" stroke-width="3"/>

        <circle cx="300" cy="95" r="13"
            fill="{INK}" stroke="{DIAL}" stroke-width="3"/>


        <!-- ================================================= -->
        <!-- TURBINA DE GAS -->
        <!-- ================================================= -->

        <text
            x="400"
            y="205"
            text-anchor="middle"
            fill="{MIST}"
            font-size="20"
        >
            Turbina de gas
        </text>


        <rect
            x="180"
            y="225"
            width="440"
            height="135"
            rx="10"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="4"
        />


        <!-- Compresor -->

        <polygon
            points="
                205,250
                370,270
                370,315
                205,335
            "
            fill="{compresor}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="245"
            y1="255"
            x2="245"
            y2="330"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="285"
            y1="260"
            x2="285"
            y2="325"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="325"
            y1="266"
            x2="325"
            y2="319"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- Cámara combustión -->

        <rect
            x="380"
            y="255"
            width="80"
            height="75"
            fill="{SIGNAL}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <!-- Turbina -->

        <polygon
            points="
                475,265
                595,245
                595,340
                475,320
            "
            fill="{turbina}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <line
            x1="510"
            y1="260"
            x2="510"
            y2="325"
            stroke="{INK}"
            stroke-width="7"
        />

        <line
            x1="550"
            y1="255"
            x2="550"
            y2="332"
            stroke="{INK}"
            stroke-width="7"
        />


        <!-- Labels -->

        <text
            x="285"
            y="350"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Compresor
        </text>

        <text
            x="420"
            y="350"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="15"
        >
            Combustión
        </text>

        <text
            x="535"
            y="350"
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
            cx="690"
            cy="235"
            r="25"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="5"
        />

        <circle
            cx="690"
            cy="355"
            r="25"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="5"
        />

        <text
            x="690"
            y="305"
            text-anchor="middle"
            fill="{MIST}"
            font-size="16"
        >
            Embragues
        </text>


        <!-- ================================================= -->
        <!-- REDUCTORAS -->
        <!-- ================================================= -->

        <rect
            x="765"
            y="90"
            width="55"
            height="140"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <rect
            x="765"
            y="310"
            width="55"
            height="140"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <text
            x="792"
            y="70"
            text-anchor="middle"
            fill="{MIST}"
            font-size="17"
        >
            Cajas
        </text>


        <!-- ================================================= -->
        <!-- MOTORES ELÉCTRICOS -->
        <!-- ================================================= -->

        <rect
            x="875"
            y="90"
            width="130"
            height="80"
            rx="5"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <rect
            x="875"
            y="350"
            width="130"
            height="80"
            rx="5"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="4"
        />


        <text
            x="940"
            y="70"
            text-anchor="middle"
            fill="{MIST}"
            font-size="17"
        >
            Motores eléctricos
        </text>


        <!-- ================================================= -->
        <!-- CONEXIONES TURBINA -->
        <!-- ================================================= -->

        <line
            x1="620"
            y1="292"
            x2="665"
            y2="235"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="620"
            y1="292"
            x2="665"
            y2="355"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <line
            x1="715"
            y1="235"
            x2="765"
            y2="160"
            stroke="{DIAL}"
            stroke-width="6"
        />

        <line
            x1="715"
            y1="355"
            x2="765"
            y2="385"
            stroke="{DIAL}"
            stroke-width="6"
        />


        <!-- ================================================= -->
        <!-- LEYENDA -->
        <!-- ================================================= -->

        <rect
            x="1040"
            y="235"
            width="125"
            height="40"
            fill="{compresor}"
            rx="4"
        />

        <text
            x="1102"
            y="260"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="14"
        >
            Compresor
        </text>


        <rect
            x="1040"
            y="295"
            width="125"
            height="40"
            fill="{turbina}"
            rx="4"
        />

        <text
            x="1102"
            y="320"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="14"
        >
            Turbina
        </text>

    </svg>
    """

    components.html(
        html,
        height=530,
        scrolling=False
    )
