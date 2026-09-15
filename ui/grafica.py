import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# PREPARAR DATOS
# ============================================================

def preparar_datos_diagnostico(data):

    # Estado sano
    sano = data[
        np.isclose(data["kMc"], 1.000) &
        np.isclose(data["kMt"], 1.000)
    ].copy()

    # Estado máximo de degradación contemplado por el dataset
    degradado = data[
        np.isclose(data["kMc"], 0.950) &
        np.isclose(data["kMt"], 0.975)
    ].copy()

    # Promedio por velocidad
    resumen_sano = (
        sano
        .groupby("v")[["mf", "T48"]]
        .mean()
        .reset_index()
    )

    resumen_deg = (
        degradado
        .groupby("v")[["mf", "T48"]]
        .mean()
        .reset_index()
    )

    # Unir ambos perfiles
    tabla = pd.merge(
        resumen_sano,
        resumen_deg,
        on="v",
        suffixes=("_Sano", "_Degradado")
    )

    # --------------------------------------------------------
    # CONVERSIÓN DE T48:
    # dataset original en K -> visualización en °C
    # --------------------------------------------------------

    tabla["T48_Sano_C"] = (
        tabla["T48_Sano"] - 273.15
    )

    tabla["T48_Degradado_C"] = (
        tabla["T48_Degradado"] - 273.15
    )

    return tabla


# ============================================================
# GRÁFICA PRINCIPAL
# ============================================================

