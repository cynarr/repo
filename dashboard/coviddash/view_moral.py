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
from .common import config_available_languages, config_min_date, config_max_date, config_available_sentiments, language_col, date_range_col

__all__ = ["layout"]

@app.callback(
    dash.dependencies.Output('ms-timeline-graph', 'figure'),
    [dash.dependencies.Input('date-range-filter', 'start_date'),
     dash.dependencies.Input('date-range-filter', 'end_date'),
     dash.dependencies.Input('language-dropdown', 'value'),
     dash.dependencies.Input('ms-sentiment-dropdown', 'value')])
def update_moral_graph(start_date, end_date, language, sentiment_type):
    start_date_object = "2020-03-01"
    end_date_object = "2020-04-01"

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
            
    df = db_conn.get_moral_sentiment_hist_df({
        'start_date': str(start_date_object), 
        'end_date': str(end_date_object),
        'language': language,
        'sentiment_type': sentiment_type
    })
    fig = px.bar(df, x="date", y="sum", color="sentiment_type", barmode="group", 
        labels={'date': 'Date', 'sum': 'Strength of moral sentiment', 'sentiment_type': 'Sentiment'}
    )
    return fig


@app.callback(
    dash.dependencies.Output('ms-maps', 'children'),
    [dash.dependencies.Input('date-range-filter', 'start_date'),
     dash.dependencies.Input('date-range-filter', 'end_date'),
     dash.dependencies.Input('language-dropdown', 'value'),
     dash.dependencies.Input('ms-sentiment-dropdown', 'value')])
def update_moral_map(start_date, end_date, language, sentiment_type):
    start_date_object = "1970-01-01"
    end_date_object = "2100-01-01"

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
            
    map_df = db_conn.get_moral_sentiments_for_countries({
        'start_date': str(start_date_object), 
        'end_date': str(end_date_object),
        'language': language,
        'sentiment_type': sentiment_type
    })

    figs = []
    for i, sent in enumerate(map_df['sentiment_type'].unique()):
        fig = px.choropleth(
            map_df[map_df['sentiment_type'] == sent], locations="country_iso3",
            color="doc_count",
            hover_name="country", 
            scope="europe",
            height=700,
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"{sent.capitalize()} sentiment",
            labels={'doc_count': 'Sentiment strength'}
        )      

        figs.append(dbc.Col(dcc.Graph(id=f'ms-map-graph{i}', figure=fig)))

    chunks = reversed([figs[x:x+2] for x in range(0, len(figs), 2)])

    rows = [dbc.Row(t) for t in chunks]
    return html.Div(rows)


layout = html.Div([
    html.H2("Moral sentiments"),
    html.P(
        "Moral sentiment measures the amount of moral language used based on the moral foundations theory (see https://moralfoundations.org/ for more details). "
        "It is split into five polar dimensions care/harm, fairness/cheating, loyalty/betrayal, authority/subversion, and sanctity/degradation."
    ),
    dbc.Row([
        dbc.Col(    # TODO: fix this back tho use the "date_range_col" from common.py
            dbc.FormGroup(
                [
                    dbc.Label("Date range", html_for="date-range-filter"),
                    html.Br(),
                    dcc.DatePickerRange(
                        id='date-range-filter',
                        display_format='YYYY-MM-DD',
                        min_date_allowed=config_min_date,
                        max_date_allowed=config_max_date,
                        start_date="2020-03-01",
                        end_date="2020-04-01"
                    ),
                ]
            ),
            width=3,
        ),
        dbc.Col(width=5),
        language_col,
        dbc.Col([
            dbc.Label("Sentiment"),
            dbc.Select(
                id='ms-sentiment-dropdown',
                options=config_available_sentiments,
                value=config_available_sentiments[0]["value"]
            ),
        ], width=2)
    ], form=True),
    dcc.Loading(
        id="analyses-section",
        type="default",
        fullscreen=True,
        style={'backgroundColor': 'rgba(0,0,0,0.5)'},
        children=[
            dcc.Graph(
                id='ms-timeline-graph'
            ),
            html.Div(
                id='ms-maps',
                style={'backgroundColor': 'white'}
            )
        ]
    )
])