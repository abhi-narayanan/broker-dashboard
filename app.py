import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

year_filter_df = class_stats[class_stats['Year'] == year]

business_class = year_filter_df.groupby('Class of Business').sum(numeric_only=True)
business_class = business_class.reset_index()

# Unique Business classesi
unique_classes = class_stats['Class of Business'].unique().tolist()

# fig_1 = go.Figure()
# fig_1.add_trace(go.Bar(x=business_class['Class of Business'],
#     y=business_class['GWP '],
#     name='GWP',
#     marker_color='indianred'))

# fig_1.add_trace(go.Bar(x=business_class['Class of Business'],
#     y=business_class['Earned Premium'],
#     name='Earned Premium',
#     marker_color='MediumPurple'))

# fig_1.add_trace(go.Bar(x=business_class['Class of Business'],
#     y=business_class['Business Plan'],
#     name='Business Plan',
#     marker_color='lightsalmon'))

fig_1 = px.bar(business_class, x=business_class['Class of Business'], y=["Business Plan", 'Earned Premium', 'GWP '], title=f"Business Class Analysis", barmode='group', width=600, height=400)

business_class = st.radio(label='Select Class of Business', options=unique_classes)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig_1)

with col4:

    dataframe = year_filter_df[year_filter_df['Class of Business']==business_class]

    fig_2 = px.bar(dataframe, x="ClassType", y=["Business Plan", 'Earned Premium', 'GWP '], title=f"{business_class} Analysis", barmode='group', width=600, height=400)

    st.plotly_chart(fig_2)