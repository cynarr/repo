import numpy as np
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from .common import load_wrap, map_sentiments_right_cols
from .database_conn import get_country_grouped_sentiment
from .base import app


@app.callback(
    Output('mention-map-animated', 'figure'),
    [Input('mode-selector', 'value'),
     Input('polarity-selector', 'value'),
     Input('language-dropdown', 'value'),
     Input('media-country', 'value'),
     Input('mention-country', 'value')])
def update_choropleth(mode, polarity, language, producing_country, mention_country):
    conditions = {
        'sentiment': polarity,
        'language': language,
        'country': producing_country,
        'mentions': mention_country,
    }

    df = get_country_grouped_sentiment(
        mode == "mention",
        conditions,
        week_group=True
    )
    kwargs = {}
    if polarity == "summary":
        kwargs["color"] = "summary"
        kwargs["range_color"] = (-1, 1)
    else:
        kwargs["color"] = "doc_count"
        kwargs["range_color"] = (0, df["doc_count"].max())
    return px.choropleth(
        df,
        animation_frame="week_num",
        animation_group="week_num",
        locations="country_iso3",
        labels={
            "summary": "Summary",
            "doc_count": "Number of articles",
            "week_num": "Week number"
        },
        locationmode="ISO-3",
        scope="europe",
        height=1000,
        **kwargs
    ).update_layout(
        dragmode=False,
    )


layout = html.Div([
    dbc.Row([
        dbc.Col(
            children="",
            width=4,
        ),
        *map_sentiments_right_cols,
    ], form=True),

    load_wrap([
        dcc.Graph(
            id='mention-map-animated',
            config=dict(
                scrollZoom=False,
                modeBarButtonsToRemove=['pan2d'],
            ),
        )
    ])
])
