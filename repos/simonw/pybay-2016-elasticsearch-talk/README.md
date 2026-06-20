# Exploring complex data with Elasticsearch and Python

Supporting code from my Elasticsearch and Python talk at PyBay 2016.

Slides: https://speakerdeck.com/simon/exploring-complex-data-with-elasticsearch-and-python

Video should be available online some time after the conference.

## index_docs.py

This script recursively walks a folder containing the official Django
documentation (though it should work on other folders containing restructured
text documentation as well) and outputs it in a format suitable to be passed
directly to Elasticsearch via the _bulk indexing endpoint.

To run this script, first download the latest version of Django and unzip it.

Then run the following:

    python index_docs.py django/docs/ https://docs.djangoproject.com/en/1.10/

This will output newline separated JSON.

To index those documents in Elasticsearch, first run Elasticsearch on a known
URL (on your local machine on port 9200 is fine), then pipe the output of the
above command to curl like so:

    python index_docs.py django/docs/ \
        https://docs.djangoproject.com/en/1.10/ | \
        curl -s XPOST localhost:9200/docsearch/doc/_bulk \
        --data-binary @-

## fetch_pypi_metadata.py

My second demo used data pulled from the Python Package Index. PyPI offers a
JSON API to retrieve metadata about individual packages - this script loops
through the 80,000+ list of packages (retrieved using XMLRPC) and downloads
them to a local metadata/ directory.

Since this hits PyPI 80,000+ times, you shouldn't run this! You'll have to
edit the script to get it to work. In place of using this script, I suggest
downloading this .zip file containing the metadata/ directory I used during
the talk:

http://s3.amazonaws.com/files.simonwillison.net/2016/pypi-metadata/metadata.zip

## index_pypi_metadata.py

This script reads every .json file in the metadata/ directory described above
and indexes the corresponding packages and releases into Elasticsearch. It
first initializes indexes for those data types with the relevant mapping (the
Elasticsearch equivalent of a schema).

Suggested usage:

    wget http://s3.amazonaws.com/files.simonwillison.net/2016/pypi-metadata/metadata.zip
    unzip metadata.zip
    python index_pypi_metadata.py

This script needs some dependencies, listed in requirements.txt
