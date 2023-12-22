import streamlit as st
import pandas as pd
import bokeh
import os
import random
import json
import numpy as np
import urllib.parse


# from openai import OpenAI
# client = OpenAI()



def set_up_page():
    """
    creates the information page up front
    """
  
    st.set_page_config(
     page_title="Ex-stream-ly Cool App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )
    st.title('_:green[Bonjourno]_, Welcome to the Campaña Group Performance Hub :sunglasses:')

    st.title('This Site is a place to come view latest performance, predictions, and reviews. Interact with performance data, ask it questions, and even chat with Massimo - your personal AI assistant who is an expert in all things Naples, Tulia, and Italy')

if __name__  == '__main__':
    set_up_page()







# data = pd.read_csv('/Users/evan.tesei/personal-work/data/output.csv')

# st.write(data)

# from bokeh.plotting import figure

# # Create a Bokeh figure



# p = figure(
#     title='Simple Bokeh Example',
#     x_axis_label='x',
#     y_axis_label='y'
# )

# # Add a line to the figure
# p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], legend_label='Trend', line_width=2)

# # Display the figure in Streamlit
# st.bokeh_chart(p)