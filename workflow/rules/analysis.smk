cnf("LOG", pjoin(WORK, "LOG"))
cnf("ANALYSES", pjoin(WORK, "analyses"))
cnf("COUNTRY_MENTION", pjoin(ANALYSES, "country_mention.jsonl.zstd"))
cnf("MBERT_SENTIMENT", pjoin(ANALYSES, "mbert_sentiment.jsonl.zstd"))
MUSE_LANGS, = glob_wildcards(MUSE + "/wiki.multi.{lang}.vec")
MORAL_SENTIMENT_ALL = [pjoin(ANALYSES, f"moral_sentiment.{lang}.jsonl.zstd") for lang in MUSE_LANGS]
cnf("COVIDSTATEBROADCASTERFILTERED", pjoin(WORK, "covidstatebroadcaster.filtered.jsonl.zstd"))


rule filter_statebroadcaster:
    input:
        COVIDSTATEBROADCASTER
    output:
        COVIDSTATEBROADCASTERFILTERED
    shell:
        "zstdcat -T0 {input} | python -m analysis.filters.no_title | python -m analysis.filters.impossible 2021-02 | zstd -T0 -14 -f - -o {output}"


rule get_country_mention:
    input:
        COVIDSTATEBROADCASTERFILTERED
    output:
        COUNTRY_MENTION
    shell:
        "zstdcat -T0 {input} | python -m analysis.country_mention | zstd -T0 -14 -f - -o {output}"


rule get_moral_sentiment_one:
    input:
        corpus = COVIDSTATEBROADCASTERFILTERED,
        muse = pjoin(MUSE, "wiki.multi.{lang}.vec"),
        mft_sentiment_word_pairs = MFT_SENTIMENT_WORD_PAIRS,
        mfd20 = MFD20,
        muse_base = MUSE,
        nltk_res = ancient(rules.fetch_nltk_resources.output)
    output:
        error_log = pjoin("moral_sentiment.{lang}.error.log"),
        moral_sentiment = pjoin(ANALYSES, "moral_sentiment.{lang}.jsonl.zstd")
    shell:
        "zstdcat -T0 {input.corpus} | MFT_SENTIMENT_WORD_PAIRS={input.mft_sentiment_word_pairs} MFD20={input.mfd20} MUSE={input.muse_base} ERRORLOG={output.error_log} python -m analysis.moral_sentiment_baseline {wildcards.lang} | zstd -T0 -14 -f - -o {output.moral_sentiment}"


def all_moral_sentiments(wildcards):
    checkpoint_output = checkpoints.download_muse.get(**wildcards).output[0]
    langcode = glob_wildcards(pjoin(
        checkpoint_output,
        "wiki.multi.{langcode}.vec"
    )).langcode
    return expand(
        pjoin(ANALYSES, "moral_sentiment.{lang}.jsonl.zstd"),
        lang=langcode
    )


rule get_moral_sentiment_all:
    input:
        all_moral_sentiments
    output:
        touch(pjoin(ANALYSES, ".moral_sentiment_all"))


rule get_mbert_sentiment:
    input:
        corpus = COVIDSTATEBROADCASTERFILTERED,
        news_sentiment_model = NEWS_SENTIMENT_MODEL,
        bert_multilingual_cased = BERT_MULTILINGUAL_CASED
    output:
        MBERT_SENTIMENT
    shell:
        "zstdcat -T0 {input.corpus} | BERT_MULTILINGUAL_CASED_PATH={input.bert_multilingual_cased} NEWS_SENTIMENT_MODEL={input.news_sentiment_model} python -m analysis.mbert_headlines --batch-size 512 | zstd -T0 -14 -f - -o {output}"
