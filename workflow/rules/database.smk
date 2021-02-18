cnf("DATABASE_DIR", pjoin(WORK, "database"))
DATABASE_SCHEMA = normpath(pjoin(workflow.current_basedir, "..", "..", "database", "database_schema.sql"))
DATABASE = pjoin(DATABASE_DIR, "database.db")


rule create_import_db:
    input:
        schema = ancient(DATABASE_SCHEMA),  # Must manually delete database to rebuild
        doc_jsonl = COVIDSTATEBROADCASTERFILTERED,
        #mbert_jsonl = MBERT_SENTIMENT,
        moral_jsonls = all_moral_sentiments,
        #countries_jsonl = COUNTRY_MENTION,
    output:
        DATABASE
    run:
        import duckdb
        conn = duckdb.connect(output[0])
        c = conn.cursor()
        c.execute(open(input.schema).read())
        conn.commit()
        conn.close()
        shell(
            "zstdcat -T0 {input.doc_jsonl} | python -m database.digest_document_jsonl {output} && "
            "zstdcat -T0 {input.mbert_jsonl} | python -m database.digest_mbert_sentiment_jsonl {output} && "
            "zstdcat -T0 {input.moral_jsonls} | python -m database.digest_moral_sentiment_jsonl {output} && "
            "zstdcat -T0 {input.countries_jsonl} | python -m database.digest_country_mentions_jsonl {output}"
        )
