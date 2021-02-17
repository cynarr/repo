import os
import sqlite3
import pandas as pd
import datetime
import time
from contextlib import contextmanager
import pycountry

DATABASE_PATH = os.environ.get("DATABASE_PATH", "database/database.db")


@contextmanager
def db_connection():
    with sqlite3.connect(
        f"file:{DATABASE_PATH}?mode=ro",
        check_same_thread=False,
        uri=True,
    ) as conn:
        yield conn


def get_min_and_max_dates():
    with db_connection() as conn:
        query = "SELECT MIN(date_publish) - 86400, MAX(date_publish) + 86400 FROM documents"
        cursor = conn.execute(query)
        min_date, max_date = next(cursor)
    return min_date, max_date

def get_available_languages():
    languages = []
    with db_connection() as conn:
        query = "SELECT DISTINCT language FROM documents"
        cursor = conn.execute(query)
        for language in cursor:
            language = language[0]
            proper_language_name = pycountry.languages.get(alpha_2=language).name
            languages.append((proper_language_name, language))
    return languages

def generate_where_conditions(conditions): # TODO: switch conditions dict to kwargs
    where_parts = []

    if 'start_date' in conditions and 'end_date' in conditions:
        start = int(time.mktime(datetime.datetime.strptime(conditions['start_date'], "%Y-%m-%d").timetuple()))
        end = int(time.mktime(datetime.datetime.strptime(conditions['end_date'], "%Y-%m-%d").timetuple()))

        where_parts.append(f"d.date_publish > {start} AND d.date_publish < {end}")

    if 'language' in conditions and len(conditions['language']) > 0:
        where_parts.append(f"d.language = '{conditions['language']}'")

    if 'mentions' in conditions:
        where_parts.append(f"d.mention_country ='{conditions['mentions']}'")

    if len(where_parts) > 0:
        return "WHERE " + " AND ".join(where_parts)

    return ""

def get_sentiment_hist_df(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = f'SELECT date_publish FROM documents AS d {where_clause} ORDER BY d.date_publish'
        df = pd.read_sql_query(query, conn)
        df = (pd.to_datetime(df['date_publish'], unit='s')
            .dt.floor('d')
            .value_counts()
            .rename_axis('date')
            .reset_index(name='Number of articles'))

        df["Sentiment"] = "Positive" # TODO: Get actual sentiments
    return df

def get_moral_sentiment_hist_df(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            f"SELECT date_publish, sentiment_type, score FROM documents AS d JOIN moral_sentiment_scores AS m ON d.canon_url = m.canon_url",
            where_clause,
            "ORDER BY d.date_publish"
        ])
        df = pd.read_sql_query(query, conn)
        df['date'] = pd.to_datetime(df['date_publish'], unit='s').dt.floor('d')

    return (df.groupby(['date', 'sentiment_type'])['score']
        .agg(['sum','count'])
        .reset_index())

def get_counts_for_countries():
    languages = []
    with db_connection() as conn:
        query = "SELECT country, COUNT(country) AS doc_count FROM documents GROUP BY country"
        df = pd.read_sql_query(query, conn)
    add_iso3_col(df, "country")
    return df    

def alpha2_to_alpha3(cc2):
    return pycountry.countries.get(alpha_2=cc2).alpha_3


def add_iso3_col(df, country_col, iso3_col="country_iso3"):
    df[iso3_col] = df[country_col].map(alpha2_to_alpha3)


def get_country_pos_neg_sentiment_counts(conditions):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            "SELECT country, sentiment, COUNT(d.document_id) AS doc_count",
            "FROM documents AS d",
            "JOIN mbert_sentiment AS m ON d.document_id = m.document_id",
            where_clause,
            "GROUP BY country, sentiment",
        ])
        df = pd.read_sql_query(query, conn)
    add_iso3_col(df, "country")
    return df


def get_country_mention_pos_neg_sentiment_counts(conditions):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            "SELECT mention_country, sentiment, COUNT(d.document_id) AS doc_count",
            "FROM documents AS d",
            "JOIN mbert_sentiment AS m ON d.document_id = m.document_id",
            "JOIN country_mentions as cm ON cm.document_id = m.document_id",
            where_clause,
            "GROUP BY mention_country, sentiment",
        ])
        df = pd.read_sql_query(query, conn)
    add_iso3_col(df, "mention_country")
    return df


if __name__ == "__main__":
    print(get_counts_for_countries())
    #print(get_moral_sentiment_hist_df({'start_date': "2020-03-01", 'end_date': "2020-03-02"}))
