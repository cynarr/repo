import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import date

from .base import app
from . import database_conn as db_conn
from .common import config_available_languages, config_min_date, config_max_date, load_wrap


__all__ = ["layout"]


@app.callback(
    Output('mention-map', 'figure'),
    [Input('filter-dates', 'start_date'),
     Input('filter-dates', 'end_date'),
     Input('polarity-selector', 'value')])
def update_choropleth(start_date, end_date, polarity):
    start_date_object = "1970-01-01"
    end_date_object = "2100-01-01"

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)

    df = db_conn.get_country_mention_pos_neg_sentiment_counts({
        'start_date': str(start_date_object),
        'end_date': str(end_date_object),
    })
    return px.choropleth(
        df[df["sentiment"] == polarity],
        locations="country_iso3",
        color="doc_count",
        locationmode="ISO-3",
        scope="europe",
        width=1000,
        height=1000
    ).update_layout(
        dragmode=False,
    )


layout = html.Div([
    html.H3(children='Filters'),

    html.Div([
        dcc.DatePickerRange(
            id='filter-dates',
            display_format='YYYY-MM-DD',
            min_date_allowed=config_min_date,
            max_date_allowed=config_max_date,
            initial_visible_month=config_min_date,
            start_date=config_min_date,
            end_date=config_max_date
        ),
        dcc.RadioItems(
            id='polarity-selector',
            options=[
                {'label': 'Positive', 'value': 'positive'},
                {'label': 'Neutral', 'value': 'neutral'},
                {'label': 'Negative', 'value': 'negative'}
            ],
            value='positive'
        ),
    ]),

    load_wrap([
        dcc.Graph(
            id='mention-map',
            config=dict(
                scrollZoom=False,
                modeBarButtonsToRemove=['pan2d'],
            ),
        )
    ])
])
