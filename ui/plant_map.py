# ui/plant_map.py

import streamlit.components.v1 as components


def mostrar_planta(
    componente=None
):

    color_compresor = (
        '#ff3b30'
        if componente in [
            'compressor',
            'both'
        ]
        else '#2d3748'
    )

    color_turbina = (
        '#ff9500'
        if componente in [
            'turbine',
            'both'
        ]
        else '#2d3748'
    )

    html = f"""
    <div style="
        background:#0d1117;
        padding:25px;
        border-radius:12px;
        color:white;
        font-family:Arial;
    ">

        <h3 style="
            text-align:center;
        ">
            CODLAG Propulsion Plant
        </h3>

        <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            gap:12px;
            margin-top:25px;
        ">

            <div style="
                padding:18px;
                background:#1f2937;
                border-radius:8px;
            ">
                Gas Turbine
            </div>

            <div>→</div>

            <div style="
                padding:18px;
                background:{color_compresor};
                border-radius:8px;
                font-weight:bold;
            ">
                COMPRESSOR
            </div>

            <div>→</div>

            <div style="
                padding:18px;
                background:#374151;
                border-radius:8px;
            ">
                COMBUSTOR
            </div>

            <div>→</div>

            <div style="
                padding:18px;
                background:{color_turbina};
                border-radius:8px;
                font-weight:bold;
            ">
                TURBINE
            </div>

            <div>→</div>

            <div style="
                padding:18px;
                background:#1f2937;
                border-radius:8px;
            ">
                Gearbox
            </div>

            <div>→</div>

            <div style="
                padding:18px;
                background:#1f2937;
                border-radius:8px;
            ">
                Propeller
            </div>

        </div>

        <div style="
            display:flex;
            justify-content:center;
            margin-top:30px;
            gap:12px;
        ">

            <div style="
                padding:14px;
                background:#1f2937;
                border-radius:8px;
            ">
                Diesel Generator
            </div>

            <div>→</div>

            <div style="
                padding:14px;
                background:#1f2937;
                border-radius:8px;
            ">
                Electric Motor
            </div>

            <div>→</div>

            <div style="
                padding:14px;
                background:#1f2937;
                border-radius:8px;
            ">
                Gearbox
            </div>

        </div>

    </div>
    """

    components.html(
        html,
        height=270
    )
