_covid_searchers = None


def get_covid_searchers():
    global _covid_searchers
    if _covid_searchers is None:
        _covid_searchers = get_covid()
    return _covid_searchers
