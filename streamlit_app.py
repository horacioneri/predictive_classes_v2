import streamlit as st
import pandas as pd
import numpy as np
from config import page_titles
from sidebar import sidebar_config
from page_body import introduction_text, exploratory_data_analysis, data_preparation, model_training, result_analysis, model_interpretation, exercise_summary

# Navigation function with forced rerun
def change_page(delta):
    st.session_state.page = max(0, min(len(page_titles) - 1, st.session_state.page + delta))
    st.session_state.expander_open = False  # Collapse the expander when going to the next page
    st.rerun()  # Force immediate rerun to reflect the updated page state

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 0

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "treated" not in st.session_state:
    st.session_state.treated = False

if "trained" not in st.session_state:
    st.session_state.trained = False

if "predict_output" not in st.session_state:
    st.session_state.predict_output = False

current_page = st.session_state.page

# Page config
st.set_page_config(page_title='Building a ML model', page_icon='', layout = 'wide')

# Display LTP logo
st.image(image= "images/Asset 6.png", caption = "Powered by", width = 100)

if current_page > 0:
    if st.button("Restart", use_container_width=True, key=f"top_restart_{current_page}"):
        st.session_state.page = 0
        st.session_state.uploaded = False
        st.session_state.df_original = pd.DataFrame()
        st.session_state.df_treated = pd.DataFrame()
        st.rerun()

# Display title of the page
st.title(page_titles[current_page], anchor='title')

# Sidebar for accepting input parameters
sidebar_config(current_page)

if current_page == 0:
    introduction_text()

if current_page == 1:
    if not st.session_state.uploaded:
        st.write('Go back to the previous page and reupload your dataset')
    else:
        exploratory_data_analysis()

if current_page == 2:
    if not st.session_state.uploaded:
        st.write('Go back to the beginning and reupload your dataset')
    else:
        data_preparation()

if current_page == 3:
    if not st.session_state.treated:
        st.write('Go back to the previous page and prepare your dataset')
    else:
        model_training()

if current_page == 4:
    if not st.session_state.trained:
        st.write('Go back to the previous page and train your model')
    else:
        result_analysis()

if current_page == 5:
    if not st.session_state.trained:
        st.write('Go back to the model training page and train your model')
    else:
        model_interpretation()

if current_page == 6:
    if not st.session_state.trained:
        st.write('Go back to the model training page and train your model')
    else:
        exercise_summary()

# Display buttons at the end to navigate between pages
if current_page == 0:
    left, right = st.columns(2)
    if right.button("Next", use_container_width=True, key="next_0"):
        change_page(1)

elif 0 < current_page < len(page_titles)-1:
    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True, key=f"prev_{current_page}"):
        change_page(-1)
    if right.button("Next", use_container_width=True, key=f"next_{current_page}"):
        change_page(1)

elif current_page == len(page_titles)-1:
    left, right = st.columns(2)
    if left.button("Previous", use_container_width=True, key=f"prev_{current_page}"):
        change_page(-1)
# Restart if needed
else:
    st.session_state.page = 0

if current_page > 0:
    if st.button("Restart", use_container_width=True, key=f"bot_restart_{current_page}"):
        st.session_state.page = 0
        st.session_state.uploaded = False
        st.session_state.df_original = pd.DataFrame()
        st.session_state.df_treated = pd.DataFrame()
        st.rerun()

