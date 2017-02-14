# coding: utf-8
from .extractors import URLContentExtractor, DOIContentExtractor, ISBNContentExtractor

url = "http://www.lemonde.fr/police-justice/article/2017/02/11/a-bobigny-le-rassemblement-contre-les-violences-policieres-tourne-mal_5078366_1653578.html"
doi = "10.1126/science.169.3946.635"
isbn = "0789312239"
content_extractor_url = URLContentExtractor(url)
content_extractor_doi = DOIContentExtractor(doi)
content_extractor_isbn = ISBNContentExtractor(isbn)
doi_data = content_extractor_doi.get_data_dict()
url_data = content_extractor_url.get_data_dict()
isbn_data = content_extractor_isbn.get_data_dict()


