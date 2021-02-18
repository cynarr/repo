import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import date

from .base import app
from . import database_conn as db_conn
from .common import config_available_languages, config_min_date, config_max_date, load_wrap, mk_date_range_col, language_col, media_country_col, mention_country_col


__all__ = ["layout"]


@app.callback(
    Output('mention-map', 'figure'),
    [Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date'),
     Input('mode-selector', 'value'),
     Input('polarity-selector', 'value'),
     Input('language-dropdown', 'value'),
     Input('media-country', 'value'),
     Input('mention-country', 'value')])
def update_choropleth(start_date, end_date, mode, polarity, language, producing_country, mention_country):
    start_date_object = "1970-01-01"
    end_date_object = "2100-01-01"

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)

    conditions = {
        'start_date': str(start_date_object),
        'end_date': str(end_date_object),
        'sentiment': polarity,
        'language': language,
        'country': producing_country,
        'mentions': mention_country,
    }

    df = db_conn.get_country_grouped_sentiment(mode == "mention", conditions)
    return px.choropleth(
        df,
        locations="country_iso3",
        color="summary" if polarity == "summary" else "doc_count",
        locationmode="ISO-3",
        scope="europe",
        width=1000,
        height=1000
    ).update_layout(
        dragmode=False,
    )


@app.callback(Output('media-country', 'value'), [Input('mode-selector', 'value')])
def clear_media_country(value):
    return ""


@app.callback(Output('mention-country', 'value'), [Input('mode-selector', 'value')])
def clear_mention_country(value):
    return ""


@app.callback(
    Output('media-country-col', 'style'),
    [Input('mode-selector', 'value')])
def hide_media_country(mode):
    if mode == "mention":
        return {}
    else:
        return {"display": "none"}


@app.callback(
    Output('mention-country-col', 'style'),
    [Input('mode-selector', 'value')])
def hide_mention_country(mode):
    if mode == "mention":
        return {"display": "none"}
    else:
        return {}


layout = html.Div([
    dbc.Row([
        mk_date_range_col(width=4),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Countries are", html_for="polarity-selector"),
                    dbc.Select(
                        id='mode-selector',
                        options=[
                            {'label': 'Producing news', 'value': 'produce'},
                            {'label': 'Mentioned in news', 'value': 'mention'},
                        ],
                        value='mentions'
                    ),
                ]
            ),
            width=2,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Sentiment polarity", html_for="polarity-selector"),
                    dbc.Select(
                        id='polarity-selector',
                        options=[
                            {'label': 'Summary', 'value': 'summary'},
                            {'label': 'Positive', 'value': 'positive'},
                            {'label': 'Neutral', 'value': 'neutral'},
                            {'label': 'Negative', 'value': 'negative'}
                        ],
                        value='summary'
                    ),
                ]
            ),
            width=2,
        ),
        language_col,
        media_country_col,
        mention_country_col,
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
