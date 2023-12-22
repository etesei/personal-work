import streamlit as st
import pandas as pd
import os
import random
import json
import numpy as np
import urllib.parse
from io import BytesIO

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

from openai import OpenAI


#these functions are to initialize a chat gpt agent to talk to the user on the page
#the file that we identity we will send to the agent
#you can save an assistant, to start though we will just recreate it every time

#then we need a chatbox for users to write in, and a chat box for the agent to write in


def initialize_chat_gpt_client():

    client = OpenAI(api_key= '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')

    return client

def add_file(client, path):
    
    file = client.files.create(
    file=open(path,'rb'),
    purpose='assistants'
    )

    return file
 

def initialize_chat_gpt_massimo_agent(client,file,prompt):
    """
    initializes the chat gpt agent
    """
    assistant = client.beta.assistants.create(
    instructions=prompt,
    model="gpt-4-1106-preview",
    tools=[{"type": "code_interpreter"}],
    file_ids=[file.id]
    )

    return assistant


def initialize_chat_gpt_thread(client):
    thread = client.beta.threads.create()
    
    return thread

def initialize_chat_gpt_run(client, thread, assistant):
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Have a fun time"
    )
    return run

def add_message(client,thread, content):
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=content
)
    return message

def fetch_messages(client,thread):
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
)
    return messages
    
