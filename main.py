import streamlit as st

from config import DATA_PATH, MODEL_KMC_PATH, MODEL_KMT_PATH
from data_utils import load_dataset
from model_utils import load_models, predict_coefficient
from styles import inject_css
from ui.plant_map import render_plant_map
from ui.results import render_result_card
from ui.telemetry import render_telemetry_inputs


st.set_page_config(
    page_title="CODLAG Condition Monitoring",
    page_icon="⚙️",
    layout="wide",
)

inject_css()

if "active_component" not in st.session_state:
    st.session_state.active_component = "none"
if "pred_kMc" not in st.session_state:
    st.session_state.pred_kMc = None
if "pred_kMt" not in st.session_state:
    st.session_state.pred_kMt = None

st.markdown('<div class="hero-title">CODLAG Condition Monitoring</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Estimación del estado de degradación del compresor y la turbina mediante Random Forest.</div>',
    unsafe_allow_html=True,
)

# Validación de archivos requeridos
missing = []
for path in [DATA_PATH, MODEL_KMC_PATH, MODEL_KMT_PATH]:
    if not path.exists():
        missing.append(str(path))

if missing:
    st.error(
        "Faltan archivos necesarios para ejecutar la aplicación:\n\n"
        + "\n".join(f"- {item}" for item in missing)
    )
    st.info(
        "Coloca el CSV en data/naval_propulsion_cbm.csv y los modelos entrenados "
        "en models/rf_kMc.joblib y models/rf_kMt.joblib."
    )
    st.stop()

# Carga de datos y modelos
data = load_dataset(DATA_PATH)
models = load_models()

# Mapa / esquema del sistema
render_plant_map(st.session_state.active_component)

# Entradas de telemetría
with st.container(border=True):
    inputs = render_telemetry_inputs(data)

st.markdown("### Estimación de coeficientes")

col_kmc, col_kmt = st.columns(2)

with col_kmc:
    st.markdown("#### Compresor")
    render_result_card(
        "Estado estimado del compresor",
        "kMc",
        st.session_state.pred_kMc,
        "El mapa superior ilumina el compresor al realizar esta estimación.",
    )

    if st.button("Estimar kMc", use_container_width=True, type="primary"):
        st.session_state.pred_kMc = predict_coefficient(models["kMc"], inputs)
        st.session_state.active_component = "compressor"
        st.rerun()

with col_kmt:
    st.markdown("#### Turbina")
    render_result_card(
        "Estado estimado de la turbina",
        "kMt",
        st.session_state.pred_kMt,
        "El mapa superior ilumina la turbina al realizar esta estimación.",
    )

    if st.button("Estimar kMt", use_container_width=True):
        st.session_state.pred_kMt = predict_coefficient(models["kMt"], inputs)
        st.session_state.active_component = "turbine"
        st.rerun()

st.markdown("")
if st.button("Estimar ambos coeficientes", use_container_width=True):
    st.session_state.pred_kMc = predict_coefficient(models["kMc"], inputs)
    st.session_state.pred_kMt = predict_coefficient(models["kMt"], inputs)
    st.session_state.active_component = "both"
    st.rerun()

st.caption(
    "Nota: el esquema CODLAG es una representación funcional simplificada para la interfaz y no un P&ID de ingeniería."
)
