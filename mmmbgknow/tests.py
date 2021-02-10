from .pickled_searchers import get_covid


CORONA_POSITIVE = [
    ("en", "Coronavirus latest: Wider variant spread projected, Finland prepares vaccine passport, 400 new cases"),
    ("fi", "50 vuotta täyttävä Jari Litmanen sairasti keväällä koronan – kärsii yhä jälkioireista: \"Fyysinen rasitus kolahtaa kovasti\""),
    ("sv", "Skyddet gäller alla varianter av coronaviruset – även de nya, dock som sagt med olika verkningsgrad. Han betonar att betydligt mer data behövs för att dra säkra slutsatser om den sydafrikanska varianten, liksom en annan ny variant som nyligen upptäckts i Brasilien."),
]

covid = get_covid()

for lang, title in CORONA_POSITIVE:
    assert covid[lang].match(title.lower().encode("utf-8")), f"not found {lang}: {title}"
