# Mendoza Trees Django Tutorial

**Presented 8th May 2018**. This was primarily a live-coding workshop to illustrate the powerful combination of Jupyter notebooks and Django.

## Initial setup

I started by creating and activating a brand new Python 3 virtual environment:

    $ mkdir mendoza-trees && cd mendoza-trees
    $ python3 -mvenv venv
    $ source venv/bin/activate

Then I installed [Django](https://www.djangoproject.com/), [django_extensions](https://django-extensions.readthedocs.io/en/latest/), [Jupyter](http://jupyter.org/) and [chardet](https://pypi.org/project/chardet/):

    $ pip install Django django_extensions jupyter chardet

I downloaded a [CSV file full of trees](https://ckan.ciudaddemendoza.gov.ar/dataset/arbolado-de-la-ciudad-de-mendoza) from the Mendoza Open Data site:

    wget http://ckan.ciudaddemendoza.gov.ar/dataset/3aaec520-6c8e-417e-85b6-5c7fc18b353e/resource/1b8b1627-9f6a-4ff6-9422-0ef79e5821bc/download/arboladolineal.csv

## Creating the Django project

I created the Django project like this:

    $ django-admin startproject mendoza_trees
    $ cd mendoza_trees
    $ ./manage.py startapp trees

Then I added the following to `trees/models.py`:

    from django.db import models

    class Species(models.Model):
        name = models.CharField(max_length=100)

        def __str__(self):
            return self.name

    class Tree(models.Model):
        species = models.ForeignKey(Species, on_delete=models.CASCADE)
        latitude = models.FloatField()
        longitude = models.FloatField()

I added both `django_extensions` and `trees` to `INSTALLED_APPS` in the `mendoza_trees/settings.py` file:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'trees',
    ]

Finally, I created and ran migrations to create the tables:

    $ ./manage.py makemigrations
    $ ./manage.py migrate

## Parsing CSV using a Jupyter notebook

Python has numerous more efficient ways to parse CSV files, but I used an interactive Jupyter session to illustrate how iterative programming in Jupyter works.

First, I started Jupyter using a new command added by `django_extensions`:

    $ ./manage.py shell_plus --notebook

This starts a Juyter notebook instance that is already configured to talk to your current Django project.

I chose `New Notebook -> Django Shell-Plus`.

See my [Import-Trees-from-CSV](https://github.com/simonw/mendoza-trees-workshop/blob/master/Import-Trees-from-CSV.ipynb) notebook for the next steps.

## Showing the trees in the Django Admin

The Django Admin isn't just for building admin interfaces: I use it on almost all of my projects as a quick visual debugging tool.

I added the following to `trees/admin.py`:

    from django.contrib import admin
    from .models import Tree, Species

    admin.site.register(Tree)
    admin.site.register(Species)

Next, I created a superuser:

    $ ./manage.py createsuperuser
    (set username, email and password)

Then I ran the development server:

    $ ./manage.py runserver

And navigated to http://localhost:8000/admin/ and signed in.

The Trees listing in admin wasn't that useful, so I changed `admin.py` to look like this:

    admin.site.register(Tree,
        list_display=('species', 'latitude', 'longitude')
    )

I carried out the above steps while the import script was still running in Jupyter - that way I could hit "refresh" in the admin list view and watch the number of trees increase as the import progressed.

## Playing with the Django ORM in Jupyter

Having loaded all of the trees, I used Jupyter to demonstrate some features of the Django ORM. The full notebook is [Trees-Django-ORM](https://github.com/simonw/mendoza-trees-workshop/blob/master/Trees-Django-ORM.ipynb). The highlights were:

    from trees.models import Species, Tree
    from django.db.models import Count

    for s in Species.objects.annotate(
        num_trees = Count('tree')
    ).order_by('-num_trees'):
        print(s.name, s.num_trees)

    Morera 18809
    Fresno europeo 8037
    Pltano 4319
    Paraiso 4064
    N/D 2831
    Fresno americano 2022
    Acacia SP 1038
    Acer 951
    Paraiso sombrilla 809
    Olmo comun 776
    Caducifolio 650
    Prunas 558
    Jacarand 523
    Perenne 470
    Aguaribay 423
    Olmo bola 323
    Ailanthus 299
    Conifera 252
    Ligustro 202
    Tilo 196
    lamo blanco 167
    Tipa 127
    Braquiquito 109
    lamo criollo 108
    Acacia visco 108
    Liquidambar 99
    Palo borracho 64
    Catalpa 45
    Eucalyptus 26
    Algarrobo 7
    Arabia 4
    rbol del cielo 2
    Maiten 1

I then demonstrated using `django.db.connection` to see exactly what SQL had been executed:

    from django.db import connection
    connection.queries[-1]

    {'sql': 'SELECT "trees_species"."id", "trees_species"."name", COUNT("trees_tree"."id") AS "num_trees" FROM "trees_species" LEFT OUTER JOIN "trees_tree" ON ("trees_species"."id" = "trees_tree"."species_id") GROUP BY "trees_species"."id", "trees_species"."name" ORDER BY "num_trees" DESC',
    'time': '0.020'}

Finally, I demonstrated how the following uses inefficient SQL, executing a SELECT against the species table for every one of the 20 trees that are displayed:

    for tree in Tree.objects.all()[:20]:
        print(tree.latitude, tree.longitude, tree.species.name)

Whereas the same thing using `.select_related()` only ran one query:

    for tree in Tree.objects.select_related('species')[:20]:
        print(tree.latitude, tree.longitude, tree.species.name)

## Displaying trees on a map

I built a simple Django view and template that could display some of the trees on a map, using [Leaflet](https://github.com/Leaflet/Leaflet.markercluster) and [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster). `trees/views.py` looked like this:

    from django.shortcuts import render
    from .models import Tree
    import json
    from django.utils.html import mark_safe

    def index(request):
        trees = list(Tree.objects.select_related('species').values(
            'latitude', 'longitude', 'species__name'
        )[:100])
        return render(request, 'index.html', {
            'trees': mark_safe(json.dumps(trees)),
        })

And `trees/templates/index.html` looked like this:

    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    <head>
    <meta charset="utf-8">
    <title>Mendoza Trees</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css" integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ==" crossorigin="anonymous">
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.3.0/dist/MarkerCluster.css" integrity="sha384-lPzjPsFQL6te2x+VxmV6q1DpRxpRk0tmnl2cpwAO5y04ESyc752tnEWPKDfl1olr" crossorigin="anonymous">
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.3.0/dist/MarkerCluster.Default.css" integrity="sha384-5kMSQJ6S4Qj5i09mtMNrWpSi8iXw230pKU76xTmrpezGnNJQzj0NzXjQLLg+jE7k" crossorigin="anonymous">
    <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js" integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw==" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/leaflet.markercluster@1.3.0/dist/leaflet.markercluster-src.js" integrity="sha384-NAOEbWFcjnXc7U9GkULPhupHZNAbqru9dS3c+4ANYAwtFoVAWuVuMVDH0DIy4ESp" crossorigin="anonymous"></script>
    </head>
    <body>
    <div id="map" style="width: 95%; height: 90vh"></div>
    <script>
    var trees = {{ trees }};
    var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        detectRetina: true,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
    });
    var latlng = L.latLng(-68.816667, -32.883333);
    var map = L.map('map', {
        center: latlng,
        zoom: 13,
        layers: [tiles]
    });
    var currentLayer = null;
    currentLayer = L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 50
    });
    var markerList = [];
    trees.forEach(tree => {
        var marker = L.marker(L.latLng(tree.latitude, tree.longitude), { title: tree.species });
        marker.bindPopup(tree.species);
        markerList.push(marker);
    });
    currentLayer.addLayers(markerList);
    map.addLayer(currentLayer);
    map.fitBounds(currentLayer.getBounds());
    </script>
    </body>
    </html>
