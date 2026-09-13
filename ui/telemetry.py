# ui/telemetry.py

import streamlit as st
from config import SENSORES, VELOCIDADES, UNIDADES
from data_utils import obtener_rangos_velocidad

def panel_telemetria(data):
    with st.expander("Variables de entrada", expanded=True):

        velocidad = st.selectbox(
            "Velocidad del buque",
            VELOCIDADES,
            index=4
        )

        rangos = obtener_rangos_velocidad(data, velocidad, SENSORES)
        valores = {}

        col1, col2 = st.columns(2)

        for i, sensor in enumerate(SENSORES):
            rango = rangos[sensor]
            minimo = rango["min"]
            maximo = rango["max"]
            promedio = rango["mean"]

            step = (maximo - minimo) / 100 if maximo != minimo else 0.001

            with (col1 if i % 2 == 0 else col2):
                valores[sensor] = st.slider(
                    f"{sensor} [{UNIDADES[sensor]}]",
                    min_value=float(minimo),
                    max_value=float(maximo),
                    value=float(promedio),
                    step=float(step)
                )

    return velocidad, valores
