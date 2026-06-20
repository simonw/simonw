# TodoMVC demo backed by Datasette

This is a modified version of the [Vanilla JavaScript TodoMVC Example](https://github.com/tastejs/todomvc/tree/gh-pages/examples/vanillajs) adapted to demonstrate the [Datasette 1.0 alpha JSON API](https://docs.datasette.io/en/latest/changelog.html#a0-2022-11-29).

To try this out, visit https://todomvc.datasette.io/

The database table used by this demo is automatically deleted every 15 minutes.

The code that talks to the Datasette API lives in this file:

https://github.com/simonw/todomvc-datasette/blob/main/js/store.js

This is the only file I changed from the original.

![Animated screenshot showing two items being added, then one is checked off as done and the other is deleted.](https://user-images.githubusercontent.com/9599/205216443-6cc58a9e-0259-474b-bfa4-c64ad83ac6a3.gif)
