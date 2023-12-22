import streamlit as st
import pandas as pd


data = pd.read_csv('/Users/evan.tesei/personal-work/data/output.csv')

st.write(data)

from bokeh.plotting import figure

# Create a Bokeh figure



p = figure(
    title='Simple Bokeh Example',
    x_axis_label='x',
    y_axis_label='y'
)

# Add a line to the figure
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], legend_label='Trend', line_width=2)

# Display the figure in Streamlit
st.bokeh_chart(p)