def grafica_diagnostico(
    data,
    velocidad_actual=None,
    valores=None
):

    tabla = preparar_datos_diagnostico(data)

    # ========================================================
    # LÍMITE OPERATIVO
    # ========================================================

    # Se conserva la misma lógica utilizada en Colab:
    # 98% del máximo T48 de la condición degradada.
    #
    # El cálculo se realiza primero en la escala original (K)
    # y posteriormente se convierte a °C.

    umbral_temp_K = (
        tabla["T48_Degradado"].max() * 0.98
    )

    umbral_temp_C = (
        umbral_temp_K - 273.15
    )


    # ========================================================
    # FIGURA CON DOBLE EJE Y
    # ========================================================

    fig = make_subplots(
        specs=[[{"secondary_y": True}]]
    )


    # --------------------------------------------------------
    # COMBUSTIBLE - CONDICIÓN SANA
    # --------------------------------------------------------

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["mf_Sano"],

            mode="lines+markers",

            name="mf - condición sana",

            line=dict(
                color=SEA,
                width=3,
                dash="dash"
            ),

            marker=dict(
                size=8,
                symbol="circle"
            ),

            hovertemplate=(
                "<b>Condición sana</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "mf: %{y:.3f} kg/s"
                "<extra></extra>"
            )
        ),

        secondary_y=False
    )


    # --------------------------------------------------------
    # COMBUSTIBLE - CONDICIÓN DEGRADADA
    # --------------------------------------------------------

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["mf_Degradado"],

            mode="lines+markers",

            name="mf - condición degradada",

            line=dict(
                color=STEEL,
                width=4
            ),

            marker=dict(
                size=9,
                symbol="square"
            ),

            hovertemplate=(
                "<b>Condición degradada</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "mf: %{y:.3f} kg/s"
                "<extra></extra>"
            )
        ),

        secondary_y=False
    )


    # --------------------------------------------------------
    # T48 - CONDICIÓN SANA
    # --------------------------------------------------------

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["T48_Sano_C"],

            mode="lines+markers",

            name="T48 - condición sana",

            line=dict(
                color=BRASS,
                width=3,
                dash="dash"
            ),

            marker=dict(
                size=9,
                symbol="triangle-up"
            ),

            hovertemplate=(
                "<b>Condición sana</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "T48: %{y:.1f} °C"
                "<extra></extra>"
            )
        ),

        secondary_y=True
    )


    # --------------------------------------------------------
    # T48 - CONDICIÓN DEGRADADA
    # --------------------------------------------------------

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["T48_Degradado_C"],

            mode="lines+markers",

            name="T48 - condición degradada",

            line=dict(
                color=SIGNAL,
                width=4
            ),

            marker=dict(
                size=9,
                symbol="diamond"
            ),

            hovertemplate=(
                "<b>Condición degradada</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "T48: %{y:.1f} °C"
                "<extra></extra>"
            )
        ),

        secondary_y=True
    )


    # ========================================================
    # LÍMITE OPERATIVO
    # ========================================================

    fig.add_hline(

        y=umbral_temp_C,

        line=dict(
            color="black",
            width=2,
            dash="dashdot"
        ),

        annotation_text=(
            f"Límite operativo: "
            f"{umbral_temp_C:.1f} °C"
        ),

        annotation_position="top left",

        annotation_font=dict(
            color=INK,
            size=12
        ),

        secondary_y=True
    )


    # ========================================================
    # CONDICIÓN ACTUAL DEL USUARIO
    # ========================================================

    t48_actual_K = None
    mf_actual = None

    if valores is not None:

        t48_actual_K = valores.get("T48")
        mf_actual = valores.get("mf")


    if (
        velocidad_actual is not None
        and t48_actual_K is not None
    ):

        t48_actual_C = (
            float(t48_actual_K) - 273.15
        )


        # Línea vertical con velocidad seleccionada
        fig.add_vline(

            x=velocidad_actual,

            line=dict(
                color=MIST,
                width=1.5,
                dash="dot"
            ),

            annotation_text=(
                f"{velocidad_actual:.0f} knots"
            ),

            annotation_position="bottom right"
        )


        # Punto T48 actual
        color_actual = (
            SIGNAL
            if t48_actual_K >= umbral_temp_K
            else SEA
        )


        fig.add_trace(

            go.Scatter(
                x=[velocidad_actual],
                y=[t48_actual_C],

                mode="markers",

                name="T48 actual",

                marker=dict(
                    size=16,
                    color=color_actual,
                    symbol="star",
                    line=dict(
                        color=INK,
                        width=2
                    )
                ),

                hovertemplate=(
                    "<b>Condición actual</b><br>"
                    f"Velocidad: "
                    f"{velocidad_actual:.0f} knots<br>"
                    f"T48: "
                    f"{t48_actual_C:.1f} °C"
                    "<extra></extra>"
                )
            ),

            secondary_y=True
        )


    # --------------------------------------------------------
    # mf ACTUAL
    # --------------------------------------------------------

    if (
        velocidad_actual is not None
        and mf_actual is not None
    ):

        fig.add_trace(

            go.Scatter(
                x=[velocidad_actual],
                y=[float(mf_actual)],

                mode="markers",

                name="mf actual",

                marker=dict(
                    size=13,
                    color=SEA,
                    symbol="star",
                    line=dict(
                        color=INK,
                        width=2
                    )
                ),

                hovertemplate=(
                    "<b>Condición actual</b><br>"
                    f"Velocidad: "
                    f"{velocidad_actual:.0f} knots<br>"
                    f"mf: "
                    f"{float(mf_actual):.3f} kg/s"
                    "<extra></extra>"
                )
            ),

            secondary_y=False
        )


    # ========================================================
    # FORMATO GENERAL
    # ========================================================

    fig.update_layout(

        title=dict(
            text=(
                "Efecto de la degradación "
                "según la velocidad"
            ),
            x=0.02,
            xanchor="left",
            font=dict(
                size=22,
                color=INK
            )
        ),

        height=620,

        margin=dict(
            l=60,
            r=70,
            t=90,
            b=60
        ),

        paper_bgcolor=DIAL,
        plot_bgcolor=DIAL,

        font=dict(
            color=INK,
            family="Arial"
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0.65)",
            bordercolor=MIST,
            borderwidth=1
        ),

        hovermode="x unified"
    )


    # ========================================================
    # EJE X
    # ========================================================

    fig.update_xaxes(

        title_text=(
            "Velocidad del buque v [knots]"
        ),

        tickmode="array",

        tickvals=tabla["v"].tolist(),

        showgrid=True,

        gridcolor="rgba(16,38,42,0.12)",

        zeroline=False,

        linecolor=MIST,

        title_font=dict(
            color=INK
        )
    )


    # ========================================================
    # EJE IZQUIERDO
    # ========================================================

    fig.update_yaxes(

        title_text=(
            "Flujo de combustible mf [kg/s]"
        ),

        secondary_y=False,

        showgrid=True,

        gridcolor="rgba(16,38,42,0.10)",

        zeroline=False,

        title_font=dict(
            color=SEA
        ),

        tickfont=dict(
            color=SEA
        )
    )


    # ========================================================
    # EJE DERECHO
    # ========================================================

    fig.update_yaxes(

        title_text=(
            "Temperatura de salida T48 [°C]"
        ),

        secondary_y=True,

        showgrid=False,

        zeroline=False,

        title_font=dict(
            color=SIGNAL
        ),

        tickfont=dict(
            color=SIGNAL
        )
    )


    # ========================================================
    # MOSTRAR
    # ========================================================

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    # ========================================================
    # DIAGNÓSTICO DE MANTENIMIENTO
    # ========================================================

    if t48_actual_K is not None:

        t48_actual_C = (
            float(t48_actual_K) - 273.15
        )


        if t48_actual_K >= umbral_temp_K:

            st.error(
                "⚠️ **Se requiere mantenimiento.** "
                f"La temperatura actual T48 "
                f"({t48_actual_C:.1f} °C) supera "
                f"el límite operativo establecido "
                f"({umbral_temp_C:.1f} °C)."
            )

        else:

            margen = (
                umbral_temp_C -
                t48_actual_C
            )

            st.success(
                "✓ **Condición térmica dentro del "
                "límite operativo.** "
                f"T48 se encuentra {margen:.1f} °C "
                "por debajo del límite de mantenimiento."
            )


    # ========================================================
    # NOTA METODOLÓGICA
    # ========================================================

    st.caption(
        "El límite mostrado conserva el criterio "
        "demostrativo utilizado en el análisis: "
        "98% del máximo T48 observado para la condición "
        "de mayor degradación simulada. No corresponde "
        "a un límite oficial del fabricante."
    )
