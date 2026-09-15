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

        @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

        /* =========================================================
           BASE GENERAL
           ========================================================= */
        html, body, [class*="css"] {{
            font-family: 'Archivo', sans-serif;
        }}

        [data-testid="stAppViewContainer"] {{
            background: {INK};
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        [data-testid="stToolbar"] {{
            right: 1rem;
        }}

        .block-container {{
            max-width: 1550px;
            padding-top: 1.8rem;
            padding-bottom: 2.5rem;
        }}

        h1, h2, h3, h4, h5, h6, p, span, label, div {{
            color: {DIAL};
        }}

        hr {{
            border-color: {STEEL} !important;
        }}

        footer, #MainMenu {{
            visibility: hidden;
        }}

        /* =========================================================
           ENCABEZADO PRINCIPAL
           ========================================================= */
        .hero-section {{
            padding: 12px 4px 26px 4px;
            margin-bottom: 10px;
            max-width: 1380px;
            margin-right: auto;
            text-align: center;
        }}

        .hero-kicker {{
            color: {BRASS};
            font-family: 'IBM Plex Mono', monospace;
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 20px;
            text-align: center;
        }}

        .hero-title {{
            color: {DIAL};
            font-size: clamp(2.4rem, 4.6vw, 4rem);
            font-weight: 800;
            line-height: 1.08;
            letter-spacing: -0.03em;
            margin-bottom: 14px;
            text-align: center;
        }}

        .hero-subtitle {{
            color: {DIAL};
            font-size: clamp(1.2rem, 2vw, 1.75rem);
            font-weight: 700;
            line-height: 1.35;
            margin-bottom: 16px;
            max-width: 1180px;
            text-align: center;
        }}

        .hero-description {{
            color: {MIST};
            font-size: 1.08rem;
            font-weight: 400;
            line-height: 1.75;
            max-width: 1240px;
            margin-left: auto;
            margin-right: auto;
            text-align: center;
        }}

        /* =========================================================
           TEXTOS AUXILIARES
           ========================================================= */
        .matricula {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.78rem;
            color: {BRASS} !important;
            letter-spacing: 0.08em;
            text-transform: uppercase;
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
            line-height: 1.6;
            max-width: 950px;
        }}

        .section-description {{
            color: {MIST} !important;
            font-size: 0.98rem;
            line-height: 1.6;
            max-width: 1000px;
            margin-bottom: 18px;
        }}

        .component-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {DIAL} !important;
            margin-bottom: 4px;
        }}

        .component-subtitle {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.78rem;
            color: {MIST} !important;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        /* =========================================================
           ENCABEZADOS DE SECCIÓN
           ========================================================= */
        .codlag-header {{
            width: 100%;
            max-width: none;
            padding: 8px 0 20px 0;
            margin-bottom: 18px;
        }}
        
        .codlag-title {{
            color: {DIAL};
            font-size: clamp(1.8rem, 2.8vw, 2.6rem);
            font-weight: 800;
            line-height: 1.15;
            letter-spacing: -0.02em;
            margin-bottom: 16px;
        }}
        
        .codlag-description {{
            color: {MIST};
            font-size: 1rem;
            font-weight: 400;
            line-height: 1.7;
        
            /* Permite utilizar todo el ancho disponible */
            width: 100%;
            max-width: none;
        
            margin: 0;
        }}

        /* =========================================================
           TARJETAS / CAJAS
           ========================================================= */
        .panel-card {{
            background: rgba(18, 54, 59, 0.65);
            border: 1px solid {STEEL};
            border-radius: 18px;
            padding: 18px 20px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
        }}

        .soft-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(159, 178, 175, 0.18);
            border-radius: 16px;
            padding: 14px 16px;
        }}

        /* =========================================================
           MÉTRICAS
           ========================================================= */
        [data-testid="stMetric"] {{
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(159, 178, 175, 0.16);
            border-radius: 14px;
            padding: 10px 12px;
        }}

        [data-testid="stMetricValue"] {{
            color: {BRASS} !important;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 1.25rem !important;
            font-weight: 700;
        }}

        [data-testid="stMetricLabel"] p {{
            color: {MIST} !important;
            font-size: 0.92rem !important;
            font-weight: 600;
        }}

        /* =========================================================
           SLIDERS / INPUTS
           ========================================================= */
        [data-testid="stSlider"] {{
            margin-bottom: 12px;
        }}

        [data-testid="stSlider"] label {{
            color: {DIAL} !important;
            font-weight: 600;
        }}

        [data-baseweb="select"] > div {{
            background-color: rgba(255,255,255,0.03) !important;
            border-color: {STEEL} !important;
            color: {DIAL} !important;
        }}

        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input {{
            background-color: rgba(255,255,255,0.03) !important;
            color: {DIAL} !important;
            border: 1px solid {STEEL} !important;
            border-radius: 8px !important;
        }}

        /* =========================================================
           BOTONES
           ========================================================= */
        [data-testid="stButton"] button {{
            min-height: 48px;
            font-weight: 700;
            background-color: {DIAL} !important;
            color: {INK} !important;
            border: 1px solid {BRASS} !important;
            border-radius: 10px !important;
            padding: 0.55rem 1.1rem !important;
            transition: all 0.2s ease-in-out;
        }}

        [data-testid="stButton"] button:hover {{
            background-color: {BRASS} !important;
            color: {INK} !important;
            border: 1px solid {BRASS} !important;
            transform: translateY(-1px);
        }}

        [data-testid="stButton"] button p {{
            color: {INK} !important;
            font-weight: 700 !important;
        }}

        /* =========================================================
           ALERTAS / ESTADOS
           ========================================================= */
        .status-ok {{
            background: rgba(38, 111, 94, 0.22);
            border: 1px solid #2E9E8F;
            color: {DIAL};
            border-radius: 16px;
            padding: 16px 18px;
        }}

        .status-warning {{
            background: rgba(176, 120, 21, 0.22);
            border: 1px solid #D98A20;
            color: {DIAL};
            border-radius: 16px;
            padding: 16px 18px;
        }}

        .status-danger {{
            background: rgba(126, 41, 41, 0.22);
            border: 1px solid {SIGNAL};
            color: {DIAL};
            border-radius: 16px;
            padding: 16px 18px;
        }}

        /* =========================================================
           TABS
           ========================================================= */
        [data-testid="stTabs"] button {{
            color: {MIST} !important;
            font-weight: 600 !important;
        }}

        [aria-selected="true"] {{
            color: {DIAL} !important;
        }}

        /* =========================================================
           DATAFRAME / TABLE
           ========================================================= */
        .stDataFrame {{
            border: 1px solid rgba(159, 178, 175, 0.18);
            border-radius: 12px;
            overflow: hidden;
        }}

        /* =========================================================
           RESPONSIVE
           ========================================================= */
        @media (max-width: 900px) {{
            .block-container {{
                padding-top: 1rem;
                padding-bottom: 1.8rem;
            }}

            .hero-section {{
                padding: 6px 0 18px 0;
            }}

            .hero-title {{
                font-size: 2.2rem;
            }}

            .hero-subtitle {{
                font-size: 1.12rem;
            }}

            .hero-description {{
                font-size: 0.98rem;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
