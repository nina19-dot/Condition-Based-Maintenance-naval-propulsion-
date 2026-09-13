# styles.py

import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .main {
        background-color: #f6f8fb;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #475569;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }

    .card {
        background: white;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
    }

    .metric-value {
        color: #0f172a;
        font-size: 1.4rem;
        font-weight: 700;
    }

    .small-note {
        color: #64748b;
        font-size: 0.85rem;
    }

    .component-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }

    .status-normal {
        color: #15803d;
        font-weight: 600;
    }

    .status-warning {
        color: #b45309;
        font-weight: 600;
    }

    .status-critical {
        color: #b91c1c;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)
