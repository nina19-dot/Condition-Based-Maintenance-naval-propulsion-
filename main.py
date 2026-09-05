import json
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# =============================================================================
# 1. CONFIGURACIÓN Y PALETA
# =============================================================================

st.set_page_config(
    page_title="Turbina de gas: estimador de degradación",
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
STEEL = "#2C5155"    # filetes y bordes

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {{ font-family: 'Archivo', system-ui, sans-serif; }}

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

    .placa {{ background: {HULL}; border-left: 4px solid; padding: 22px 20px; height: 100%; }}
    .placa h4 {{ margin: 0 0 10px !important; font-size: 1.08rem !important;
                 font-weight: 600 !important; color: {DIAL} !important; }}
    .placa p  {{ margin: 0 !important; font-size: .93rem !important;
                 color: {MIST} !important; line-height: 1.55 !important; }}
    .placa .coste {{ display: block; margin-top: 14px; font-family: 'IBM Plex Mono', monospace;
                     font-size: .74rem; letter-spacing: .04em; color: {BRASS}; }}

    .cifra {{ font-family: 'IBM Plex Mono', monospace !important; font-weight: 600 !important;
              font-size: clamp(1.9rem, 4vw, 2.6rem) !important; color: {BRASS} !important;
              line-height: 1.05 !important; display: block; margin: 4px 0 10px !important; }}
    .rotulo {{ font-size: .88rem !important; color: {MIST} !important;
               margin: 0 !important; line-height: 1.55 !important; }}

    .semaforo {{ padding: 12px 16px; font-weight: 600; font-size: .95rem;
                 text-align: center; border-radius: 2px; }}

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

    .esquema {{ width: 100%; overflow-x: auto; padding: 8px 0 4px; }}

    footer, #MainMenu {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 2. ESQUEMA DE LA PLANTA DE PROPULSIÓN
#    Dibuja la cadena completa y coloca cada sensor donde está físicamente.
# =============================================================================

def esquema_planta():
    """SVG de la planta CODLAG con los 16 sensores situados en la máquina."""
    etapas = [
        (35, "Admisión de aire", "T1 · P1"),
        (225, "Compresor", "T2 · P2"),
        (415, "Cámara de combustión", "mf · TIC"),
        (605, "Turbina de alta presión", "T48 · P48"),
        (795, "Turbina de potencia", "GTT · GTn · GGn · Pexh"),
    ]

    cajas = ""
    for x, titulo, sensores in etapas:
        cajas += f"""
        <rect x="{x}" y="46" width="170" height="62" rx="4"
              fill="{HULL}" stroke="{BRASS}" stroke-width="1.4"/>
        <text x="{x + 85}" y="72" text-anchor="middle" fill="{DIAL}"
              font-size="13" font-weight="600" font-family="Archivo">{titulo}</text>
        <text x="{x + 85}" y="93" text-anchor="middle" fill="{BRASS}"
              font-size="10.5" font-family="IBM Plex Mono">{sensores}</text>
        """

    flechas = ""
    for x in (205, 395, 585, 775):
        flechas += f"""<line x1="{x}" y1="77" x2="{x + 18}" y2="77"
                       stroke="{MIST}" stroke-width="1.6" marker-end="url(#pta)"/>"""

    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap');
      body {{ margin:0; padding:0; background:{INK}; }}
      svg {{ width:100%; max-width:1000px; height:auto; display:block; margin:0 auto; }}
    </style>
    <svg viewBox="0 0 1000 300" width="100%" role="img"
         aria-label="Esquema de la planta de propulsión con la posición de cada sensor">
      <defs>
        <marker id="pta" viewBox="0 0 10 10" refX="8" refY="5"
                markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M2 1 L8 5 L2 9" fill="none" stroke="{MIST}"
                stroke-width="1.6" stroke-linecap="round"/>
        </marker>
      </defs>

      <text x="35" y="28" fill="{MIST}" font-size="11.5"
            font-family="IBM Plex Mono" letter-spacing="1">TURBINA DE GAS</text>
      {cajas}
      {flechas}

      <!-- bajada de la turbina de potencia a la reductora -->
      <path d="M 880 108 L 880 150 L 310 150 L 310 186" fill="none"
            stroke="{MIST}" stroke-width="1.6" marker-end="url(#pta)"/>

      <text x="35" y="178" fill="{MIST}" font-size="11.5"
            font-family="IBM Plex Mono" letter-spacing="1">LÍNEA DE PROPULSIÓN</text>

      <!-- diésel-eléctrico, modo crucero -->
      <rect x="35" y="192" width="170" height="62" rx="4"
            fill="{INK}" stroke="{STEEL}" stroke-width="1.4" stroke-dasharray="5 4"/>
      <text x="120" y="216" text-anchor="middle" fill="{MIST}"
            font-size="12.5" font-weight="600" font-family="Archivo">Diésel-eléctrico</text>
      <text x="120" y="236" text-anchor="middle" fill="{MIST}"
            font-size="10" font-family="IBM Plex Mono">modo crucero</text>
      <line x1="205" y1="223" x2="223" y2="223" stroke="{STEEL}"
            stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#pta)"/>

      <!-- reductora -->
      <rect x="225" y="192" width="170" height="62" rx="4"
            fill="{HULL}" stroke="{SEA}" stroke-width="1.4"/>
      <text x="310" y="218" text-anchor="middle" fill="{DIAL}"
            font-size="13" font-weight="600" font-family="Archivo">Reductora</text>
      <text x="310" y="238" text-anchor="middle" fill="{SEA}"
            font-size="10.5" font-family="IBM Plex Mono">lp · v</text>
      <line x1="395" y1="223" x2="413" y2="223" stroke="{MIST}"
            stroke-width="1.6" marker-end="url(#pta)"/>

      <!-- ejes y hélices -->
      <rect x="415" y="192" width="270" height="62" rx="4"
            fill="{HULL}" stroke="{SEA}" stroke-width="1.4"/>
      <text x="550" y="218" text-anchor="middle" fill="{DIAL}"
            font-size="13" font-weight="600" font-family="Archivo">Eje y hélice de estribor</text>
      <text x="550" y="238" text-anchor="middle" fill="{SEA}"
            font-size="10.5" font-family="IBM Plex Mono">Ts</text>

      <rect x="705" y="192" width="260" height="62" rx="4"
            fill="{HULL}" stroke="{SEA}" stroke-width="1.4"/>
      <text x="835" y="218" text-anchor="middle" fill="{DIAL}"
            font-size="13" font-weight="600" font-family="Archivo">Eje y hélice de babor</text>
      <text x="835" y="238" text-anchor="middle" fill="{SEA}"
            font-size="10.5" font-family="IBM Plex Mono">Tp</text>

      <line x1="310" y1="254" x2="310" y2="272" stroke="{MIST}" stroke-width="1.6"/>
      <line x1="310" y1="272" x2="550" y2="272" stroke="{MIST}" stroke-width="1.6"/>
      <line x1="550" y1="272" x2="550" y2="256" stroke="{MIST}"
            stroke-width="1.6" marker-end="url(#pta)"/>
      <line x1="310" y1="272" x2="835" y2="272" stroke="{MIST}" stroke-width="1.6"/>
      <line x1="835" y1="272" x2="835" y2="256" stroke="{MIST}"
            stroke-width="1.6" marker-end="url(#pta)"/>
    </svg>
    """


# =============================================================================
# 3. LOS DOS MODELOS: COMPRESOR Y TURBINA
# =============================================================================

# Coeficientes de demostración. En cuanto entrenen los modelos reales, exporten
# data/modelo.json desde el cuaderno y esta función lo cargará solo.
MODELO_DEMO = {
    "compresor": {
        "intercepto": 0.9750,
        "coeficientes": {"velocidad": 0.0000, "temperatura": -0.0080,
                         "combustible": 0.0060, "presion": 0.0040},
        "medias": {"velocidad": 15.00, "temperatura": 750.0,
                   "combustible": 0.60, "presion": 12.00},
        "desviaciones": {"velocidad": 7.75, "temperatura": 175.0,
                         "combustible": 0.42, "presion": 4.90},
    },
    "turbina": {
        "intercepto": 0.9875,
        "coeficientes": {"velocidad": 0.0000, "temperatura": -0.0045,
                         "combustible": 0.0028, "presion": 0.0015},
        "medias": {"velocidad": 15.00, "temperatura": 750.0,
                   "combustible": 0.60, "presion": 12.00},
        "desviaciones": {"velocidad": 7.75, "temperatura": 175.0,
                         "combustible": 0.42, "presion": 4.90},
    },
}

# Rango físico de cada coeficiente de degradación, según la documentación del dataset
RANGOS = {"compresor": (0.950, 1.000), "turbina": (0.975, 1.000)}


@st.cache_data
def cargar_modelo():
    """Lee data/modelo.json si existe. Si no, usa los coeficientes de demostración."""
    ruta = Path(__file__).parent / "data" / "modelo.json"
    if ruta.exists():
        with open(ruta, encoding="utf-8") as f:
            return json.load(f), True
    return MODELO_DEMO, False


def predecir(submodelo, entradas, rango):
    """Aplica la misma normalización que se usó al entrenar y suma los términos.

    Si en el cuaderno NO normalizaron las features, borren la línea de la z
    y multipliquen el coeficiente por el valor crudo.
    """
    y = submodelo["intercepto"]
    for nombre, coef in submodelo["coeficientes"].items():
        z = (entradas[nombre] - submodelo["medias"][nombre]) / submodelo["desviaciones"][nombre]
        y += coef * z
    return min(rango[1], max(rango[0], y))


def diagnostico(valor, rango, componente):
    """Traduce el coeficiente a una recomendación de mantenimiento.

    Los umbrales están al 30 % y al 70 % del rango físico de cada componente,
    de modo que el criterio sea el mismo para el compresor y para la turbina.
    """
    minimo, maximo = rango
    amplitud = maximo - minimo
    if valor >= minimo + 0.70 * amplitud:
        return (f"{componente} en buen estado",
                "Sin acción. Continuar navegación normal.", SEA, "#0B1F1C")
    if valor >= minimo + 0.30 * amplitud:
        return (f"{componente} con degradación apreciable",
                "Programar lavado o inspección en la próxima escala.", BRASS, "#241705")
    return (f"{componente} con degradación severa",
            "Intervenir cuanto antes. Sobreconsumo y pérdida de empuje.", SIGNAL, "#FFF1EE")


def manometro(valor, rango, titulo):
    """Manómetro con las tres zonas de estado, escalado al rango del componente."""
    minimo, maximo = rango
    amplitud = maximo - minimo
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        number={"font": {"size": 40, "color": DIAL, "family": "IBM Plex Mono"},
                "valueformat": ".3f"},
        gauge={
            "axis": {"range": [minimo, maximo], "tickwidth": 1, "tickcolor": MIST,
                     "tickvals": [minimo, maximo],
                     "tickfont": {"size": 11, "color": MIST}},
            "bar": {"color": "rgba(0,0,0,0)"},          # la barra estorba: usamos aguja
            "threshold": {"line": {"color": DIAL, "width": 5},
                          "thickness": 0.9, "value": valor},
            "bgcolor": HULL,
            "borderwidth": 0,
            "steps": [
                {"range": [minimo, minimo + 0.30 * amplitud], "color": SIGNAL},
                {"range": [minimo + 0.30 * amplitud, minimo + 0.70 * amplitud], "color": BRASS},
                {"range": [minimo + 0.70 * amplitud, maximo], "color": SEA},
            ],
        },
    ))
    fig.update_layout(
        height=235,
        margin=dict(l=20, r=20, t=18, b=8),
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
        height=200,
        margin=dict(l=8, r=48, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 1], showgrid=True, gridcolor=STEEL,
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
# 4. PORTADA
# =============================================================================

izq, der = st.columns([1.15, 0.85], gap="large")

with izq:
    st.markdown(
        '<p class="matricula">Planta CODLAG · turbina de gas · 11.934 lecturas</p>'
        '<p class="titular">La turbina se gasta por dentro y nadie lo ve</p>'
        '<hr class="guia">'
        '<p class="entrada">El compresor y la turbina de una planta de propulsión naval '
        'pierden rendimiento con cada hora de navegación. La máquina sigue moviendo las '
        'hélices, pero quema más combustible para dar el mismo empuje. Aquí puedes estimar '
        'ese desgaste a partir de lo que ya miden los sensores de la planta, sin desmontar '
        'nada.</p>',
        unsafe_allow_html=True,
    )

with der:
    st.plotly_chart(manometro(0.987, RANGOS["compresor"], "Compresor"),
                    use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        f'<div class="semaforo" style="background:{SEA};color:#0B1F1C">'
        'Lectura de ejemplo</div>',
        unsafe_allow_html=True,
    )

st.write("")
st.divider()


# =============================================================================
# 5. CÓMO FUNCIONA LA PLANTA
# =============================================================================

st.header("Cómo se mueve una fragata")
st.markdown(
    '<p class="rotulo">La planta es CODLAG: diésel-eléctrico para navegar despacio y '
    'ahorrar, turbina de gas cuando hace falta potencia. Las dos vías terminan en la misma '
    'reductora y en los mismos dos ejes.</p>',
    unsafe_allow_html=True,
)

# components.html renderiza el SVG en un iframe: st.markdown lo sanearía
components.html(esquema_planta(), height=320, scrolling=False)

st.markdown(
    '<p class="rotulo">Cada etiqueta en color es un sensor real del conjunto de datos. '
    'Los dieciséis están situados donde se miden de verdad.</p>',
    unsafe_allow_html=True,
)

st.write("")

recorrido = [
    (BRASS, "El compresor",
     "Aspira aire y lo comprime hasta unas quince veces la presión atmosférica antes de la "
     "combustión. Es la pieza que más sufre: la sal marina y las partículas se adhieren a los "
     "álabes y ensucian su perfil aerodinámico. A eso se le llama fouling.",
     "Se degrada de 1.000 a 0.950"),
    (SIGNAL, "La turbina",
     "Recibe los gases de la combustión a más de mil grados y los convierte en giro. Parte de "
     "ese giro realimenta al compresor y el resto sale por la turbina de potencia hacia la "
     "reductora. Se degrada por erosión y por depósitos a alta temperatura.",
     "Se degrada de 1.000 a 0.975"),
    (SEA, "Los propulsores",
     "La reductora baja las revoluciones y reparte el par entre los dos ejes, que mueven las "
     "hélices de babor y estribor. El par de cada hélice es la medida final de cuánto empuje "
     "está entregando realmente la planta.",
     "Se miden como Ts y Tp"),
]

for col, (color, titulo, texto, nota) in zip(st.columns(3, gap="medium"), recorrido):
    col.markdown(
        f'<div class="placa" style="border-color:{color}">'
        f'<h4>{titulo}</h4><p>{texto}</p><span class="coste">{nota}</span></div>',
        unsafe_allow_html=True,
    )

st.write("")
st.divider()


# =============================================================================
# 6. LOS DIECISÉIS SENSORES
# =============================================================================

st.header("Qué mide cada sensor y para qué sirve")
st.markdown(
    '<p class="rotulo">Ninguno de estos instrumentos mide el desgaste. Todos miden '
    'consecuencias del desgaste. Ese es el problema que resuelve el modelo.</p>',
    unsafe_allow_html=True,
)
st.write("")

sensores = [
    ("Admisión de aire", "T1, P1", "Temperatura y presión del aire ambiente antes de entrar al compresor.", "Constantes en todo el conjunto: se descartan"),
    ("Compresor", "T2, P2", "Temperatura y presión del aire ya comprimido.", "Un compresor sucio comprime peor y calienta más"),
    ("Combustión", "mf, TIC", "Flujo de combustible y control de inyección de la turbina.", "Aquí está el dinero: mf va en kg/s"),
    ("Turbina de alta presión", "T48, P48", "Temperatura y presión de los gases a la salida.", "Sube cuando la máquina trabaja forzada"),
    ("Turbina de potencia", "GTT, GTn, GGn, Pexh", "Par, revoluciones de la turbina y del generador de gas, presión de escape.", "La potencia que sale de la planta"),
    ("Propulsión", "lp, v, Ts, Tp", "Palanca, velocidad del buque y par de cada hélice.", "Ts y Tp son idénticos: se conserva uno"),
]

for etapa, cols, que_mide, nota in sensores:
    with st.container(border=True):
        a, b, c = st.columns([1.1, 2.4, 1.6])
        a.markdown(f"**{etapa}**  \n<span style='font-family:IBM Plex Mono;"
                   f"font-size:.8rem;color:{BRASS}'>{cols}</span>",
                   unsafe_allow_html=True)
        b.markdown(f"<p class='rotulo'>{que_mide}</p>", unsafe_allow_html=True)
        c.markdown(f"<p class='rotulo' style='color:{DIAL}'>{nota}</p>",
                   unsafe_allow_html=True)

st.write("")
st.divider()


# =============================================================================
# 7. TRES FORMAS DE DECIDIR CUÁNDO REPARAR
# =============================================================================

st.header("Tres formas de decidir cuándo abrir la turbina")
st.markdown('<p class="rotulo">Solo una de las tres mira el estado real de la máquina.</p>',
            unsafe_allow_html=True)
st.write("")

placas = [
    (SIGNAL, "Esperar a que falle",
     "La turbina se para en plena navegación. En un buque, eso no es un taller a media hora: "
     "es una avería en mitad del mar con la misión comprometida.",
     "Coste por avería: máximo"),
    (BRASS, "Reparar por horas de operación",
     "Cada tantas horas de funcionamiento se desmonta y se revisa, esté como esté. Se retiran "
     "componentes con vida útil restante y las averías fuera de ciclo siguen ocurriendo.",
     "Coste por avería: alto y constante"),
    (SEA, "Reparar cuando los sensores lo piden",
     "La instrumentación que la planta ya lleva instalada permite estimar la degradación del "
     "compresor y de la turbina. Se lava o se interviene justo cuando el rendimiento lo exige.",
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
# 8. CALCULADORA DE SOBRECONSUMO
# =============================================================================

st.header("Lo que cuesta navegar con la turbina sucia")
st.markdown(
    '<p class="rotulo">El desgaste no se paga solo en repuestos. Se paga cada hora, en '
    'combustible, mucho antes de que nadie abra la máquina. El cálculo parte del flujo de '
    'combustible medido en la propia planta.</p>',
    unsafe_allow_html=True,
)
st.write("")

entradas_col, resultado_col = st.columns([1, 1], gap="large")

with entradas_col:
    # CAMBIAR: sustituyan el valor por defecto por el sobreconsumo real que
    # obtengan de su dataset, comparando mf con kMc = 1.000 y kMc = 0.950
    # a la misma velocidad.
    sobreconsumo_pct = st.slider(
        "Sobreconsumo de combustible por degradación (%)",
        min_value=0.5, max_value=10.0, value=3.0, step=0.1,
        help="Medido en el propio conjunto de datos: diferencia de mf entre "
             "compresor nuevo y compresor gastado, a igual velocidad.",
    )
    mf_base = st.slider("Flujo de combustible con la turbina limpia (kg/s)",
                        min_value=0.05, max_value=1.90, value=0.60, step=0.01)
    horas_anio = st.number_input("Horas de navegación con turbina al año",
                                 min_value=0, value=2_000, step=100)
    precio_ton = st.number_input("Precio del MGO (USD por tonelada)",
                                 min_value=0, value=600, step=25,
                                 help="Cotización de Ship & Bunker. Anoten puerto y fecha.")
    turbinas = st.number_input("Turbinas en la flota", min_value=1, value=1, step=1)

# kg/s extra -> kg/h -> toneladas/h -> USD/h -> USD/año
delta_mf = mf_base * (sobreconsumo_pct / 100)
ton_hora = delta_mf * 3600 / 1000
usd_hora = ton_hora * precio_ton
usd_anio = usd_hora * horas_anio * turbinas

with resultado_col:
    st.markdown(
        f'<p class="rotulo">Combustible extra al año, solo por degradación</p>'
        f'<span class="cifra">{pesos(usd_anio)} USD</span>'
        f'<p class="rotulo">No incluye repuestos, mano de obra ni el coste de la '
        f'indisponibilidad del buque. Es únicamente el combustible que se quema de más '
        f'por mover las mismas hélices con una máquina degradada.</p>',
        unsafe_allow_html=True,
    )
    st.write("")
    a, b, c = st.columns(3)
    a.metric("Sobreconsumo", f"{delta_mf:.4f} kg/s")
    b.metric("Coste por hora", pesos_corto(usd_hora))
    c.metric("Toneladas al año", f"{ton_hora * horas_anio * turbinas:,.0f}")

st.write("")
st.divider()


# =============================================================================
# 9. ESTIMADOR DE DEGRADACIÓN (COMPRESOR Y TURBINA)
# =============================================================================

if not modelo_real:
    st.markdown('<span class="aviso">Versión alfa, coeficientes de demostración</span>',
                unsafe_allow_html=True)

st.header("Estimador de degradación de la planta")
st.markdown(
    '<p class="rotulo">Mueve los controles como si fueran las lecturas de la sala de '
    'máquinas. El modelo devuelve por separado el estado del compresor y el de la turbina, '
    'porque se degradan por causas distintas y a ritmos distintos.</p>',
    unsafe_allow_html=True,
)
st.write("")

controles_col, compresor_col, turbina_col = st.columns([1.1, 0.95, 0.95], gap="medium")

with controles_col:
    velocidad = st.select_slider("Velocidad del buque (nudos)",
                                 options=[3, 6, 9, 12, 15, 18, 21, 24, 27], value=15)
    temperatura = st.slider("T48, salida de turbina de alta presión (K)",
                            min_value=460, max_value=1120, value=750, step=5)
    combustible = st.slider("mf, flujo de combustible (kg/s)",
                            min_value=0.05, max_value=1.85, value=0.60, step=0.01)
    presion = st.slider("P2, salida del compresor (bar)",
                        min_value=5.8, max_value=23.2, value=12.0, step=0.1)

entradas = {"velocidad": velocidad, "temperatura": temperatura,
            "combustible": combustible, "presion": presion}

for col, clave, nombre in [(compresor_col, "compresor", "Compresor"),
                           (turbina_col, "turbina", "Turbina")]:
    valor = predecir(modelo[clave], entradas, RANGOS[clave])
    etiqueta, consejo, fondo, tinta = diagnostico(valor, RANGOS[clave], nombre)
    with col:
        st.markdown(f"<p class='rotulo' style='text-align:center;color:{DIAL};"
                    f"font-weight:600'>{nombre}</p>", unsafe_allow_html=True)
        st.plotly_chart(manometro(valor, RANGOS[clave], nombre),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            f'<div class="semaforo" style="background:{fondo};color:{tinta}">{etiqueta}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<p class="rotulo" style="margin-top:10px">{consejo}</p>',
                    unsafe_allow_html=True)

st.write("")
st.divider()


# =============================================================================
# 10. HALLAZGOS
# =============================================================================

st.header("Lo que encontramos en los datos de la planta")
st.markdown(
    '<p class="rotulo">Once mil novecientas treinta y cuatro lecturas de un simulador de '
    'propulsión naval calibrado sobre buques reales, con dieciséis mediciones por lectura.</p>',
    unsafe_allow_html=True,
)
st.write("")

hallazgos = [
    ("T1 · P1", "Dos sensores de admisión que no miden nada",
     "La temperatura y la presión del aire de entrada al compresor son idénticas en las "
     "11.934 lecturas: el simulador fija condiciones atmosféricas estándar. Sin variación no "
     "hay información, así que se descartan."),
    ("Ts = Tp", "Las dos hélices dan el mismo par",
     "El par del eje de estribor y el de babor coinciden hasta el último decimal en todos los "
     "casos: la reductora reparte por igual. Se conserva una sola de las dos columnas."),
    ("9×51×26", "No es una muestra, es un banco de pruebas",
     "Nueve velocidades por cincuenta y un niveles de degradación del compresor por veintiséis "
     "de la turbina dan exactamente el número de filas. Se simuló toda la matriz, sin azar."),
    ("288 K", "Un error de unidades en la documentación",
     "La ficha declara grados Celsius para las temperaturas, pero 288 en la admisión del "
     "compresor es el día estándar ISO expresado en Kelvin. Lo dejamos anotado porque afecta a "
     "quien reutilice estos datos."),
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
st.subheader("La velocidad esconde el desgaste")
st.markdown(
    '<p class="rotulo">Relación entre el flujo de combustible y la degradación del '
    'compresor, medida de dos maneras.</p>',
    unsafe_allow_html=True,
)

# CAMBIAR: sustituyan por sus dos correlaciones reales
CORR_MEZCLADA = 0.02
CORR_A_15_NUDOS = 0.71

st.plotly_chart(barras_correlacion(CORR_MEZCLADA, CORR_A_15_NUDOS),
                use_container_width=True, config={"displayModeBar": False})
st.markdown(
    '<p class="rotulo">Pasar de 3 a 27 nudos multiplica el consumo muchas veces; la '
    'degradación completa del compresor lo mueve un pequeño porcentaje. Al mezclar los nueve '
    'regímenes, el efecto de la velocidad entierra el del desgaste. Solo comparando a igualdad '
    'de velocidad aparece la señal. Un sensor por sí solo no dice nada: hay que leerlo en su '
    'régimen de operación.</p>',
    unsafe_allow_html=True,
)

st.write("")
st.divider()


# =============================================================================
# 11. MÉTODO Y LIMITACIONES
# =============================================================================

metodo_col, limites_col = st.columns(2, gap="large")

with metodo_col:
    st.subheader("Cómo lo construimos")
    st.markdown("""
- Exploración de las 11.934 lecturas: valores faltantes, duplicados y estadística descriptiva.
- Descarte de los sensores de admisión sin variación y del par de hélice duplicado.
- Análisis de la relación entre cada sensor y la degradación, controlando por régimen de navegación.
- Un modelo de regresión por componente, compresor y turbina, entrenado en Python y servido por esta misma aplicación.
- Conversión del sobreconsumo de combustible medido en la planta a coste anual, con cotización de MGO.
""")

with limites_col:
    st.subheader("Qué no puedes concluir de esto")
    st.markdown("""
- Los datos proceden de un simulador numérico calibrado sobre plantas reales, no de sensores instalados a bordo. El modelo debe recalibrarse con mediciones reales antes de decidir una intervención.
- Los coeficientes del estimador de esta versión son de demostración.
- El modelo solo cubre el rango simulado: compresor de 1.000 a 0.950 y turbina de 1.000 a 0.975. Fuera de él no hay evidencia.
- Las horas de navegación, el precio del combustible y el número de turbinas son supuestos que introduce el usuario, no datos del conjunto.
- El coste calculado es únicamente combustible. No incluye repuestos, mano de obra ni indisponibilidad del buque.
""")

st.divider()


# =============================================================================
# 12. PIE
# =============================================================================

datos_col, codigo_col, equipo_col = st.columns(3, gap="large")

with datos_col:
    st.markdown("**Datos y referencias**")
    st.markdown(
        "[Condition Based Maintenance of Naval Propulsion Plants]"
        "(https://archive.ics.uci.edu/dataset/316/condition+based+maintenance+of+naval+propulsion+plants)  \n"
        "UCI Machine Learning Repository, conjunto 316. Licencia CC BY 4.0  \n"
        "Coraddu et al. (2016), *J. Engineering for the Maritime Environment*  \n"
        "DOE/PNNL, *O&M Best Practices Guide*, Release 3.0"
    )

with codigo_col:
    st.markdown("**Código**")
    # CAMBIAR: enlaces al repositorio
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
