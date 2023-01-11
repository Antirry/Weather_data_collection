from Data_Visualisation_3.Extract_Data_6 import retrieve_documents
import pandas as pd
import panel as pn
pn.extension('tabulator')

data, collections_date = retrieve_documents()
df = pd.DataFrame(data)
idf = df.interactive()

day_slider = pn.widgets.DateSlider(name='Day time slider',
                                   start=df['date_time'].min(),
                                   end=df['date_time'].max(),
                                   value=df['date_time'].min()
                                   )

yaxis_temp = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['temp', 'temp_max', 'temp_min'],
    button_type='success'
)

temp_pipeline = (
    idf[
        idf.date_time <= day_slider
    ]
    .groupby('date_time')[yaxis_temp].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='date_time')
    .reset_index(drop=True)
)

temp_plot = temp_pipeline.hvplot(x='date_time', by='temp',
                                 y=yaxis_temp, line_width=2,
                                 title='Время и температура в городах')

temp_table = temp_pipeline.pipe(pn.widgets.Tabulator,
                                pagination='remote',
                                page_size=10,
                                sizing_mode='stretch_width')


temp_scatterplot_pipeline = (
    idf[
        (idf.date_time == day_slider)
    ]
    .groupby(['weather_disc', 'name'])[yaxis_temp].mean()
    .to_frame()
    .reset_index()
    .sort_values('name')
    .reset_index(drop=True)
)

temp_scatterplot = temp_scatterplot_pipeline.hvplot(x='weather_disc', y=yaxis_temp, by='name', size=80, kind='scatter',
                                                    alpha=0.7, legend=False, height=500, width=500)

yaxis_wind = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['wind', 'wind_deg'],
    button_type='success'
)

wind_source_bar_pipeline = (
    idf[
        (idf.date_time == day_slider)
    ]
    .groupby(['temp', 'name'])[yaxis_wind].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='temp')
    .reset_index(drop=True)
)

wind_source_bar_plot = wind_source_bar_pipeline.hvplot(kind='bar',
                                                       x='name',
                                                       y=yaxis_wind,
                                                       title='Ветер по городам')

#Layout using Template
template = pn.template.FastListTemplate(
    title='Панель погоды Росссии в популярных городах',
    sidebar=[pn.pane.Markdown("# Температура и ветер, а также описание погоды"),
             pn.pane.Markdown("#### Это программа сделана для задания от АО 'Почта России', которая должна собирать информацию от 50 крупнейших городов России, после чего сохранять данные в базу данных и также выводить эти данные в этой программе"),
             pn.pane.Markdown("## Настройки"),
             day_slider],
    main=[pn.Row(pn.Column(yaxis_temp,
                           temp_plot.panel(width=700), margin=(0,25)),
                 temp_table.panel(width=500)),
          pn.Row(pn.Column(temp_scatterplot.panel(width=600), margin=(0,25)),
                 pn.Column(yaxis_wind, wind_source_bar_plot.panel(width=600)))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
# template.show()
template.servable()