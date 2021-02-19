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
from .common import (
    config_available_languages,
    config_min_date,
    config_max_date,
    date_range_col,
    language_col,
    media_country_col,
    mention_country_col,
)

__all__ = ["layout"]

@app.callback(
    dash.dependencies.Output('timeline-graph', 'figure'),
    [dash.dependencies.Input('date-range-filter', 'start_date'),
     dash.dependencies.Input('date-range-filter', 'end_date'),
     dash.dependencies.Input('language-dropdown', 'value'),
     dash.dependencies.Input('media-country', 'value'),
     dash.dependencies.Input('mention-country', 'value')])
def update_sentiment_timeline(start_date, end_date, language, producing_country, mention_country):
    start_date_object = "1970-01-01"
    end_date_object = "2100-01-01"

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
            
    df = db_conn.get_sentiment_hist_df({
        'start_date': str(start_date_object), 
        'end_date': str(end_date_object),
        'language': language,
        'country': producing_country,
        'mentions': mention_country,
    })

    fig_timeline = px.histogram(df, x="date", y="articles", color="sentiment", barmode="stack", nbins=31)

    fig_timeline.update_layout(
        xaxis=dict(
            title='Date',
            tickmode='linear'),
        yaxis=dict(
            title="Number of news articles",
        )
    )

    return fig_timeline


layout = html.Div([
    dbc.Row([
        date_range_col,
        dbc.Col(width=3),
        language_col,
        media_country_col,
        mention_country_col,
    ], form=True),

    dcc.Graph(
        id='timeline-graph'
    )
])
