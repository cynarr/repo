rule mmmbgknow_all:
    input:
        "mmmbgknow/data/fqdn_country.csv",
        "mmmbgknow/data/lang_country.csv",
        "mmmbgknow/data/tld_country.csv",
        "mmmbgknow/data/euro_language.csv",
        "mmmbgknow/data/euro_country.csv"

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
