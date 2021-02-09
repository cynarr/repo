cnf("COVIDMARCH", pjoin(WORK, "covidmarch.jsonl.zstd"))
cnf("USENEWS_FULLTEXT", pjoin(WORK, "usenews.fulltext.jsonl.zstd"))


rule ingress_all:
    input:
        COVIDMARCH,
        USENEWS_FULLTEXT

rule get_usenews_2019:
    output:
        pjoin(WORK, "usenews.2019.RData.xz")
    shell:
        "wget -nv -O {output} 'https://files.de-1.osf.io/v1/resources/uzca3/providers/osfstorage/5fabf6e81b9cb2005a6d3aa5?action=download&direct&version=2'"

rule get_usenews_2020:
    output:
        pjoin(WORK, "usenews.2020.RData.xz")
    shell:
        "wget -nv -O {output} 'https://files.de-1.osf.io/v1/resources/uzca3/providers/osfstorage/5fabfce00ec26c00618057c8?action=download&direct&version=2'"

rule extract_rdata:
    input:
        pjoin(WORK, "{base}.RData.xz")
    output:
        temp(pjoin(WORK, "{base}.RData"))
    shell:
        "xz -dk -T0 {input}"

rule convert_rdata:
    input:
        pjoin(WORK, "{base}.RData")
    output:
        directory(pjoin(WORK, "{base}.pickles"))
    shell:
        "python -m ingress.usenews_to_pickles {input} {output}"

rule save_usenews_urls:
    input:
        pjoin(WORK, "usenews.{year}.pickles/crowdtangle{year}.pkl")
    output:
        temp(pjoin(WORK, "usenews.{year}.urls.txt"))
    shell:
        "python -m ingress.save_usenews_urls {input} > {output}"

rule cat_usenews_urls:
    input:
        urls19 = pjoin(WORK, "usenews.2019.urls.txt"),
        urls20 = pjoin(WORK, "usenews.2020.urls.txt")
    output:
        pjoin(WORK, "usenews.urls.txt")
    shell:
        "sort -u {input.urls19} {input.urls20} > {output}"

rule get_covid_march:
    output:
        COVIDMARCH
    shell:
        "python -m ingress.covidmarch | zstd -T0 -14 -f - -o {output}"

rule get_usenews_fulltext:
    input:
        pjoin(WORK, "usenews.urls.txt")
    output:
        USENEWS_FULLTEXT
    shell:
        "python -m ingress.usenews_fulltext {input} | zstd -T0 -14 -f - -o {output}"
