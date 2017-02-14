from setuptools import setup

setup(name='unicontent',
      version='0.1',
      description='Python module to extract structured metadata from URL, DOI or ISBN',
      keywords='metadata extraction OpenGraph DublinCore isbn GoogleBooks doi',
      url='http://github.com/hboisgibault/python-metadata-extractor',
      author='hboisgibault',
      license='MIT',
      packages=['unicontent'],
      install_requires=['requests', 'bs4', 'bibtexparser'],
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
