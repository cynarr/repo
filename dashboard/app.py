# -*- coding: utf-8 -*-
# Run this file and navigate to http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import flask

flask_app = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    server=flask_app,
    url_base_pathname="/",
    external_stylesheets=[
        dbc.themes.SLATE,
        "https://use.fontawesome.com/releases/v5.9.0/css/all.css", ],
    meta_tags=[{
        "name": "description",
        "content": "COVID-19 European news dashboard"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}])

df = pd.DataFrame({
    "Number of articles": [602, 100, 55, 3444, 500, 1000, 600, 100, 55, 3000, 500, 2654, 600, 100, 89, 2987, 500, 1345,
                           600, 100, 55, 3212, 500, 1000, 55, 100, 55, 3222, 500, 899, 600],
    "Sentiment": ["Positive", "Negative", "Positive", "Negative", "Positive", "Negative", "Positive", "Negative",
    "Positive", "Negative", "Positive", "Negative", "Positive", "Negative", "Positive", "Negative", "Positive", "Negative",
    "Positive", "Negative", "Positive", "Negative", "Positive", "Negative", "Positive", "Negative", "Positive", "Negative",
    "Positive", "Negative", "Positive"]
})
x = ["2020-03-01", "2020-03-02","2020-03-03","2020-03-04","2020-03-05","2020-03-06","2020-03-07","2020-03-08","2020-03-09",
      "2020-03-10","2020-03-11","2020-03-12","2020-03-13","2020-03-14","2020-03-15","2020-03-16","2020-03-17","2020-03-18",
      "2020-03-19","2020-03-20","2020-03-21","2020-03-22","2020-03-23","2020-03-24","2020-03-25","2020-03-26","2020-03-27",
      "2020-03-28","2020-03-29","2020-03-30","2020-03-31"]

fig_timeline = px.histogram(df, x=x, y="Number of articles", color="Sentiment", barmode="stack",
                            title="News sentiment on the COVID-19 pandemic in March 2020", nbins=31)

fig_timeline.update_layout(
    xaxis=dict(
        title='Date',
        tickmode='linear'),
    yaxis=dict(
        title="Number of news articles",
    )
)

fig_map = px.choropleth(locations=["UK", "Finland", "Sweden"], locationmode="ISO-3", scope="europe",
                        width=1000, height=1000, color_continuous_scale="Blues")

app.layout = html.Div(children=[
    html.H1(children='COVID-19 European news dashboard'),

    html.Div(children='''
        EMBEDDIA Hackathon 2021
    '''),

    html.Div(children='''
    Mood-Mapping Muppets
'''),

    dcc.Graph(
        id='timeline-graph',
        figure=fig_timeline
    ),
    dcc.Graph(
        id='map-graph',
        figure=fig_map
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
