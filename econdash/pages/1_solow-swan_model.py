import streamlit as st

import plotly.express as px

import pandas as pd
import numpy as np


st.set_page_config(page_title="Solow-Swan Model", page_icon="📈", layout="wide")

col1, col2 = st.columns([1, 2], gap="medium")

with col1:
    st.write("$$ Y(t) = K(t)^\\alpha(A(t)L(t))^{1-\\alpha} $$")
    lat = st.slider('"A" Labor-Augmenting Technology', min_value=1.0, max_value=5.0, value=1.2, step=0.1)
    alpha = st.slider('"$\\alpha$"', min_value=0.0, max_value=1.0, value=0.3, step=0.01)

with col2:
    capital = np.arange(0, 50, 0.01)
    output = lat**(1-alpha) * capital**(alpha)
    depreciation = 0.2 * capital
    solow_df = pd.DataFrame([capital, output, depreciation], index=["Capital per Capita `k(t)`", "Output per Capita `y(t)`", "Depreciation per Capita"]).T
    fig = px.line(solow_df, x="Capital per Capita `k(t)`", y=["Output per Capita `y(t)`", "Depreciation"])
    fig.update_yaxes(title={"text": "Output per Capita"})
    st.plotly_chart(fig)