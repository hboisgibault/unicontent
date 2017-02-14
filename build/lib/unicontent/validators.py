from urllib import parse
import re


def is_url(identifier):
    parsed_url = parse.urlparse(identifier)
    if not parsed_url.scheme or not parsed_url.netloc:
        return False
    else:
        return True


def is_isbn(identifier):
    isbn_regex = re.compile("(?:[0-9]{3}-)?[0-9]{1,5}-[0-9]{1,7}-[0-9]{1,6}-[0-9]")
    if isbn_regex.match(identifier):
        return True
    else:
        return False


def is_doi(identifier):
    doi_regex = re.compile('\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b')
    if doi_regex.match(identifier):
        return True
    else:
        return False
