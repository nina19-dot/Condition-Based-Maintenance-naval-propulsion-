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

from ui.plant_map import esquema_planta

from ui.telemetry import panel_telemetria

from ui.results import (
    resultado_compresor,
    resultado_turbina
)
from ui.process_diagram import diagrama_proceso

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
# VARIABLES DE SESIÓN
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

with st.spinner(
    "Inicializando modelos de degradación..."
):

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
        La plataforma utiliza las condiciones de operación
        y las variables de telemetría de la planta para
        estimar el coeficiente de degradación del compresor
        kMc y de la turbina kMt.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# PLANTA CODLAG
# ============================================================

st.header(
    "Planta de propulsión CODLAG"
)

st.markdown(
    """
    <p class="section-description">
        Diagrama general del sistema de propulsión.
        Al realizar una estimación se resaltará el componente
        que está siendo analizado.
    </p>
    """,
    unsafe_allow_html=True
)

esquema_planta(
    st.session_state.active_component
)


st.divider()


# ============================================================
# TELEMETRÍA
# ============================================================

st.header(
    "Condiciones de operación y telemetría"
)

st.markdown(
    """
    <p class="section-description">
        Selecciona la velocidad de operación y modifica
        las lecturas de los sensores. Los límites de cada
        variable cambian automáticamente de acuerdo con
        los valores observados para esa velocidad.
    </p>
    """,
    unsafe_allow_html=True
)

velocidad, valores = panel_telemetria(data)

observacion = crear_observacion(
    velocidad,
    valores
)


# ============================================================
# BOTONES
# ============================================================

st.markdown(
    "<div style='height:15px'></div>",
    unsafe_allow_html=True
)

b1, b2, b3 = st.columns(
    [1, 1, 1],
    gap="medium"
)


with b1:

    if st.button(
        "Analizar compresor",
        use_container_width=True
    ):

        st.session_state.kMc = (
            predecir_kMc(
                rf_kMc,
                observacion
            )
        )

        st.session_state.active_component = (
            "compressor"
        )

        st.rerun()


with b2:

    if st.button(
        "Analizar turbina",
        use_container_width=True
    ):

        st.session_state.kMt = (
            predecir_kMt(
                rf_kMt,
                observacion
            )
        )

        st.session_state.active_component = (
            "turbine"
        )

        st.rerun()


with b3:

    if st.button(
        "Analizar sistema completo",
        use_container_width=True
    ):

        st.session_state.kMc = (
            predecir_kMc(
                rf_kMc,
                observacion
            )
        )

        st.session_state.kMt = (
            predecir_kMt(
                rf_kMt,
                observacion
            )
        )

        st.session_state.active_component = (
            "both"
        )

        st.rerun()


st.divider()


# ============================================================
# RESULTADOS
# ============================================================

st.divider()

st.header("Estado estimado de los componentes")

st.markdown(
    """
    <p class="section-description">
        El diagrama central muestra las variables de telemetría
        seleccionadas para cada fase del proceso, así como los
        coeficientes estimados del compresor y la turbina.
    </p>
    """,
    unsafe_allow_html=True
)

col_comp, col_diag, col_turb = st.columns(
    [1.0, 1.8, 1.0],
    gap="large"
)

with col_comp:
    resultado_compresor(st.session_state.kMc)

with col_diag:
    st.markdown(
        """
        <div class="component-title">Diagrama del proceso</div>
        <div class="component-subtitle">Telemetría por etapa</div>
        """,
        unsafe_allow_html=True
    )

    diagrama_proceso(
        valores=valores,
        velocidad=velocidad,
        kMc=st.session_state.kMc,
        kMt=st.session_state.kMt
    )

with col_turb:
    resultado_turbina(st.session_state.kMt)


# ============================================================
# LIMITACIONES
# ============================================================

st.divider()

st.header(
    "Alcance de la estimación"
)

st.markdown(
    """
    Los resultados corresponden al espacio de operación
    representado por el simulador. Los indicadores de
    mantenimiento son criterios demostrativos y una
    implementación real requeriría validación con datos
    operacionales y límites definidos por ingeniería de
    mantenimiento.
    """
)
