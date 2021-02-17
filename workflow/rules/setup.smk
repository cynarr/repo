DATA_DIR = normpath(pjoin(workflow.current_basedir, "..", "..", "data"))
cnf("MFD20", pjoin(WORK, "mfd2.0.dic"))
cnf("MFT_SENTIMENT_WORD_PAIRS", pjoin(WORK, "mft_sentiment_word_pairs.pkl"))
cnf("NEWS_SENTIMENT_MODEL", pjoin(WORK, "news_sentiment_model.bin"))
cnf("MUSE", pjoin(WORK, "muse"))
cnf("BERT_MULTILINGUAL_CASED", pjoin(WORK, "bert_multilingual_cased"))


rule mk_data_dir:
    output:
        touch(pjoin(DATA_DIR, ".dir"))
    shell:
        "mkdir -p " + DATA_DIR


rule fetch_nltk_resources:
    input:
        rules.mk_data_dir.output
    output:
        touch(pjoin(DATA_DIR, ".got_nltk_res"))
    run:
        import nltk
        nltk.download('wordnet')
        nltk.download('punkt')


rule get_mft_dictionary:
    output:
        MFD20
    shell:
        "wget -nv -O {output} https://osf.io/whjt2/download"


rule generate_moral_sentiment_pairs:
    input:
        mdf = MFD20,
        nltk_res = ancient(rules.fetch_nltk_resources.output)
    output:
        MFT_SENTIMENT_WORD_PAIRS
    shell:
        "python -m analysis.sentiment_antonym_pair_util {input.mdf} {output}"


rule download_mbert_tokenizer:
    output:
        directory(BERT_MULTILINGUAL_CASED)
    run:
        from transformers import BertTokenizerFast
        tokenizer = BertTokenizerFast.from_pretrained(
            "bert-base-multilingual-cased",
            cache_dir=pjoin(os.environ.get("TMPDIR", "/tmp/"), "transformerscache")
        ).save_pretrained(output[0])


rule download_news_sentiment_model:
    output:
        NEWS_SENTIMENT_MODEL
    shell:
        "wget -nv -O {output} https://a3s.fi/swift/v1/AUTH_d9eb9f26c2514801b54f21e00f15f5d4/mbert_news_sentiment/pytorch_model.bin"


checkpoint download_muse:
    output:
        directory(MUSE)
    run:
        from mmmbgknow.european import LANGDETECT_EURO_LANGAUGES
        shell(f"mkdir -p {MUSE}")
        for langcode in LANGDETECT_EURO_LANGAUGES:
            shell(f"cd {MUSE} && wget -nv https://dl.fbaipublicfiles.com/arrival/vectors/wiki.multi.{langcode}.vec || true")


rule setup_all:
    input:
        rules.generate_moral_sentiment_pairs.output,
        rules.download_news_sentiment_model.output,
        rules.download_muse.output
