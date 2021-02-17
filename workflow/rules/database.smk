cnf("DATABASE_DIR", pjoin(WORK, "database"))
DATABASE_SCHEMA = normpath(pjoin(workflow.current_basedir, "..", "..", "database", "database_schema.sql"))
DATABASE = pjoin(DATABASE_DIR, "database.db")


rule create_import_db:
    input:
        schema = ancient(DATABASE_SCHEMA),  # Must manually delete database to rebuild
        doc_jsonl = COVIDSTATEBROADCASTERFILTERED,
        mbert_jsonl = MBERT_SENTIMENT,
        moral_jsonls = all_moral_sentiments,
        countries_jsonl = COUNTRY_MENTION,
    output:
        DATABASE
    shell:
        "cat {input.schema} | sqlite3 {output} && "
        "echo 'PRAGMA journal_mode = WAL; PRAGMA synchronous = OFF;' | sqlite3 {output} && "
        "zstdcat -T0 {input.doc_jsonl} | python -m database.digest_document_jsonl {output} && "
        "zstdcat -T0 {input.mbert_jsonl} | python -m database.digest_mbert_sentiment_jsonl {output} && "
        "zstdcat -T0 {input.moral_jsonls} | python -m database.digest_moral_sentiment_jsonl {output} && "
        "zstdcat -T0 {input.countries_jsonl} | python -m database.digest_country_mentions_jsonl {output} && "
        "echo 'PRAGMA synchronous = NORMAL;' | sqlite3 {output}"
