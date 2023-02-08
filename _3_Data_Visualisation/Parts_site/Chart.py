import altair as alt
import random
import pandas as pd


def interactive_chart(df: pd.DataFrame, plot_height, plot_width):
    weather_dict_list = df['weather_disc'].unique()

    scale = alt.Scale(domain=weather_dict_list,
                      range=["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                             for i in range(len(weather_dict_list))])
    color = alt.Color('weather_disc:N', scale=scale)

    brush = alt.selection_interval(encodings=['x'])
    click = alt.selection_multi(encodings=['color'])

    points1 = alt.Chart(df).mark_point().encode(
        alt.Y('name:O', title='Название города'),
        alt.X('temp:Q', title='Температура (°C)'),
        color=alt.condition(brush, color, alt.value('lightgray')),
        size=alt.Size('wind:Q')
    ).properties(
        width=plot_width,
        height=plot_height
    ).add_selection(
        brush
    ).transform_filter(
        click
    )

    points2 = alt.Chart(df).mark_point().encode(
        alt.Y('temp:O', title='Температура (°C)'),
        alt.X('wind:O', title='Ветер (м/c)'),
        color=alt.condition(brush, color, alt.value('lightgray')),
    ).properties(
        width=plot_width,
        height=plot_height
    ).add_selection(
        brush
    ).transform_filter(
        click
    )

    bar1 = alt.Chart(df).mark_bar().encode(
        x='count()',
        y='name:O',
        color=alt.condition(click, color, alt.value('lightgray')),
    ).transform_filter(
        brush
    ).properties(
        width=plot_width,
    ).add_selection(
        click
    )

    bar2 = alt.Chart(df).mark_bar().encode(
        x='count()',
        y='wind_dir:N',
        color=alt.condition(click, color, alt.value('lightgray')),
    ).transform_filter(
        brush
    ).properties(
        width=plot_width,
    ).add_selection(
        click
    )

    bar3 = alt.Chart(df).mark_bar().encode(
        x='count()',
        y='weather_disc:N',
        color=alt.condition(click, color, alt.value('lightgray')),
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
