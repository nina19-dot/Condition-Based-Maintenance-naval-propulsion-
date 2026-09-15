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
from ui.grafica import grafica_diagnostico

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
st.set_page_config(
    page_title="Mantenimiento Basado en Condición",
    layout="wide"
)

load_css()

# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================

st.markdown(
    """
<section class="hero-section">
<div class="hero-kicker">MANTENIMIENTO BASADO EN CONDICIÓN · PROPULSIÓN NAVAL</div>

<div class="hero-title">Mantenimiento Basado en Condición para Propulsión Naval</div>

<div class="hero-subtitle">
Estimación del estado de degradación del compresor y la turbina mediante telemetría operativa
</div>

<div class="hero-description">
Esta plataforma analiza las condiciones de operación y las variables de telemetría de una planta de propulsión naval para estimar el nivel de degradación del compresor y de la turbina. Su propósito es apoyar el diagnóstico del sistema y la toma de decisiones de monitoreo, inspección y mantenimiento preventivo.
</div>
</section>
    """,
    unsafe_allow_html=True
)
# ============================================================
# PLANTA CODLAG
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

st.divider()

# ============================================================
# PLANTA CODLAG
# ============================================================

st.header("Planta de propulsión CODLAG")

st.markdown(
    """
    <p class="section-description">
        La telemetría seleccionada se muestra directamente sobre la planta
        en el componente físico correspondiente.
    </p>
    """,
    unsafe_allow_html=True
)

esquema_planta(
    componente=st.session_state.active_component,
    valores=valores,
    velocidad=velocidad
)

st.divider()

# ============================================================
# BOTONES DE ANÁLISIS
# ============================================================

b1, b2, b3 = st.columns(3)

with b1:

    if st.button(
        "Analizar compresor",
        use_container_width=True
    ):

        # Calcular solamente kMc
        st.session_state.kMc = predecir_kMc(
            rf_kMc,
            observacion
        )

        # Borrar resultado anterior de turbina
        st.session_state.kMt = None

        # Indicar componente activo
        st.session_state.active_component = "compressor"

        st.rerun()


with b2:

    if st.button(
        "Analizar turbina",
        use_container_width=True
    ):

        # Calcular solamente kMt
        st.session_state.kMt = predecir_kMt(
            rf_kMt,
            observacion
        )

        # Borrar resultado anterior del compresor
        st.session_state.kMc = None

        # Indicar componente activo
        st.session_state.active_component = "turbine"

        st.rerun()


with b3:

    if st.button(
        "Analizar sistema completo",
        use_container_width=True
    ):

        # Calcular ambos
        st.session_state.kMc = predecir_kMc(
            rf_kMc,
            observacion
        )

        st.session_state.kMt = predecir_kMt(
            rf_kMt,
            observacion
        )

        # Ambos componentes activos
        st.session_state.active_component = "both"

        st.rerun()


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


if st.session_state.active_component == "compressor":

    resultado_compresor(
        st.session_state.kMc
    )


elif st.session_state.active_component == "turbine":

    resultado_turbina(
        st.session_state.kMt
    )


elif st.session_state.active_component == "both":

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


else:

    st.info(
        "Selecciona un análisis para obtener "
        "el estado estimado del componente."
    )

# ============================================================
# Grafica 
# ============================================================
st.markdown(
    "## Condición operativa de combustible y temperatura"
)

st.write(
    "Comparación del flujo de combustible y la temperatura de salida de la turbina" 
     " entre los estados extremos de degradación simulados, mostrando además la condición operativa" 
     " seleccionada por el usuario."
)

grafica_diagnostico(
    data=data,
    velocidad_actual=velocidad,
    valores=valores
)
