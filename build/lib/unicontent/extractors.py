# coding: utf-8
import requests
from bs4 import BeautifulSoup
from .schemas import SchemaFactory
from .libraries import LibraryFactory
from .validators import is_doi, is_isbn, is_url
import bibtexparser
import json


def get_metadata(identifier, format='dict', property_keys=None, schema_names=None):
    factory = ExtractorFactory()
    extractor = factory.create_extractor(identifier=identifier, format=format, property_keys=property_keys, schema_names=schema_names)
    if not extractor:
        return False
    return extractor.get_data()


class ContentExtractor:
    content = None
    property_keys = ['title', 'description', 'url', 'image_url', 'author_name', 'date_published', 'publisher', 'language']

    def __init__(self, identifier, format='dict', property_keys=None):
        if property_keys:
            self.property_keys = property_keys
        self.format = format
        self.identifier = identifier
        self.content = self.fetch_content()

    def get_data(self):
        if self.format == 'dict':
            return self.get_data_dict()
        elif self.format == 'json':
            return self.get_data_json()
        else:
            return self.get_data_dict()

    def get_data_dict(self):
        data_dict = {}
        for property_key in self.property_keys:
            data_dict[property_key] = self.get_property(property_key)
        return data_dict

    def get_data_json(self):
        data_dict = self.get_data_dict()
        return json.dumps(data_dict)

    def fetch_content(self):
        pass

    @staticmethod
    def get_page(url, headers=None, params=None):
        response = requests.get(url, headers=headers, params=params)
        return response.text

    def get_property(self, property_name):
        pass


class URLContentExtractor(ContentExtractor):
    schema_names = ['opengraph', 'dublincore', 'htmltags']
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

    def get_property(self, property_name):
        for schema in self.schemas:
            path = schema.get_property_path(property_name)
            # If path does not exist, try the next schema
            if not path:
                continue
            property_value = path.find_element(self.content)
            if property_value:
                return property_value


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

    def __init__(self, isbn, **kwargs):
        super(ISBNContentExtractor, self).__init__(identifier=isbn, **kwargs)

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
        return False

    def get_property(self, property_name):
        schema = self.library.get_schema()
        path = schema.get_property_path(property_name)
        if not path:
            return False
        property_value = path.find_element(self.content)
        return property_value


class ExtractorFactory:
    @staticmethod
    def create_extractor(identifier, property_keys=None, format='dict', schema_names=None):
        if is_url(identifier):
            return URLContentExtractor(identifier, property_keys=property_keys, format=format, schema_names=schema_names)
        if is_doi(identifier):
            return DOIContentExtractor(identifier, property_keys=property_keys, format=format)
        if is_isbn(identifier):
            return ISBNContentExtractor(identifier, property_keys=property_keys, format=format)
        return False
