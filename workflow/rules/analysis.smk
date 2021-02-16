cnf("ANALYSES", pjoin(WORK, "analyses"))
cnf("COUNTRY_MENTION", pjoin(ANALYSES, "country_mention.jsonl.zstd"))
cnf("MBERT_SENTIMENT", pjoin(ANALYSES, "mbert_sentiment.jsonl.zstd"))
MUSE_LANGS, = glob_wildcards(MUSE + "/wiki.multi.{lang}.vec")
MORAL_SENTIMENT_ALL = [pjoin(ANALYSES, f"moral_sentiment.{lang}.jsonl.zstd") for lang in MUSE_LANGS]


rule get_country_mention:
    input:
        COVIDSTATEBROADCASTER
    output:
        COUNTRY_MENTION
    shell:
        "zstdcat -T0 {input} | python -m analysis.country_mention | zstd -T0 -14 -f - -o {output}"


rule get_moral_sentiment_one:
    input:
        corpus = COVIDSTATEBROADCASTER,
        muse = dynamic(pjoin(MUSE, "wiki.multi.{langcode}.vec")),
        mft_sentiment_word_pairs = MFT_SENTIMENT_WORD_PAIRS
    output:
        pjoin(ANALYSES, "moral_sentiment.{lang}.jsonl.zstd")
    shell:
        "zstdcat -T0 {input.corpus} | MFT_SENTIMENT_WORD_PAIRS={input.mft_sentiment_word_pairs} python -m analysis.moral_sentiment_baseline {lang} | zstd -T0 -14 -f - -o {output}"


rule get_moral_sentiment_all:
    input:
        dynamic(pjoin(ANALYSES, "moral_sentiment.{lang}.jsonl.zstd"))
    output:
        touch(pjoin(ANALYSES, ".moral_sentiment_all"))


rule get_mbert_sentiment:
    input:
        COVIDSTATEBROADCASTER,
        news_sentiment_model = NEWS_SENTIMENT_MODEL
    output:
        MBERT_SENTIMENT
    shell:
        "zstdcat -T0 {input} | NEWS_SENTIMENT_MODEL={input.news_sentiment_model} python -m analysis.mbert_headlines --batch-size 512 | zstd -T0 -14 -f - -o {output}"
