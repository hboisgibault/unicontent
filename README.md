# unicontent
Unicontent is a Python library to extract metadata from different types of sources and for different types of objects. The
goal is to normalize metadata and to provide an easy-to-use extractor. Given an identifier (URL, DOI, ISBN), unicontent can retrieve
structured data about the corresponding object.

## Usage

Here is the basic usage if you want to extract metadata with any kind of identifier. unicontent will detect the type of identifier and use the right extractor. Use get_metadata function if you just want metadata.

```python
from unicontent.extractors import get_metadata
data = get_metadata(identifier="http://example.com", format='n3')
```
See below if you want to use the extractor for a specific kind of identifier (URL, DOI or ISBN).

### Extraction from URL

The class ```URLContentExtractor``` is used to extract data from an URL. Several formats are available : RDF formats will return a rdflib graph (n3, turtle, xml). 'dict' and 'json' format will return a dictionary and a JSON file according to the mapping defined. A default mapping is provided.

```python
url = 'http://www.lemonde.fr/big-browser/article/2017/02/13/comment-les-americains-s-informent-oublient-et-reagissent-sur-les-reseaux-sociaux_5079137_4832693.html'
url_extractor = URLContentExtractor(identifier=url, format='dict', schema_names=['opengraph', 'dublincore', 'htmltags']) # 'dict' is the default format
metadata_dict = url_extractor.get_data()
```

The order of the ```schema_names``` parameters defines how the extractor will fetch metadata as explained before. Always use htmltags to get at least the ```<title>``` tag in the webpage.

### Extraction from DOI

The module uses the DOI system Proxy Server to extract metadata from DOI codes. The extractor name is DOIContentExtractor.

```python
doi = '10.10.1038/nphys1170'
doi_extractor = DOIContentExtractor(identifier=doi, format='dict')
metadata_dict = doi_extractor.get_data()
```

### Extraction from ISBN

To retrieve metadata from books, the library uses GoogleBooks and OpenLibrary (in this order). The extractor class is called ISBNContentExtractor.
If GoogleBooks does not find the volume corresponding to the ISBN code, a request is sent to OpenLibrary to fetch the data.


