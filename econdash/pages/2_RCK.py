import streamlit as st
import plotly.express as px

import pandas as pd
import numpy as np

import plotly.figure_factory as ff
from math import exp
import plotly.graph_objects as go

def next_k_c(k, c, alpha=0.33, delta=0.05, g = 0.03, n = 0.02, beta = 0.95, theta = 1.5):
    k_n = ((k ** alpha) + k * exp(- delta) - c ) * exp(-g-n)
    c_n = ((((alpha * (k_n ** (alpha-1))) + exp(- delta)) * beta * exp(-g*theta)) **(1/theta)) * c
    return np.real(k_n), np.real(c_n)

def arrow(k, c, alpha=0.33, delta=0.05, g = 0.03, n = 0.02, beta = 0.95, theta = 1.5):
    k_n, c_n =  next_k_c(k,c, alpha, delta, g, n, beta, theta)
    return  (k_n - k), (c_n - c)

def c_cns(k, alpha=0.33, delta=0.05, g = 0.03, n = 0.02):
    return (k ** alpha) + k * (exp(- delta) - exp(g+n))

def k_cns(g = 0.03, theta = 1.5, beta = 0.95, alpha=0.3, delta=0.05):
    return ((exp(g * theta) - beta * exp(-delta))/(alpha*beta)) ** (1/(alpha-1))   

x_end = 30
y_end = 1.3

k_ax = np.linspace(0.1, x_end, 30)
c_ax = np.linspace(0, y_end, 12)

k, c = np.meshgrid(k_ax, c_ax)

st.set_page_config(page_title="RCK", page_icon="📈", layout="wide")
col1, col2 = st.columns([1, 3], gap="medium")

def reset_sliders():
    st.session_state["theta_slider"] = 1.5
    st.session_state["n_slider"] = 0.02
    st.session_state["delta_slider"] = 0.05
    st.session_state["alpha_slider"] = 0.3
    st.session_state["beta_slider"] = 0.95
    st.session_state["g_slider"] = 0.03

    
with col1:
    st.write("$$ \\frac{ \dot{k}}{k} = \\frac{k ^ \\alpha - c}{k} - (\\delta + g + n) $$")
    st.write("$$ \\frac{ \dot{c}}{c} = \\frac{1}{\\sigma} (\\alpha k^{\\alpha -1} - \\delta - \\rho - \\sigma g) $$")
        
    theta = st.slider('$ \\sigma $', min_value=0.3, max_value=2.0, value=1.5, step=0.1, key="theta_slider")
    n = st.slider('$ n $', min_value=0.01, max_value=0.06, value=0.02, step=0.01, key="n_slider")
    delta = st.slider('$ \\delta $', min_value=0.0, max_value=0.1, value=0.05, step=0.01, key="delta_slider")
    alpha = st.slider('$ \\alpha $', min_value=0.1, max_value=0.6, value=0.3, step=0.1, key="alpha_slider")
    beta = st.slider('$ \\rho $', min_value=0.7, max_value=1.0, value=0.95, step=0.05, key="beta_slider")
    g = st.slider('$ g $', min_value=0.01, max_value=0.06, value=0.03, step=0.01, key="g_slider")
    st.button("RESET", on_click=reset_sliders)



with col2:
    k_dif, c_dif = arrow(k, c, alpha, delta, g, n, beta, theta)

    fig = ff.create_quiver(k, c, k_dif, c_dif, scale=.75, line_width=1, arrow_scale=.05)

    fig.add_shape(
        type="line",
        x0=k_cns(g, theta, beta, alpha, delta), y0=0,
        x1=k_cns(g, theta, beta, alpha, delta), y1=y_end,
        line=dict(color="#3EB489", width=3))
        
    fig.add_trace(go.Scatter(x=k_ax, y=c_cns(k_ax, alpha, delta, g, n) , mode='lines', line=dict(color="#DA70D6", width=3)))
    fig.update_layout(width=900, height=700) 
    fig.update_layout(yaxis_range=[0, 1.3])
    fig.update_layout(xaxis_range=[0, 30])
    fig.update_yaxes(title={"text": "c(t)"})
    fig.update_xaxes(title={"text": "k(t)"})
    st.plotly_chart(fig)
    

