import dash


TITLE = "COVID-19 mood map of Europe"


app = dash.Dash(
    __name__,
    title=TITLE,
    url_base_pathname="/",
    external_stylesheets=[
        "https://rawcdn.githack.com/tcbegley/dash-bootstrap-css/7ea5edb88ca7ae4814ea204503a464f1f4dd23ff/dist/flatly/bootstrap.min.css",
        "https://use.fontawesome.com/releases/v5.9.0/css/all.css"
    ], meta_tags=[
        {
            "name": "description",
            "content": TITLE
        },
        {
            "name": "viewport",
            "content": "width=device-width,initial-scale=1.0"
        }
    ],
    serve_locally=False
)
