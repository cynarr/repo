cnf("ANALYSES", pjoin(WORK, "analyses"))
cnf("COUNTRY_MENTION", pjoin(ANALYSES, "country_mention.jsonl.zstd"))


rule get_country_mention:
    input:
        COVIDMARCH
    output:
        COUNTRY_MENTION
    shell:
        "zstdcat {input} | python -m analysis.country_mention | zstd -T0 -14 -f - -o {output}"

rule get_mft_dictionary:
    shell:
        "curl -J -L https://osf.io/whjt2/download > data/mfd2.0.dic"