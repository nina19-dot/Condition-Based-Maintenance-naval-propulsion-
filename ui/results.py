# ui/results.py

import streamlit as st

from maintenance import (
    estado_compresor,
    estado_turbina
)


def bloque_compresor(kMc=None):

    st.markdown(
        '## Compresor'
    )

    if kMc is None:

        st.info(
            'Presiona el botón para '
            'estimar kMc.'
        )

        return

    degradacion, estado = (
        estado_compresor(kMc)
    )

    st.metric(
        'kMc estimado',
        f'{kMc:.4f}'
    )

    st.metric(
        'Degradación relativa',
        f'{degradacion:.1f}%'
    )

    if degradacion >= 80:

        st.error(estado)

    elif degradacion >= 60:

        st.warning(estado)

    else:

        st.success(estado)


def bloque_turbina(kMt=None):

    st.markdown(
        '## Turbina'
    )

    if kMt is None:

        st.info(
            'Presiona el botón para '
            'estimar kMt.'
        )

        return

    degradacion, estado = (
        estado_turbina(kMt)
    )

    st.metric(
        'kMt estimado',
        f'{kMt:.4f}'
    )

    st.metric(
        'Degradación relativa',
        f'{degradacion:.1f}%'
    )

    if degradacion >= 80:

        st.error(estado)

    elif degradacion >= 60:

        st.warning(estado)

    else:

        st.success(estado)
