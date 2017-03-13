from unittest import TestCase
from unicontent.paths import *
import string
import datetime


class JsonPathTest(TestCase):
    def setUp(self):
        self.keys = ['un', 'deux', 'trois']
        self.json_path = JsonPath(self.keys)


class AttributePathTest(TestCase):
    def setUp(self):
        self.attribute_name = "digits"
        self.attribute_path = AttributePath(self.attribute_name)

    def test_find_element(self):
        success_value = string.digits
        success_object = string
        fail_object = datetime
        fail_string = "foo"
        self.assertTrue(self.attribute_path.find_element(success_object))
        self.assertIsInstance(self.attribute_path.find_element(success_object), str)
        self.assertEqual(self.attribute_path.find_element(success_object), success_value)

        self.assertIsNone(self.attribute_path.find_element(fail_object))
        self.assertIsNone(self.attribute_path.find_element(fail_string))


class PlainTextPathTest(TestCase):
    def setUp(self):
        self.text = "test"
        self.plain_text_path = PlainTextPath(self.text)

    def test_find_element(self):
        element = self.plain_text_path.find_element()
        self.assertTrue(element)
        self.assertIsInstance(element, str)
        self.assertEqual(element, self.text)