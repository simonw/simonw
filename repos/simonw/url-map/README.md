# url-map

Use URL parameters to generate a map with markers, using Leaflet and OpenStreetMap

Visit it here: https://map.simonwillison.net/

Read about the project's background in [A tiny web app to create images from OpenStreetMap maps](https://simonwillison.net/2022/Jun/12/url-map/)

## Parameters

To center the map on a specific location, add `?center=lat,lon`. To set the zoom, use `?zoom=8`.

- https://map.simonwillison.net/?center=51.49,0&zoom=8

As an alternative to a latitude and longitude you can use `?q=` to provide text which will be looked up against the [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/ui/search.html). The map will then zoom to the best available bounding box for the first matching result:

- https://map.simonwillison.net/?q=san+francisco
- https://map.simonwillison.net/?q=islington+london

If you add a `&zoom=` to that the zoom you specify will be used instead of the automatic zoom calculated using the bounding box:

- https://map.simonwillison.net/?q=islington+london&zoom=12

To add markers to the map, use `?marker=lat,lon`. You can pass this multiple times:

- https://map.simonwillison.net/?center=51.49,0&zoom=8&marker=51.49,0&marker=51.3,0.2

## Using this with shot-scraper

You can use this tool to create static map images using [shot-scraper](https://shot-scraper.datasette.io/). For example:

```
shot-scraper 'https://map.simonwillison.net/?center=51.49,0&zoom=8&marker=51.49,0&marker=51.3,0.2' \
  --retina --width 600 --height 400 --wait 3000
```
Produces this image:

![A map of London with two blue markers](https://user-images.githubusercontent.com/9599/173208299-b44c34f1-887b-48b7-86d8-4038945ec80f.png)
