DATA_DIR = pjoin(workflow.current_basedir, "..", "data")
cnf("MFD20", pjoin(DATA_DIR, "mfd2.0.dic"))
cnf("MFT_SENTIMENT_WORD_PAIRS", pjoin(DATA_DIR, "mft_sentiment_word_pairs.pkl"))
cnf("NEWS_SENTIMENT_MODEL", pjoin(DATA_DIR, "news_sentiment_model.bin"))


rule mk_data_dir:
    output:
        directory(DATA_DIR)
    shell:
        "mkdir -p {output}"


rule fetch_wordnet:
    input:
        DATA_DIR
    output:
        touch(pjoin(DATA_DIR, ".got_wordnet"))
    run:
        import nltk
        nltk.download('wordnet')


rule get_mft_dictionary:
    output:
        MFD20
    shell:
        "curl -J -L https://osf.io/whjt2/download > {output}"


rule generate_moral_sentiment_pairs:
    input:
        MFD20
    output:
        MFT_SENTIMENT_WORD_PAIRS
    shell:
        "python -m analysis.sentiment_antonym_pair_util {input} {output}"


rule download_news_sentiment_model:
    output:
        NEWS_SENTIMENT_MODEL
    shell:
        "wget -o {output} https://a3s.fi/swift/v1/AUTH_d9eb9f26c2514801b54f21e00f15f5d4/mbert_news_sentiment/pytorch_model.bin"


rule setup_all:
    input:
        generate_moral_sentiment_pairs.output,
        download_news_sentiment_model.output
