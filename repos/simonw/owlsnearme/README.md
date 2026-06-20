## Owls Near Me

https://www.owlsnearme.com/

A website that tells you where your nearest owls are!

This is a re-imagining of the original `owlsnearyou.com`, which launched way
back in January 2010 (it's now a website about lawyers). This new version uses
2018-era web technology and pulls its data from
[iNaturalist](https://www.inaturalist.org/).

It's built as a single page React application that loads all of its data from
the iNaturalist API. You can use it to find your nearest owls via browser
geolocation or you can search for a place and see the owls that have been
spotted in or around that location.

Built by [Natalie Downe](https://twitter.com/natbat) and [Simon Willison](https://twitter.com/simonw). Favicon by [Cindy Li](https://twitter.com/cindyli).

Technology used:

* React, using [create-react-app](https://github.com/facebook/create-react-app)
  (hence also Babel, Webpack and much other open-source JavaScript goodness)
* [The iNaturalist API](https://api.inaturalist.org/v1/docs/)
* [Leaflet](http://leafletjs.com/) for maps, using
  [react-leaflet](https://github.com/PaulLeCam/react-leaflet)
* [axios](https://github.com/axios/axios) for our API requests
