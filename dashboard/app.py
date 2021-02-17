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

import database_conn as db_conn

# Load configs for filters
config_available_languages = [{'label': 'All', 'value': ''}] 
config_available_languages += [{'label': pl, 'value': l} for pl, l in db_conn.get_available_languages()]
config_min_date, config_max_date = [date.fromtimestamp(ts) for ts in db_conn.get_min_and_max_dates()]

__all__ = ["server"]

app = dash.Dash(
    __name__,
    url_base_pathname="/",
    external_stylesheets=[
        dbc.themes.SLATE,
        "https://use.fontawesome.com/releases/v5.9.0/css/all.css", ],
    meta_tags=[{
        "name": "description",
        "content": "COVID-19 European news dashboard"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}])

server = app.server

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


fig_map = px.choropleth(locations=["UK", "Finland", "Sweden"], locationmode="ISO-3", scope="europe",
                        width=1000, height=1000, color_continuous_scale="Blues")

page_layouts = {
    "/": html.Div([
        html.H3(children='Filters'),

        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                display_format='YYYY-MM-DD',
                min_date_allowed=config_min_date,
                max_date_allowed=config_max_date,
                initial_visible_month=config_min_date,
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
    ]),
    "/mentions/": html.Div([
        html.H3(children='Filters'),

        dcc.Graph(
            id='map-graph',
            figure=fig_map
        )
    ])
}

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def page_router(pathname):
    return page_layouts.get(pathname, page_layouts["/"])


app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),

    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("News from: countries", href="/")),
            dbc.NavItem(dbc.NavLink("News @mentioning countries", href="/mentions/")),
        ],
        brand="COVID-19 mood map",
        brand_href="/",
        color="primary",
        dark=True,
    ),

    dbc.Container([html.Div(id="page-content")])
])

app.validation_layout = html.Div([
    app.layout,
    *page_layouts.values(),
])

if __name__ == '__main__':
    app.run_server(debug=True)
