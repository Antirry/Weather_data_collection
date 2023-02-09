import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from os import getcwd
from PIL import Image
from _6_Extract_Data import start_retrieve_documents as documents
from Parts_site.Metrics import metrics
from Parts_site.Chart import interactive_chart as chart_
from Parts_site.map import main_map as map_


st.set_page_config(page_title='Погода в г. России',
                   layout='wide',
                   initial_sidebar_state='expanded')

file_path = getcwd()
with open(fr"{file_path}\_3_Data_Visualisation\Parts_site\style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def data():
    df = pd.DataFrame(documents())
    return df


df = data()
df_map = data()

st.markdown('## Погода в самых населенных городах России')

with st.sidebar:
    st.markdown('### (free-cooling), свободное охлаждение серверов воздухом с улицы, работает от -30 до +20 - +22 °C,')
    st.markdown('### После (+22 - +35 °C) устанавливаются холодильные машины, без свободного охлаждения')

    st.markdown('''---''')
    plot_height = st.sidebar.slider('Настройка высоты графика', 200, 1000, 200)
    plot_width = st.sidebar.slider('Настройка широты графиков', 200, 1000, 800)

    st.markdown('''---''')
    st.markdown('### Создано ❤️ студентом [Антипиным Дмитрием](https://github.com/Antirry) 4 ИС-2.')

Metrics = metrics(df)

st.markdown('### Среднее значение данных')
st.markdown('')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Мин. темп. - " + Metrics[0], str(Metrics[1]) + ' °C')
col2.metric("Отклон темп. - " + Metrics[2], str(Metrics[3]) + ' °C')
col3.metric("Макс. темп. - " + Metrics[4], str(Metrics[5]) + ' °C')
col4.metric("Отклон темп. - " + Metrics[6], str(Metrics[7]) + ' °C')
col5.metric("Макс. ветер - " + Metrics[8], str(Metrics[9]) + ' м/с')

st.markdown('')

tab1, tab2 = st.tabs(["Описание", "Графики"])
with tab1:
    st.markdown('## Это сайт -  интерактивная аналитическая панель - форма визуализации данных')
    st.markdown('#### Нужен для выбора из самых популярных городов и установки на них серверов.')
    st.markdown('')
    left1, right1 = st.columns((1, 3))
    with left1:
        st.markdown('#### API, который я использовал для данных - [OpenWeatherAPI](https://openweathermap.org/api).')
        st.markdown('#### Откуда я брал данные самых популярных городов ' +
                    '[Росстат](https://rosstat.gov.ru/compendium/document/13282)')
        image = Image.open(fr"{file_path}\_3_Data_Visualisation\Parts_site\Images\1compass.png")
        st.image(image, use_column_width='Auto', caption='Компас с градусами из столбца "wind_deg"')
    with right1:
        st.write(df)

    st.markdown('#### Карта с самыми населенными городами')
    st_folium(map_(df_map), key="fig1", width=2000, height=700)

with tab2:
    left, middle, right = st.columns((1, 5, 1))
    chart = chart_(df, plot_height, plot_width)
    with middle:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
