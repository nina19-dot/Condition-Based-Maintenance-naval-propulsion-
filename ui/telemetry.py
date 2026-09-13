# ui/telemetry.py

import streamlit as st

from config import (
    SENSORES,
    VELOCIDADES,
    UNIDADES
)

from data_utils import (
    obtener_rangos_velocidad
)


def panel_telemetria(data):

    # ========================================================
    # CONDICIÓN OPERACIONAL
    # ========================================================

    op1, op2 = st.columns(
        [2, 1],
        gap="large"
    )

    with op1:

        velocidad = st.select_slider(
            "Velocidad del buque [knots]",
            options=VELOCIDADES,
            value=15
        )


    # lp correspondiente a esa velocidad
    data_speed = data[
        data["v"] == velocidad
    ]

    lp = float(
        data_speed["lp"].mean()
    )


    with op2:

        st.metric(
            "Lever position (lp)",
            f"{lp:.3f}"
        )


    # ========================================================
    # RANGOS POR VELOCIDAD
    # ========================================================

    rangos = obtener_rangos_velocidad(
        data,
        velocidad,
        SENSORES
    )

    # lp también se devuelve para los diagramas
    valores = {
        "lp": lp
    }


    st.markdown(
        "### Variables de telemetría"
    )


    # Dos columnas amplias
    col1, col2 = st.columns(
        2,
        gap="large"
    )


    for i, sensor in enumerate(SENSORES):

        rango = rangos[sensor]

        minimo = rango["min"]
        maximo = rango["max"]
        promedio = rango["mean"]

        step = (
            (maximo - minimo) / 100
            if maximo != minimo
            else 0.001
        )

        columna = (
            col1
            if i % 2 == 0
            else col2
        )


        with columna:

            valores[sensor] = st.slider(
                f"{sensor} [{UNIDADES[sensor]}]",
                min_value=float(minimo),
                max_value=float(maximo),
                value=float(promedio),
                step=float(step),
                key=f"{sensor}_{velocidad}"
            )


    return velocidad, valores
