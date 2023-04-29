import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

    
df = px.data.gapminder()
st.set_page_config(page_title="Gap Minder", page_icon="📈", layout="wide")

fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
        size="pop", color="continent", hover_name="country",
        log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

fig.update_layout(width=900, height=600) 

st.plotly_chart(fig)
    
