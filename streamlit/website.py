import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the web app
st.title('Rustic Italian Restaurant Dashboard')

data = pd.read_csv('data/output.csv')

# Display the data on the website
st.write(data)

# Create a bar chart from the data
chart_data = data[data['category']=='total_net_sales'].groupby('date').value.sum().reset_index()

print(chart_data)
fig, ax = plt.subplots()
chart_data.plot(kind='bar', ax=ax)
ax.set_xlabel('date')
ax.set_ylabel('sales')

st.pyplot(fig)





# # A simple textt
