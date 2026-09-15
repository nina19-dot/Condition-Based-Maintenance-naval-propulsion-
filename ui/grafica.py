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

    # Condición óptima
    sano = data[
        np.isclose(data["kMc"], 1.000) &
        np.isclose(data["kMt"], 1.000)
    ].copy()

    # Condición de máxima degradación simulada
    degradado = data[
        np.isclose(data["kMc"], 0.950) &
        np.isclose(data["kMt"], 0.975)
    ].copy()

    # Promedios por velocidad
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

    # Unir perfiles
    tabla = pd.merge(
        resumen_sano,
        resumen_deg,
        on="v",
        suffixes=("_Optimo", "_Degradado")
    )

    return tabla


# ============================================================
# TARJETA DE ESTADO
# ============================================================

def tarjeta_estado(
    titulo,
    valor_actual,
    limite,
    unidad,
    mantenimiento
):

    if mantenimiento:

        fondo = "#4B1F1F"
        borde = SIGNAL
        icono = "⚠"
        estado = "SE REQUIERE MANTENIMIENTO"

        detalle = (
            f"El valor actual de {valor_actual:.2f} {unidad} "
            f"supera el límite de {limite:.2f} {unidad}."
        )

    else:

        fondo = "#123F38"
        borde = SEA
        icono = "✓"
        estado = "DENTRO DEL LÍMITE OPERATIVO"

        margen = limite - valor_actual

        detalle = (
            f"Margen disponible: {margen:.2f} {unidad} "
            f"antes del límite de {limite:.2f} {unidad}."
        )


    html = (
        f'<div style="'
        f'background:{fondo};'
        f'border:2px solid {borde};'
        f'border-radius:12px;'
        f'padding:20px 24px;'
        f'margin-top:8px;'
        f'margin-bottom:8px;'
        f'min-height:145px;'
        f'">'
        f'<div style="'
        f'color:{DIAL};'
        f'font-size:22px;'
        f'font-weight:800;'
        f'margin-bottom:10px;'
        f'">'
        f'{icono} {titulo}'
        f'</div>'
        f'<div style="'
        f'color:{DIAL};'
        f'font-size:19px;'
        f'font-weight:700;'
        f'margin-bottom:8px;'
        f'">'
        f'{estado}'
        f'</div>'
        f'<div style="'
        f'color:{MIST};'
        f'font-size:17px;'
        f'line-height:1.5;'
        f'">'
        f'{detalle}'
        f'</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


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
    # LÍMITES DEMOSTRATIVOS
    # ========================================================

    # Se conserva el mismo criterio utilizado en Colab:
    # 98% del máximo observado en condición degradada.

    limite_t48 = (
        tabla["T48_Degradado"].max() * 0.98
    )

    limite_mf = (
        tabla["mf_Degradado"].max() * 0.98
    )


    # ========================================================
    # FIGURA CON DOBLE EJE Y
    # ========================================================

    fig = make_subplots(
        specs=[
            [{"secondary_y": True}]
        ]
    )


    # ========================================================
    # mf ÓPTIMO
    # ========================================================

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["mf_Optimo"],

            mode="lines+markers",

            name="mf óptimo (kMc = 1.0)",

            line=dict(
                color=SEA,
                width=3,
                dash="dash"
            ),

            marker=dict(
                size=8,
                symbol="circle",
                color=SEA
            ),

            hovertemplate=(
                "<b>mf óptimo</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "mf: %{y:.3f} kg/s"
                "<extra></extra>"
            )
        ),

        secondary_y=False
    )


    # ========================================================
    # mf DEGRADADO
    # ========================================================

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["mf_Degradado"],

            mode="lines+markers",

            name="mf degradado (kMc = 0.95)",

            line=dict(
                color=STEEL,
                width=4
            ),

            marker=dict(
                size=9,
                symbol="square",
                color=STEEL
            ),

            hovertemplate=(
                "<b>mf degradado</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "mf: %{y:.3f} kg/s"
                "<extra></extra>"
            )
        ),

        secondary_y=False
    )


    # ========================================================
    # T48 ÓPTIMA
    # ========================================================

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["T48_Optimo"],

            mode="lines+markers",

            name="T48 óptima (kMt = 1.0)",

            line=dict(
                color=BRASS,
                width=3,
                dash="dash"
            ),

            marker=dict(
                size=9,
                symbol="triangle-up",
                color=BRASS
            ),

            hovertemplate=(
                "<b>T48 óptima</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "T48: %{y:.1f} K"
                "<extra></extra>"
            )
        ),

        secondary_y=True
    )


    # ========================================================
    # T48 DEGRADADA
    # ========================================================

    fig.add_trace(

        go.Scatter(
            x=tabla["v"],
            y=tabla["T48_Degradado"],

            mode="lines+markers",

            name="T48 degradada (kMt = 0.975)",

            line=dict(
                color=SIGNAL,
                width=4
            ),

            marker=dict(
                size=9,
                symbol="diamond",
                color=SIGNAL
            ),

            hovertemplate=(
                "<b>T48 degradada</b><br>"
                "Velocidad: %{x:.0f} knots<br>"
                "T48: %{y:.1f} K"
                "<extra></extra>"
            )
        ),

        secondary_y=True
    )


    # ========================================================
    # LÍMITE DE COMBUSTIBLE
    # IMPORTANTE:
    # Se agrega como Scatter para que NO altere el eje de T48
    # ========================================================

    fig.add_trace(

        go.Scatter(
            x=[
                tabla["v"].min(),
                tabla["v"].max()
            ],

            y=[
                limite_mf,
                limite_mf
            ],

            mode="lines",
            showlegend=False,

            line=dict(
                color=STEEL,
                width=2,
                dash="dot"
            ),

            hovertemplate=(
                f"<b>Límite de combustible</b><br>"
                f"{limite_mf:.3f} kg/s"
                "<extra></extra>"
            )
        ),

        secondary_y=False
    )


    # ========================================================
    # LÍMITE DE T48
    # Se dibuja como una serie SOBRE EL EJE SECUNDARIO.
    # Esto evita el problema del eje mf 0–800.
    # ========================================================

    fig.add_trace(

        go.Scatter(
            x=[
                tabla["v"].min(),
                tabla["v"].max()
            ],

            y=[
                limite_t48,
                limite_t48
            ],

            mode="lines",
            showlegend=False,
            line=dict(
                color=INK,
                width=2.5,
                dash="dashdot"
            ),

            hovertemplate=(
                f"<b>Límite térmico</b><br>"
                f"{limite_t48:.1f} K"
                "<extra></extra>"
            )
        ),

        secondary_y=True
    )


    # ========================================================
    # CONDICIÓN ACTUAL
    # ========================================================

    mf_actual = None
    t48_actual = None

    if valores is not None:

        mf_actual = valores.get("mf")
        t48_actual = valores.get("T48")


    if velocidad_actual is not None:

        # Línea vertical de velocidad
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

            annotation_position="bottom right",

            annotation_font=dict(
                color=INK
            )
        )


    # ========================================================
    # mf ACTUAL
    # ========================================================

    if (
        velocidad_actual is not None
        and mf_actual is not None
    ):

        mf_actual = float(mf_actual)

        mantenimiento_mf = (
            mf_actual >= limite_mf
        )

        color_mf_actual = (
            SIGNAL
            if mantenimiento_mf
            else SEA
        )

        fig.add_trace(

            go.Scatter(
                x=[velocidad_actual],
                y=[mf_actual],

                mode="markers",

                name="mf actual",

                marker=dict(
                    size=17,
                    color=color_mf_actual,
                    symbol="star",
                    line=dict(
                        color=INK,
                        width=2
                    )
                ),

                hovertemplate=(
                    "<b>mf actual</b><br>"
                    f"Velocidad: "
                    f"{velocidad_actual:.0f} knots<br>"
                    f"mf: {mf_actual:.3f} kg/s"
                    "<extra></extra>"
                )
            ),

            secondary_y=False
        )


    # ========================================================
    # T48 ACTUAL
    # ========================================================

    if (
        velocidad_actual is not None
        and t48_actual is not None
    ):

        t48_actual = float(t48_actual)

        mantenimiento_t48 = (
            t48_actual >= limite_t48
        )

        color_t48_actual = (
            SIGNAL
            if mantenimiento_t48
            else BRASS
        )

        fig.add_trace(

            go.Scatter(
                x=[velocidad_actual],
                y=[t48_actual],

                mode="markers",

                name="T48 actual",

                marker=dict(
                    size=18,
                    color=color_t48_actual,
                    symbol="star",
                    line=dict(
                        color=INK,
                        width=2
                    )
                ),

                hovertemplate=(
                    "<b>T48 actual</b><br>"
                    f"Velocidad: "
                    f"{velocidad_actual:.0f} knots<br>"
                    f"T48: {t48_actual:.1f} K"
                    "<extra></extra>"
                )
            ),

            secondary_y=True
        )


    # ========================================================
    # RANGOS DE LOS EJES
    # ========================================================

    # Combustible:
    # fuerza el eje izquierdo a la escala correcta.
    mf_max_visual = max(
        tabla["mf_Optimo"].max(),
        tabla["mf_Degradado"].max(),
        limite_mf
    )

    if mf_actual is not None:
        mf_max_visual = max(
            mf_max_visual,
            mf_actual
        )

    mf_max_visual *= 1.08


    # Temperatura en Kelvin
    t48_min_visual = min(
        tabla["T48_Optimo"].min(),
        tabla["T48_Degradado"].min()
    )

    t48_max_visual = max(
        tabla["T48_Optimo"].max(),
        tabla["T48_Degradado"].max(),
        limite_t48
    )

    if t48_actual is not None:

        t48_min_visual = min(
            t48_min_visual,
            t48_actual
        )

        t48_max_visual = max(
            t48_max_visual,
            t48_actual
        )

    margen_temp = (
        t48_max_visual -
        t48_min_visual
    ) * 0.08


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
            y=0.98,
            xanchor="left",
            yanchor="top",
            font=dict(
                size=24,
                color=INK,
                family="Arial Black"
            )
        ),

        height=650,

        margin=dict(
            l=70,
            r=85,
            t=145,
            b=70
        ),

        paper_bgcolor=DIAL,
        plot_bgcolor=DIAL,

        font=dict(
            color=INK,
            family="Arial",
            size=13
        ),

        legend=dict(
    orientation="h",

    # Colocar la leyenda arriba del área de la gráfica
    yanchor="bottom",
    y=1.015,

    xanchor="left",
    x=0.01,

    font=dict(
        size=12
    ),

    bgcolor="rgba(255,255,255,0.78)",

    bordercolor=MIST,
    borderwidth=1
),
    
        bgcolor="rgba(255,255,255,0.78)",

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

        gridcolor=(
            "rgba(16,38,42,0.12)"
        ),

        zeroline=False,

        linecolor=MIST,

        title_font=dict(
            color=INK,
            size=16
        ),

        tickfont=dict(
            size=13
        )
    )


    # ========================================================
    # EJE Y IZQUIERDO — mf
    # ========================================================

    fig.update_yaxes(

        title_text=(
            "Flujo de combustible mf [kg/s]"
        ),

        range=[
            0,
            mf_max_visual
        ],

        tickformat=".2f",

        secondary_y=False,

        showgrid=True,

        gridcolor=(
            "rgba(16,38,42,0.10)"
        ),

        zeroline=False,

        title_font=dict(
            color=SEA,
            size=16
        ),

        tickfont=dict(
            color=SEA,
            size=13
        )
    )


    # ========================================================
    # EJE Y DERECHO — T48 EN KELVIN
    # ========================================================

    fig.update_yaxes(

        title_text=(
            "Temperatura de salida T48 [K]"
        ),

        range=[
            t48_min_visual - margen_temp,
            t48_max_visual + margen_temp
        ],

        secondary_y=True,

        showgrid=False,

        zeroline=False,

        title_font=dict(
            color=SIGNAL,
            size=16
        ),

        tickfont=dict(
            color=SIGNAL,
            size=13
        )
    )


    # ========================================================
    # MOSTRAR GRÁFICA
    # ========================================================

    st.plotly_chart(
        fig,
        use_container_width=True,

        config={
            "displayModeBar": False
        }
    )


    # ========================================================
    # DIAGNÓSTICO DE COMBUSTIBLE Y TEMPERATURA
    # ========================================================

    if (
        mf_actual is not None
        and t48_actual is not None
    ):

        mantenimiento_mf = (
            mf_actual >= limite_mf
        )

        mantenimiento_t48 = (
            t48_actual >= limite_t48
        )


        col_mf, col_t48 = st.columns(2)


        with col_mf:

            tarjeta_estado(
                titulo="Condición de combustible",
                valor_actual=mf_actual,
                limite=limite_mf,
                unidad="kg/s",
                mantenimiento=mantenimiento_mf
            )


        with col_t48:

            tarjeta_estado(
                titulo="Condición térmica",
                valor_actual=t48_actual,
                limite=limite_t48,
                unidad="K",
                mantenimiento=mantenimiento_t48
            )


        # ====================================================
        # ALERTA GLOBAL
        # ====================================================

        if (
            mantenimiento_mf
            or mantenimiento_t48
        ):

            causas = []

            if mantenimiento_mf:
                causas.append(
                    "el flujo de combustible"
                )

            if mantenimiento_t48:
                causas.append(
                    "la temperatura T48"
                )

            texto_causas = " y ".join(causas)

            st.markdown(
                f"""
                <div style="
                    background:#4B1F1F;
                    border:2px solid {SIGNAL};
                    border-radius:12px;
                    padding:18px 22px;
                    margin-top:12px;
                    color:{DIAL};
                    font-size:19px;
                    font-weight:700;
                ">
                    ⚠ Mantenimiento recomendado:
                    {texto_causas} ha superado el
                    límite operativo establecido.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    background:#123F38;
                    border:2px solid {SEA};
                    border-radius:12px;
                    padding:18px 22px;
                    margin-top:12px;
                    color:{DIAL};
                    font-size:19px;
                    font-weight:700;
                ">
                    ✓ Condición operativa dentro de
                    los límites establecidos de combustible
                    y temperatura.
                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # NOTA METODOLÓGICA
    # ========================================================

    st.caption(
        "Los límites mostrados conservan el criterio "
        "demostrativo utilizado en el análisis: 98% del "
        "máximo observado en la condición de mayor "
        "degradación simulada para mf y T48. "
        "No corresponden a límites oficiales del fabricante."
    )
