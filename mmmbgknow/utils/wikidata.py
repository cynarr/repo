from SPARQLWrapper import SPARQLWrapper, JSON, __agent__ as __sparqlwrapper_agent__


class Wikidata:
    __agent__ = (
        "Mood Mapping Muppet's Covid Mood Map/0.0 " +
        "(https://github.com/mood-mapping-muppets/repo/) " +
        __sparqlwrapper_agent__
    )

    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent=self.__agent__)

    def query(self, query_str):
        self.sparql.setQuery(query_str)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        return results['results']['bindings']
