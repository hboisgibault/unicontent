# coding: utf-8
from .paths import *


class MetadataSchema:
    def get_property_path(self, property_name):
        property_path_name = property_name + "_path"
        path = getattr(self, property_path_name, None)
        return path


class OpenGraph(MetadataSchema):
    title_path = HtmlPath(tag_name="meta", attributes={"property": "og:title"}, content_name="content")
    description_path = HtmlPath(tag_name="meta", attributes={"property": "og:description"}, content_name="content")
    url_path = HtmlPath(tag_name="meta", attributes={"property": "og:url"}, content_name="content")
    publisher_path = HtmlPath(tag_name="meta", attributes={"property": "og:site_name"}, content_name="content")
    image_url_path = HtmlPath(tag_name="meta", attributes={"property": "og:image"}, content_name="content")
    language_path = HtmlPath(tag_name="meta", attributes={"property": "og:locale"}, content_name="content")
    type_path = HtmlPath(tag_name="meta", attributes={"property": "og:type"}, content_name="content")


class DublinCore(MetadataSchema):
    tag_name = "meta"
    content_name = "content"
    title_path = HtmlPath(tag_name=tag_name, attributes={"name": "DC.title"}, content_name=content_name)
    description_path = HtmlPath(tag_name=tag_name, attributes={"name": "DC.description"}, content_name=content_name)
    publisher_path = HtmlPath(tag_name=tag_name, attributes={"name": "DC.publisher"}, content_name=content_name)
    language_path = HtmlPath(tag_name=tag_name, attributes={"name": "DC.language"}, content_name=content_name)
    type_path = HtmlPath(tag_name=tag_name, attributes={"name": "DC.type"}, content_name=content_name)


class HtmlTags(MetadataSchema):
    title_path = HtmlPath(tag_name='title')
    url_path = HtmlPath(tag_name='link', attributes={'rel': 'canonical'}, content_name="href")
    description_path = HtmlPath(tag_name='meta', attributes={'name': 'description'}, content_name="content")
    author_name_path = HtmlPath(tag_name='meta', attributes={'name': 'author'}, content_name="content")
    publisher_path = HtmlPath(tag_name='meta', attributes={'name': 'application-name'}, content_name="content")
    language_path = HtmlPath(tag_name='html', content_name="lang")


class Wikipedia(MetadataSchema):
    publisher_path = PlainTextPath('Wikipedia')


class OpenLibrary(MetadataSchema):
    title_path = JsonPath(['title'])
    image_url_path = JsonPath(['cover', 'large'])


class GoogleBooks(MetadataSchema):
    title_path = JsonPath(['volumeInfo', 'title'])
    url_path = JsonPath(['volumeInfo', 'canonicalVolumeLink'])
    image_url_path = JsonPath(['volumeInfo', 'imageLinks', 'thumbnail'])
    description_path = JsonPath(['volumeInfo', 'description'])
    author_name_path = JsonPath(['volumeInfo', 'authors', 'ARRAY'])
    publisher_path = JsonPath(['volumeInfo', 'publisher'])
    language_path = JsonPath(['volumeInfo', 'language'])
    date_published_path = JsonPath(['volumeInfo', 'publishedDate'])
    type_path = JsonPath(['kind'])


class SchemaFactory:
    @staticmethod
    def create_schema(type):
        if type == 'opengraph':
            return OpenGraph()
        elif type == 'dublincore':
            return DublinCore()
        elif type == 'html':
            return HtmlTags()
        elif type == 'openlibrary':
            return OpenLibrary()
        elif type == 'googlebooks':
            return GoogleBooks()
        elif type == 'wikipedia':
            return Wikipedia()
        else:
            raise ValueError("Schema not recognized")
