# ui/results.py

import plotly.graph_objects as go
import streamlit as st

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


def manometro(
    valor,
    rango
):

    minimo, maximo = rango

    amplitud = (
        maximo - minimo
    )

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
                    "range": [
                        minimo,
                        maximo
                    ],
                    "tickvals": [
                        minimo,
                        maximo
                    ],
                    "tickcolor": MIST,
                    "tickfont": {
                        "color": MIST
                    }
                },

                "bar": {
                    "color": "rgba(0,0,0,0)"
                },

                "threshold": {
                    "line": {
                        "color": DIAL,
                        "width": 5
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
        height=230,
        margin=dict(
            l=15,
            r=15,
            t=20,
            b=5
        ),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


def icono_compresor():

    st.markdown(
        """
        <svg
            viewBox="0 0 300 100"
            width="100%"
            height="90"
        >

            <polygon
                points="20,20 185,36 185,64 20,80"
                fill="#4F9BD8"
                stroke="#EDE7D8"
                stroke-width="4"
            />

            <line
                x1="55" y1="27"
                x2="55" y2="73"
                stroke="#10262A"
                stroke-width="5"
            />

            <line
                x1="95" y1="31"
                x2="95" y2="69"
                stroke="#10262A"
                stroke-width="5"
            />

            <line
                x1="135" y1="34"
                x2="135" y2="66"
                stroke="#10262A"
                stroke-width="5"
            />

            <line
                x1="185" y1="50"
                x2="275" y2="50"
                stroke="#EDE7D8"
                stroke-width="7"
            />

        </svg>
        """,
        unsafe_allow_html=True
    )


def icono_turbina():

    st.markdown(
        """
        <svg
            viewBox="0 0 300 100"
            width="100%"
            height="90"
        >

            <line
                x1="20" y1="50"
                x2="105" y2="50"
                stroke="#EDE7D8"
                stroke-width="7"
            />

            <polygon
                points="105,20 275,38 275,62 105,80"
                fill="#C0872C"
                stroke="#EDE7D8"
                stroke-width="4"
            />

            <line
                x1="145" y1="27"
                x2="145" y2="73"
                stroke="#10262A"
                stroke-width="5"
            />

            <line
                x1="190" y1="32"
                x2="190" y2="68"
                stroke="#10262A"
                stroke-width="5"
            />

            <line
                x1="235" y1="36"
                x2="235" y2="64"
                stroke="#10262A"
                stroke-width="5"
            />

        </svg>
        """,
        unsafe_allow_html=True
    )


def resultado_compresor(kMc):

    st.markdown(
        "<div class='component-title'>Compresor</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='component-subtitle'>GT COMPRESSOR · kMc</div>",
        unsafe_allow_html=True
    )

    icono_compresor()

    if kMc is None:

        st.info(
            "Sin estimación disponible."
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

    c1, c2 = st.columns(2)

    c1.metric(
        "kMc",
        f"{kMc:.4f}"
    )

    c2.metric(
        "Degradación",
        f"{degradacion:.1f}%"
    )

    if degradacion >= 80:

        st.error(estado)

    elif degradacion >= 60:

        st.warning(estado)

    else:

        st.success(estado)


def resultado_turbina(kMt):

    st.markdown(
        "<div class='component-title'>Turbina</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='component-subtitle'>GT TURBINE · kMt</div>",
        unsafe_allow_html=True
    )

    icono_turbina()

    if kMt is None:

        st.info(
            "Sin estimación disponible."
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

    c1, c2 = st.columns(2)

    c1.metric(
        "kMt",
        f"{kMt:.4f}"
    )

    c2.metric(
        "Degradación",
        f"{degradacion:.1f}%"
    )

    if degradacion >= 80:

        st.error(estado)

    elif degradacion >= 60:

        st.warning(estado)

    else:

        st.success(estado)
