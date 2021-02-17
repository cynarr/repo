from datetime import date
from . import database_conn as db_conn


# Load configs for filters
config_available_languages = [{'label': 'All', 'value': ''}] 
config_available_languages += [{'label': pl, 'value': l} for pl, l in db_conn.get_available_languages()]
config_min_date, config_max_date = [date.fromtimestamp(ts) for ts in db_conn.get_min_and_max_dates()]
