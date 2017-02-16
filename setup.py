from setuptools import setup

setup(name='unicontent',
      version='0.4',
      description='Python module to extract structured metadata from URL, DOI or ISBN',
      keywords='metadata extraction OpenGraph DublinCore isbn GoogleBooks doi',
      url='http://github.com/hboisgibault/unicontent',
      author='hboisgibault',
      author_email='h.boisgibault@gmail.com',
      license='MIT',
      packages=['unicontent'],
      install_requires=['requests', 'bs4', 'bibtexparser', 'wikipedia', 'tldextract', 'isbnlib'],
      classifiers=[
          'Development Status :: 4 - Beta',

          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      zip_safe=False
)
