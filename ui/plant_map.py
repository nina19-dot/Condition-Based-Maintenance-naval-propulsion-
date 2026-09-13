# ui/plant_map.py

import streamlit.components.v1 as components

def render_plant_map(active_component=None):
    comp_color = "#ef4444" if active_component in ["compressor", "both"] else "#60a5fa"
    turb_color = "#f97316" if active_component in ["turbine", "both"] else "#60a5fa"

    html = f"""
    <div style="
        background:white;
        border-radius:18px;
        padding:16px;
        box-shadow:0 4px 16px rgba(0,0,0,0.08);
        border:1px solid #e2e8f0;
    ">
        <div style="font-family:Arial; font-weight:700; color:#0f172a; margin-bottom:10px;">
            Esquema general de la planta CODLAG
        </div>

        <svg width="100%" height="320" viewBox="0 0 900 320" xmlns="http://www.w3.org/2000/svg">

            <!-- Líneas principales -->
            <line x1="50" y1="90" x2="720" y2="90" stroke="black" stroke-width="6"/>
            <line x1="50" y1="240" x2="720" y2="240" stroke="black" stroke-width="6"/>

            <!-- Hélices -->
            <circle cx="30" cy="90" r="10" stroke="black" stroke-width="4" fill="none"/>
            <line x1="30" y1="100" x2="30" y2="120" stroke="black" stroke-width="4"/>
            <line x1="30" y1="80" x2="20" y2="60" stroke="black" stroke-width="4"/>
            <line x1="30" y1="80" x2="40" y2="60" stroke="black" stroke-width="4"/>

            <circle cx="30" cy="240" r="10" stroke="black" stroke-width="4" fill="none"/>
            <line x1="30" y1="250" x2="30" y2="270" stroke="black" stroke-width="4"/>
            <line x1="30" y1="230" x2="20" y2="210" stroke="black" stroke-width="4"/>
            <line x1="30" y1="230" x2="40" y2="210" stroke="black" stroke-width="4"/>

            <!-- Generadores diésel -->
            <rect x="160" y="30" width="150" height="48" fill="#9333ea" stroke="black" stroke-width="4"/>
            <rect x="320" y="35" width="40" height="38" fill="#d4a017" stroke="black" stroke-width="4"/>
            <text x="175" y="22" font-size="18" font-family="Arial">Generadores diésel</text>

            <rect x="160" y="190" width="150" height="48" fill="#9333ea" stroke="black" stroke-width="4"/>
            <rect x="320" y="195" width="40" height="38" fill="#d4a017" stroke="black" stroke-width="4"/>

            <rect x="160" y="245" width="150" height="48" fill="#9333ea" stroke="black" stroke-width="4"/>
            <rect x="320" y="250" width="40" height="38" fill="#d4a017" stroke="black" stroke-width="4"/>

            <!-- Motores eléctricos -->
            <rect x="680" y="30" width="100" height="58" fill="#c49c1a" stroke="black" stroke-width="4"/>
            <text x="655" y="20" font-size="18" font-family="Arial">Motores eléctricos</text>

            <rect x="680" y="210" width="100" height="58" fill="#c49c1a" stroke="black" stroke-width="4"/>

            <!-- Cajas -->
            <rect x="590" y="25" width="28" height="120" fill="#86efac" stroke="black" stroke-width="4"/>
            <rect x="590" y="175" width="28" height="120" fill="#86efac" stroke="black" stroke-width="4"/>
            <text x="570" y="18" font-size="18" font-family="Arial">Cajas</text>

            <!-- Embragues -->
            <rect x="520" y="85" width="38" height="30" fill="#fecaca" stroke="black" stroke-width="4"/>
            <circle cx="539" cy="100" r="10" fill="none" stroke="red" stroke-width="4"/>

            <rect x="520" y="185" width="38" height="30" fill="#fecaca" stroke="black" stroke-width="4"/>
            <circle cx="539" cy="200" r="10" fill="none" stroke="red" stroke-width="4"/>

            <text x="505" y="145" font-size="18" font-family="Arial">Embragues</text>

            <!-- Turbina de gas -->
            <rect x="160" y="95" width="210" height="85" fill="none" stroke="{comp_color}" stroke-width="0"/>
            <polygon points="170,110 250,130 170,150" fill="{comp_color}" stroke="black" stroke-width="4"/>
            <rect x="250" y="115" width="50" height="30" fill="#60a5fa" stroke="black" stroke-width="4"/>
            <polygon points="300,110 360,130 300,150" fill="{turb_color}" stroke="black" stroke-width="4"/>

            <text x="190" y="95" font-size="18" font-family="Arial">Turbina de gas</text>

            <!-- Etiquetas internas -->
            <text x="185" y="168" font-size="15" font-family="Arial" fill="#0f172a">Compresor</text>
            <text x="303" y="168" font-size="15" font-family="Arial" fill="#0f172a">Turbina</text>

            <!-- Uniones -->
            <line x1="370" y1="130" x2="490" y2="130" stroke="black" stroke-width="6"/>
            <line x1="370" y1="130" x2="490" y2="200" stroke="black" stroke-width="6"/>

            <line x1="618" y1="55" x2="680" y2="55" stroke="black" stroke-width="6"/>
            <line x1="618" y1="240" x2="680" y2="240" stroke="black" stroke-width="6"/>
        </svg>
    </div>
    """
    components.html(html, height=360)
