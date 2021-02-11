cnf("ANALYSES", pjoin(WORK, "analyses"))
cnf("COUNTRY_MENTION", pjoin(ANALYSES, "country_mention.jsonl.zstd"))


rule get_country_mention:
    input:
        COVIDMARCH
    output:
        COUNTRY_MENTION
    shell:
        "zstdcat {input} | python -m analysis.country_mention | zstd -T0 -14 -f - -o {output}"
