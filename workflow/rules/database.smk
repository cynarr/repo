cnf("DATABASE_DIR", pjoin(WORK, "database"))
DATABASE_SCHEMA = normpath(pjoin(workflow.current_basedir, "..", "..", "database", "database_schema.sql"))
DATABASE = pjoin(DATABASE_DIR, "database.db")


rule create_db:
    input:
        ancient(DATABASE_SCHEMA)  # Must manually delete database to rebuild
    output:
        DATABASE
    shell:
        "cat {input} | sqlite3 {output} && "
        "echo 'PRAGMA journal_mode = WAL; PRAGMA synchronous = OFF;' | sqlite3 {output}"


rule load_documents:
    input:
        prev = rules.create_db.output,
        jsonl = COVIDSTATEBROADCASTERFILTERED
    output:
        touch(pjoin(DATABASE_DIR, ".documents"))
    shell:
        "zstdcat -T0 {input.jsonl} | python -m database.digest_document_jsonl " + DATABASE



rule load_mbert_sentiment:
    input:
        prev = rules.load_documents.output,
        jsonl = MBERT_SENTIMENT
    output:
        touch(pjoin(DATABASE_DIR, ".mbert_sentiment_imported"))
    shell:
        "zstdcat -T0 {input.jsonl} | python -m database.digest_mbert_sentiment_jsonl " + DATABASE


rule load_moral_sentiment:
    input:
        prev = rules.load_mbert_sentiment.output,
        jsonls = all_moral_sentiments
    output:
        touch(pjoin(DATABASE_DIR, ".moral_sentiment_imported"))
    shell:
        "zstdcat -T0 {input.jsonls} | python -m database.digest_moral_sentiment_jsonl " + DATABASE


rule load_country_mentions:
    input:
        prev = rules.load_moral_sentiment.output,
        jsonl = MBERT_SENTIMENT
    output:
        touch(pjoin(DATABASE_DIR, ".country_mentions_imported"))
    shell:
        "zstdcat -T0 {input.jsonl} | python -m database.digest_country_mentions_jsonl " + DATABASE


rule finalise_db:
    input:
        prev = rules.load_country_mentions.output
    output:
        touch(pjoin(DATABASE_DIR, ".db_finalised"))
    shell:
        "echo 'PRAGMA synchronous = NORMAL;' | sqlite3 " + DATABASE


rule database_all:
    input:
        rules.load_documents.output,
        rules.load_mbert_sentiment.output,
        rules.load_moral_sentiment.output,
        rules.load_country_mentions.output,
        rules.finalise_db.output
