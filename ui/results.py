# ui/results.py

import streamlit as st
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


def manometro(valor, rango):

    minimo, maximo = rango
    amplitud = maximo - minimo

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=valor,
            number={
                "font": {
                    "size": 34,
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
                        "range": [minimo, minimo + 0.20 * amplitud],
                        "color": SIGNAL
                    },
                    {
                        "range": [minimo + 0.20 * amplitud, minimo + 0.40 * amplitud],
                        "color": BRASS
                    },
                    {
                        "range": [minimo + 0.40 * amplitud, maximo],
                        "color": SEA
                    }
                ]
            }
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(l=15, r=15, t=15, b=5),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


def resultado_compresor(kMc):

    st.markdown(
        """
        <div class="component-title">Compresor</div>
        <div class="component-subtitle">GT COMPRESSOR · kMc</div>
        """,
        unsafe_allow_html=True
    )

    if kMc is None:
        st.info("Realiza una estimación para obtener el estado del compresor.")
        return

    degradacion, estado = estado_compresor(kMc)

    st.plotly_chart(
        manometro(kMc, RANGO_KMC),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    c1, c2 = st.columns(2)

    c1.metric("kMc estimado", f"{kMc:.4f}")
    c2.metric("Degradación", f"{degradacion:.1f}%")

    if degradacion >= 80:
        st.error(estado)
    elif degradacion >= 60:
        st.warning(estado)
    else:
        st.success(estado)


def resultado_turbina(kMt):

    st.markdown(
        """
        <div class="component-title">Turbina</div>
        <div class="component-subtitle">GT TURBINE · kMt</div>
        """,
        unsafe_allow_html=True
    )

    if kMt is None:
        st.info("Realiza una estimación para obtener el estado de la turbina.")
        return

    degradacion, estado = estado_turbina(kMt)

    st.plotly_chart(
        manometro(kMt, RANGO_KMT),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    c1, c2 = st.columns(2)

    c1.metric("kMt estimado", f"{kMt:.4f}")
    c2.metric("Degradación", f"{degradacion:.1f}%")

    if degradacion >= 80:
        st.error(estado)
    elif degradacion >= 60:
        st.warning(estado)
    else:
        st.success(estado)
