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

    # Velocidad
    velocidad = st.select_slider(
        "Velocidad del buque [knots]",
        options=VELOCIDADES,
        value=15
    )

    rangos = obtener_rangos_velocidad(
        data,
        velocidad,
        SENSORES
    )

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True
    )

    valores = {}

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
