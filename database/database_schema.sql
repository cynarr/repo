CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    canon_url TEXT UNIQUE,
    date_publish INTEGER,	-- Unix format dates
    title TEXT,
    country TEXT,
    language TEXT
);

CREATE INDEX documents_date_publish_idx ON documents (date_publish);
CREATE INDEX documents_country_idx ON documents (country);
CREATE INDEX documents_language_idx ON documents (language);

CREATE TABLE moral_sentiment_scores (
    canon_url TEXT NOT NULL,
    sentiment_type TEXT NOT NULL,
    score REAL NOT NULL,
    PRIMARY KEY (canon_url, sentiment_type)
);

CREATE TABLE mbert_sentiment (
    document_id INTEGER PRIMARY KEY,
    sentiment TEXT NOT NULL
);

CREATE TABLE country_mentions (
    pk INTEGER PRIMARY KEY,
    document_id INTEGER,
    mention_country TEXT
);

CREATE INDEX country_mentions_document_id_idx ON country_mentions (document_id);
