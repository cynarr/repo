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
        name=sent_type.split("_")[0].capitalize(),
    ))

sentiment_fig.update_layout(barmode='stack')

df = df[['country', 'positive_cnt', 'neutral_cnt', 'negative_cnt']]
sentiment_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i.split("_")[0].capitalize(), "id": i} for i in df.columns],
    data=df.to_dict('records'),
    sort_action="native",
    style_table={'height': '500px', 'overflowY': 'auto'},
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
    columns=[{"name": i.split("_")[0].capitalize(), "id": i} for i in df.columns],
    data=df.to_dict('records'),
    sort_action="native",
    style_table={'height': '500px', 'overflowY': 'auto'}
)

layout = html.Div([
    html.H2("Sentiment modeling of COVID-19 news in Europe"),
    html.Div([
        html.P("The COVID-19 mood map of Europe is a dashboard that visualizes the sentiment of reporting around COVID-19 news coverage in from different European state broadcasters.\n"
               "The dashboard shows analyses how reporting has evolved over time and varies over countries different languages."),
        dbc.Alert(
            "Disclaimer: All analyses represented here have been automatically made without thorough evaluation. The analyses themselves may not be entirely accurate, and the resulting plots may therefore be misleading. They should not be used as as a basis for decision making.",
            color="danger",
        ),
    ]),
    html.H2("Tools"),
    html.P([
        "How did we do it? With a little help from our friends! We used various tools, including those from the ",
        html.A("Embeddia project", href="http://embeddia.eu/"),
        " to create a corpus of European reporting about COVID-19 and produce different analyses of it automatically."
    ]),
    html.P([
        "First we created the news corpus of COVID-19 reporting by European state broadcasters using...",
    ]),
    html.Ul([
        html.Li(html.A("Wikidata for obtaining background information like the list of state broadcasters and keywords for COVID-19 and names of different countries in diffferent languages", href="https://www.wikidata.org/", target="_blank")),
        html.Li(html.A("News-Crawl for the raw news dumps", href="https://github.com/commoncrawl/news-crawl", target="_blank")),
        html.Li(html.A("News-Please to extract the article texts from the dumps", href="https://github.com/fhamborg/news-please", target="_blank"))
    ]),
    html.P([
        "Then we enriched the corpus with different automatic analyses such as...",
    ]),
    html.Ul([
        html.Li(html.A("The Embeddia multilingual BERT based news sentiment analysis tool for extracting polar sentiments.", href="https://gitlab.com/Andrazp/news_sentiment_tool_mebeddia", target="_blank")),
        html.Li(html.A("Moral Foundations Dictionary for moral sentiment analysis.", href="https://osf.io/ezn37/", target="_blank")),
        html.Li(html.A("MUSE embeddings for performing cross-lingual moral sentiment analysis.", href="https://github.com/facebookresearch/MUSE", target="_blank")),
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
