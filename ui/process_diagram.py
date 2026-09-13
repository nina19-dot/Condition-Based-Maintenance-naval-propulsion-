import streamlit.components.v1 as components

from config import INK, HULL, DIAL, MIST, SIGNAL, STEEL


def _fmt(valor, dec=2):
    if valor is None:
        return "-"
    return f"{valor:.{dec}f}"


def diagrama_proceso_turbina(valores=None):
    if valores is None:
        valores = {}

    # =========================
    # Variables
    # =========================
    t1 = _fmt(valores.get("T1"))
    t2 = _fmt(valores.get("T2"))
    p2 = _fmt(valores.get("P2"))
    mf = _fmt(valores.get("mf"), 3)
    tic = _fmt(valores.get("TIC"))
    t48 = _fmt(valores.get("T48"))
    p48 = _fmt(valores.get("P48"))
    pexh = _fmt(valores.get("Pexh"))
    ggn = _fmt(valores.get("GGn"))
    gtn = _fmt(valores.get("GTn"))
    gtt = _fmt(valores.get("GTT"))
    lp = _fmt(valores.get("lp"), 3)
    v = _fmt(valores.get("v"), 0)

    azul_aire = "#4E9FDB"
    rojo_gases = "#E5483F"
    naranja_turbina = "#F59E0B"
    rosa_borde = "#D16BA5"

    html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: {INK};
            font-family: Arial, sans-serif;
        }}

        svg {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .titulo {{
            fill: {DIAL};
            font-size: 24px;
            font-weight: 800;
        }}

        .subtitulo {{
            fill: {DIAL};
            font-size: 17px;
            font-weight: 700;
        }}

        .texto {{
            fill: {MIST};
            font-size: 14px;
        }}

        .texto-azul {{
            fill: {azul_aire};
            font-size: 15px;
            font-weight: 700;
        }}

        .caja-titulo {{
            fill: {DIAL};
            font-size: 16px;
            font-weight: 700;
        }}

        .caja-texto {{
            fill: {MIST};
            font-size: 14px;
        }}
    </style>
    </head>

    <body>
    <svg viewBox="0 0 1400 520" xmlns="http://www.w3.org/2000/svg">

        <defs>
            <filter id="shadow">
                <feDropShadow dx="0" dy="4" stdDeviation="6"
                    flood-color="#000000" flood-opacity="0.25"/>
            </filter>
        </defs>

        <!-- ====================================== -->
        <!-- TÍTULOS DE ETAPAS -->
        <!-- ====================================== -->

        <text x="100" y="430" text-anchor="middle" class="titulo">Admisión</text>
        <text x="340" y="430" text-anchor="middle" class="titulo">Compresor</text>
        <text x="700" y="430" text-anchor="middle" class="titulo">Cámara de combustión</text>
        <text x="980" y="430" text-anchor="middle" class="titulo">Turbina</text>
        <text x="1260" y="430" text-anchor="middle" class="titulo">Escape</text>

        <!-- ====================================== -->
        <!-- FLUJO DE ADMISIÓN -->
        <!-- ====================================== -->

        <line x1="20" y1="210" x2="200" y2="210" stroke="{azul_aire}" stroke-width="4"/>
        <line x1="20" y1="240" x2="200" y2="240" stroke="{azul_aire}" stroke-width="4"/>
        <line x1="20" y1="270" x2="200" y2="270" stroke="{azul_aire}" stroke-width="4"/>
        <line x1="20" y1="300" x2="200" y2="300" stroke="{azul_aire}" stroke-width="4"/>

        <!-- Solo T1 y T2, sin recuadro -->
        <text x="80" y="185" class="texto-azul">T1 = {t1} °C</text>
        <text x="190" y="340" class="texto-azul">T2 = {t2} °C</text>

        <!-- ====================================== -->
        <!-- COMPRESOR -->
        <!-- ====================================== -->

        <polygon
            points="210,190 420,215 420,295 210,320"
            fill="{azul_aire}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <line x1="275" y1="202" x2="275" y2="308" stroke="{INK}" stroke-width="7"/>
        <line x1="340" y1="210" x2="340" y2="300" stroke="{INK}" stroke-width="7"/>

        <text x="315" y="365" text-anchor="middle" class="subtitulo">Compresor</text>
        <text x="315" y="390" text-anchor="middle" class="texto">P2 = {p2} bar</text>

        <!-- ====================================== -->
        <!-- CÁMARA DE COMBUSTIÓN -->
        <!-- ====================================== -->

        <rect
            x="560" y="190" width="140" height="130" rx="8"
            fill="{SIGNAL}" stroke="{DIAL}" stroke-width="4"
        />

        <text x="630" y="365" text-anchor="middle" class="subtitulo">Combustión</text>
        <text x="630" y="390" text-anchor="middle" class="texto">mf = {mf} kg/s | TIC = {tic} %</text>

        <!-- ====================================== -->
        <!-- TURBINA -->
        <!-- ====================================== -->

        <polygon
            points="820,205 1040,180 1040,330 820,305"
            fill="{naranja_turbina}"
            stroke="{DIAL}"
            stroke-width="4"
        />

        <line x1="900" y1="195" x2="900" y2="315" stroke="{INK}" stroke-width="7"/>
        <line x1="970" y1="188" x2="970" y2="322" stroke="{INK}" stroke-width="7"/>

        <text x="930" y="365" text-anchor="middle" class="subtitulo">Turbina</text>
        <text x="930" y="388" text-anchor="middle" class="texto">Salida turbina HP</text>
        <text x="930" y="410" text-anchor="middle" class="texto">T48 = {t48} °C | P48 = {p48} bar</text>

        <!-- ====================================== -->
        <!-- ESCAPE / GASES -->
        <!-- ====================================== -->

        <line x1="1050" y1="205" x2="1370" y2="185" stroke="{rojo_gases}" stroke-width="4"/>
        <line x1="1050" y1="240" x2="1370" y2="230" stroke="{rojo_gases}" stroke-width="4"/>
        <line x1="1050" y1="280" x2="1370" y2="290" stroke="{rojo_gases}" stroke-width="4"/>
        <line x1="1050" y1="315" x2="1370" y2="345" stroke="{rojo_gases}" stroke-width="4"/>

        <!-- ====================================== -->
        <!-- RECUADROS DE TELEMETRÍA -->
        <!-- ====================================== -->

        <!-- Operación -->
        <g filter="url(#shadow)">
            <rect
                x="30" y="25" width="180" height="95" rx="10"
                fill="{HULL}" stroke="{rosa_borde}" stroke-width="3"
            />
            <text x="50" y="55" class="caja-titulo">Operación</text>
            <text x="50" y="82" class="caja-texto">lp = {lp}</text>
            <text x="50" y="106" class="caja-texto">v = {v} knots</text>
        </g>

        <!-- Eje / generador -->
        <g filter="url(#shadow)">
            <rect
                x="830" y="20" width="230" height="110" rx="10"
                fill="{HULL}" stroke="{rosa_borde}" stroke-width="3"
            />
            <text x="850" y="50" class="caja-titulo">Eje / generador</text>
            <text x="850" y="77" class="caja-texto">GGn = {ggn} rpm</text>
            <text x="850" y="101" class="caja-texto">GTn = {gtn} rpm</text>
            <text x="850" y="125" class="caja-texto">GTT = {gtt} kN m</text>
        </g>

        <!-- Escape -->
        <g filter="url(#shadow)">
            <rect
                x="1130" y="25" width="180" height="90" rx="10"
                fill="{HULL}" stroke="{rosa_borde}" stroke-width="3"
            />
            <text x="1150" y="55" class="caja-titulo">Escape</text>
            <text x="1150" y="85" class="caja-texto">Pexh = {pexh} bar</text>
        </g>

    </svg>
    </body>
    </html>
    """

    components.html(
        html,
        height=520,
        scrolling=False
    )
