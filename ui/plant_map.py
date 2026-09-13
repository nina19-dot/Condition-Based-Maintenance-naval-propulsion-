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

    compressor_fill = (
        SIGNAL
        if componente in [
            "compressor",
            "both"
        ]
        else "#4F9BD8"
    )

    turbine_fill = (
        BRASS
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
            background: {INK};
            font-family: Arial;
        }}
    </style>

    <svg
        viewBox="0 0 1100 440"
        width="100%"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- TÍTULO -->
        <text
            x="25"
            y="30"
            fill="{MIST}"
            font-size="15"
        >
            CODLAG PROPULSION PLANT
        </text>


        <!-- HÉLICE SUPERIOR -->
        <line
            x1="60"
            y1="125"
            x2="930"
            y2="125"
            stroke="{DIAL}"
            stroke-width="7"
        />

        <ellipse
            cx="45"
            cy="125"
            rx="10"
            ry="30"
            fill="none"
            stroke="{DIAL}"
            stroke-width="5"
        />


        <!-- HÉLICE INFERIOR -->
        <line
            x1="60"
            y1="330"
            x2="930"
            y2="330"
            stroke="{DIAL}"
            stroke-width="7"
        />

        <ellipse
            cx="45"
            cy="330"
            rx="10"
            ry="30"
            fill="none"
            stroke="{DIAL}"
            stroke-width="5"
        />


        <!-- GENERADORES DIÉSEL -->
        <rect
            x="160"
            y="65"
            width="180"
            height="55"
            rx="5"
            fill="#7138A8"
            stroke="{DIAL}"
            stroke-width="3"
        />

        <text
            x="250"
            y="55"
            text-anchor="middle"
            fill="{MIST}"
            font-size="14"
        >
            Diesel generators
        </text>


        <!-- MOTOR SUPERIOR -->
        <rect
            x="850"
            y="65"
            width="105"
            height="65"
            rx="4"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="3"
        />

        <text
            x="900"
            y="55"
            text-anchor="middle"
            fill="{MIST}"
            font-size="14"
        >
            Electric motor
        </text>


        <!-- MOTOR INFERIOR -->
        <rect
            x="850"
            y="285"
            width="105"
            height="65"
            rx="4"
            fill="{BRASS}"
            stroke="{DIAL}"
            stroke-width="3"
        />


        <!-- REDUCTORAS -->
        <rect
            x="750"
            y="75"
            width="42"
            height="110"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="3"
        />

        <rect
            x="750"
            y="255"
            width="42"
            height="110"
            fill="{SEA}"
            stroke="{DIAL}"
            stroke-width="3"
        />


        <!-- TURBINA DE GAS -->
        <rect
            x="230"
            y="180"
            width="330"
            height="105"
            rx="7"
            fill="{HULL}"
            stroke="{STEEL}"
            stroke-width="3"
        />

        <text
            x="395"
            y="170"
            text-anchor="middle"
            fill="{MIST}"
            font-size="16"
        >
            Gas turbine
        </text>


        <!-- COMPRESOR -->
        <polygon
            points="
            250,205
            360,225
            360,260
            250,275
            "
            fill="{compressor_fill}"
            stroke="{DIAL}"
            stroke-width="3"
        />

        <text
            x="305"
            y="297"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="13"
        >
            Compressor
        </text>


        <!-- COMBUSTIÓN -->
        <rect
            x="365"
            y="214"
            width="62"
            height="55"
            fill="{SIGNAL}"
            stroke="{DIAL}"
            stroke-width="3"
        />

        <text
            x="396"
            y="242"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="12"
        >
            Comb.
        </text>


        <!-- TURBINA -->
        <polygon
            points="
            440,215
            540,195
            540,280
            440,260
            "
            fill="{turbine_fill}"
            stroke="{DIAL}"
            stroke-width="3"
        />

        <text
            x="490"
            y="300"
            text-anchor="middle"
            fill="{DIAL}"
            font-size="13"
        >
            Turbine
        </text>


        <!-- EJE TURBINA -->
        <line
            x1="560"
            y1="235"
            x2="700"
            y2="235"
            stroke="{DIAL}"
            stroke-width="7"
        />


        <!-- EMBRAGUES -->
        <circle
            cx="690"
            cy="180"
            r="22"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="4"
        />

        <circle
            cx="690"
            cy="290"
            r="22"
            fill="{HULL}"
            stroke="{SIGNAL}"
            stroke-width="4"
        />


        <!-- RAMIFICACIONES -->
        <line
            x1="700"
            y1="235"
            x2="750"
            y2="125"
            stroke="{DIAL}"
            stroke-width="5"
        />

        <line
            x1="700"
            y1="235"
            x2="750"
            y2="330"
            stroke="{DIAL}"
            stroke-width="5"
        />


        <!-- SENSORES PRINCIPALES -->
        <text
            x="280"
            y="220"
            fill="{INK}"
            font-size="12"
        >
            T2 · P2
        </text>

        <text
            x="460"
            y="235"
            fill="{DIAL}"
            font-size="12"
        >
            T48 · P48
        </text>

        <text
            x="575"
            y="220"
            fill="{BRASS}"
            font-size="12"
        >
            GTT · GTn · GGn
        </text>


    </svg>
    """

    components.html(
        html,
        height=390,
        scrolling=False
    )
