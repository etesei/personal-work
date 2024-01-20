import streamlit as st
import pandas as pd
import os
import random
import json
import numpy as np
import time

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

def initialize_gpt_wrapper():
    client = initialize_chat_gpt_client()
    file = add_file(client,'tulia.csv')
    massimo = initialize_chat_gpt_massimo_agent(client,file,"Your name is Massimo - You are an italian restaurant expert, who enjoys analyzing restaurant business data, improving the business, and talking about all things italiang restaurants")
    thread = initialize_chat_gpt_thread(client)

    return client, thread, massimo



  
if __name__  == '__main__':
    set_up_page()

    user_name = st.text_input('Enter your name!')
    
    #cached df pull
    df = get_tidy_excel_data('data/BTM SALES REPORT 11.5.2023.xlsx')
    df.to_csv('tulia.csv',index=False)

    #print the dataframe to the webpage
    st.write(df.sort_values('date',ascending=False))

    #create a timeseries plot off of a chosen metric
    metric = st.selectbox('Select a metric to view',df.columns[1:])
    p = create_time_series(df,metric)
    st.bokeh_chart(p)

    #create a text box for users to enter prompts to Massimo, the chat gpt assistant
    user_input = st.text_input('Enter a message to Massimo')

    st.image('data/massimo_headshot.png')

    #initialize refresh button
    new_query_button = st.button('Request a new response from Massimo')
    refresh_button = st.button('Refresh Massimo Responses')
    
    #initialize chat gpt functions
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = initialize_gpt_wrapper()
    
    client, thread, massimo = st.session_state.chatbot

    #create massimo placeholder
    massimo_output = st.empty()

    #submit a response, and return the latest thread output
    #if the refresh button is clicked, then return the latest thread output without rerunning a new response
    #maybe we also have a "new query" option, where we also gate that

    if new_query_button:
        message = add_message(client,thread,user_input)
        run = initialize_chat_gpt_run(client, thread, massimo)
        #add run to a session state
        st.session_state.run = run
        st.text('Preparing answer...')
        time.sleep(1)
        
        run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
                )
        
        message_thread = fetch_messages(client, thread)

        response_body = ''
        
        if message_thread: 
            message_list = message_thread.data
            #reverse the order of message_list
            message_list.reverse()
            for i in range(len(message_list)):



                if message_list[i].role == 'assistant':
                    st.markdown(f'<p style="color: green;">Massimo: {message_list[i].content[0].text.value}</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p style="color: blue;">User: {message_list[i].content[0].text.value}</p>', unsafe_allow_html=True)

            st.text(response_body)
    


    if refresh_button:
        st.session_state.run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=st.session_state.run.id
                )
        message_thread = fetch_messages(client, thread)

        response_body = ''
        
        if message_thread: 
            message_list = message_thread.data
            #reverse the order of message_list
            message_list.reverse()
            for i in range(len(message_list)):
                if message_list[i].role == 'assistant':
                    response_body = response_body + 'Massimo: ' + message_list[i].content[0].text.value + '\n'
                else:
                    response_body = response_body + 'User: ' + message_list[i].content[0].text.value + '\n'

            st.text(response_body)



    def create_matplotlib_chart():
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 20, 100)
        plt.plot(x, np.sin(x))
        plt.show()



    