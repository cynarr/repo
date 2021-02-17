# -*- coding: utf-8 -*-
# Run this file and navigate to http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import datetime
from datetime import date

from .base import app
from . import database_conn as db_conn
from .mentions import layout as mentions_layout
from .common import config_available_languages, config_min_date, config_max_date

__all__ = ["layout"]

@app.callback(
    dash.dependencies.Output('timeline-graph', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('language-dropdown', 'value')])
def update_sentiment_timeline(start_date, end_date, value):
    start_date_object = "1970-01-01"
    end_date_object = "2100-01-01"

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
            
    df = db_conn.get_sentiment_hist_df({
        'start_date': str(start_date_object), 
        'end_date': str(end_date_object),
        'language': value
    })

    fig_timeline = px.histogram(df, x="date", y="Number of articles", color="Sentiment", barmode="stack",
                                title="News sentiment on the COVID-19 pandemic in March 2020", nbins=31)

    fig_timeline.update_layout(
        xaxis=dict(
            title='Date',
            tickmode='linear'),
        yaxis=dict(
            title="Number of news articles",
        )
    )

    return fig_timeline

@app.callback(
    dash.dependencies.Output('moral-graph', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('language-dropdown', 'value')])
def update_moral_graph(start_date, end_date, value):
    start_date_object = "1970-01-01"
    end_date_object = "2100-01-01"

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
            
    df = db_conn.get_moral_sentiment_hist_df({
        'start_date': str(start_date_object), 
        'end_date': str(end_date_object),
        'language': value
    })
    fig = px.bar(df, x="date", y="sum", color="sentiment_type", barmode="group")
    return fig

map_df = db_conn.get_counts_for_countries()

fig_map = px.choropleth(map_df, locations="country_iso3",
                    color="doc_count",
                    hover_name="country", 
                    scope="europe",
                    height=1000,
                    color_continuous_scale=px.colors.sequential.Plasma)

layout = html.Div([
    html.H3(children='Filters'),

    html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range',
            display_format='YYYY-MM-DD',
            min_date_allowed=config_min_date,
            max_date_allowed=config_max_date,
            start_date=config_min_date,
            end_date=config_max_date
        ), 
        dcc.Dropdown(
            id='language-dropdown',
            options=config_available_languages,
            value=''
        )
    ]),

    dcc.Graph(
        id='timeline-graph'
    ),
    dcc.Graph(
        id='moral-graph'
    ),
    dcc.Graph(
        id='map-graph',
        figure=fig_map
    )
])