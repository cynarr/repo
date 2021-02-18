CREATE SEQUENCE document_id_seq START 1;

CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    canon_url TEXT UNIQUE,
    date_publish TIMESTAMP,	-- Unix format dates
    title TEXT,
    country TEXT,
    language TEXT
);

CREATE INDEX documents_country_idx ON documents (country);
CREATE INDEX documents_language_idx ON documents (language);

CREATE TABLE moral_sentiment_scores (
    document_id INTEGER,
    sentiment_type TEXT NOT NULL,
    score REAL NOT NULL
);

CREATE INDEX moral_sentiment_scores_document_id_idx ON moral_sentiment_scores (document_id);

CREATE TABLE mbert_sentiment (
    document_id INTEGER PRIMARY KEY,
    sentiment TEXT NOT NULL
);

CREATE TABLE country_mentions (
    document_id INTEGER,
    mention_country TEXT
);

CREATE INDEX country_mentions_document_id_idx ON country_mentions (document_id);
