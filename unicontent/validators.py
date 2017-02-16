from urllib import parse
import re
import tldextract
import isbnlib


def is_url(identifier):
    parsed_url = parse.urlparse(identifier)
    if not parsed_url.scheme or not parsed_url.netloc:
        return False
    else:
        return True


def has_domain(url, domain_name):
    ext = tldextract.extract(url)
    if domain_name == ext.registered_domain:
        return True
    else:
        return False


def is_isbn(identifier):
    return isbnlib.notisbn(identifier)


def is_doi(identifier):
    doi_regex = re.compile('(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)')
    if doi_regex.match(identifier):
        return True
    else:
        return False


def clean_identifier(identifier):
    if is_url(identifier):
        return clean_url(identifier)
    elif is_doi(identifier):
        return clean_doi(identifier)
    elif is_isbn(identifier):
        return clean_isbn(identifier)
    else:
        return False

def clean_isbn(isbn):
    return isbnlib.to_isbn13(isbn)


def clean_url(url):
    return url


def clean_doi(doi):
    return doi