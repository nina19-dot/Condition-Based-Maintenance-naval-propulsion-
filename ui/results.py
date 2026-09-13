# ui/results.py

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

from config import (
    DIAL,
    BRASS,
    SIGNAL,
    SEA,
    MIST,
    HULL,
    RANGO_KMC,
    RANGO_KMT
)

from maintenance import (
    estado_compresor,
    estado_turbina
)


# ============================================================
# MANÓMETRO
# ============================================================

def manometro(valor, rango):

    minimo, maximo = rango
    amplitud = maximo - minimo

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=valor,

            number={
                "font": {
                    "size": 38,
                    "color": DIAL,
                    "family": "IBM Plex Mono"
                },
                "valueformat": ".4f"
            },

            gauge={
                "axis": {
                    "range": [minimo, maximo],
                    "tickvals": [minimo, maximo],
                    "tickfont": {
                        "color": MIST,
                        "size": 12
                    }
                },

                "bar": {
                    "color": "rgba(0,0,0,0)"
                },

                "threshold": {
                    "line": {
                        "color": DIAL,
                        "width": 6
                    },
                    "thickness": 0.9,
                    "value": valor
                },

                "bgcolor": HULL,

                "steps": [
                    {
                        "range": [
                            minimo,
                            minimo + 0.20 * amplitud
                        ],
                        "color": SIGNAL
                    },

                    {
                        "range": [
                            minimo + 0.20 * amplitud,
                            minimo + 0.40 * amplitud
                        ],
                        "color": BRASS
                    },

                    {
                        "range": [
                            minimo + 0.40 * amplitud,
                            maximo
                        ],
                        "color": SEA
                    }
                ]
            }
        )
    )

    fig.update_layout(
        height=260,
        margin=dict(
            l=15,
            r=15,
            t=15,
            b=5
        ),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


# ============================================================
# DIAGRAMA TURBINA DE GAS
# ============================================================

def diagrama_turbina_gas(componente):

    # Resaltar compresor o turbina
    comp_color = (
        SIGNAL
        if componente == "compressor"
        else "#536568"
    )

    turb_color = (
        BRASS
        if componente == "turbine"
        else "#536568"
    )

    html = f"""
    <html>

    <head>

    <style>

    body {{
        margin: 0;
        padding: 0;
        background-color: #10262A;
        font-family: Arial, sans-serif;
    }}

    svg {{
        width: 100%;
        height: auto;
        display: block;
    }}

    </style>

    </head>

    <body>

    <svg
        viewBox="0 0 900 270"
        xmlns="http://www.w3.org/2000/svg"
    >

        <!-- ADMISIÓN -->

        <polygon
            points="10,65 155,90 155,180 10,205"
            fill="none"
            stroke="#9FB2AF"
            stroke-width="3"
        />

        <path
            d="M 15 95 C 70 95, 100 105, 145 115"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="4"
        />

        <path
            d="M 15 135 C 70 135, 100 135, 145 135"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="4"
        />

        <path
            d="M 15 175 C 70 175, 100 165, 145 155"
            fill="none"
            stroke="#4F9BD8"
            stroke-width="4"
        />


        <!-- COMPRESOR -->

        <polygon
            points="155,80 340,105 340,165 155,190"
            fill="{comp_color}"
            stroke="#EDE7D8"
            stroke-width="4"
        />

        <line
            x1="185" y1="84"
            x2="185" y2="186"
            stroke="#10262A"
            stroke-width="7"
        />

        <line
            x1="220" y1="89"
            x2="220" y2="181"
            stroke="#10262A"
            stroke-width="7"
        />

        <line
            x1="255" y1="94"
            x2="255" y2="176"
            stroke="#10262A"
            stroke-width="7"
        />

        <line
            x1="290" y1="99"
            x2="290" y2="171"
            stroke="#10262A"
            stroke-width="7"
        />

        <line
            x1="320" y1="103"
            x2="320" y2="167"
            stroke="#10262A"
            stroke-width="7"
        />


        <!-- CÁMARA DE COMBUSTIÓN -->

        <rect
            x="345"
            y="82"
            width="225"
            height="106"
            fill="#263C40"
            stroke="#EDE7D8"
            stroke-width="4"
        />

        <rect
            x="380"
            y="100"
            width="155"
            height="70"
            rx="8"
            fill="#374E52"
            stroke="#9FB2AF"
            stroke-width="2"
        />

        <polygon
            points="395,122 485,122 530,135 485,148 395,148"
            fill="#C0402C"
        />

        <polygon
            points="390,135 420,112 412,130 445,135 412,143 420,160"
            fill="#F5C542"
        />


        <!-- TURBINA -->

        <polygon
            points="575,105 730,75 730,195 575,165"
            fill="{turb_color}"
            stroke="#EDE7D8"
            stroke-width="4"
        />

        <line
            x1="605" y1="99"
            x2="605" y2="171"
            stroke="#10262A"
            stroke-width="7"
        />

        <line
            x1="640" y1="92"
            x2="640" y2="178"
            stroke="#10262A"
            stroke-width="7"
        />

        <line
            x1="675" y1="85"
            x2="675" y2="185"
            stroke="#10262A"
            stroke-width="7"
        />

        <line
            x1="705" y1="80"
            x2="705" y2="190"
            stroke="#10262A"
            stroke-width="7"
        />


        <!-- ESCAPE -->

        <polygon
            points="730,75 890,45 890,225 730,195"
            fill="none"
            stroke="#9FB2AF"
            stroke-width="3"
        />

        <path
            d="M 740 105 C 785 95, 825 85, 880 80"
            fill="none"
            stroke="#B44B8A"
            stroke-width="4"
        />

        <path
            d="M 740 135 C 790 135, 830 135, 880 135"
            fill="none"
            stroke="#B44B8A"
            stroke-width="4"
        />

        <path
            d="M 740 165 C 785 175, 825 185, 880 190"
            fill="none"
            stroke="#B44B8A"
            stroke-width="4"
        />


        <!-- EJE -->

        <line
            x1="155"
            y1="135"
            x2="730"
            y2="135"
            stroke="#D8D8D8"
            stroke-width="7"
        />


        <!-- ETIQUETAS -->

        <text
            x="75"
            y="250"
            text-anchor="middle"
            fill="#9FB2AF"
            font-size="16"
        >
            Admisión
        </text>

        <text
            x="245"
            y="250"
            text-anchor="middle"
            fill="#EDE7D8"
            font-size="16"
            font-weight="bold"
        >
            Compresor
        </text>

        <text
            x="455"
            y="250"
            text-anchor="middle"
            fill="#EDE7D8"
            font-size="16"
        >
            Cámara de combustión
        </text>

        <text
            x="650"
            y="250"
            text-anchor="middle"
            fill="#EDE7D8"
            font-size="16"
            font-weight="bold"
        >
            Turbina
        </text>

        <text
            x="815"
            y="250"
            text-anchor="middle"
            fill="#9FB2AF"
            font-size="16"
        >
            Escape
        </text>

    </svg>

    </body>

    </html>
    """

    components.html(
        html,
        height=280,
        scrolling=False
    )


# ============================================================
# RESULTADO COMPRESOR
# ============================================================

def resultado_compresor(kMc):

    st.markdown(
        """
        <div class="component-title">
            Compresor
        </div>

        <div class="component-subtitle">
            GT COMPRESSOR · kMc
        </div>
        """,
        unsafe_allow_html=True
    )

    # Diagrama con compresor resaltado
    diagrama_turbina_gas(
        "compressor"
    )

    if kMc is None:

        st.info(
            "Realiza una estimación para "
            "obtener el estado del compresor."
        )

        return

    degradacion, estado = (
        estado_compresor(kMc)
    )

    st.plotly_chart(
        manometro(
            kMc,
            RANGO_KMC
        ),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    m1, m2 = st.columns(2)

    m1.metric(
        "kMc estimado",
        f"{kMc:.4f}"
    )

    m2.metric(
        "Degradación relativa",
        f"{degradacion:.1f}%"
    )

    if degradacion >= 80:

        st.error(estado)

    elif degradacion >= 60:

        st.warning(estado)

    else:

        st.success(estado)


# ============================================================
# RESULTADO TURBINA
# ============================================================

def resultado_turbina(kMt):

    st.markdown(
        """
        <div class="component-title">
            Turbina
        </div>

        <div class="component-subtitle">
            GT TURBINE · kMt
        </div>
        """,
        unsafe_allow_html=True
    )

    # Diagrama con turbina resaltada
    diagrama_turbina_gas(
        "turbine"
    )

    if kMt is None:

        st.info(
            "Realiza una estimación para "
            "obtener el estado de la turbina."
        )

        return

    degradacion, estado = (
        estado_turbina(kMt)
    )

    st.plotly_chart(
        manometro(
            kMt,
            RANGO_KMT
        ),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    m1, m2 = st.columns(2)

    m1.metric(
        "kMt estimado",
        f"{kMt:.4f}"
    )

    m2.metric(
        "Degradación relativa",
        f"{degradacion:.1f}%"
    )

    if degradacion >= 80:

        st.error(estado)

    elif degradacion >= 60:

        st.warning(estado)

    else:

        st.success(estado)
