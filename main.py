# main.py

import streamlit as st

from styles import load_css
from data_utils import cargar_datos
from model_utils import (
    entrenar_modelos,
    crear_observacion,
    predecir_kMc,
    predecir_kMt
)
from ui.telemetry import panel_telemetria
from ui.plant_map import esquema_planta
from ui.process_diagram import diagrama_proceso
from ui.results import (
    resultado_compresor,
    resultado_turbina
)

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Naval CBM",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()

# ============================================================
# SESSION STATE
# ============================================================

if "kMc" not in st.session_state:
    st.session_state.kMc = None

if "kMt" not in st.session_state:
    st.session_state.kMt = None

if "active_component" not in st.session_state:
    st.session_state.active_component = None

# ============================================================
# DATOS Y MODELOS
# ============================================================

data = cargar_datos()

with st.spinner("Inicializando modelos de degradación..."):
    rf_kMc, rf_kMt = entrenar_modelos(data)

# ============================================================
# PORTADA
# ============================================================

st.markdown(
    """
    <p class="matricula">
        CONDITION-BASED MAINTENANCE · NAVAL PROPULSION
    </p>

    <p class="titular">
        Estimación del estado de degradación
        de una planta de propulsión naval
    </p>

    <p class="entrada">
        La plataforma utiliza condiciones de operación y
        variables de telemetría para estimar el coeficiente
        de degradación del compresor kMc y de la turbina kMt.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# TELEMETRÍA
# ============================================================

st.header("Condiciones de operación y telemetría")

st.markdown(
    """
    <p class="section-description">
        Selecciona la velocidad y ajusta los sensores.
        Los rangos cambian automáticamente según la velocidad elegida.
    </p>
    """,
    unsafe_allow_html=True
)

velocidad, valores = panel_telemetria(data)

# Variables para mostrar en diagramas
# T1 y P1 se agregan como constantes conocidas del dataset.
valores_mostrar = valores.copy()
valores_mostrar["T1"] = 288.0
valores_mostrar["P1"] = 1.0
valores_mostrar["Tp"] = None
valores_mostrar["lp"] = None

observacion = crear_observacion(velocidad, valores)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ============================================================
# BOTONES
# ============================================================

b1, b2, b3 = st.columns(3, gap="medium")

with b1:
    if st.button("Analizar compresor", use_container_width=True):
        st.session_state.kMc = predecir_kMc(rf_kMc, observacion)
        st.session_state.active_component = "compressor"
        st.rerun()

with b2:
    if st.button("Analizar turbina", use_container_width=True):
        st.session_state.kMt = predecir_kMt(rf_kMt, observacion)
        st.session_state.active_component = "turbine"
        st.rerun()

with b3:
    if st.button("Analizar sistema completo", use_container_width=True):
        st.session_state.kMc = predecir_kMc(rf_kMc, observacion)
        st.session_state.kMt = predecir_kMt(rf_kMt, observacion)
        st.session_state.active_component = "both"
        st.rerun()

st.divider()

# ============================================================
# PLANTA CODLAG
# ============================================================

st.header("Planta de propulsión CODLAG")

st.markdown(
    """
    <p class="section-description">
        El diagrama muestra la planta CODLAG y la telemetría
        seleccionada colocada en los puntos donde físicamente corresponde.
    </p>
    """,
    unsafe_allow_html=True
)

esquema_planta(
    componente=st.session_state.active_component,
    valores=valores_mostrar,
    velocidad=velocidad,
    kMc=st.session_state.kMc,
    kMt=st.session_state.kMt
)

st.divider()

# ============================================================
# DIAGRAMA DEL PROCESO
# ============================================================

st.header("Diagrama del proceso")

st.markdown(
    """
    <p class="section-description">
        Se muestra el flujo del proceso desde la admisión hasta el escape,
        con las variables asociadas a cada fase.
    </p>
    """,
    unsafe_allow_html=True
)

diagrama_proceso(
    valores=valores_mostrar,
    velocidad=velocidad,
    kMc=st.session_state.kMc,
    kMt=st.session_state.kMt
)

st.divider()

# ============================================================
# MÉTRICAS DE RESULTADO
# ============================================================

st.header("Estado estimado de los componentes")

res1, res2 = st.columns(2, gap="large")

with res1:
    resultado_compresor(st.session_state.kMc)

with res2:
    resultado_turbina(st.session_state.kMt)

st.divider()

# ============================================================
# ALCANCE
# ============================================================

st.header("Alcance de la estimación")

st.markdown(
    """
    Los resultados corresponden al espacio operativo representado por el
    simulador. Los criterios de mantenimiento mostrados en la interfaz son
    demostrativos y una aplicación real requeriría validación con datos
    operacionales y criterios formales de ingeniería de mantenimiento.
    """
)
