import streamlit as st
import plotly.express as px
import time


import pandas as pd
import numpy as np

import plotly.graph_objs as go
from plotly.subplots import make_subplots

L_end = 10
Y_end = 5
K_end = 1.5
C_end = 5

L = np.linspace(0.1, L_end, 50)
K = np.linspace(0.1, K_end, 50)
sigma = 1

fig = make_subplots(rows=2, cols=2, vertical_spacing=0, horizontal_spacing=0, shared_xaxes=True, shared_yaxes=True)

def Y1_L(L, alpha):
    Y1 = A1 * L ** (1-alpha)
    return Y1

def C1_L(L, alpha, theta, epsilon, sigma=1):
    temp = (A1 * (1-alpha)/theta)*(L ** (-alpha-epsilon))
    C1 = temp ** (1/sigma)
    return C1

def C1_K(K, alpha, beta, sigma=1):
    temp = (beta * alpha) * (K ** (alpha - 1 - (alpha * sigma)))
    C1 = temp ** (-1/sigma)
    return C1

def Y1_K(K, alpha, beta, sigma=1):
    C1 = C1_K(K, alpha, beta, sigma)
    Y1 = C1 + K
    return Y1

def L_bar(alpha, beta, epsilon, theta):
    temp = ((1-alpha)/theta) * (beta * alpha + 1)
    L_bar_ = temp ** (1/(1+epsilon))
    return L_bar_

def K_bar(alpha, beta, epsilon, theta):
    L_bar_ = L_bar(alpha, beta, epsilon, theta)
    K_bar_ = (L_bar_ ** (-alpha-epsilon)) * (A1 * beta * alpha * (1-alpha)) / theta
    return K_bar_

def C1_bar(alpha, beta, epsilon, theta):
    L_bar_ = L_bar(alpha, beta, epsilon, theta)
    C1_bar_ = C1_L(L_bar_, alpha=alpha, theta=theta, epsilon=epsilon)
    return C1_bar_

def Y1_bar(alpha, beta, epsilon, theta):
    L_bar_ = L_bar(alpha, beta, epsilon, theta)
    Y1_bar_ = Y1_L(L_bar_, alpha=alpha)
    return Y1_bar_    
    
st.set_page_config(page_title="RBC", page_icon="📈", layout="wide")
col1, col2 = st.columns([2, 7], gap="medium")

def reset_sliders():
    st.session_state["alpha_slider"] = 0.3
    st.session_state["beta_slider"] = 0.9
    st.session_state["theta_slider"] = 0.5
    st.session_state["epsilon_slider"] = 1.5
    st.session_state["A_slider"] = 1
    
with col1:        
    alpha = st.slider('$ \\alpha $', min_value=0.1, max_value=0.8, value=0.3, step=0.1, key="alpha_slider")
    theta = st.slider('$ \\theta $', min_value=0.1, max_value=1.0, value=0.5, step=0.1, key="theta_slider")
    epsilon = st.slider('$ \\epsilon $', min_value=0.3, max_value=2.0, value=1.5, step=0.1, key="epsilon_slider")
    beta = st.slider('$ \\beta $', min_value=0.3, max_value=1.0, value=0.9, step=0.1, key="beta_slider")
    A1 = st.slider('$ A_1 $', min_value=0.5, max_value=1.5, value=1.0, step=0.1, key="A_slider")
    st.button("RESET", on_click=reset_sliders)
    

with col2:    
    chart_line = dict(color="orange", width=3)
    # add traces to each subplot
    fig.add_trace(go.Scatter(x=L, y=Y1_L(L, alpha), mode='lines', line=chart_line, showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=K, y=Y1_K(K, alpha, beta), mode='lines', line=chart_line, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=L, y=C1_L(L, alpha, theta, epsilon), mode='lines', line=chart_line, showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=K, y=C1_K(K, alpha, beta), mode='lines', line=chart_line, showlegend=False), row=2, col=2)

    # update layout and axis properties
    fig.update_layout(height=600, width=800 , title_text="RBC Charts")
    fig.update_yaxes(range=[0, Y_end], autorange=False, title_text="GDP-Y1", row=1, col=1)
    fig.update_yaxes(range=[0, C_end], autorange=False, title_text="Consumption-c1", row=2, col=1)
    fig.update_yaxes(range=[0, Y_end], autorange=False, row=1, col=2)
    fig.update_yaxes(range=[0, C_end], autorange=False, row=2, col=2)
    fig.update_xaxes(title_text="Employment-L", row=2, col=1, mirror=True)
    fig.update_xaxes(title_text="Investment-K", row=2, col=2)

    equilibrium_line = dict(color="palegreen", width=3, dash='dash')
    
    # chart 1
    fig.add_shape(type="line", line=equilibrium_line, row=1, col=1,
        x0=L_bar(alpha, beta, epsilon, theta), y0=0,
        x1=L_bar(alpha, beta, epsilon, theta), y1=Y1_bar(alpha, beta, epsilon, theta))
    
    fig.add_shape(type="line", line=equilibrium_line, row=1, col=1,
        x0=L_bar(alpha, beta, epsilon, theta), y0=Y1_bar(alpha, beta, epsilon, theta),
        x1=L_end, y1=Y1_bar(alpha, beta, epsilon, theta))
    
    # chart 2
    fig.add_shape(type="line", line=equilibrium_line, row=2, col=1,
        x0=L_bar(alpha, beta, epsilon, theta), y0=C1_bar(alpha, beta, epsilon, theta),
        x1=L_bar(alpha, beta, epsilon, theta), y1=Y_end)
    
    fig.add_shape(type="line", line=equilibrium_line, row=2, col=1,
        x0=L_bar(alpha, beta, epsilon, theta), y0=C1_bar(alpha, beta, epsilon, theta),
        x1=L_end, y1=C1_bar(alpha, beta, epsilon, theta))
    
    # chart 3
    fig.add_shape(type="line", line=equilibrium_line, row=2, col=2,
        x0=K_bar(alpha, beta, epsilon, theta), y0=C1_bar(alpha, beta, epsilon, theta),
        x1=K_bar(alpha, beta, epsilon, theta), y1=Y_end)
    
    fig.add_shape(type="line", line=equilibrium_line, row=2, col=2,
        x0=0, y0=C1_bar(alpha, beta, epsilon, theta),
        x1=K_bar(alpha, beta, epsilon, theta), y1=C1_bar(alpha, beta, epsilon, theta))

    # chart 4
    fig.add_shape(type="line", line=equilibrium_line, row=1, col=2,
        x0=K_bar(alpha, beta, epsilon, theta), y0=0,
        x1=K_bar(alpha, beta, epsilon, theta), y1=Y1_bar(alpha, beta, epsilon, theta))
    
    fig.add_shape(type="line", line=equilibrium_line, row=1, col=2,
        x0=0, y0=Y1_bar(alpha, beta, epsilon, theta),
        x1=K_bar(alpha, beta, epsilon, theta), y1=Y1_bar(alpha, beta, epsilon, theta))        
    
    # fig.update_layout(width=900, height=700) 
    st.plotly_chart(fig)
    
    st.write("$$ Y_1 = A_1 L^{1-\\alpha}$$ ______________________________________ $$Y_1 = \\frac {K} {\\beta \\alpha} + K $$")
    st.write("$$ \\frac {\\theta L^\\epsilon} {c_1^{-1}} = A_1 (1-\\alpha) L^{-\\alpha}$$ _______________________________ $$ c_1 = \\frac {K} {\\beta \\alpha} $$")
    

