# -*- coding: utf-8 -*-
# Run this file and navigate to http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

default_layout = {
    'autosize': True,
    'xaxis': {'title': None},
    'yaxis': {'title': None},
    'margin': {'l': 40, 'r': 20, 't': 40, 'b': 10},
    'paper_bgcolor': '#303030',
    'plot_bgcolor': '#303030',
    'hovermode': 'x',
}

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css',
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.DataFrame({
    "Date, 2020": ["March 1", "March 2", "March 3", "March 4", "March 5", "March 6"],
    "Number of articles": [600, 100, 55, 3000, 500, 1000],
    "Sentiment": ["Positive", "Negative", "Negative", "Positive", "Positive", "Neutral"]
})

fig_timeline = px.bar(df, x="Date, 2020", y="Number of articles", color="Sentiment", barmode="group")
fig_map = px.choropleth(locations=["UK", "Finland", "Sweden"], locationmode="ISO-3", scope="europe",
                        width=1000, height=1000, color_continuous_scale="Blues")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

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