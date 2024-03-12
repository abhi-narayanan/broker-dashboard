import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Set the app title and header
st.set_page_config(page_title="Broker Dashboard", layout="wide")
st.header('Broker Dashboard')

# Read data from given Excel file
broker_stats = pd.read_excel('2024 Dashboard Data.xlsx', sheet_name='Broker stats', dtype={'Year': str})
class_stats = pd.read_excel('2024 Dashboard Data.xlsx', sheet_name='Class stats', dtype={'Year': str})

# Get the unique years from dataframe
unique_years = broker_stats.Year.unique().tolist()
year = st.selectbox('Select a year:', options=unique_years)

# Get the unique Market Type from dataframe
market_type = broker_stats['Market Type'].unique().tolist()
# Add Combined to list
market_type.append('Combined')
category = st.selectbox('Select a category:', market_type)

# Filter dataframe based on selections
if category == 'Combined':
    req_df = broker_stats[broker_stats['Year'] == year]
    req_df = req_df.groupby(by=['Broker Name']).sum(numeric_only=True).head(10)
    req_df = req_df.reset_index()

else:
    req_df = broker_stats[(broker_stats['Year'] == year) & (broker_stats['Market Type'] == category)].sort_values(by='GWP',
                                                                                        ascending=False).head(10)
    req_df = req_df.reset_index(drop=True)
    
st.subheader('"Top 10 Brokers" performance tables', divider='rainbow')
# Create column for difference in Planned and Actual GWP
req_df['GWP Deficit (%)'] = (req_df['GWP'] - req_df['Planned GWP'])*100/req_df['Planned GWP']
req_df = req_df.round()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=req_df['Broker Name'],
    y=req_df['GWP'],
    name='GWP',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=req_df['Broker Name'],
    y=req_df['Planned GWP'],
    name='Planned GWP',
    marker_color='lightsalmon'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-45)

col1, col2 = st.columns(2)
with col1:
    st.dataframe(req_df)
with col2:
    st.plotly_chart(fig)

# ----------------------------------------END OF SECTION-------------------------------------------------------------
    
