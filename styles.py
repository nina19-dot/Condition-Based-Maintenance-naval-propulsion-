# styles.py

import streamlit as st

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


def load_css():

    st.markdown(
        f"""
        <style>

        @import url(
        'https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap'
        );

        /* Fondo general */
        [data-testid="stAppViewContainer"] {{
            background: {INK};
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        html, body, [class*="css"] {{
            font-family: 'Archivo', sans-serif;
        }}

        /* Ancho de página */
        .block-container {{
            max-width: 1450px;
            padding-top: 1.3rem;
            padding-bottom: 2rem;
        }}

        /* Texto */
        h1, h2, h3, h4, p, label {{
            color: {DIAL} !important;
        }}

        h1 {{
            font-weight: 800 !important;
            letter-spacing: -0.025em;
        }}

        h2 {{
            font-weight: 700 !important;
        }}

        /* Portada */
        .matricula {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.76rem;
            color: {BRASS} !important;
            letter-spacing: 0.07em;
        }}

        .titular {{
            font-size: clamp(2.0rem, 4vw, 3.2rem);
            font-weight: 800;
            line-height: 1.05;
            color: {DIAL} !important;
            margin-bottom: 12px;
        }}

        .entrada {{
            color: {MIST} !important;
            font-size: 1.0rem;
            line-height: 1.55;
        }}

        /* Tarjetas */
        .naval-card {{
            background: {HULL};
            border: 1px solid {STEEL};
            border-radius: 8px;
            padding: 18px;
            height: 100%;
        }}

        .component-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {DIAL} !important;
            margin-bottom: 4px;
        }}

        .component-subtitle {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.76rem;
            color: {MIST} !important;
        }}

        /* Métricas */
        [data-testid="stMetricValue"] {{
            color: {BRASS} !important;
            font-family: 'IBM Plex Mono', monospace;
        }}

        [data-testid="stMetricLabel"] p {{
            color: {MIST} !important;
        }}

        /* Estado */
        .status {{
            padding: 10px 14px;
            border-radius: 4px;
            font-weight: 600;
            text-align: center;
            margin-top: 6px;
        }}

        /* Sensores */
        .sensor-tag {{
            display: inline-block;
            border: 1px solid {STEEL};
            color: {SEA};
            padding: 5px 8px;
            margin: 3px;
            border-radius: 3px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.74rem;
        }}

        .small-note {{
            color: {MIST} !important;
            font-size: 0.82rem;
            line-height: 1.45;
        }}

        hr {{
            border-color: {STEEL} !important;
        }}

        footer, #MainMenu {{
            visibility: hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
