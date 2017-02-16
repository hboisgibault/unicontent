from urllib import parse
import re
import tldextract


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
    isbn_regex = re.compile("(?:[0-9]{3}-)?[0-9]{1,5}-?[0-9]{1,7}-?[0-9]{1,6}-?[0-9]")
    if isbn_regex.match(identifier):
        return True
    else:
        return False


def is_doi(identifier):
    doi_regex = re.compile('(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)')
    if doi_regex.match(identifier):
        return True
    else:
        return False
