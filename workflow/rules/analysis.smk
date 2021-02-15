cnf("ANALYSES", pjoin(WORK, "analyses"))
cnf("COUNTRY_MENTION", pjoin(ANALYSES, "country_mention.jsonl.zstd"))
cnf("MBERT_SENTIMENT", pjoin(ANALYSES, "mbert_sentiment.jsonl.zstd"))


rule get_country_mention:
    input:
        COVIDSTATEBROADCASTER
    output:
        COUNTRY_MENTION
    shell:
        "zstdcat -T0 {input} | python -m analysis.country_mention | zstd -T0 -14 -f - -o {output}"


rule get_mft_dictionary:
    shell:
        "curl -J -L https://osf.io/whjt2/download > data/mfd2.0.dic"


rule generate_moral_sentiment_pairs:
    shell:
        "python -m analysis.sentiment_antonym_pair_util"


rule get_mbert_sentiment:
    input:
        COVIDSTATEBROADCASTER
    output:
        MBERT_SENTIMENT
    shell:
        "zstdcat -T0 {input} | python -m analysis.mbert_headlines --batch-size 512 | zstd -T0 -14 -f - -o {output}"
