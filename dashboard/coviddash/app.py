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
from .view_mentions import layout as mentions_layout
from .view_main import layout as main_layout
from .view_moral import layout as moral_layout
from .view_news import layout as news_layout


from .common import config_available_languages, config_min_date, config_max_date

__all__ = ["server"]

server = app.server

page_layouts = {
    "/": main_layout,
    "/news/": news_layout,
    "/moral/": moral_layout,
    "/mentions/": mentions_layout
}

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def page_router(pathname):
    return page_layouts.get(pathname, page_layouts["/"])


app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),

    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Introduction", href="/")),
            dbc.NavItem(dbc.NavLink("News from: countries", href="/news/")),
            dbc.NavItem(dbc.NavLink("News @mentioning countries", href="/mentions/")),
            dbc.NavItem(dbc.NavLink("Moral sentiments", href="/moral/")),
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
