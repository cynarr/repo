# -*- coding: utf-8 -*-
# Run this file and navigate to http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import database_conn as db_conn


__all__ = ["server"]

app = dash.Dash(
    __name__,
    url_base_pathname="/",
    external_stylesheets=[
        dbc.themes.SLATE,
        "https://use.fontawesome.com/releases/v5.9.0/css/all.css", ],
    meta_tags=[{
        "name": "description",
        "content": "COVID-19 European news dashboard"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}])

server = app.server

df = db_conn.get_sentiment_hist_df({'start_date': '2020-01-01', 'end_date': '2020-05-01'})

fig_timeline = px.histogram(df, x="date", y="Number of articles", color="Sentiment", barmode="stack",
                            title="News sentiment on the COVID-19 pandemic in March 2020")


fig_timeline.update_layout(
    xaxis=dict(
        title='Date',
        tickmode='linear'),
    yaxis=dict(
        title="Number of news articles",
    )
)

fig_map = px.choropleth(locations=["UK", "Finland", "Sweden"], locationmode="ISO-3", scope="europe",
                        width=1000, height=1000, color_continuous_scale="Blues")

app.layout = html.Div(children=[
    html.H1(children='COVID-19 European news dashboard'),

    html.Div(children='''
        EMBEDDIA Hackathon 2021
    '''),

    html.Div(children='''
    Mood-Mapping Muppets
'''),

    dcc.Graph(
        id='timeline-graph',
        figure=fig_timeline
    ),
    dcc.Graph(
        id='map-graph',
        figure=fig_map
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
