# coding: utf-8


class Path:
    def find_element(self, *args):
        pass


class HtmlPath(Path):
    tag_name = ""
    attributes = {}
    content_name = ""

    def __init__(self, tag_name, attributes=None, content_name=None):
        self.tag_name = tag_name
        self.attributes = attributes
        self.content_name = content_name

    def find_element(self, soup):
        element = soup.find(self.tag_name, attrs=self.attributes)
        if not element:
            return False
        if not self.content_name:
            return element.text
        else:
            return element[self.content_name]


class JsonPath(Path):
    def __init__(self, keys):
        self.keys = keys

    def find_element(self, json_data):
        sub_array = json_data
        for key in self.keys:
            if key == "ARRAY":
                sub_array = sub_array[0]
            else:
                if key in sub_array:
                    sub_array = sub_array[key]
                else:
                    return False
        return sub_array


class AttributePath(Path):
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def find_element(self, object):
        attribute = getattr(object, self.attribute_name, None)
        return attribute


class PlainTextPath(Path):
    def __init__(self, text):
        self.text = text

    def find_element(self, *args):
        return self.text
