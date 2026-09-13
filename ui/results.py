# ui/results.py

import streamlit as st
import plotly.graph_objects as go
from maintenance import estado_compresor, estado_turbina

def gauge_chart(value, min_value, max_value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        number={'valueformat': '.4f'},
        gauge={
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': '#2563eb'},
            'steps': [
                {'range': [min_value, min_value + (max_value-min_value)*0.4], 'color': '#fecaca'},
                {'range': [min_value + (max_value-min_value)*0.4, min_value + (max_value-min_value)*0.7], 'color': '#fde68a'},
                {'range': [min_value + (max_value-min_value)*0.7, max_value], 'color': '#bbf7d0'}
            ]
        }
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def component_card(title, image_path, coef_value, target_type):
    st.markdown(f'<div class="component-title">{title}</div>', unsafe_allow_html=True)

    if image_path:
        st.image(image_path, use_container_width=True)

    if coef_value is None:
        st.info(f'Aún no se ha estimado {target_type}.')
        return

    if target_type == "kMc":
        degradacion, estado = estado_compresor(coef_value)
        fig = gauge_chart(coef_value, 0.95, 1.00, "Coeficiente kMc")
    else:
        degradacion, estado = estado_turbina(coef_value)
        fig = gauge_chart(coef_value, 0.975, 1.00, "Coeficiente kMt")

    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Coeficiente estimado", f"{coef_value:.4f}")
    with c2:
        st.metric("Degradación relativa", f"{degradacion:.1f}%")

    if "CRÍTICO" in estado:
        st.error(estado)
    elif "REVISIÓN" in estado:
        st.warning(estado)
    else:
        st.success(estado)
