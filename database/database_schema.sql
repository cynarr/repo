CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
	canon_url TEXT UNIQUE,
	date_publish INTEGER,	-- Unix format dates
	title TEXT,
	country TEXT,
	language TEXT
);

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
