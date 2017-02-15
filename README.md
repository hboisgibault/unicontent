# unicontent
Unicontent is a Python library to extract metadata from different types of sources and for different types of objects. The
goal is to normalize metadata and to provide an easy-to-use extractor. Given an identifier (URL, DOI, ISBN), unicontent can retrieve
structured data about the corresponding object.


Here's a list of the metadata information extracted if available :
* Title -> ```title``` : Title of the object (title of the webpage, book or other type of object)
* URL -> ```url``` : URL to access the object
* Description -> ```description``` : Description of the object
* Image URL -> ```image_url``` : URL of the object's image
* Author name -> ```author_name``` : Author or creator of the object's name
* Date published -> ```date_published``` : Date of publication or creation
* Publisher -> ```publisher``` : Name of the source or publisher
* Language -> ```language``` : Language of the content

## Installation

```pip install unicontent```

## Usage

```python
from unicontent.extractors import get_metadata
data = get_metadata(identifier="http://example.com")
```

### Extraction from URL

The class ```URLContentExtractor``` is used to extract data from an URL. Several schemas can be used : OpenGraph, DublinCore or HtmlTags.
For each property key, the extractor will try to get the property value based on the first schema. If the property is not defined in the schema,
or not available for the object, the extractor will try the next schema.

```python
url = 'http://www.lemonde.fr/big-browser/article/2017/02/13/comment-les-americains-s-informent-oublient-et-reagissent-sur-les-reseaux-sociaux_5079137_4832693.html'
url_extractor = URLContentExtractor(identifier=url, format='dict', schema_names=['opengraph', 'dublincore', 'htmltags']) # 'dict' is the default format
metadata_dict = url_extractor.get_data()
```

The order of the ```schema_names``` parameters defines how the extractor will fetch metadata as explained data. Always use htmltags to get at least the title from the html tag.

### Extraction from DOI

The module uses the DOI system Proxy Server to extract metadata from DOI codes.

```python
doi = '10.10.1038/nphys1170'
doi_extractor = DOIContentExtractor(identifier=doi, format='dict')
metadata_dict = doi_extractor.get_data()
```

### Extraction from ISBN

To retrieve metadata from books, the library uses GoogleBooks and OpenLibrary (in this order). The extractor class is called ISBNContentExtractor.
If GoogleBooks does not find the volume corresponding to the ISBN code, a request is sent to OpenLibrary to fetch the data.
