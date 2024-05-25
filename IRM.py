import streamlit as st
import pandas as pd
from PIL import Image
#import folium
#from folium.plugins import MarkerCluster
#from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.graph_objects as go


st.set_page_config(page_title= "IRM",  layout= "wide", initial_sidebar_state= "expanded",
                   menu_items={'About': """# This page is created by *Gnanambiagai"""})


with st.sidebar:
    selected = option_menu(None, ["Home","Data Visualization","Geo Visualization"],
                icons=["house","pie-chart-fill","globe-americas"],
                default_index=0,
                styles={"nav-link": {"font-size": "18px", "text-align": "left", "margin": "-2px", "--hover-color": "#65B741"},
                        "nav-link-selected": {"background-color": "#65B741"}})

data = pd.read_csv("C:/Users/GVJai/Desktop/Project/resourse_management/cleaned_data.csv")

# HOME MENU
if selected == "Home":
    st.markdown("<h1 style='text-align: center; color: #65B741;'>Industrial Human Resource Geo-Visualization</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#65B741;font-size:26px;'>Technologies Used</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:24px;'>Python, EDA, NLP, Visualization, Streamlit</p>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#65B741;font-size:26px;'>Overview</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:24px;'>This project aims to update and analyze the industrial classification of workers in India, focusing on main and marginal workers excluding cultivators and agricultural laborers. The results will be visualized in an interactive dashboard created using Streamlit and Plotly.</p>", unsafe_allow_html=True)

