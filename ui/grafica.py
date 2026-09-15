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

    # Condición óptima / sin degradación
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
# CLASIFICAR CONDICIÓN OPERATIVA
# ============================================================

def clasificar_condicion(
    valor_actual,
    valor_desgaste,
    limite_critico
):

    # CRÍTICO:
    # supera el límite negro punteado
    if valor_actual > limite_critico:

        return (
            "CRÍTICO",
            "⛔",
            "#541F1F",
            SIGNAL,
            "Detener la máquina y realizar las "
            "reparaciones correspondientes."
        )

    # PREVENTIVO:
    # alcanza o supera la curva degradada
    elif valor_actual >= valor_desgaste:

        return (
            "SERVICIO PREVENTIVO",
            "⚠",
            "#544019",
            BRASS,
            "La condición actual alcanzó la línea de "
            "desgaste. Programar servicio preventivo."
        )

    # NORMAL
    else:

        return (
            "NORMAL",
            "✓",
            "#123F38",
            SEA,
            "La condición actual se mantiene por "
            "debajo de la línea de desgaste."
        )


# ============================================================
# TARJETA DE ESTADO
# ============================================================

def tarjeta_estado(
    titulo,
    valor_actual,
    valor_desgaste,
    limite_critico,
    unidad
):

    (
        estado,
        icono,
        fondo,
        borde,
        mensaje
    ) = clasificar_condicion(
        valor_actual,
        valor_desgaste,
        limite_critico
    )

    html = (
        f'<div style="'
        f'background:{fondo};'
        f'border:2px solid {borde};'
        f'border-radius:12px;'
        f'padding:18px 20px;'
        f'margin-bottom:16px;'
        f'">'

        f'<div style="'
        f'color:{DIAL};'
        f'font-size:20px;'
        f'font-weight:800;'
        f'margin-bottom:9px;'
        f'">'
        f'{icono} {titulo}'
        f'</div>'

        f'<div style="'
        f'color:{DIAL};'
        f'font-size:17px;'
        f'font-weight:800;'
        f'margin-bottom:11px;'
        f'">'
        f'{estado}'
        f'</div>'

        f'<div style="'
        f'color:{MIST};'
        f'font-size:14px;'
        f'line-height:1.55;'
        f'">'
        f'Actual: <b>{valor_actual:.2f} {unidad}</b><br>'
        f'Línea de desgaste: '
        f'<b>{valor_desgaste:.2f} {unidad}</b><br>'
        f'Límite crítico: '
        f'<b>{limite_critico:.2f} {unidad}</b><br><br>'
        f'{mensaje}'
        f'</div>'

        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# TARJETA DE ESTADO GLOBAL
# ============================================================

def tarjeta_estado_global(
    estado_mf,
    estado_t48
):

    # --------------------------------------------------------
    # CRÍTICO
    # --------------------------------------------------------

    if (
        estado_mf == "CRÍTICO"
        or estado_t48 == "CRÍTICO"
    ):

        fondo = "#541F1F"
        borde = SIGNAL
        icono = "⛔"

        titulo = "ESTADO CRÍTICO"

        mensaje = (
            "Al menos una variable superó su límite crítico. "
            "Detener la máquina y realizar las reparaciones "
            "correspondientes antes de continuar la operación."
        )

    # --------------------------------------------------------
    # SERVICIO PREVENTIVO
    # --------------------------------------------------------

    elif (
        estado_mf == "SERVICIO PREVENTIVO"
        or estado_t48 == "SERVICIO PREVENTIVO"
    ):

        fondo = "#544019"
        borde = BRASS
        icono = "⚠"

        titulo = "SERVICIO PREVENTIVO"

        mensaje = (
            "Al menos una variable alcanzó o superó "
            "su línea de desgaste. Programar servicio "
            "preventivo antes de llegar al estado crítico."
        )

    # --------------------------------------------------------
    # NORMAL
    # --------------------------------------------------------

    else:

        fondo = "#123F38"
        borde = SEA
        icono = "✓"

        titulo = "OPERACIÓN NORMAL"

        mensaje = (
            "El flujo de combustible y la temperatura "
            "permanecen por debajo de sus líneas de desgaste."
        )

    html = (
        f'<div style="'
        f'background:{fondo};'
        f'border:2px solid {borde};'
        f'border-radius:12px;'
        f'padding:17px 20px;'
        f'margin-top:6px;'
        f'">'

        f'<div style="'
        f'color:{DIAL};'
        f'font-size:18px;'
        f'font-weight:800;'
        f'margin-bottom:8px;'
        f'">'
        f'{icono} {titulo}'
        f'</div>'

        f'<div style="'
        f'color:{MIST};'
        f'font-size:14px;'
        f'line-height:1.5;'
        f'">'
        f'{mensaje}'
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
    # LÍMITE CRÍTICO DEMOSTRATIVO
    # ========================================================

    # Debe quedar por ENCIMA de la condición degradada.
    # Se utiliza 5% adicional sobre el máximo degradado.
    #
    # Esto permite:
    #
    # NORMAL
    # ↓
    # línea degradada
    # ↓
    # SERVICIO PREVENTIVO
    # ↓
    # línea crítica
    # ↓
    # CRÍTICO

    FACTOR_CRITICO = 1.05

    limite_t48 = (
        tabla["T48_Degradado"].max()
        * FACTOR_CRITICO
    )

    limite_mf = (
        tabla["mf_Degradado"].max()
        * FACTOR_CRITICO
    )


    # ========================================================
    # CONDICIÓN ACTUAL
    # ========================================================

    mf_actual = None
    t48_actual = None

    mf_desgaste = None
    t48_desgaste = None


    if (
        valores is not None
        and velocidad_actual is not None
    ):

        mf_actual = valores.get("mf")
        t48_actual = valores.get("T48")


        # ----------------------------------------------------
        # Línea de desgaste en la velocidad actual
        # ----------------------------------------------------

        mf_desgaste = np.interp(
            velocidad_actual,
            tabla["v"],
            tabla["mf_Degradado"]
        )

        t48_desgaste = np.interp(
            velocidad_actual,
            tabla["v"],
            tabla["T48_Degradado"]
        )


        if mf_actual is not None:
            mf_actual = float(mf_actual)

        if t48_actual is not None:
            t48_actual = float(t48_actual)


    # ========================================================
    # DETERMINAR ESTADO ACTUAL
    # ========================================================

    estado_mf = None
    estado_t48 = None


    if (
        mf_actual is not None
        and mf_desgaste is not None
    ):

        estado_mf = clasificar_condicion(
            mf_actual,
            mf_desgaste,
            limite_mf
        )[0]


    if (
        t48_actual is not None
        and t48_desgaste is not None
    ):

        estado_t48 = clasificar_condicion(
            t48_actual,
            t48_desgaste,
            limite_t48
        )[0]


    # ========================================================
    # COLOR DE LOS PUNTOS ACTUALES
    # ========================================================

    def color_estado(estado):

        if estado == "CRÍTICO":
            return SIGNAL

        elif estado == "SERVICIO PREVENTIVO":
            return BRASS

        return SEA


    color_mf_actual = color_estado(
        estado_mf
    )

    color_t48_actual = color_estado(
        estado_t48
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
                size=7,
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
                size=8,
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
                size=8,
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
                size=8,
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
    # LÍMITE CRÍTICO DE mf
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
                color=INK,
                width=2,
                dash="dashdot"
            ),

            hovertemplate=(
                "<b>Límite crítico de combustible</b><br>"
                f"{limite_mf:.3f} kg/s"
                "<extra></extra>"
            )
        ),

        secondary_y=False
    )


    # ========================================================
    # LÍMITE CRÍTICO DE T48
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
                "<b>Límite crítico térmico</b><br>"
                f"{limite_t48:.1f} K"
                "<extra></extra>"
            )
        ),

        secondary_y=True
    )


    # ========================================================
    # VELOCIDAD ACTUAL
    # ========================================================

    if velocidad_actual is not None:

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

        fig.add_trace(

            go.Scatter(
                x=[velocidad_actual],
                y=[mf_actual],

                mode="markers",

                name="mf actual",

                marker=dict(
                    size=16,
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
                    f"mf: {mf_actual:.3f} kg/s<br>"
                    f"Estado: {estado_mf}"
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

        fig.add_trace(

            go.Scatter(
                x=[velocidad_actual],
                y=[t48_actual],

                mode="markers",

                name="T48 actual",

                marker=dict(
                    size=17,
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
                    f"T48: {t48_actual:.1f} K<br>"
                    f"Estado: {estado_t48}"
                    "<extra></extra>"
                )
            ),

            secondary_y=True
        )


    # ========================================================
    # RANGOS DE LOS EJES
    # ========================================================

    # --------------------------------------------------------
    # mf
    # --------------------------------------------------------

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

    mf_max_visual *= 1.07


    # --------------------------------------------------------
    # T48
    # --------------------------------------------------------

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
    ) * 0.07


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
            y=0.95,

            xanchor="left",
            yanchor="top",

            font=dict(
                size=21,
                color=INK,
                family="Arial Black"
            )
        ),

        # Más pequeña para dejar espacio a las tarjetas
        height=535,

        margin=dict(
            l=65,
            r=65,
            t=125,
            b=60
        ),

        paper_bgcolor=DIAL,
        plot_bgcolor=DIAL,

        font=dict(
            color=INK,
            family="Arial",
            size=11
        ),

        legend=dict(
            orientation="h",

            yanchor="bottom",
            y=1.01,

            xanchor="left",
            x=0.01,

            font=dict(
                size=10
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
            size=14
        ),

        tickfont=dict(
            size=11
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
            size=14
        ),

        tickfont=dict(
            color=SEA,
            size=11
        )
    )


    # ========================================================
    # EJE Y DERECHO — T48
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
            size=14
        ),

        tickfont=dict(
            color=SIGNAL,
            size=11
        )
    )


    # ========================================================
    # DISTRIBUCIÓN:
    # GRÁFICA IZQUIERDA + CONDICIONES DERECHA
    # ========================================================

    col_grafica, col_estado = st.columns(
        [3.25, 1.15],
        gap="large"
    )


    # ========================================================
    # MOSTRAR GRÁFICA
    # ========================================================

    with col_grafica:

        st.plotly_chart(
            fig,
            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


    # ========================================================
    # CONDICIONES ACTUALES
    # ========================================================

    with col_estado:

        st.markdown(
            "### Condición actual"
        )


        if (
            mf_actual is not None
            and mf_desgaste is not None
        ):

            tarjeta_estado(
                titulo="Combustible",
                valor_actual=mf_actual,
                valor_desgaste=mf_desgaste,
                limite_critico=limite_mf,
                unidad="kg/s"
            )


        if (
            t48_actual is not None
            and t48_desgaste is not None
        ):

            tarjeta_estado(
                titulo="Temperatura T48",
                valor_actual=t48_actual,
                valor_desgaste=t48_desgaste,
                limite_critico=limite_t48,
                unidad="K"
            )


        # ====================================================
        # ESTADO GLOBAL
        # ====================================================

        if (
            estado_mf is not None
            and estado_t48 is not None
        ):

            tarjeta_estado_global(
                estado_mf,
                estado_t48
            )


    # ========================================================
    # NOTA METODOLÓGICA
    # ========================================================

    st.caption(
        "La curva degradada se utiliza como referencia "
        "para iniciar servicio preventivo. El límite crítico "
        "se establece, con fines demostrativos, 5% por encima "
        "del máximo observado en la condición de mayor "
        "degradación simulada. Estos criterios no corresponden "
        "a límites oficiales del fabricante."
    )
