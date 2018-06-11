# coding: utf-8
import requests
from bs4 import BeautifulSoup
from schemas import SchemaFactory
from libraries import LibraryFactory
from validators import is_doi, is_isbn, is_url, has_domain
import bibtexparser
import json
import re
import rdflib


def get_metadata(identifier, format='n3', property_keys=None, schema_names=None):
    factory = ExtractorFactory()
    extractor = factory.create_extractor(identifier=identifier, format=format, property_keys=property_keys, schema_names=schema_names)
    if not extractor:
        return False
    return extractor.get_data()


class ContentExtractor:
    content = None
    property_keys = ['title', 'description', 'url', 'image_url', 'author_name', 'date_published', 'publisher', 'language']
    mapping = {'title': ['http://ogp.me/ns#title', "http://purl.org/dc/terms/title"], 'description': ['http://ogp.me/ns#description', "http://purl.org/dc/terms/description", 'http://schema.org/description'], 'image': ['http://ogp.me/ns#image']}
    prefixes = {}
    graph = rdflib.Graph()

    def __init__(self, identifier, format='n3', mapping=None, property_keys=None):
        if property_keys:
            self.property_keys = property_keys
        if mapping:
            self.mapping = mapping
        self.format = format
        self.identifier = identifier
        self.content = self.fetch_content()
        self.build_metadata()

    def build_metadata(self):
        pass

    def get_data(self):
        if self.format == 'dict':
            return self.get_data_dict()
        elif self.format == 'json':
            return self.get_data_json()
        elif self.format == 'n3':
            return self.get_data_rdf(format=self.format)
        elif self.format == 'turtle':
            return self.get_data_rdf(format=self.format)
        elif self.format == 'json-ld':
            return self.get_data_rdf(format=self.format)
        else:
            return self.get_data_dict()

    def get_data_dict(self):
        data_dict = {}
        for property_key in self.property_keys:
            property_value = self.get_property(property_key)
            data_dict[property_key] = property_value
        return data_dict

    def get_data_json(self):
        data_dict = self.get_data_dict()
        return json.dumps(data_dict)

    def get_data_rdf(self, format='n3'):
        return self.graph.serialize(format=format).decode('utf-8')

    def fetch_content(self):
        pass

    @staticmethod
    def get_page(url, headers=None, params=None):
        response = requests.get(url, headers=headers, params=params)
        if response.encoding != 'UTF-8':
            response.encoding = 'UTF-8'
        return response.text

    def get_property(self, property_name):
        pass

    def print_graph(self):
        for s,p,o in self.graph:
            print(s + " -> " + p + " -> " + o)


class URLContentExtractor(ContentExtractor):
    schema_names = ['opengraph', 'dublincore', 'html']
    schemas = []

    def __init__(self, url, schema_names=None, **kwargs):
        super(URLContentExtractor, self).__init__(identifier=url, **kwargs)
        if schema_names:
            self.schema_names = schema_names
        self.init_schemas(self.schema_names)

    def init_schemas(self, schema_names):
        factory = SchemaFactory()
        for schema_name in schema_names:
            schema = factory.create_schema(schema_name)
            if schema:
                self.schemas.append(schema)

    def fetch_content(self):
        html = self.get_page(self.identifier)
        return BeautifulSoup(html, "lxml")

    def build_metadata(self):
        self.get_json_ld()
        self.get_rdfa()
        self.get_metatags()

    def get_data_dict(self):
        data_dict = {}
        for s,p,o in self.graph:
            if str(s) == self.identifier:
                if self.mapping is None:
                    data_dict[str(p)] = o
                else:
                    for m in self.mapping:
                        if str(p) in self.mapping[m] and str(o) is not None:
                            data_dict[str(m)] = str(o)
                            break
        return data_dict

    def get_property(self, property_name):
        for schema in self.schemas:
            path = schema.get_property_path(property_name)
            # If path does not exist, try the next schema
            if not path:
                continue
            property_value = path.find_element(self.content)
            if property_value:
                return property_value
        return None

    def get_json_ld(self):
        html_data = self.content.find("script", attrs={"type": "application/ld+json"})
        if html_data:
            json_ld = json.loads(html_data.contents[0])
            if "@id" not in json_ld:
                json_ld["@id"] = self.identifier
            self.graph.parse(data=json.dumps(json_ld), format='json-ld')
        return None

    def get_rdfa(self):
        html_string = str(self.content)
        g = rdflib.Graph()
        rdfa = g.parse(data=html_string, format='rdfa', media_type='text/html')
        if rdfa:
            for s,p,o in rdfa:
                if s:
                    self.graph.add((s,p,o))
                else:
                    self.graph.add((rdflib.URIRef(self.identifier),p,o))
        return None

    def get_metatags(self):
        # Dublin Core
        base = "http://purl.org/dc/terms/"
        metatags = self.content.find_all('meta', attrs={'name': re.compile("^(dc.|DC.)")})
        for m in metatags:
            property = base + m["name"].split(".", 1)[1]
            self.graph.add((rdflib.URIRef(self.identifier), rdflib.URIRef(property), rdflib.Literal(m["content"])))


class WikipediaContentExtractor(URLContentExtractor):
    schema_names = ['opengraph', 'html', 'wikipedia']


class DOIContentExtractor(ContentExtractor):
    doi_base_url = "https://doi.org/"
    headers = {'Accept': 'application/x-bibtex; charset=utf-8'}

    def fetch_content(self):
        doi_url = self.doi_base_url + self.identifier
        page = self.get_page(doi_url, headers=self.headers)
        bibtex = bibtexparser.loads(page)
        return bibtex.entries[0]

    def get_property(self, property_name):
        if property_name in self.content:
            return self.content[property_name]
        else:
            return None


class ISBNContentExtractor(ContentExtractor):
    library_names = ['googlebooks', 'openlibrary']
    library = None
    schema = None

    def fetch_content(self):
        factory = LibraryFactory()
        for library_name in self.library_names:
            library = factory.create_library(library_name)
            data_json = library.get_json(self.identifier)
            if not data_json:
                continue
            else:
                self.library = library
                return data_json
        raise Exception("Volume not found")

    def get_property(self, property_name):
        schema = self.library.get_schema()
        path = schema.get_property_path(property_name)
        if not path:
            return None
        property_value = path.find_element(self.content)
        return property_value


class ExtractorFactory:
    @staticmethod
    def create_extractor(identifier, property_keys=None, format='dict', schema_names=None):
        if is_url(identifier):
            if has_domain(identifier, 'wikipedia.org'):
                return WikipediaContentExtractor(identifier, property_keys=property_keys, format=format)
            else:
                return URLContentExtractor(identifier, property_keys=property_keys, format=format, schema_names=schema_names)
        if is_doi(identifier):
            return DOIContentExtractor(identifier, property_keys=property_keys, format=format)
        if is_isbn(identifier):
            return ISBNContentExtractor(identifier, property_keys=property_keys, format=format)
        raise ValueError("Extractor not recognized")
