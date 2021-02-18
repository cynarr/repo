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
from .common import config_available_languages, config_min_date, config_max_date

import dash_table


__all__ = ["layout"]

language_count_df = db_conn.get_language_distribution()

language_count_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in language_count_df.columns],
    data=language_count_df.to_dict('records'),
)

lang_count_fig = px.pie(language_count_df, values="Count", names="Language")


lang_timeline_df = db_conn.get_language_timeline()
lang_timeline_fig = px.bar(lang_timeline_df, x="date", y="count", color="language")

layout = html.Div([
    html.H1("COVID-19 mood map"),
    html.H2("What is COVID-19 mood map?"),
    html.Div([
        html.P("COVID-19 mood map is a dashboard that visualizes the general mood of COVID news over time."),
        html.P("DISCLAIMER: data and analyses represented here might not be accurate and should not be used as XXX")
    ]),
    html.H2("Tools used"),
    html.Div([
        html.P("what methods, tools and data are you using")
    ]),
    html.H2("Data stastistics"),
    html.H3("Languages"),
    dcc.Loading(
        id="analyses-section",
        type="default",
        children=[    
            dbc.Row([
                dbc.Col(html.Div(language_count_table), width=4),
                dbc.Col(html.Div(dcc.Graph(figure=lang_count_fig))),
            ]),
            html.Div(
                dcc.Graph(figure=lang_timeline_fig)
            )
    ])
])
