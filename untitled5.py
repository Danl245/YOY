# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WqFYkh1asR5MZX3yKdo0iFVQGYHKbuuh
"""

pip install streamlit

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pprint

!streamlit hello

!git clone 'https://github.com/datasets/geo-countries.git'

import io
csv_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
req = requests.get(csv_url)
s=requests.get(csv_url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')))

df

"""ПОДГОТОВКА ДАННЫХ"""

# Оставляем только необходимые переменные

df = df[['iso_code','location','total_cases_per_million','total_deaths_per_million','people_vaccinated_per_hundred','date']]
df = df[df.location != 'World']
df["date"] = pd.to_datetime(df["date"])
# Сохраним данные в формате csv для создания приложения
df.to_csv('data.csv', index = False)

df

#НАСТРОЙКА ЗАГОЛОВКА И БОКОВОЙ ПАНЕЛИ

# Настройка заголовка и текста
st.title("COVID 19 IN THE WORLD DASHBOARD")
st.write("""This dashboard will present the spread of COVID-19 in the world by visualizing the timeline of the total cases and deaths. As well as the total number of vaccinated people.""")

# Настройка боковой панели
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/COVID_dashboard_proglib).")

# Загружаем новые оптимизированные данные
DATA = ('data.csv')
DATE_COLUMN = 'date'
@st.cache # для оптимизации работы приложения

# Создадим функцию для загрузки данных
def load_data():
    df = pd.read_csv(DATA, parse_dates=[DATE_COLUMN])
    return df

# Применим функцию
df = load_data()

# Загружаем координаты стран для карты
with open('/content/geo-countries/data/countries.geojson') as json_file:
    json_locations = json.load(json_file)

"""ВИЗУАЛИЗАЦИЯ"""

# Создадим функции для визуализации количества случаев заражения, смертей и вакцинированных людей.
def draw_map_cases():
    fig = px.choropleth_mapbox(df, geojson=json_locations, locations='iso_code', color='total_cases_per_million',
                               color_continuous_scale="Reds",
                               mapbox_style="carto-positron",
                               title = "COVID 19 cases per million",
                               zoom=1,
                               opacity=0.5,
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def draw_map_deaths():
    fig = px.choropleth_mapbox(df, geojson=json_locations, locations='iso_code', color='total_deaths_per_million',
                               color_continuous_scale="Greys",
                               mapbox_style="carto-positron",
                               title = "Deaths from COVID 19 per million",
                               zoom=1,
                               opacity=0.5,
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def draw_map_vaccine():
    fig = px.choropleth_mapbox(df, geojson=json_locations, locations='iso_code', color='people_vaccinated_per_hundred',
                               color_continuous_scale="BuGn",
                               mapbox_style="carto-positron",
                               title = "Vaccinations from COVID 19 per hundred",
                               zoom=1,
                               opacity=0.5,
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "#### Data on COVID-19 (coronavirus) by Our World in Data could be found [here](https://github.com/owid/covid-19-data/tree/master/public/data).")
    st.write(df)

# Создадим поле выбора для даты
show_timerange = st.sidebar.checkbox("Show date range")
if show_timerange == True:
    # Вычислим даты для создания временного слайдера
    min_ts = min(df[DATE_COLUMN]).to_pydatetime()
    max_ts = max(df[DATE_COLUMN]).to_pydatetime()
    day_date = pd.to_datetime(st.sidebar.slider("Date to chose", min_value=min_ts, max_value=max_ts, value=max_ts))
    st.write(f"Data for {day_date.date()}")
    df = df[(df['date'] == day_date)]

# Создадим поле выбора для визуализации общего количества случаев, смертей или вакцинаций
select_event = st.sidebar.selectbox('Show map', ('cases per million', 'deaths per million', 'vaccinated per hundred'))
if select_event == 'cases per million':
    st.plotly_chart(draw_map_cases(), use_container_width=True)
if select_event == 'deaths per million':
    st.plotly_chart(draw_map_deaths(), use_container_width=True)

if select_event == 'vaccinated per hundred':
    st.plotly_chart(draw_map_vaccine(), use_container_width=True)

# Настройка заголовка и текста
st.title("COVID 19 IN THE WORLD DASHBOARD")
st.write("""This dashboard will present the spread of COVID-19 in the world by visualizing the timeline of the total cases and deaths. As well as the total number of vaccinated people.""")

# Настройка боковой панели
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/COVID_dashboard_proglib).")
# Загружаем новые оптимизированные данные
DATA = ('data.csv')
DATE_COLUMN = 'date'
@st.cache # для оптимизации работы приложения

# Создадим функцию для загрузки данных
def load_data():
    df = pd.read_csv(DATA, parse_dates=[DATE_COLUMN])
    return df

# Применим функцию
df = load_data()


# Создадим функции для визуализации количества случаев заражения, смертей и вакцинированных людей.
def draw_map_cases():
    fig = px.choropleth(df, locations="iso_code",
                         color="total_cases_per_million",
                         hover_name="location",
                         title="Total COVID 19 cases in the world",
                         color_continuous_scale=px.colors.sequential.Redor)
    return fig

def draw_map_deaths():
    fig = px.choropleth(df, locations="iso_code",
                         color="total_deaths_per_million",
                         hover_name="location",
                         title="Total deaths from COVID 19 in the world",
                         color_continuous_scale=px.colors.sequential.Greys)
    return fig

def draw_map_vaccine():
    fig = px.choropleth(df, locations="iso_code",
                         color="people_vaccinated_per_hundred	",
                         hover_name="location",
                         title="Total vaccinated from COVID 19 in the world",
                         color_continuous_scale=px.colors.sequential.Greens)
    return fig

show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "#### Data on COVID-19 (coronavirus) by Our World in Data could be found [here](https://github.com/owid/covid-19-data/tree/master/public/data).")
    st.write(df)

# Вычислим даты для создания временного слайдера
min_ts = min(df[DATE_COLUMN]).to_pydatetime()
max_ts = max(df[DATE_COLUMN]).to_pydatetime()

# Создадим поле выбора для даты
show_timerange = st.sidebar.checkbox("Show date range")
if show_timerange:
    min_selection, max_selection = st.sidebar.slider("Timeline", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts])
    df = df[(df[DATE_COLUMN] >= min_selection) & (df[DATE_COLUMN] <= max_selection)]

# Создадим поле выбора для визуализации общего количества случаев, смертей или вакцинаций
select_event = st.sidebar.selectbox('Show map', ('total_cases', 'total_deaths', 'total_vaccinations'))
if select_event == 'total_cases':
    st.plotly_chart(draw_map_cases(), use_container_width=True)

if select_event == 'total_deaths':
    st.plotly_chart(draw_map_deaths(), use_container_width=True)

if select_event == 'total_vaccinations':
    st.plotly_chart(draw_map_vaccine(), use_container_width=True)

show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.markdown(
        "#### Data on COVID-19 (coronavirus) by Our World in Data could be found [here](https://github.com/owid/covid-19-data/tree/master/public/data).")
    st.write(df)