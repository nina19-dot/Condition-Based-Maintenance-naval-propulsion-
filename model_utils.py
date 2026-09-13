# model_utils.py

import pandas as pd
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from config import FEATURES


@st.cache_resource
def entrenar_modelos(data):

    # Variables de entrada
    X = data[FEATURES]

    # =============================
    # MODELO kMc
    # =============================

    y_kMc = data['kMc']

    X_train, X_test, y_train_kMc, y_test_kMc = (
        train_test_split(
            X,
            y_kMc,
            test_size=0.20,
            random_state=42
        )
    )

    rf_kMc = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    rf_kMc.fit(
        X_train,
        y_train_kMc
    )

    # =============================
    # MODELO kMt
    # =============================

    y_kMt = data['kMt']

    (
        X_train_mt,
        X_test_mt,
        y_train_kMt,
        y_test_kMt
    ) = train_test_split(
        X,
        y_kMt,
        test_size=0.20,
        random_state=42
    )

    rf_kMt = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    rf_kMt.fit(
        X_train_mt,
        y_train_kMt
    )

    return rf_kMc, rf_kMt
