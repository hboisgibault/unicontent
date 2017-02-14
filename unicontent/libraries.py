import json
import requests
from .schemas import SchemaFactory


class Library:
    base_url = ""

    @staticmethod
    def get_page(url, headers=None, params=None):
        try:
            response = requests.get(url, headers=headers, params=params)
            return response.text
        except requests.exceptions.RequestException as e:
            return False

    def get_schema(self):
        pass

    def get_json(self, *args):
        pass

    def query_isbn(self, isbn):
        pass


class OpenLibrary(Library):
    base_url = "https://openlibrary.org/api/books?jscmd=data&format=json&bibkeys="

    def get_url(self, isbn):
        return self.base_url + self.get_query(isbn)

    @staticmethod
    def get_query(isbn):
        return "ISBN:" + isbn

    def get_json(self, isbn):
        data_raw = self.get_page(self.get_url(isbn))
        return json.loads(data_raw)[self.get_query(isbn)]

    def get_schema(self):
        factory = SchemaFactory()
        return factory.create_schema("openlibrary")


class GoogleBooks(Library):
    base_url = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    def get_url(self, isbn):
        return self.base_url + isbn

    def get_json(self, isbn):
        data_raw = self.get_page(self.get_url(isbn))
        return json.loads(data_raw)["items"][0]

    def get_schema(self):
        factory = SchemaFactory()
        return factory.create_schema("googlebooks")


class LibraryFactory:
    @staticmethod
    def create_library(type):
        if type == 'googlebooks':
            return GoogleBooks()
        elif type == 'openlibrary':
            return OpenLibrary()
        else:
            return None