if selected == "Data Visualization":
    # Get unique states and districts
    unique_states = sorted(data['State'].unique())
    selected_state = st.sidebar.selectbox("Select State", unique_states)

    filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
    selected_district = st.sidebar.selectbox("Select District", filtered_districts)
    # Filter data for selected state and district
    state_data = data[data['State'] == selected_state]
    district_data = state_data[state_data['District'] == selected_district]

    filtered_nic_names = data[data['District'] == selected_district]['NICName'].unique()
    filtered_nic_names = sorted(filtered_nic_names)

    selected_nic_name = st.sidebar.selectbox("Select NIC Name", filtered_nic_names, key="nic_name_selector")

    nic_filteredData = district_data[district_data['NICName'] == selected_nic_name]

    # Display selected state and district
    st.write(f"Showing data for {selected_state} - {selected_district}")

    # Calculate total number of workers
    total_state_workers = state_data['MainWorkersTotalPersons'].sum()
    st.write(f"Total number of state workers: {total_state_workers}")

    total_district_workers = district_data['MainWorkersTotalPersons'].sum()
    st.write(f"Total number of district workers: {total_district_workers}")

    # Display summary statistics for filtered data
    st.subheader("Data Summary for Selected District")
    st.write(district_data.describe())

    st.write(" ")
    st.write(" ")
    st.markdown("<h1 style='text-align: center; color: #65B741;font-size:30px'>Main Workers vs Marginal Workers</h1>",unsafe_allow_html=True)
    r2col1, r2col2 = st.columns(2)
    with r2col1:
        st.markdown("<h2 style='color:#151515;font-size:24px;'>Main Workers Rural and Urban</h2>", unsafe_allow_html=True)
        st.markdown(" ")
        # Plotting data for Rural, Main, and Urban workers
        rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
        urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

        rural_data = nic_filteredData[rural_cols].sum().values
        urban_data = nic_filteredData[urban_cols].sum().values

        fig, ax = plt.subplots(figsize=(10, 6))

        rural_labels = ['Rural Total', 'Rural Male', 'Rural Female']
        urban_labels = ['Urban Total', 'Urban Male', 'Urban Female']
        ax.bar(rural_labels, rural_data, color='#65B741', label='Rural')
        ax.bar(urban_labels, urban_data, color='#C1F2B0', label='Urban')
        # Adjusting label styles
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize('large')  # Set font size to large
            label.set_fontweight('bold')  # Set font weight to bold
        # Setting title
        title = f"{selected_state} - {selected_district} - Main Workers Distribution"
        ax.set_title(title, fontweight='bold')  # Set title to bold
        ax.legend()
        st.pyplot(fig)
    with r2col2:
        st.markdown("<h2 style='color:#151515;font-size:24px;'>Marginal Workers Rural and Urban</h2>",unsafe_allow_html=True)
        st.markdown(" ")
        # Plotting data for Rural, Main, and Urban workers
        marginal_cols_rural = ['MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales',
                               'MarginalWorkersRuralFemales']
        marginal_cols_urban = ['MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales',
                               'MarginalWorkersUrbanFemales']

        marginal_data_rural = nic_filteredData[marginal_cols_rural].sum().values
        marginal_data_urban = nic_filteredData[marginal_cols_urban].sum().values

        fig, ax = plt.subplots(figsize=(10, 6))
        rural_labels = ['Rural Total', 'Rural Male', 'Rural Female']
        urban_labels = ['Urban Total', 'Urban Male', 'Urban Female']
        ax.bar(rural_labels, marginal_data_rural, color='#65B741', label='Rural')
        ax.bar(urban_labels, marginal_data_urban, color='#C1F2B0', label='Urban')
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize('large')  # Set font size to large
            label.set_fontweight('bold')  # Set font weight to bold

        title=(f"{selected_state} - {selected_district} - Marginal Workers Distribution")
        ax.set_title(title, fontweight='bold')  # Set title to bold
        ax.legend()
        st.pyplot(fig)
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("<h1 style='text-align: center; color: #65B741;font-size:30px'>Marginal Workers Rural vs Urban</h1>",unsafe_allow_html=True)
    r3col1, r3col2=st.columns(2)
    with r3col1:
        st.markdown("<h2 style='color:#151515;font-size:24px;'>Marginal Workers Rural Male and Female (%)</h2>",unsafe_allow_html=True)
        st.markdown(" ")
        # Plotting data for Marginal workers (using pie chart)
        marginal_cols_rural = ['MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales', 'MarginalWorkersRuralFemales']

        marginal_data_rural = nic_filteredData[marginal_cols_rural].sum().values

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(marginal_data_rural, labels=['Rural Persons', 'Rural Males','Rural Females'], autopct='%1.1f%%', startangle=90,
               colors=['#40A578', '#90D26D', '#D9EDBF'])
        ax.set_title(f"{selected_state} - {selected_district} - Rural Marginal Workers Distribution")
        st.pyplot(fig)
    with r3col2:
        st.markdown("<h2 style='color:#151515;font-size:24px;'>Marginal Workers Urban Male and Female (%)</h2>",unsafe_allow_html=True)
        st.markdown(" ")
        marginal_cols_urban = ['MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales',
                               'MarginalWorkersUrbanFemales']
        marginal_data_urban = nic_filteredData[marginal_cols_urban].sum().values

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(marginal_data_urban, labels=['Urban Persons', 'Urban Males','Urban Females'], autopct='%1.1f%%', startangle=90,
               colors=['#40A578', '#90D26D', '#D9EDBF'])
        ax.set_title(f"{selected_state} - {selected_district} - Urban Marginal Workers Distribution")
        st.pyplot(fig)
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("<h1 style='text-align: center; color: #90D26D;font-size:30px'>Main Workers Rural vs Urban</h1>",unsafe_allow_html=True)
    r4col1, r4col2 = st.columns(2)
    with r4col1:
        st.markdown("<h2 style='color:#151515;font-size:24px;'>Main Workers Rural Male and Female (%)</h2>",unsafe_allow_html=True)
        st.markdown(" ")
        # Plotting data for Main workers (using pie chart)
        main_cols_rural = ['MainWorkersRuralPersons', 'MainWorkersRuralMales','MainWorkersRuralFemales']

        main_data_rural = nic_filteredData[main_cols_rural].sum().values
        # Create a pie trace
        fig = go.Figure(go.Pie(
            labels=['Rural Persons', 'Rural Males','Rural Females'],
            values=main_data_rural,
            hole=0.5,  # Set the size of the hole to create a donut chart
            textinfo='percent+label',  # Display both percentage and label
            marker=dict(colors=['#40A578', '#90D26D', '#D9EDBF'])
        ))

        # Update layout
        fig.update_layout(
            title=f"{selected_state} - {selected_district} - Rural Main Workers Distribution"
        )

        # Display the chart in the Streamlit app
        st.plotly_chart(fig)
    with r4col2:
        st.markdown("<h2 style='color:#151515;font-size:24px;'>Main Workers Urban Male and Female (%)</h2>",unsafe_allow_html=True)
        st.markdown(" ")
        main_cols_urban = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']
        main_data_urban = nic_filteredData[main_cols_urban].sum().values

        # Create a pie trace
        fig = go.Figure(go.Pie(
            labels=['Urban Persons', 'Urban Males','Urban Females'],
            values=main_data_urban,
            hole=0.5,  # Set the size of the hole to create a donut chart
            textinfo='percent+label',  # Display both percentage and label
            marker=dict(colors=['#40A578', '#90D26D', '#D9EDBF'])
        ))

        # Update layout
        fig.update_layout(
            title=f"{selected_state} - {selected_district} - Urban Main Workers Distribution"
        )

        # Display the chart in the Streamlit app
        st.plotly_chart(fig)

    # Sort the data based on 'TotalWorkers' column and select top 10 rows
    top_10_workers = district_data.iloc[1:].drop_duplicates(subset=['NICName']).nlargest(10, 'TotalWorkers')

    # Create a bar trace
    fig = go.Figure(go.Bar(
        y=top_10_workers['NICName'],
        x=top_10_workers['TotalWorkers'],
        orientation='h',  # Set orientation to horizontal
        marker=dict(color='#40A578')  # Set bar color
    ))

    # Update layout
    fig.update_layout(
        title=f"{selected_state} - {selected_district} - Top 10 Total Workers by NICName",
        xaxis=dict(title='Total Workers Count (Log Scale)', type='log',
                   tickfont=dict(size=14, family='Arial', color='black', weight='bold'),  # Update x-axis font
                   titlefont=dict(size=16, family='Arial', color='black', weight='bold')),  # Update x-axis title font
        yaxis=dict(title='NICName',
                   tickfont=dict(size=14, family='Arial', color='black', weight='bold'),  # Update y-axis font
                   titlefont=dict(size=16, family='Arial', color='black', weight='bold')),  # Update y-axis title font
        showlegend=False,
        height=600, width=900
    )

    # Display the chart in Streamlit app
    st.plotly_chart(fig)

