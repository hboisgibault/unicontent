# python_metadata_extractor
Metadata-extractor is a Python library to extract metadata easily from different identifiers : URL, DOI or ISBN.


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

```pip install python_metadata_extractor```

## Usage



### Extraction from URL

The class ```URLContentExtractor``` is used to extract data from an URL. Several schemas can be used : OpenGraph, DublinCore or HtmlTags.
For each property key, the extractor will try to get the property value based on the first schema. If the property is not defined in the schema,
or not available for the object, the extractor will try the next schema.

```python
url = 'http://www.lemonde.fr/big-browser/article/2017/02/13/comment-les-americains-s-informent-oublient-et-reagissent-sur-les-reseaux-sociaux_5079137_4832693.html'
url_extractor = URLContentExtractor(identifier=url, schema_names=['opengraph', 'dublincore', 'htmltags']
metadata_dict = url_extractor.get_data_dict()
```

The order of the ```schema_names``` parameters defines how the extractor will fetch metadata as explained data. Always use htmltags to get at least the title from the html tag.

### Extraction from DOI

The module uses the DOI system Proxy Server to extract metadata from DOI codes.

```python
doi = '10.10.1038/nphys1170'
doi_extractor = DOIContentExtractor(identifier=doi)
metadata_dict = doi_extractor.get_data_dict()
```

### Extraction from ISBN

To retrieve metadata from books, the library uses GoogleBooks and OpenLibrary (in this order). The class is called ISBNContentExtractor.
If GoogleBooks does not find the volume corresponding to the ISBN code, a request is sent to OpenLibrary.
