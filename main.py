# main.py

import streamlit as st
from styles import load_css
from data_utils import cargar_datos
from model_utils import entrenar_modelos, crear_observacion, predecir_coeficientes
from ui.plant_map import render_plant_map
from ui.telemetry import panel_telemetria
from ui.results import component_card

st.set_page_config(
    page_title="Naval Condition-Based Maintenance",
    page_icon="⚙️",
    layout="wide"
)

load_css()

if "kMc" not in st.session_state:
    st.session_state.kMc = None
if "kMt" not in st.session_state:
    st.session_state.kMt = None
if "active_component" not in st.session_state:
    st.session_state.active_component = None

st.markdown('<div class="app-title">Condition-Based Maintenance for Naval Propulsion</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Estimación del nivel de degradación del compresor y la turbina mediante Random Forest.</div>',
    unsafe_allow_html=True
)

data = cargar_datos()
rf_kMc, rf_kMt = entrenar_modelos(data)

# Fila principal
left, right = st.columns([1.55, 1.0], gap="large")

with left:
    render_plant_map(st.session_state.active_component)

with right:
    st.markdown('<div class="section-title">Panel de operación</div>', unsafe_allow_html=True)
    velocidad, valores = panel_telemetria(data)

observacion = crear_observacion(velocidad, valores)

st.markdown("### Acciones")
b1, b2, b3 = st.columns(3)

with b1:
    if st.button("Estimar kMc", use_container_width=True):
        st.session_state.kMc = rf_kMc.predict(observacion)[0]
        st.session_state.active_component = "compressor"
        st.rerun()

with b2:
    if st.button("Estimar kMt", use_container_width=True):
        st.session_state.kMt = rf_kMt.predict(observacion)[0]
        st.session_state.active_component = "turbine"
        st.rerun()

with b3:
    if st.button("Estimar ambos", use_container_width=True):
        pred_kMc, pred_kMt = predecir_coeficientes(rf_kMc, rf_kMt, observacion)
        st.session_state.kMc = pred_kMc
        st.session_state.kMt = pred_kMt
        st.session_state.active_component = "both"
        st.rerun()

st.markdown("---")

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    component_card(
        title="Compresor",
        image_path="assets/compressor.png",
        coef_value=st.session_state.kMc,
        target_type="kMc"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    component_card(
        title="Turbina",
        image_path="assets/turbine.png",
        coef_value=st.session_state.kMt,
        target_type="kMt"
    )
    st.markdown('</div>', unsafe_allow_html=True)
