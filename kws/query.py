from typing import Dict
from pathlib import Path
from bs4 import BeautifulSoup


class Query:
    def __init__(self, kwid: str, kwtext: str):
        self.kwid = kwid
        self.kwtext = kwtext.split()
        self.is_word = (len(self.kwtext)) == 1

    def __str__(self):
        return f"Query(kwid={self.kwid}, kwtext={self.kwtext})"

    def __repr__(self):
        return self.__str__()
        


class Queries:
    def __init__(self, queries_filepath: str):
        self.queries_filepath = Path(queries_filepath)
        assert self.queries_filepath.is_file(), f"Queries file not found: {queries_filepath}"
        assert self.queries_filepath.suffix == ".xml", f"Queries file must be an XML file: {queries_filepath}"
        
        self.queries = self._build_queries()

    
    def _build_queries(self) -> Dict[str, Query]:
        queries = {}
        
        with open(self.queries_filepath) as queries_file:
            xml_str = queries_file.read()
            soup = BeautifulSoup(xml_str, features="xml")

        kws = soup.find_all("kw")
        for kw in kws:
            kwid = kw.get("kwid")
            kwtext = kw.kwtext.text
            queries[kwid] = Query(kwid=kwid, kwtext=kwtext)

        return queries
