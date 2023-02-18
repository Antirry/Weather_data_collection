import pandas as pd
import streamlit as st
from os import path
from PIL import Image

from _6_Extract_Data import start_retrieve_documents as documents
from Parts_site.Metrics import metrics
from Parts_site.Chart import interactive_chart as chart_
from Parts_site.map import extract_name_coor as name_coor

st.set_page_config(page_title='Погода в г. России',
                   layout='wide',
                   initial_sidebar_state='expanded')

dir_name = path.dirname(path.abspath(__file__))

with open(path.join(dir_name, 'Parts_site', 'style.css')) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache_data
def data():
    df = pd.DataFrame(documents())
    return df


df = data()

st.title('Погода в самых населенных городах России')

with st.sidebar:
    st.markdown('#### (free-cooling), свободное охлаждение серверов воздухом с улицы, работает от -30 до +20 - +22 °C,')
    st.markdown('#### После (+22 - +35 °C) устанавливаются холодильные машины, без свободного охлаждения.')
    st.markdown('#### Меньше скорость ветра = лучше для кулера, меньше засориться грязью - пылью фильтр.')

    st.markdown('''---''')
    plot_height = st.sidebar.slider('Настройка высоты графика', 200, 1000, 200)
    plot_width = st.sidebar.slider('Настройка широты графиков', 200, 1000, 800)

    st.markdown('''---''')
    st.markdown('#### Создано ❤️ студентом [Антипиным Дмитрием](https://github.com/Antirry) 4 ИС-2.')

Metrics = metrics(df)

st.markdown('## Среднее значение данных')
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
    st.title('Это сайт -  интерактивная аналитическая панель - форма визуализации данных')
    st.markdown('### Нужен для выбора из самых популярных городов и установки на них серверов. ' +
                'Свободное охлаждение это высокий коэффициент энергосбережения. ' +
                'Так как можно охлаждать помещение окружающим воздухом, не используя кондиционеры.')

    st.markdown('## Проблема одна - это грязный воздух, он увеличивает скорость износа оборудования. ' +
                'Поэтому я сделал такие цвета от 1 до 50 города.')
    st.markdown('')
    image = Image.open(path.join(dir_name, 'Parts_site', 'Images', 'Color_Scheme.jpg'))
    st.image(image, use_column_width='always',
             caption='Палитра цветов городов (От самого популярного - до не популярного)')

    st.title('')

    left2, right2 = st.columns((1, 1))
    with left2:
        st.markdown('### API, который я использовал для данных - [OpenWeatherAPI](https://openweathermap.org/api). ' +
                    'Откуда я брал данные самых популярных городов (Использовал 50 городов) - ' +
                    '[Росстат](https://rosstat.gov.ru/compendium/document/13282).')

    with right2:
        st.markdown('### Статьи на тему свободного охлаждения - ' +
                    '[Общая статья](https://iclim.ru/articles/chto_takoe_frikuling/), ' +
                    '[Общая статья](https://evroprom.com/kz/novosti-i-stati-kz/chiller-s-frikulingom-preimushhestva-i' +
                    '-osobennosti-3/), ' +
                    '[Подробная статья](https://hvac-school.ru/vestnik_ano/vestnik_ano_ukc_universitet_29' +
                    '/rezhim_svobodnogo_ohlazhdenija/)')

    left1, right1 = st.columns((1, 1))
    with left1:
        image1 = Image.open(path.join(dir_name, 'Parts_site', 'Images', 'Compass1.jpg'))
        st.image(image1, use_column_width='never', caption='Компас с градусами из столбца "wind_deg"')

    with right1:
        image2 = Image.open(path.join(dir_name, 'Parts_site', 'Images', 'Map_Free_Cooling.png'))
        st.image(image2, use_column_width='always',
                 caption='Карта для оптимального климата под свободное охлаждение')

    st.markdown('## Карта с самыми населенными городами')
    st.map(name_coor(df), zoom=2, use_container_width=True)

    st.markdown('## Данные которые я использовал')
    st.dataframe(df, use_container_width=True)

with tab2:
    left, middle, right = st.columns((1, 5, 1))
    chart = chart_(df, plot_height, plot_width)

    with middle:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
