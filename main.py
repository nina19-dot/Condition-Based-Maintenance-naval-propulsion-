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
        La plataforma utiliza las condiciones de operación
        y las variables de telemetría para estimar el estado
        de degradación del compresor y de la turbina.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# PLANTA CODLAG
# Reservamos su lugar ANTES de los controles
# ============================================================

st.header("Planta de propulsión CODLAG")

st.markdown(
    """
    <p class="section-description">
        La telemetría se muestra directamente en el componente
        o punto físico correspondiente de la planta.
    </p>
    """,
    unsafe_allow_html=True
)

plant_placeholder = st.empty()

st.divider()


# ============================================================
# CONDICIONES DE OPERACIÓN
# ============================================================

st.header("Condiciones de operación y telemetría")

velocidad, valores = panel_telemetria(data)

observacion = crear_observacion(
    velocidad,
    valores
)


# ============================================================
# AHORA DIBUJAMOS LA PLANTA EN EL PLACEHOLDER SUPERIOR
# ============================================================

with plant_placeholder.container():

    esquema_planta(
        componente=st.session_state.active_component,
        valores=valores,
        velocidad=velocidad,
        kMc=st.session_state.kMc,
        kMt=st.session_state.kMt
    )


# ============================================================
# BOTONES
# ============================================================

st.markdown(
    "<div style='height:15px'></div>",
    unsafe_allow_html=True
)

b1, b2, b3 = st.columns(3)


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

        st.session_state.active_component = "compressor"

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

        st.session_state.active_component = "turbine"

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

        st.session_state.active_component = "both"

        st.rerun()


st.divider()


# ============================================================
# DIAGRAMA DEL PROCESO
# ============================================================

st.header("Proceso de la turbina de gas")

st.markdown(
    """
    <p class="section-description">
        Las lecturas seleccionadas se muestran en la etapa
        física correspondiente del proceso.
    </p>
    """,
    unsafe_allow_html=True
)

diagrama_proceso(
    valores=valores,
    velocidad=velocidad,
    kMc=st.session_state.kMc,
    kMt=st.session_state.kMt
)


st.divider()


# ============================================================
# RESULTADOS
# ============================================================

st.header("Estado estimado de los componentes")

comp_col, turb_col = st.columns(
    2,
    gap="large"
)


with comp_col:

    resultado_compresor(
        st.session_state.kMc
    )


with turb_col:

    resultado_turbina(
        st.session_state.kMt
    )
