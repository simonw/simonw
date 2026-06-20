# dcinbox_explorer

A Flask+Elasticsearch UI for exploring the DC Inbox dataset from
http://web.stevens.edu/dcinbox/Home.html

See it in action at https://dcinbox.herokuapp.com/

## Background

DC Inbox is a collection of over 60,000 official e-newsletters sent from
members of the U.S. Congress to their constituents, established by Dr. Lindsey
Cormack at Stevens Institute of Technology.

This repository contains a Flask app which uses Elasticsearch to provide a
faceted search interface to the collection, along with some scripts to import
the dataset into Elasticsearch.

## Development environment

You'll need an Elasticsearch server. The easiest way to get this is to
download Elasticsearch 5 from https://www.elastic.co/downloads/elasticsearch
then extract the archive and run it locally using bin/elasticsearch

I recommend setting up a Python virtual environment. Assuming you have
virtualenv installed, you can do so like this:

    cd dcinbox_explorer
    virtualenv venv
    source venv/bin/activate

Then install the dependencies:

    pip install -r requirements.txt

Next, initialize the Elasticsearch index:

    ELASTICSEARCH_HOST='localhost' \
    ELASTICSEARCH_PORT=9200 \
    ELASTICSEARCH_AUTH='' \
    venv/bin/python script_create_index.py

Now you can run the development server using:

    ELASTICSEARCH_HOST='localhost' \
    ELASTICSEARCH_PORT=9200 \
    ELASTICSEARCH_AUTH='' \
    FLASK_APP=dcinbox.py \
    FLASK_DEBUG=1 \
    venv/bin/flask run

The site should be available on http://localhost:5000/

## Importing the data

First, download the dataset from http://web.stevens.edu/dcinbox/dataset.json
(around 250MB).

Then run the following:

    ELASTICSEARCH_HOST='localhost' \
    ELASTICSEARCH_PORT=9200 \
    ELASTICSEARCH_AUTH='' \
    venv/bin/python importer.py dataset.json

The importer script can accept a URL instead of a filename.

## Hosting

The app is ready to host on Heroku - it has the necessary Procfile already in
place. You'll need to specify the Elasticsearch server location using
environment variables like so:

    heroku config:set ELASTICSEARCH_HOST=blah.us-east-1.aws.found.io
    heroku config:set ELASTICSEARCH_PORT=9243
    heroku config:set ELASTICSEARCH_AUTH='user:password'
    heroku config:set ELASTICSEARCH_USE_SSL=1

Once you have deployed to Heroku you can configure the index like so:

    heroku run python script_create_index.py

And even kick off a full dataset import like so:

    heroku run python importer.py http://web.stevens.edu/dcinbox/dataset.json
