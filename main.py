import json
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

# =============================================================================
# 1. CONFIGURACIÓN Y PALETA
# =============================================================================

st.set_page_config(
    page_title="Deja de cambiar piezas que todavía funcionan",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

INK = "#10262A"      # petróleo profundo, fondo
HULL = "#17383B"     # paneles
DIAL = "#EDE7D8"     # texto claro y caras de instrumento
BRASS = "#C0872C"    # latón, acento
SIGNAL = "#C0402C"   # rojo de señal
SEA = "#3E8F80"      # verde de estado correcto
MIST = "#9FB2AF"     # texto secundario

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {{ font-family: 'Archivo', system-ui, sans-serif; }}

    /* Titulares con el peso y el interletraje del rótulo industrial */
    h1 {{ font-weight: 800 !important; letter-spacing: -.022em; line-height: 1.08; }}
    h2 {{ font-weight: 800 !important; letter-spacing: -.02em; }}
    h3 {{ font-weight: 600 !important; }}

    .titular {{ font-size: clamp(2.2rem, 5vw, 3.6rem) !important; font-weight: 800 !important;
                line-height: 1.06 !important; letter-spacing: -.025em; margin: 0 0 18px !important;
                color: {DIAL} !important; }}
    .matricula {{ font-family: 'IBM Plex Mono', monospace !important; font-size: .78rem !important;
                  color: {BRASS} !important; letter-spacing: .06em; margin-bottom: 14px !important; }}
    .entrada {{ color: {MIST} !important; font-size: 1.05rem !important;
                line-height: 1.62 !important; max-width: 60ch; }}
    .guia {{ border: 0; border-top: 1px solid rgba(159,178,175,.34);
             max-width: 200px; margin: 22px 0; }}

    /* Placas del bloque del problema */
    .placa {{ background: {HULL}; border-left: 4px solid; padding: 22px 20px;
              height: 100%; }}
    .placa h4 {{ margin: 0 0 10px !important; font-size: 1.08rem !important;
                 font-weight: 600 !important; color: {DIAL} !important; }}
    .placa p  {{ margin: 0 !important; font-size: .93rem !important;
                 color: {MIST} !important; line-height: 1.55 !important; }}
    .placa .coste {{ display: block; margin-top: 14px; font-family: 'IBM Plex Mono', monospace;
                     font-size: .74rem; letter-spacing: .04em; color: {BRASS}; }}

    /* Lectura grande de resultado */
    .cifra {{ font-family: 'IBM Plex Mono', monospace !important; font-weight: 600 !important;
              font-size: clamp(2rem, 4.4vw, 2.8rem) !important; color: {BRASS} !important;
              line-height: 1.05 !important; display: block; margin: 4px 0 10px !important; }}
    .rotulo {{ font-size: .88rem !important; color: {MIST} !important;
               margin: 0 !important; line-height: 1.55 !important; }}

    /* Semáforo de estado */
    .semaforo {{ padding: 12px 16px; font-weight: 600; font-size: .95rem;
                 text-align: center; border-radius: 2px; }}

    /* Hallazgos */
    .hallazgo .dato {{ font-family: 'IBM Plex Mono', monospace !important; font-weight: 600 !important;
                       font-size: 1.8rem !important; color: {SIGNAL} !important; line-height: 1 !important;
                       display: block; margin-bottom: 10px !important; }}
    .hallazgo h4 {{ margin: 0 0 8px !important; font-size: 1.02rem !important;
                    font-weight: 600 !important; color: {DIAL} !important; }}
    .hallazgo p  {{ margin: 0 !important; font-size: .91rem !important;
                    color: {MIST} !important; line-height: 1.55 !important; }}

    .aviso {{ display: inline-block; font-family: 'IBM Plex Mono', monospace;
              font-size: .7rem; letter-spacing: .06em; padding: 4px 9px;
              border: 1px solid {BRASS}; color: {BRASS}; margin-bottom: 14px; }}

    footer, #MainMenu {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 2. EL MODELO
# =============================================================================

# Coeficientes de demostración. En cuanto entrenes el modelo real, exporta
# data/modelo.json desde el cuaderno y esta función lo cargará sola.
MODELO_DEMO = {
    "intercepto": 0.9750,
    "coeficientes": {"velocidad": 0.0000, "temperatura": -0.0080,
                     "combustible": 0.0060, "presion": 0.0040},
    "medias": {"velocidad": 15.00, "temperatura": 750.0,
               "combustible": 0.60, "presion": 12.00},
    "desviaciones": {"velocidad": 7.75, "temperatura": 175.0,
                     "combustible": 0.42, "presion": 4.90},
}


@st.cache_data
def cargar_modelo():
    """Lee data/modelo.json si existe. Si no, usa los coeficientes de demostración."""
    ruta = Path(__file__).parent / "data" / "modelo.json"
    if ruta.exists():
        with open(ruta, encoding="utf-8") as f:
            return json.load(f), True
    return MODELO_DEMO, False


def predecir(modelo, entradas):
    """Aplica la misma normalización que se usó al entrenar y suma los términos.

    Si en el cuaderno NO normalizaste las features, borra la línea de la z
    y multiplica el coeficiente por el valor crudo.
    """
    y = modelo["intercepto"]
    for nombre, coef in modelo["coeficientes"].items():
        z = (entradas[nombre] - modelo["medias"][nombre]) / modelo["desviaciones"][nombre]
        y += coef * z
    return min(1.0, max(0.95, y))   # el modelo solo es válido en este rango


def diagnostico(kmc):
    """Traduce el coeficiente a una recomendación de mantenimiento."""
    if kmc >= 0.985:
        return "Compresor en buen estado", "Sin acción. Continuar operación normal.", SEA, "#0B1F1C"
    if kmc >= 0.965:
        return "Degradación apreciable", "Programar revisión en la próxima ventana de parada.", BRASS, "#241705"
    return "Degradación severa", "Intervenir cuanto antes. Riesgo de fallo y sobreconsumo.", SIGNAL, "#FFF1EE"


def manometro(kmc):
    """Manómetro analógico con las tres zonas de estado."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=kmc,
        number={"font": {"size": 46, "color": DIAL, "family": "IBM Plex Mono"},
                "valueformat": ".3f"},
        gauge={
            "axis": {"range": [0.95, 1.0], "tickwidth": 1, "tickcolor": MIST,
                     "tickvals": [0.95, 0.965, 0.985, 1.0],
                     "tickfont": {"size": 11, "color": MIST}},
            "bar": {"color": "rgba(0,0,0,0)"},          # la barra estorba: usamos aguja
            "threshold": {"line": {"color": DIAL, "width": 5},
                          "thickness": 0.9, "value": kmc},
            "bgcolor": HULL,
            "borderwidth": 0,
            "steps": [
                {"range": [0.950, 0.965], "color": SIGNAL},
                {"range": [0.965, 0.985], "color": BRASS},
                {"range": [0.985, 1.000], "color": SEA},
            ],
        },
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=24, r=24, t=16, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": DIAL, "family": "Archivo"},
    )
    return fig


def barras_correlacion(mezclada, a_15_nudos):
    """Compara la correlación cruda con la correlación a régimen constante."""
    fig = go.Figure(go.Bar(
        x=[mezclada, a_15_nudos],
        y=["Mezclando las nueve velocidades", "Comparando solo a 15 nudos"],
        orientation="h",
        marker_color=[SIGNAL, SEA],
        text=[f"{mezclada:.2f}", f"{a_15_nudos:.2f}"],
        textposition="outside",
        textfont={"family": "IBM Plex Mono", "size": 14, "color": DIAL},
    ))
    fig.update_layout(
        height=210,
        margin=dict(l=8, r=48, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 1], showgrid=True, gridcolor="#24474A",
                   zeroline=False, tickfont={"color": MIST, "size": 11}),
        yaxis=dict(tickfont={"color": DIAL, "size": 13}),
        font={"family": "Archivo"},
        showlegend=False,
    )
    return fig


def pesos(n):
    """Formato de moneda: $1,500,000"""
    return f"${n:,.0f}"


def pesos_corto(n):
    """Formato compacto para que quepa en las métricas: $1.5 M"""
    if n >= 1_000_000:
        return f"${n / 1_000_000:,.1f} M"
    if n >= 1_000:
        return f"${n / 1_000:,.0f} mil"
    return f"${n:,.0f}"


modelo, modelo_real = cargar_modelo()


# =============================================================================
# 3. PORTADA
# =============================================================================

izq, der = st.columns([1.15, 0.85], gap="large")

with izq:
    st.markdown(
        '<p class="matricula">Turbina de gas marina, 11.934 lecturas de sensores</p>'
        '<p class="titular">Deja de cambiar piezas que todavía funcionan</p>'
        '<hr class="guia">'
        '<p class="entrada">El mantenimiento por calendario tira dinero de dos formas: '
        'sustituye componentes sanos y aun así no evita las averías. Aquí puedes calcular '
        'cuánto te cuesta eso y probar un estimador que deduce el desgaste interno de un '
        'motor a partir de lo que ya miden sus sensores.</p>',
        unsafe_allow_html=True,
    )

with der:
    st.plotly_chart(manometro(0.987), use_container_width=True,
                    config={"displayModeBar": False})
    st.markdown(
        f'<div class="semaforo" style="background:{SEA};color:#0B1F1C">'
        'Lectura de ejemplo del compresor</div>',
        unsafe_allow_html=True,
    )

st.write("")
st.divider()


# =============================================================================
# 4. EL PROBLEMA
# =============================================================================

st.header("Tres formas de decidir cuándo reparar")
st.markdown(f'<p class="rotulo">Solo una de las tres mira el estado real de la máquina.</p>',
            unsafe_allow_html=True)
st.write("")

placas = [
    (SIGNAL, "Esperar a que falle",
     "La máquina se rompe en el peor momento posible y arrastra el producto, la entrega y al cliente.",
     "Coste por avería: máximo"),
    (BRASS, "Reparar por calendario",
     "Cada tantas horas se sustituye la pieza, esté como esté. Se tiran componentes sanos y las averías fuera de ciclo siguen ocurriendo.",
     "Coste por avería: alto y constante"),
    (SEA, "Reparar cuando los datos lo piden",
     "Los sensores que ya están instalados indican cuánto se ha degradado la máquina por dentro. Se interviene justo antes del fallo.",
     "Coste por avería: mínimo"),
]

for col, (color, titulo, texto, coste) in zip(st.columns(3, gap="medium"), placas):
    col.markdown(
        f'<div class="placa" style="border-color:{color}">'
        f'<h4>{titulo}</h4><p>{texto}</p><span class="coste">{coste}</span></div>',
        unsafe_allow_html=True,
    )

st.write("")
st.divider()


# =============================================================================
# 5. CALCULADORA DE AHORRO
# =============================================================================

st.header("Cuánto te cuesta el mantenimiento a ciegas")
st.markdown(
    '<p class="rotulo">Pon tus propios números. El cálculo es deliberadamente simple '
    'y puedes ver la fórmula completa en el código.</p>',
    unsafe_allow_html=True,
)
st.write("")

entradas_col, resultado_col = st.columns([1, 1], gap="large")

with entradas_col:
    maquinas = st.number_input("Máquinas críticas en operación",
                               min_value=1, value=10, step=1)
    paradas = st.number_input("Paradas no planeadas por máquina al año",
                              min_value=0.0, value=3.0, step=0.5)
    coste_parada = st.number_input("Coste de una parada no planeada (MXN)",
                                   min_value=0, value=50_000, step=1_000)
    evitable = st.slider("Paradas evitables con aviso anticipado (%)",
                         min_value=0, max_value=70, value=30, step=5)

# ahorro = máquinas x paradas x coste x porcentaje evitable
paradas_totales = maquinas * paradas
coste_actual = paradas_totales * coste_parada
evitadas = paradas_totales * (evitable / 100)
ahorro = evitadas * coste_parada

with resultado_col:
    st.markdown(
        f'<p class="rotulo">Ahorro anual estimado</p>'
        f'<span class="cifra">{pesos(ahorro)}</span>'
        f'<p class="rotulo">Solo cuenta las paradas evitadas. No incluye el ahorro por '
        f'dejar de sustituir piezas que aún servían, que suele ser de la misma magnitud.</p>',
        unsafe_allow_html=True,
    )
    st.write("")
    a, b, c = st.columns(3)
    a.metric("Paradas al año", f"{paradas_totales:,.0f}")
    b.metric("Coste actual", pesos_corto(coste_actual))
    c.metric("Paradas evitadas", f"{evitadas:,.1f}")

st.write("")
st.divider()


# =============================================================================
# 6. ESTIMADOR DE DESGASTE
# =============================================================================

if not modelo_real:
    st.markdown('<span class="aviso">Versión alfa, coeficientes de demostración</span>',
                unsafe_allow_html=True)

st.header("Estimador de desgaste del compresor")
st.markdown(
    '<p class="rotulo">Mueve los controles como si fueran las lecturas de tu motor. '
    'El estimador devuelve el coeficiente de degradación del compresor: 1.000 es una '
    'pieza nueva y 0.950 es el límite del rango estudiado.</p>',
    unsafe_allow_html=True,
)
st.write("")

controles_col, lectura_col = st.columns([1, 1], gap="large")

with controles_col:
    velocidad = st.select_slider("Velocidad del buque (nudos)",
                                 options=[3, 6, 9, 12, 15, 18, 21, 24, 27], value=15)
    temperatura = st.slider("Temperatura de salida de turbina (K)",
                            min_value=460, max_value=1120, value=750, step=5)
    combustible = st.slider("Flujo de combustible (kg/s)",
                            min_value=0.05, max_value=1.85, value=0.60, step=0.01)
    presion = st.slider("Presión de salida del compresor (bar)",
                        min_value=5.8, max_value=23.2, value=12.0, step=0.1)

kmc = predecir(modelo, {
    "velocidad": velocidad,
    "temperatura": temperatura,
    "combustible": combustible,
    "presion": presion,
})
etiqueta, consejo, fondo, tinta = diagnostico(kmc)

with lectura_col:
    st.plotly_chart(manometro(kmc), use_container_width=True,
                    config={"displayModeBar": False})
    st.markdown(
        f'<div class="semaforo" style="background:{fondo};color:{tinta}">{etiqueta}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="rotulo" style="margin-top:12px">{consejo}</p>',
                unsafe_allow_html=True)

st.write("")
st.divider()


# =============================================================================
# 7. HALLAZGOS
# =============================================================================

st.header("Lo que encontramos en los datos")
st.markdown(
    '<p class="rotulo">Once mil novecientas treinta y cuatro lecturas de un simulador '
    'de propulsión naval calibrado sobre buques reales, con dieciséis mediciones por lectura.</p>',
    unsafe_allow_html=True,
)
st.write("")

hallazgos = [
    ("2", "Sensores que no medían nada",
     "La temperatura y la presión de entrada al compresor son idénticas en las 11.934 "
     "lecturas. Una columna que nunca cambia no puede explicar nada, así que se descartan."),
    ("0.00", "Diferencia entre las dos hélices",
     "El par de babor y el de estribor coinciden hasta el último decimal en todos los "
     "casos. Información duplicada: se conserva una sola."),
    ("9×51×26", "No es una muestra, es un experimento",
     "El producto de velocidades, niveles de desgaste del compresor y de la turbina da "
     "exactamente el número de filas. Se probaron todas las combinaciones posibles, sin azar."),
    ("288 K", "Un error en la documentación de la fuente",
     "La ficha del conjunto de datos declara grados Celsius, pero el valor corresponde al "
     "día estándar ISO en Kelvin. Lo dejamos anotado porque afecta a quien reutilice estos datos."),
]

fila1 = st.columns(2, gap="medium")
fila2 = st.columns(2, gap="medium")
for col, (dato, titulo, texto) in zip(fila1 + fila2, hallazgos):
    with col.container(border=True):
        st.markdown(
            f'<div class="hallazgo"><span class="dato">{dato}</span>'
            f'<h4>{titulo}</h4><p>{texto}</p></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.subheader("Por qué hay que comparar a velocidad constante")
st.markdown(
    '<p class="rotulo">Relación entre el consumo de combustible y el desgaste del '
    'compresor, medida de dos maneras.</p>',
    unsafe_allow_html=True,
)

# CAMBIAR: sustituye por tus dos correlaciones reales
CORR_MEZCLADA = 0.02
CORR_A_15_NUDOS = 0.71

st.plotly_chart(barras_correlacion(CORR_MEZCLADA, CORR_A_15_NUDOS),
                use_container_width=True, config={"displayModeBar": False})
st.markdown(
    '<p class="rotulo">La velocidad mueve el consumo mucho más que el desgaste, así que '
    'al mezclar regímenes la señal desaparece. Un sensor por sí solo no dice nada; hay que '
    'leerlo en su contexto de operación.</p>',
    unsafe_allow_html=True,
)

st.write("")
st.divider()


# =============================================================================
# 8. MÉTODO Y LIMITACIONES
# =============================================================================

metodo_col, limites_col = st.columns(2, gap="large")

with metodo_col:
    st.subheader("Cómo lo construimos")
    st.markdown("""
- Exploración de las 11.934 lecturas: valores faltantes, duplicados y estadística descriptiva.
- Descarte de las columnas sin variación y de la información duplicada.
- Análisis de la relación entre cada sensor y el desgaste, controlando por régimen de operación.
- Modelo de regresión entrenado en Python y servido por esta misma aplicación.
""")

with limites_col:
    st.subheader("Qué no puedes concluir de esto")
    st.markdown("""
- Los datos vienen de un simulador, no de sensores instalados en un barco. El modelo debe recalibrarse con mediciones reales antes de usarse para decidir una intervención.
- Los coeficientes del estimador de esta versión son de demostración.
- El ahorro que calcula la herramienta es una estimación aritmética a partir de los números que introduces, no una auditoría.
- El modelo cubre el rango de desgaste estudiado (compresor de 1.000 a 0.950). Fuera de él no hay evidencia.
""")

st.divider()


# =============================================================================
# 9. PIE
# =============================================================================

datos_col, codigo_col, equipo_col = st.columns(3, gap="large")

with datos_col:
    st.markdown("**Datos**")
    st.markdown(
        "[Condition Based Maintenance of Naval Propulsion Plants]"
        "(https://archive.ics.uci.edu/dataset/316/condition+based+maintenance+of+naval+propulsion+plants)  \n"
        "UCI Machine Learning Repository, conjunto 316  \n"
        "Licencia CC BY 4.0"
    )

with codigo_col:
    st.markdown("**Código**")
    # CAMBIAR: enlaces a tu repositorio
    st.markdown(
        "[Repositorio en GitHub](#)  \n"
        "[Cuaderno de exploración](#)  \n"
        "[Cuaderno de modelado](#)"
    )

with equipo_col:
    st.markdown("**Equipo**")
    # CAMBIAR: nombres del equipo
    st.markdown(
        "Nombre y apellido  \n"
        "Nombre y apellido  \n"
        "Nombre y apellido  \n"
        "Business Intelligence, 2026"
    )

st.caption(
    "Coraddu, A., Oneto, L., Ghio, A., Savio, S., Anguita, D. y Figari, M. (2014). "
    "Machine learning approaches for improving condition-based maintenance of naval "
    "propulsion plants. Conjunto de datos alojado en el UCI Machine Learning Repository."
)
