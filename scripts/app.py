import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from datetime import datetime
from datetime import time


icon = Image.open("/Users/anandsaran/Documents/Code/Projects/Streamlit Applications/StreamGenie/media/2.png")

st.set_page_config(
     page_title="StreamGenie",
     page_icon=icon,
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/anandsarank',
     }
 )



#st.subheader("Master Streaming")

logo_image = Image.open("/Users/anandsaran/Documents/Code/Projects/Streamlit Applications/StreamGenie/media/1-nobg.png")


#creating required datasets
x, net, pri, dis, y = st.columns(5)

header_logo = Image.open("/Users/anandsaran/Documents/Code/Projects/Streamlit Applications/StreamGenie/media/headerimage.png")

st.image(header_logo, use_column_width = True)


data = pd.read_csv("/Users/anandsaran/Documents/Code/Projects/Streamlit Applications/StreamGenie/data/ott_data.csv")

release_years = data['release_year'].unique().tolist()
ratings = data['rating'].unique().tolist()

#[0:"Movie", 1:"TV Show"]
selected_types = []
search = False

with st.container():

    s1, s2,s3 = st.columns(3)
    search_input = s2.text_input('')
    s3.write("")
    s3.write("")
    if s3.button("Search"):
        search = True

st.sidebar.image(logo_image, use_column_width=True)


release_years = st.sidebar.slider('Release Year',
                    min_value= min(release_years),
                    max_value= max(release_years),
                    value=(min(release_years),max(release_years)))
movies = st.sidebar.checkbox('Movies')
if movies:
    selected_types.append("Movie")
tv = st.sidebar.checkbox("TV Shows")
if tv:
    selected_types.append("TV Show")

rating_selection = st.sidebar.multiselect('Rating', ratings, default=ratings)


#filtered conditions
conditions = (data['release_year'].between(*release_years)) & (data['type'].isin(selected_types)) & (data['rating'].isin(rating_selection))
filtered_data = data[conditions]

#filtering using words
if search:
    search_condition = (filtered_data.title.str.contains(search_input, case=False)) | (filtered_data.director.str.contains(search_input, case=False)) | (filtered_data.cast.str.contains(search_input, case=False)) | (filtered_data.country.str.contains(search_input, case=False))
    filtered_data = filtered_data[search_condition]

#dispay data
#Renaming columns in the output dataframe
filtered_data.columns = ['Index','Show Id', 'Type', 'Title', 'Director', 'Cast', 'Country', 'Release Year', 'Rating', 'Duration', 'Listed In', 'Description', 'Platform']

number_of_result = filtered_data.shape[0]
st.markdown(f'*Available Results: {number_of_result}*')
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
st.dataframe(filtered_data[['Type', 'Title', 'Director', 'Release Year', 'Rating', 'Duration', 'Platform']].sort_values(by='Release Year', ascending=False))
