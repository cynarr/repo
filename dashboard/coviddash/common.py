from datetime import date
from . import database_conn as db_conn


# Load configs for filters
config_available_languages = [{'label': 'All', 'value': ''}] 
config_available_languages += [{'label': pl, 'value': l} for pl, l in db_conn.get_available_languages()]

config_min_date, config_max_date = [date.fromtimestamp(ts) for ts in db_conn.get_min_and_max_dates()]

config_available_sentiments = [{'label': 'All', 'value': ''}]
config_available_sentiments += [{'label': s, 'value': s} for s in db_conn.get_available_sentiments()]


def load_wrap(children):
    import dash_core_components as dcc
    return dcc.Loading(
        type="default",
        fullscreen=True,
        style={'backgroundColor': 'rgba(0,0,0,0.5)'},
        children=children
    )
