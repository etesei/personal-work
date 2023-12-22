import streamlit as st
import pandas as pd
import os
import random
import json
import numpy as np
import urllib.parse

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, CustomJS, Slider, Div, RangeSlider, Legend, Span, HoverTool
from bokeh.plotting import figure, output_file, show, save
from bokeh.embed import *
from bokeh.models.widgets import DateSlider
from bokeh.resources import CDN
from bokeh.palettes import inferno, Category20, all_palettes
from bokeh.transform import dodge
from bokeh.palettes import Category20 as palette

from data_api import get_file_paths, get_tidy_excel_data
from chat_gpt import *


# from openai import OpenAI
# client = OpenAI()

#code this as a template for all of the restaurants

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
    st.title('Osteria Tulia Section')

def create_time_series(df,
                       metric):
    
    cds = ColumnDataSource(df[['date',metric]])
    p = figure(plot_width=1500, plot_height=750, x_axis_type="datetime", title=f"Daily {metric}")
    p.line(x='date', y=metric, source=cds)
    
    hover = HoverTool(tooltips=[
        (metric,f'@{metric}'),
        ('Date', '@date{%F}'),
        ('Variance Explanation', '@explanation_of_sales_variance_plus_minus_2percent')
    ],
    formatters={'@date': 'datetime'}
    )
    p.add_tools(hover)
    p.legend.click_policy="mute"

    return p



  
if __name__  == '__main__':
    set_up_page()

    user_name = st.text_input('Enter your name!')
    
    #cached df pull
    df = get_tidy_excel_data('../data/BTM SALES REPORT 11.5.2023.xlsx')
    df.to_csv('tulia.csv',index=False)

    #print the dataframe to the webpage
    st.write(df.sort_values('date',ascending=False))

    #create a timeseries plot off of a chosen metric
    metric = st.selectbox('Select a metric to view',df.columns[1:])
    p = create_time_series(df,metric)
    st.bokeh_chart(p)

    #create a text box for users to enter prompts to Massimo, the chat gpt assistant
    user_input = st.text_input('Enter a message to Massimo')

    st.image('../data/massimo_headshot.png')

    #initialize chat gpt functions
    client = initialize_chat_gpt_client()
    file = add_file(client,'tulia.csv')
    massimo = initialize_chat_gpt_massimo_agent(client,file,"Your name is Massimo - You are an italian restaurant expert, who enjoys analyzing restaurant business data, improving the business, and talking about all things italiang restaurants")
    thread = initialize_chat_gpt_thread(client)
    #create massimo placeholder
    massimo_output = st.empty()

    if user_input!='Enter a message to Massimo':

    #if new text is entered then run add_message and fetch_messages
        message = add_message(client,thread,user_input)
        run = initialize_chat_gpt_run(client,thread,massimo)
        message_thread = fetch_messages(client,thread)

        massimo_output.text(message_thread.data[0].content[1].text.value)
    else:
        'Hi I am Massimo! Enter a message above to chat with me!'
       




    