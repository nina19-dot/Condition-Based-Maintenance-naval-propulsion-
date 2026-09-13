# data_utils.py

import pandas as pd
import streamlit as st


@st.cache_data
def cargar_datos():

    data = pd.read_csv(
        'data/naval_propulsion_cbm.csv'
    )

    # Eliminar variables constantes
    columnas_eliminar = [
        'T1',
        'P1',
        'Tp'
    ]

    data = data.drop(
        columns=columnas_eliminar,
        errors='ignore'
    )

    return data


def obtener_rangos_velocidad(
    data,
    velocidad,
    sensores
):

    data_speed = data[
        data['v'] == velocidad
    ]

    rangos = {}

    for sensor in sensores:

        rangos[sensor] = {
            'min': float(
                data_speed[sensor].min()
            ),

            'max': float(
                data_speed[sensor].max()
            ),

            'mean': float(
                data_speed[sensor].mean()
            )
        }

    return rangos
