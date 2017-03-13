from unittest import TestCase
from unicontent.schemas import *


class OpenGraphSchemaTest(TestCase):
    def setUp(self):
        self.opengraph_schema = OpenGraph()

    def test_opengraph_paths(self):
        properties = ['title', 'description', 'url', 'publisher', 'image_url', 'language', 'type']
        for property in properties:
            path = self.opengraph_schema.get_property_path(property)
            self.assertTrue(path)
            self.assertIsInstance(path, HtmlPath)
            self.assertEqual(path.tag_name, "meta")
            self.assertEqual(path.content_name, "content")
            self.assertIn(member="property", container=path.attributes.keys())
            self.assertIn(member="og:", container=path.attributes["property"])


class DublinCoreSchemaTest(TestCase):
    def setUp(self):
        self.dublincore_schema = DublinCore()

    def test_dublincore_paths(self):
        properties = ['title', 'description', 'publisher', 'language', 'type']
        for property in properties:
            path = self.dublincore_schema.get_property_path(property)
            self.assertTrue(path)
            self.assertIsInstance(path, HtmlPath)
            self.assertEqual(path.tag_name, "meta")
            self.assertEqual(path.content_name, "content")
            self.assertIn(member="name", container=path.attributes.keys())
            self.assertIn(member="DC.", container=path.attributes["name"])


class HtmlTagsSchemaTest(TestCase):
    def setUp(self):
        self.htmltags_schema = HtmlTags()

    def test_htmltags_paths(self):
        properties = ['description', 'author_name', 'publisher']
        for property in properties:
            path = self.htmltags_schema.get_property_path(property)
            self.assertTrue(path)
            self.assertIsInstance(path, HtmlPath)
            self.assertEqual(path.tag_name, "meta")
            self.assertEqual(path.content_name, "content")
            self.assertIn(member="name", container=path.attributes.keys())

    def test_title_path(self):
        path = self.htmltags_schema.get_property_path("title")
        self.assertTrue(path)
        self.assertIsInstance(path, HtmlPath)
        self.assertEqual(path.tag_name, "title")
        self.assertIsNone(path.content_name)
        self.assertIsNone(path.attributes)

    def test_url_path(self):
        path = self.htmltags_schema.get_property_path("url")
        self.assertTrue(path)
        self.assertIsInstance(path, HtmlPath)
        self.assertEqual(path.tag_name, "link")
        self.assertEqual(path.content_name, "href")
        self.assertIn(member="rel", container=path.attributes.keys())
        self.assertEqual("canonical", path.attributes["rel"])

    def test_language_path(self):
        path = self.htmltags_schema.get_property_path("language")
        self.assertTrue(path)
        self.assertIsInstance(path, HtmlPath)
        self.assertEqual(path.tag_name, "html")
        self.assertEqual(path.content_name, "lang")
        self.assertIsNone(path.attributes)


class WikipediaSchemaTest(TestCase):
    def setUp(self):
        self.wikipedia_schema = Wikipedia()

    def test_publisher_path(self):
        path = self.wikipedia_schema.get_property_path("publisher")
        self.assertTrue(path)
        self.assertIsInstance(path, PlainTextPath)
        self.assertEqual(path.text, "Wikipedia")

class OpenLibrarySchemaTest(TestCase):
    def setUp(self):
        self.openlibrary_schema = OpenLibrary()

    def test_openlibrary_paths(self):
        properties = ['title', 'image_url']
        for property in properties:
            path = self.openlibrary_schema.get_property_path(property)
            self.assertTrue(path)
            self.assertIsInstance(path, JsonPath)
            self.assertIsNotNone(path.keys)
            self.assertIsInstance(path.keys, list)


class GoogleBooksSchemaTest(TestCase):
    def setUp(self):
        self.googlebooks_schema = GoogleBooks()

    def test_googlebooks_paths(self):
        properties = ['title', 'url', 'image_url', 'description', 'author_name', 'publisher', 'language', 'date_published', 'type']
        for property in properties:
            path = self.googlebooks_schema.get_property_path(property)
            self.assertTrue(path)
            self.assertIsInstance(path, JsonPath)
            self.assertIsNotNone(path.keys)
            self.assertIsInstance(path.keys, list)


class SchemaFactoryTest(TestCase):
    def setUp(self):
        self.factory = SchemaFactory()

    def test_create_schema(self):
        self.assertTrue(self.factory.create_schema("opengraph"))
        self.assertIsInstance(self.factory.create_schema("opengraph"), OpenGraph)
        self.assertTrue(self.factory.create_schema("dublincore"))
        self.assertIsInstance(self.factory.create_schema("dublincore"), DublinCore)
        self.assertTrue(self.factory.create_schema("html"))
        self.assertIsInstance(self.factory.create_schema("html"), HtmlTags)
        self.assertTrue(self.factory.create_schema("openlibrary"))
        self.assertIsInstance(self.factory.create_schema("openlibrary"), OpenLibrary)
        self.assertTrue(self.factory.create_schema("googlebooks"))
        self.assertIsInstance(self.factory.create_schema("googlebooks"), GoogleBooks)
        self.assertTrue(self.factory.create_schema("wikipedia"))
        self.assertIsInstance(self.factory.create_schema("wikipedia"), Wikipedia)

    def test_create_schema_fail(self):
        self.assertRaises(ValueError, self.factory.create_schema, "test")
