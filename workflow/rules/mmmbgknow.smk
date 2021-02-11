rule mmmbgknow_all:
    input:
        "mmmbgknow/data/fqdn_country.csv",
        "mmmbgknow/data/lang_country.csv",
        "mmmbgknow/data/tld_country.csv",
        "mmmbgknow/data/euro_language.csv",
        "mmmbgknow/data/euro_country.csv",
        "mmmbgknow/data/country_labels.csv",
        "mmmbgknow/data/covid_labels.csv",
        "mmmbgknow/data/country_search.pkl",
        "mmmbgknow/data/covid_search.pkl"

rule get_fqdn_country:
    output:
        "mmmbgknow/data/fqdn_country.csv"
    shell:
        "python -m mmmbgknow.queries.get_fqdn_country > {output}"

rule get_lang_country:
    output:
        "mmmbgknow/data/lang_country.csv"
    shell:
        "python -m mmmbgknow.queries.get_lang_country > {output}"

rule get_tld_country:
    output:
        "mmmbgknow/data/tld_country.csv"
    shell:
        "python -m mmmbgknow.queries.get_tld_country > {output}"

rule get_euro_languages:
    output:
        "mmmbgknow/data/euro_language.csv"
    shell:
        "python -m mmmbgknow.queries.get_euro_language > {output}"

rule get_euro_country:
    output:
        "mmmbgknow/data/euro_country.csv"
    shell:
        "python -m mmmbgknow.queries.get_euro_country > {output}"

rule get_langdetect_euro_country:
    input:
        "mmmbgknow/data/langdetect_languages.csv",
        "mmmbgknow/data/euro_country.csv"
    output:
        "mmmbgknow/data/langdetect_euro_country.csv"
    shell:
        "python -m mmmbgknow.langdetect_euro > {output}"

rule get_country_labels:
    output:
        "mmmbgknow/data/country_labels.csv"
    shell:
        "python -m mmmbgknow.queries.get_country_labels > {output}"

rule get_covid_labels:
    output:
        "mmmbgknow/data/covid_labels.csv"
    shell:
        "python -m mmmbgknow.queries.get_covid_labels > {output}"

rule get_country_search_pkl:
    input:
        "mmmbgknow/data/langdetect_euro_country.csv",
        "mmmbgknow/data/country_labels.csv"
    output:
        "mmmbgknow/data/country_search.pkl"
    shell:
        "python -m mmmbgknow.searchers.country {output}"

rule get_covid_search_pkl:
    input:
        "mmmbgknow/data/langdetect_euro_country.csv",
        "mmmbgknow/data/covid_labels.csv"
    output:
        "mmmbgknow/data/covid_search.pkl"
    shell:
        "python -m mmmbgknow.searchers.covid {output}"
