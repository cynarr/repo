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
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    if polarity == "summary":
        value_col = "summary"
        min_val = df[value_col].min()
        max_val = df[value_col].max()
    else:
        value_col = "doc_count"
        min_val = 0
        max_val = df[value_col].max()
    return px.choropleth(
        df,
        range_color=(min_val, max_val),
        animation_frame="week_num",
        animation_group="week_num",
        locations="country_iso3",
        color=value_col,
        locationmode="ISO-3",
        scope="europe",
        width=1000,
        height=1000
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
    ]),

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
