# streamlit_app.py
import streamlit as st
import pandas as pd
import datetime
import numpy as np

st.set_page_config(
    page_title="Painel do Clima",
    page_icon="✅",
    layout="wide",
)


# Carregando os dados.
conn = st.experimental_connection('mysql', type='sql')
df = conn.query('SELECT data, temperatura, umidade FROM Clima;', ttl=600)
#html = 'https://raw.githubusercontent.com/luizrsassi/clima-time-series/main/clima.csv'

#df = pd.read_csv(html, usecols=['data', 'temperatura', 'umidade'])

df['data'] = pd.to_datetime(df['data'])

st.title("Temperatura e Umidade")

# Dados agrupados por dia
temperatura_dia = df.groupby(pd.Grouper(key="data", freq="D")).temperatura.agg(['mean', 'min', 'max']).dropna(axis = 0, how ='any')
umidade_dia = df.groupby(pd.Grouper(key="data", freq="D")).umidade.agg(['mean', 'min', 'max']).dropna(axis = 0, how ='any')

# Colunas dos gráficos por dia
col1, col2 = st.columns(2)

with col1:
    st.header("Temperatura Diária")
    # Cards
    col11, col12, col13 = st.columns(3)
    col11.metric(label="Média", value=df['temperatura'].mean().round(decimals=1))
    col12.metric(label="Mínima", value=df['temperatura'].min().round(decimals=1))
    col13.metric(label="Máxima", value=df['temperatura'].max().round(decimals=1))
    # Gráfico de linha
    st.line_chart(data=temperatura_dia, y=['mean', 'min', 'max'], use_container_width=True)

with col2:
    st.header("Umidade Diária")
    # Cards
    col21, col22, col23 = st.columns(3)
    col21.metric(label="Média", value=df['umidade'].mean().round(decimals=1))
    col22.metric(label="Mínima", value=df['umidade'].min().round(decimals=1))
    col23.metric(label="Máxima", value=df['umidade'].max().round(decimals=1))
    # Gráfico de linha
    st.line_chart(data=umidade_dia, y=['mean', 'min', 'max'], use_container_width=True)


# Seletor de data
periodo = "Dados disponíveis de  " + \
          str(df['data'].max().day) + "/" + \
          str(df['data'].max().month) + "/" + \
          str(df['data'].max().year) + \
          " até " + \
          str(df['data'].min().day) + "/" + \
          str(df['data'].min().month) + "/" + \
          str(df['data'].min().year)
dia = st.date_input(label=periodo, value=df['data'].max())

# Dados agrupados por hora
temperatura_hora = df.groupby(pd.Grouper(key="data", freq="H")).temperatura.agg(['mean', 'min', 'max']).dropna(axis = 0, how ='any')
umidade_hora = df.groupby(pd.Grouper(key="data", freq="H")).umidade.agg(['mean', 'min', 'max']).dropna(axis = 0, how ='any')


col31, col32 = st.columns([1, 2])

col31.dataframe(temperatura_hora.loc[str(dia)])

with col32:
    st.header("Temperatura média ao longo do dia " + str(f"{dia.day}/{dia.month}/{dia.year}"))
    st.line_chart(temperatura_hora.loc[str(dia), ['mean']])

col41, col42 = st.columns([2, 1])

col42.dataframe(umidade_hora.loc[str(dia)])

with col41:
    st.header("Umidade média ao longo do dia " + str(f"{dia.day}/{dia.month}/{dia.year}"))
    st.line_chart(umidade_hora.loc[str(dia), ['mean']])
