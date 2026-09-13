import streamlit as st

from data_utils import cargar_datos

from model_utils import (
    entrenar_modelos,
    crear_observacion,
    predecir_coeficientes
)

from ui.telemetry import (
    panel_telemetria
)

from ui.plant_map import (
    mostrar_planta
)

from ui.results import (
    bloque_compresor,
    bloque_turbina
)


# =============================
# CONFIGURACIÓN STREAMLIT
# =============================

st.set_page_config(
    page_title='Naval CBM',
    page_icon='⚙️',
    layout='wide'
)


# =============================
# VARIABLES DE SESIÓN
# =============================

if 'kMc' not in st.session_state:
    st.session_state.kMc = None

if 'kMt' not in st.session_state:
    st.session_state.kMt = None

if 'componente' not in st.session_state:
    st.session_state.componente = None


# =============================
# TÍTULO
# =============================

st.title(
    'Condition-Based Maintenance '
    'for Naval Propulsion'
)

st.caption(
    'Estimación del estado de '
    'degradación del compresor '
    'y la turbina mediante '
    'Random Forest.'
)


# =============================
# CARGAR DATOS
# =============================

data = cargar_datos()


# =============================
# ENTRENAR MODELOS
# =============================

with st.spinner(
    'Inicializando modelos...'
):

    rf_kMc, rf_kMt = (
        entrenar_modelos(data)
    )


# =============================
# MAPA CODLAG
# =============================

mostrar_planta(
    st.session_state.componente
)


st.divider()


# =============================
# TELEMETRÍA
# =============================

velocidad, valores = (
    panel_telemetria(data)
)


# Crear observación para modelo
observacion = crear_observacion(
    velocidad,
    valores
)


st.divider()


# =============================
# BOTONES
# =============================

col1, col2, col3 = st.columns(3)


with col1:

    calcular_kMc = st.button(
        'Estimar kMc',
        use_container_width=True
    )


with col2:

    calcular_kMt = st.button(
        'Estimar kMt',
        use_container_width=True
    )


with col3:

    calcular_ambos = st.button(
        'Estimar ambos',
        use_container_width=True
    )


# =============================
# PREDICCIONES
# =============================

if calcular_kMc:

    pred_kMc = rf_kMc.predict(
        observacion
    )[0]

    st.session_state.kMc = pred_kMc
    st.session_state.componente = (
        'compressor'
    )

    st.rerun()


if calcular_kMt:

    pred_kMt = rf_kMt.predict(
        observacion
    )[0]

    st.session_state.kMt = pred_kMt
    st.session_state.componente = (
        'turbine'
    )

    st.rerun()


if calcular_ambos:

    pred_kMc, pred_kMt = (
        predecir_coeficientes(
            rf_kMc,
            rf_kMt,
            observacion
        )
    )

    st.session_state.kMc = pred_kMc
    st.session_state.kMt = pred_kMt
    st.session_state.componente = (
        'both'
    )

    st.rerun()


st.divider()


# =============================
# RESULTADOS
# =============================

col_compresor, col_turbina = (
    st.columns(2)
)


with col_compresor:

    bloque_compresor(
        st.session_state.kMc
    )


with col_turbina:

    bloque_turbina(
        st.session_state.kMt
    )
