cnf("DATABASE_DIR", pjoin(WORK, "database"))
DATABASE_SCHEMA = normpath(pjoin(workflow.current_basedir, "..", "..", "database", "database_schema.sql"))
DATABASE = pjoin(DATABASE_DIR, "database.db")


rule create_db:
    input:
        DATABASE_SCHEMA 
    output:
        DATABASE
    shell:
        "cat {input} | sqlite3 {output}"


rule load_mbert_sentiment:
    input:
        database = DATABASE,
        jsonl = MBERT_SENTIMENT
    output:
        touch(pjoin(DATABASE_DIR, ".mbert_sentiment_imported"))
    shell:
        "zstdcat -T0 {input.jsonl} | python -m database.digest_mbert_sentiment_jsonl {input.database}"


rule load_moral_sentiment:
    input:
        database = DATABASE,
        jsonls = dynamic(pjoin(ANALYSES, "moral_sentiment.{lang}.jsonl.zstd"))
    output:
        touch(pjoin(DATABASE_DIR, ".moral_sentiment_imported"))
    shell:
        "zstdcat -T0 {input.jsonls} | python -m database.digest_mbert_sentiment_jsonl {input.database}"


rule load_country_mentions:
    input:
        database = DATABASE,
        jsonl = MBERT_SENTIMENT
    output:
        touch(pjoin(DATABASE_DIR, ".country_mentions_imported"))
    shell:
        "zstdcat -T0 {input.jsonl} | python -m database.digest_country_mentions_jsonl {input.database}"


rule database_all:
    input:
        rules.load_mbert_sentiment.output,
        rules.load_moral_sentiment.output,
        rules.load_country_mentions.output