if selected == "Geo Visualization":
    st.markdown("<h2 style='text-align: center;color:#151515;font-size:30px;'>Overall State Data - Workers Details</h2>",unsafe_allow_html=True)
    geo_cols = ['State', 'TotalPopulation', 'TotalWorkers', 'MaleFemaleRatio']
    geo_data = data[geo_cols].groupby('State').sum().reset_index()
    df1 = pd.DataFrame(geo_data, columns=geo_cols)
    df2 = pd.read_csv(r"C:/Users/GVJai/Desktop/Project/resourse_management/Statenames.csv")
    #df1['State'] = df2['State'].to_string().strip()
    # Loop through each state in df2
    # Create a copy of df1 for iteration
    df1_copy = geo_data.copy()
    # Initialize an empty DataFrame to collect rows
    appended_data = []

    # Loop through each state in df2
    for state in df2['State']:
        # Check if the state exists in df1
        if state not in df1_copy['State'].values:
            # If state doesn't exist, append a new row with population and total workers as zero
            appended_data.append({'State': state, 'TotalPopulation': 0, 'TotalWorkers': 0, 'MaleFemaleRatio': 0})

    # Convert the collected rows into a DataFrame and append it to df1_copy
    if appended_data:
        df1_copy = pd.concat([df1_copy, pd.DataFrame(appended_data)], ignore_index=True)
    # Plot choropleth map
    fig = px.choropleth(df1_copy,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='TotalWorkers',
                        color_continuous_scale='Reds',
                        hover_data={'State': True, 'TotalPopulation': True, 'TotalWorkers': True,'MaleFemaleRatio': True})
    fig.update_geos(fitbounds="locations", visible=False)
    # Set the height and width of the figure layout
    fig.update_layout(height=800, width=1000)  # Adjust these values as needed
    st.plotly_chart(fig, use_container_width=True)






