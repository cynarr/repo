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
from dash_table.Format import Format, Scheme


__all__ = ["layout"]

language_count_df = db_conn.get_language_distribution()

num_fmt_dict = dict(type="numeric", format=Format(scheme=Scheme.decimal_integer))

language_count_table = dash_table.DataTable(
    id='table',
    columns=[
        {
            "name": i,
            "id": i,
            **(num_fmt_dict if i != "Language" else {})
        }
        for i
        in language_count_df.columns
    ],
    data=language_count_df.to_dict('records'),
    sort_action="native",
    style_table={'height': '500px', 'overflowY': 'auto'}
)

lang_count_fig = px.pie(language_count_df, values="Count", names="Language")
lang_count_fig.update_traces(textposition='inside')
lang_count_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


lang_timeline_df = db_conn.get_language_timeline()
lang_timeline_fig = px.bar(
    lang_timeline_df, 
    x="date", 
    y="count", 
    color="language", 
    labels={'date': 'Week', 'count': 'Count', 'language': 'Languages'}
)

country_count_df = db_conn.get_country_distribution()
country_news_count_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in country_count_df.columns],
    data=country_count_df.to_dict('records'),
    sort_action="native",
    style_table={'height': '500px', 'overflowY': 'auto'}
)

country_mention_count_df = db_conn.get_country_mention_distribution()
country_mention_count_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in country_mention_count_df.columns],
    data=country_mention_count_df.to_dict('records'),
    sort_action="native",
    style_table={'height': '500px', 'overflowY': 'auto'}
)


df = db_conn.get_sentiment_country_distribution()

sentiment_fig = go.Figure()

for sent_type in ['positive_cnt', 'neutral_cnt', 'negative_cnt']:
    sentiment_fig.add_trace(go.Bar(
        y=df['country'],
        x=df[sent_type] / df['sent_sum'],
        orientation='h',
        name=sent_type.split("_")[0].capitalize()
    ))

sentiment_fig.update_layout(barmode='stack')

df = df[['country', 'positive_cnt', 'neutral_cnt', 'negative_cnt']]
sentiment_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    sort_action="native",
    style_table={'height': '500px', 'overflowY': 'auto'}
)


df = db_conn.get_sentiment_country_mention_distribution()

sentiment_mention_fig = go.Figure()

for sent_type in ['positive_cnt', 'neutral_cnt', 'negative_cnt']:
    sentiment_mention_fig.add_trace(go.Bar(
        y=df['country'],
        x=df[sent_type] / df['sent_sum'],
        orientation='h',
        name=sent_type.split("_")[0].capitalize()
    ))

sentiment_mention_fig.update_layout(barmode='stack')
df = df[['country', 'positive_cnt', 'neutral_cnt', 'negative_cnt']]
sentiment_mentioning_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    sort_action="native",
    style_table={'height': '500px', 'overflowY': 'auto'}
)








layout = html.Div([
    html.H2("What is the COVID-19 mood map?"),
    html.Div([
        html.P("COVID-19 mood map is a dashboard that visualizes the general mood of COVID news over time."),
        html.P("DISCLAIMER: data and analyses represented here might not be accurate and should not be used as XXX")
    ]),
    html.H2("Tools used"),
    html.Div([
        html.P("what methods, tools and data are you using")
    ]),
    html.H2("Data overview"),
    html.H3("Language distributions"),
    dcc.Loading(
        id="analyses-section",
        type="default",
        children=[    
            dbc.Row([
                dbc.Col(html.Div(language_count_table), width=6),
                dbc.Col(html.Div(dcc.Graph(figure=lang_count_fig)), width=6),
            ]),
            html.Div(
                dcc.Graph(figure=lang_timeline_fig)
            )
    ]),
    html.H3("Country distributions"),
    dbc.Row([
        dbc.Col([
            html.H4("News from country"),
            country_news_count_table
        ]),
        dbc.Col([
            html.H4("News mentioning country"),
            country_mention_count_table
        ])        
    ]),
    html.H3("Overall sentiments"),
    dbc.Row([
        dbc.Col([
            html.H4("Sentiments"),
            sentiment_table,
            dcc.Graph(figure=sentiment_fig)
        ], width=6),
        dbc.Col([
            html.H4("Sentiments mentioning"),
            sentiment_mentioning_table,
            dcc.Graph(figure=sentiment_mention_fig)
        ], width=6) 
    ]),    
])
