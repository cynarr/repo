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