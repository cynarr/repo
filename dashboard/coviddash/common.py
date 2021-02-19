from datetime import date
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from . import database_conn as db_conn


# Load configs for filters
config_available_languages = [{'label': 'All', 'value': ''}] 
config_available_languages += [{'label': pl, 'value': l} for pl, l in db_conn.get_available_languages()]

config_min_date, config_max_date = db_conn.get_min_and_max_dates()

config_available_sentiments = [{'label': 'All', 'value': ''}]
config_available_sentiments += [{'label': s, 'value': s} for s in db_conn.get_available_sentiments()]

config_available_producing_countries = [{'label': 'All', 'value': ''}]
config_available_producing_countries += [{'label': n, 'value': s} for n, s in db_conn.get_available_producing_countries()]

config_available_mentioned_countries = [{'label': 'All', 'value': ''}]
config_available_mentioned_countries += [{'label': n, 'value': s} for n, s in db_conn.get_available_mentioned_countries()]


def load_wrap(children):
    return dcc.Loading(
        type="default",
        fullscreen=True,
        style={'backgroundColor': 'rgba(0,0,0,0.5)'},
        children=children
    )


date_range_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Date range", html_for="date-range-filter"),
            html.Br(),
            dcc.DatePickerRange(
                id='date-range-filter',
                display_format='YYYY-MM-DD',
                min_date_allowed=config_min_date,
                max_date_allowed=config_max_date,
                start_date=config_min_date,
                end_date=config_max_date
            ),
        ]
    ),
    width=3,
)


mode_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Countries are", html_for="polarity-selector"),
            dbc.Select(
                id='mode-selector',
                options=[
                    {'label': 'Producing news', 'value': 'produce'},
                    {'label': 'Mentioned in news', 'value': 'mention'},
                ],
                value='mentions'
            ),
        ]
    ),
    width=2,
)


polarity_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Sentiment polarity", html_for="polarity-selector"),
            dbc.Select(
                id='polarity-selector',
                options=[
                    {'label': 'Summary', 'value': 'summary'},
                    {'label': 'Positive', 'value': 'positive'},
                    {'label': 'Neutral', 'value': 'neutral'},
                    {'label': 'Negative', 'value': 'negative'}
                ],
                value='summary'
            ),
        ]
    ),
    width=2,
)


language_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Language", html_for="language-dropdown"),
            dbc.Select(
                id='language-dropdown',
                options=config_available_languages,
                value=''
            )
        ]
    ),
    width=2,
)

media_country_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Producing country", html_for="media-country"),
            dbc.Select(
                id='media-country',
                options=config_available_producing_countries,
                value=''
            )
        ]
    ),
    id="media-country-col",
    width=2,
)

mention_country_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Mentioned country", html_for="mention-country"),
            dbc.Select(
                id='mention-country',
                options=config_available_mentioned_countries,
                value=''
            )
        ]
    ),
    id="mention-country-col",
    width=2,
)

map_sentiments_right_cols = [
    mode_col,
    polarity_col,
    language_col,
    media_country_col,
    mention_country_col,
]
