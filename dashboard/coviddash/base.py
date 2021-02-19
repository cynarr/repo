import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    url_base_pathname="/",
    external_stylesheets=[
        "https://rawcdn.githack.com/tcbegley/dash-bootstrap-css/7ea5edb88ca7ae4814ea204503a464f1f4dd23ff/dist/flatly/bootstrap.min.css",
        "https://use.fontawesome.com/releases/v5.9.0/css/all.css"
    ], meta_tags=[
        {
            "name": "description",
            "content": "COVID-19 European news dashboard"
        },
        {
            "name": "viewport",
            "content": "width=device-width,initial-scale=1.0"
        }
    ],
    serve_locally=False
)
