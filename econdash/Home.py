from pathlib import Path

import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home", page_icon="🏠")

root_dir = Path(__file__).parent

st.image(Image.open(root_dir.joinpath("assets", "images", "sdac.png")))
