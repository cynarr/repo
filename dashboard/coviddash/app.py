# -*- coding: utf-8 -*-
# Run this file and navigate to http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from .base import app, TITLE
from .view_animated import layout as animated_layout
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
    "/mentions/": mentions_layout,
    "/animated/": animated_layout,
}

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def page_router(pathname):
    return page_layouts.get(pathname, page_layouts["/"])


app.layout = html.Div(
    className="dash-bootstrap",
    children=[
        dcc.Location(id='url', refresh=False),

        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("❓ Introduction", href="/")),
                dbc.DropdownMenu(
                    label="😀/😢 Polar sentiments…",
                    children=[
                        dbc.DropdownMenuItem("📅 …in time", href="/news/"),
                        dbc.DropdownMenuItem("🌍 …across countries", href="/mentions/"),
                        dbc.DropdownMenuItem("⏩ …animated", href="/animated/"),
                    ],
                    nav=True,
                    in_navbar=True,
                    color="primary",
                ),
                dbc.NavItem(dbc.NavLink("⚖️ Moral sentiments", href="/moral/")),
            ],
            brand="😷　" + TITLE,
            brand_href="/",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="py-md-3"),
        html.Div([
            html.A("View our repository on GitHub ❤️", href="https://github.com/mood-mapping-muppets/repo", target="_blank"),
        ], style={"background-color": "#2d3d50", "padding": "20px", "text-align": "center", "vertical-align": "middle"})
    ]
)

app.validation_layout = html.Div([
    app.layout,
    *page_layouts.values(),
])
