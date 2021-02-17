import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from .base import app


__all__ = ["layout"]


fig_map = px.choropleth(locations=["UK", "Finland", "Sweden"], locationmode="ISO-3", scope="europe",
                        width=1000, height=1000, color_continuous_scale="Blues")


def get_fig_map(location):
    pass


@app.callback(
    Output('mention-map', 'figure'),
    [Input('mention-map', 'clickData')])
def update_figure(clickData):
    if clickData is not None:
        location = clickData['points'][0]['location']
        get_fig_map(location)
    else:
        return fig_map


layout = html.Div([
    html.H3(children='Filters'),

    dcc.Graph(
        id='mention-map',
        figure=fig_map
    )
])
