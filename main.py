# main.py

import streamlit as st

from styles import load_css

from data_utils import (
    cargar_datos
)

from model_utils import (
    entrenar_modelos,
    crear_observacion,
    predecir_kMc,
    predecir_kMt
)

from ui.plant_map import (
    esquema_planta
)

from ui.telemetry import (
    panel_telemetria
)

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

with st.spinner(
    "Inicializando modelos de degradación..."
):

    rf_kMc, rf_kMt = (
        entrenar_modelos(data)
    )


# ============================================================
# PORTADA
# ============================================================

left, right = st.columns(
    [1.20, 0.80],
    gap="large"
)

with left:

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
            La plataforma utiliza las variables de
            telemetría de la planta para estimar el
            coeficiente de degradación del compresor
            kMc y de la turbina kMt mediante modelos
            Random Forest Regressor.
        </p>
        """,
        unsafe_allow_html=True
    )


with right:

    st.markdown(
        """
        <div class="naval-card">

        <div class="component-title">
        Modelo seleccionado
        </div>

        <p class="small-note">
        Random Forest Regressor
        </p>

        <hr>

        <p class="small-note">
        kMc · R² prueba = 0.9964
        </p>

        <p class="small-note">
        kMt · R² prueba = 0.9930
        </p>

        <p class="small-note">
        11,934 observaciones simuladas
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# PLANTA + TELEMETRÍA
# ============================================================

st.header(
    "Planta CODLAG y condición operacional"
)

planta_col, control_col = st.columns(
    [1.45, 1],
    gap="large"
)


with planta_col:

    esquema_planta(
        st.session_state.active_component
    )


with control_col:

    velocidad, valores = (
        panel_telemetria(data)
    )


observacion = crear_observacion(
    velocidad,
    valores
)


# ============================================================
# BOTONES
# ============================================================

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

st.header(
    "Estado estimado de los componentes"
)

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


# ============================================================
# METODOLOGÍA
# ============================================================

st.divider()

st.header(
    "Metodología"
)

metodo1, metodo2, metodo3 = (
    st.columns(3)
)


with metodo1:

    st.markdown(
        """
        <div class="naval-card">

        <div class="component-title">
        Preparación
        </div>

        <p class="small-note">
        Se eliminaron T1 y P1 por ser
        constantes y Tp por contener
        exactamente la misma información
        que Ts.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with metodo2:

    st.markdown(
        """
        <div class="naval-card">

        <div class="component-title">
        Aprendizaje supervisado
        </div>

        <p class="small-note">
        Dos Random Forest Regressor
        independientes estiman kMc y kMt
        utilizando doce variables de
        telemetría y operación.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with metodo3:

    st.markdown(
        """
        <div class="naval-card">

        <div class="component-title">
        Decisión
        </div>

        <p class="small-note">
        La estimación se convierte en un
        indicador relativo de degradación
        para apoyar decisiones de inspección
        y mantenimiento.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LIMITACIONES
# ============================================================

st.divider()

st.header(
    "Alcance y limitaciones"
)

st.markdown(
    """
    - Los datos provienen de un simulador numérico de una planta
      de propulsión naval.
    - Los elevados valores de R² corresponden principalmente a
      interpolación dentro del espacio simulado.
    - Los umbrales de mantenimiento mostrados por la plataforma
      son criterios propuestos para fines demostrativos.
    - Una aplicación operacional requeriría validación con datos
      reales y criterios definidos por ingeniería de mantenimiento.
    """
)
