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

        [data-testid="stAppViewContainer"] {{
            background: {INK};
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        html, body, [class*="css"] {{
            font-family: 'Archivo', sans-serif;
        }}

        .block-container {{
            max-width: 1550px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }}

        h1, h2, h3, h4, p, label {{
            color: {DIAL} !important;
        }}

        .matricula {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.76rem;
            color: {BRASS} !important;
            letter-spacing: 0.07em;
        }}

        .titular {{
            font-size: clamp(2rem, 4vw, 3.2rem);
            font-weight: 800;
            line-height: 1.05;
            color: {DIAL} !important;
            margin-bottom: 12px;
        }}

        .entrada {{
            color: {MIST} !important;
            font-size: 1rem;
            line-height: 1.55;
            max-width: 950px;
        }}

        .section-description {{
            color: {MIST} !important;
            font-size: 0.95rem;
            line-height: 1.55;
            max-width: 1000px;
            margin-bottom: 18px;
        }}

        .component-title {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {DIAL} !important;
            margin-bottom: 4px;
        }}

        .component-subtitle {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.76rem;
            color: {MIST} !important;
            margin-bottom: 10px;
        }}

        [data-testid="stMetricValue"] {{
            color: {BRASS} !important;
            font-family: 'IBM Plex Mono', monospace;
        }}

        [data-testid="stMetricLabel"] p {{
            color: {MIST} !important;
        }}

        [data-testid="stSlider"] {{
            margin-bottom: 12px;
        }}

        /* BOTONES */
        [data-testid="stButton"] button {{
            min-height: 48px;
            font-weight: 700;
            background-color: {DIAL} !important;
            color: {INK} !important;
            border: 1px solid {BRASS} !important;
            border-radius: 8px !important;
        }}

        [data-testid="stButton"] button:hover {{
            background-color: {BRASS} !important;
            color: {INK} !important;
            border: 1px solid {BRASS} !important;
        }}

        [data-testid="stButton"] button p {{
            color: {INK} !important;
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
