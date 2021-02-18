import os
import duckdb
import pandas as pd
import datetime
import time
from contextlib import contextmanager
import pycountry

DATABASE_PATH = os.environ.get("DATABASE_PATH", "database/database.db")


@contextmanager
def db_connection():
    conn = duckdb.connect(
        DATABASE_PATH,
        read_only=True,
    )
    yield conn
    conn.close()


def get_min_and_max_dates():
    with db_connection() as conn:
        query = "SELECT MIN(date_publish), MAX(date_publish) FROM documents"
        cursor = conn.execute(query)
        min_date, max_date = cursor.fetchone()
    return min_date.date(), max_date.date()

def get_available_languages():
    languages = []
    with db_connection() as conn:
        query = "SELECT DISTINCT language FROM documents"
        cursor = conn.execute(query)
        for language in cursor.fetchall():
            language = language[0]
            proper_language_name = pycountry.languages.get(alpha_2=language).name
            languages.append((proper_language_name, language))
    return languages

def get_available_sentiments():
    sentiments = []
    with db_connection() as conn:
        query = "SELECT DISTINCT sentiment_type FROM moral_sentiment_scores"
        cursor = conn.execute(query)
        for sentiment in cursor.fetchall():
            sentiments.append(sentiment[0])
    return sentiments
    

def generate_where_conditions(conditions): # TODO: switch conditions dict to kwargs
    where_parts = []

    if 'start_date' in conditions and 'end_date' in conditions:
        start = datetime.datetime.strptime(conditions['start_date'], "%Y-%m-%d").isoformat()
        end = datetime.datetime.strptime(conditions['end_date'], "%Y-%m-%d").isoformat()

        where_parts.append(f"d.date_publish >= '{start}' AND d.date_publish <= '{end}'")

    if 'language' in conditions and len(conditions['language']) > 0:
        where_parts.append(f"d.language = '{conditions['language']}'")

    if 'mentions' in conditions:
        where_parts.append(f"d.mention_country ='{conditions['mentions']}'")

    if 'sentiment' in conditions:
        where_parts.append(f"m.sentiment= '{conditions['sentiment']}'")

    if 'sentiment_type' in conditions and len(conditions['sentiment_type']) > 0:
        where_parts.append(f"m.sentiment_type = '{conditions['sentiment_type']}'")

    if len(where_parts) > 0:
        return "WHERE " + " AND ".join(where_parts)

    return ""

def get_sentiment_hist_df(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            "SELECT date_trunc('day', date_publish) AS date, sentiment, COUNT(sentiment) AS articles",
            "FROM documents AS d",
            "JOIN mbert_sentiment AS m ON d.document_id = m.document_id",
            where_clause,
            "GROUP BY date, sentiment",
            "ORDER BY date",
        ])
        df = conn.execute(query).fetchdf()
    return df

def get_moral_sentiment_hist_df(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            f"SELECT date_trunc('day', date_publish) AS date, sentiment_type, SUM(score) AS sum FROM documents AS d JOIN moral_sentiment_scores AS m ON d.document_id = m.document_id",
            where_clause,
            "GROUP BY date, sentiment_type",
            "ORDER BY date",
        ])
        df = conn.execute(query).fetchdf()

    return df

def get_moral_sentiments_for_countries(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            "SELECT country, sentiment_type, SUM(score) AS doc_count FROM documents AS d JOIN moral_sentiment_scores AS m ON d.document_id = m.document_id",
            where_clause,
            "GROUP BY country, sentiment_type"
        ])
        df = conn.execute(query).fetchdf()
    add_iso3_col(df, "country")
    return df    

def alpha2_to_alpha3(cc2):
    return pycountry.countries.get(alpha_2=cc2).alpha_3


def add_iso3_col(df, country_col, iso3_col="country_iso3"):
    df[iso3_col] = df[country_col].map(alpha2_to_alpha3)


def add_language_name_col(df, language_code_col, language_col="proper_language"):
    df[language_col] = df[language_code_col].map(lambda x: pycountry.languages.get(alpha_2=x).name)


def get_country_pos_neg_sentiment_counts(conditions):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            "SELECT country, COUNT(d.document_id) AS doc_count",
            "FROM documents AS d",
            "JOIN mbert_sentiment AS m ON d.document_id = m.document_id",
            where_clause,
            "GROUP BY country",
        ])
        df = conn.execute(query).fetchdf()
    add_iso3_col(df, "country")
    return df


def get_country_mention_pos_neg_sentiment_counts(conditions):
    where_clause = generate_where_conditions(conditions)

    with db_connection() as conn:
        query = " ".join([
            "SELECT mention_country, COUNT(d.document_id) AS doc_count",
            "FROM documents AS d",
            "JOIN mbert_sentiment AS m ON d.document_id = m.document_id",
            "JOIN country_mentions as cm ON cm.document_id = m.document_id",
            where_clause,
            "GROUP BY mention_country",
        ])
        df = conn.execute(query).fetchdf()
    add_iso3_col(df, "mention_country")
    return df

def get_language_distribution():
    with db_connection() as conn:
        query = " ".join([
            "SELECT language AS lang_code, COUNT(language) AS Count FROM documents GROUP BY language",
        ])
        df = pd.read_sql_query(query, conn)
        add_language_name_col(df, "lang_code", "Language")  
    return df[['Language', 'Count']]

def get_language_timeline():
    with db_connection() as conn:
        query = " ".join([
            "SELECT language AS lang_code, COUNT(language) as count, date_publish FROM documents GROUP BY language, (date_publish / 86400) ORDER BY date_publish",
        ])
        df = pd.read_sql_query(query, conn)
        add_language_name_col(df, "lang_code", "language")  
        df['date'] = pd.to_datetime(df['date_publish'], unit='s').dt.floor('d')
    return df

if __name__ == "__main__":
    print(get_language_timeline())
    #print(get_moral_sentiment_hist_df({'start_date': "2020-03-01", 'end_date': "2020-03-02"}))
