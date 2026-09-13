# data_utils.py

from pathlib import Path

import pandas as pd
import streamlit as st


@st.cache_data
def cargar_datos():

    base_dir = Path(__file__).resolve().parent

    ruta_csv = (
        base_dir
        / "data"
        / "naval_propulsion_cbm.csv"
    )

    data = pd.read_csv(ruta_csv)

    # Variables eliminadas durante el EDA
    data = data.drop(
        columns=[
            "T1",
            "P1",
            "Tp"
        ],
        errors="ignore"
    )

    return data


def obtener_rangos_velocidad(
    data,
    velocidad,
    sensores
):

    data_speed = data[
        data["v"] == velocidad
    ]

    rangos = {}

    for sensor in sensores:

        rangos[sensor] = {
            "min": float(
                data_speed[sensor].min()
            ),
            "max": float(
                data_speed[sensor].max()
            ),
            "mean": float(
                data_speed[sensor].mean()
            )
        }

    return rangos
