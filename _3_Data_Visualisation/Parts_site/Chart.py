import altair as alt
import random
import pandas as pd




def interactive_chart(df: pd.DataFrame, plot_height, plot_width):
    cities_dict_list = df['name'].unique()

    # color1 = alt.Color('count():Q', scale=alt.Scale(scheme='blueorange'), title='Количество одинаковых')
    color1 = alt.Color('name:N', scale=alt.Scale(domain=cities_dict_list, scheme='viridis'), title='Количество одинаковых')
    brush = alt.selection_interval(encodings=['x'])
    click = alt.selection_multi(encodings=['color'])

    # color=alt.condition(brush, alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'), title='Количество одинаковых'), alt.value('lightgray')),

    points1 = alt.Chart(df).mark_rect().encode(
        alt.Y('wind:Q', bin=alt.Bin(maxbins=60), title='Ветер (м/c)'),
        alt.X('temp:Q', bin=alt.Bin(maxbins=40), title='Температура (°C)'),
        color=alt.condition(brush, color1, alt.value('lightgray'))
    ).properties(
        width=plot_width,
        height=plot_height
    ).add_selection(
        brush
    ).transform_filter(
        click
    )

    points2 = alt.Chart(df).mark_point().encode(
        alt.Y('temp:N', title='Температура (°C)'),
        alt.X('wind:N', title='Ветер (м/c)'),
        color=alt.condition(brush, color1, alt.value('lightgray')),
    ).properties(
        width=plot_width,
        height=plot_height
    ).add_selection(
        brush
    ).transform_filter(
        click
    )

    bar1 = alt.Chart(df).mark_bar().encode(
        alt.X('count()', title='Количество'),
        alt.Y('name:N', title='Название городов'),
        color=alt.condition(click, color1, alt.value('lightgray')),
    ).transform_filter(
        brush
    ).properties(
        width=plot_width,
    ).add_selection(
        click
    )

    bar2 = alt.Chart(df).mark_bar().encode(
        alt.X('count()', title='Количество'),
        alt.Y('wind_dir:N', title='Направление ветра'),
        color=alt.condition(click, color1, alt.value('lightgray')),
    ).transform_filter(
        brush
    ).properties(
        width=plot_width,
    ).add_selection(
        click
    )

    bar3 = alt.Chart(df).mark_bar().encode(
        alt.X('count()', title='Количество'),
        alt.Y('weather_disc:N', title='Описание погоды'),
        color=alt.condition(click, color1, alt.value('lightgray')),
    ).transform_filter(
        brush
    ).properties(
        width=plot_width,
    ).add_selection(
        click
    )

    alt.renderers.enable('html')

    chart = alt.vconcat(
        points1,
        points2,
        bar1,
        bar2,
        bar3,
        data=df,
        title="Погода России c " + str(df.iloc[0]['date'])[-4:] + " по " + str(df.iloc[-1]['date'])[-4:] + " года"
    )

    return chart
