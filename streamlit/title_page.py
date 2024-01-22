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
    page_title="Hello",
    page_icon="👋",
)

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

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