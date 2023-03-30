from typing import Dict, List
from collections import defaultdict
from pathlib import Path
from textwrap import dedent, indent

from bs4 import BeautifulSoup


DEFAULT_HEADER = '<kwlist ecf_filename="" language="swahili" encoding="UTF-8" compareNormalize="lowercase" version="">'


class Query:
    def __init__(self, kwid: str, kwtext: str):
        self.kwid = kwid
        self.kwtext = kwtext.lower().split()
        self.is_word = (len(self.kwtext)) == 1

    def __str__(self):
        return f"Query(kwid={self.kwid}, kwtext={self.kwtext})"

    def __repr__(self):
        return self.__str__()
        


class Queries:
    def __init__(self):
        self.kwid_to_list_queries: Dict[str, List[Query]] = defaultdict(list)


    @staticmethod
    def from_str(xml_str: str) -> "Queries":
        queries = Queries()

        soup = BeautifulSoup(xml_str, features="xml")
        kws = soup.find_all("kw")
        for kw in kws:
            kwid = kw.get("kwid")
            kwtext = kw.kwtext.text
            queries.kwid_to_list_queries[kwid].append(Query(kwid=kwid, kwtext=kwtext))

        return queries

     
    @staticmethod
    def from_file(queries_filepath: str) -> "Queries":
        queries_filepath_ = Path(queries_filepath)
        assert queries_filepath_.is_file(), f"Queries file not found: {queries_filepath_}"
        assert queries_filepath_.suffix == ".xml", f"Queries file must be an XML file: {queries_filepath_}"
        
        with open(queries_filepath) as queries_file:
            xml_str = queries_file.read()
        
        return Queries.from_str(xml_str)

    
    @staticmethod
    def from_list_of_queries(list_queries: List[Query]) -> "Queries":
        queries = Queries()
        for query in list_queries:
            queries.kwid_to_list_queries[query.kwid].append(query)
        return queries
    
    
    def to_xml(self, header: str=DEFAULT_HEADER, prettify: bool=False) -> str:
        xml = header + "\n"
        
        for kwid, list_queries in self.kwid_to_list_queries.items():
            for query in list_queries:
                kwtext = " ".join(query.kwtext)
                str_to_append = dedent(f"""\
                <kw kwid="{kwid}">
                    <kwtext>{kwtext}</kwtext>
                </kw>""")
                xml += indent(str_to_append, "\t") + "\n"
        
        xml += "\n</kwlist>\n"
        
        if prettify:
            return BeautifulSoup(xml, "xml").prettify()
        else:
            return xml
