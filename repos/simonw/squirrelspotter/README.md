squirrelspotter
===============

1. A "Squirrel!" button which creates a geocoded "spot"
http://www.flickr.com/photos/simon/474553279/sizes/m/in/photostream/

A spot has...
- who spotted the squirrel
- when the squirrel was spotted
- a latitude/longitude
- a human readable location? can facebook APIs offer that? 
   http://where.yahooapis.com/geocode?q=51.566133427963145,-0.10402679443359375&gflags=R&appid=.
- an optional photo (user can upload one) - 
    using input type="file" for the moment and push to S3, same mechanism as Lanyrd
    (can we delay posting the action to Facebook until the user has added the photo?)
    - can we upload the photo to some service that resizes it for us? Might be able to use transloadit.com
- shows other nearby spots?

The Twilio connection...
- SMS to record a squirrel spot (how does this tie to facebook? Make people sign in to the web app first, then tell them to SMS a particular code to us which will enable SMS reporting)
- SMS includes a location which we geocode... if it fails, we do an SMS conversation
- Subscribe to an SMS whenever a squirrel is spotted near you?

The Pusher connection...
- a live feed of squirrels being spotted, in realtime, on a funky map
  (with a replay mode in case we need to fake it)

In order then...

1. Get a Heroku app set up and installed
2. Get that app to talk to postgresql
3. Get Facebook auth working for that app
4. Get the "Squirrel!" button to create a "spot" (only allowed to click if you are geolocated)
5. The spot should include a name derived from where.yahooapis.com
6. Write the "spotted a squirrel" action to Facebook (with geodata)

(I'll use robots.txt to prevent Google from indexing)

Better Facebook integration...

7. auto-login
8. "your friends using this app" widget
9. Invite your friends to help spot squirrels, perhaps?
- Use the scoreboard stuff in Facebook to show who has seen the most squirrels!

graph.facebook.com/app_id/scores?access_token=...

https://developers.facebook.com/docs/scores/
"You can post a score for a user by issuing an HTTP POST request to /USER_ID/scores with a user or app access_token as long as the user has granted the publish_actions permission for your app."

And maybe https://developers.facebook.com/docs/achievements/ too?

I'll do a "Not really just testing" button at about this point.

... and a where can I see squirrels button? Squirrels near me?

Pusher stuff:

10. A web page tool for generating fake squirrel spots
11. Live page showing a map of where squirrels have been spotted (using a mapbox map)

Twilio stuff:

12. Text this code to a number to enable SMS reports
13. Report a squirrel via SMS (with a reply if we can't geocode it) - we'll also reply with a link to their spot page
  (if we can't write to Facebook because they're not signed in, the reply spot link page will prompt them to sign in to post their spot to facebook)
14. Text "Subscribe XXX" where XXX is a location we can geocode and we'll text you whenever a squirrel is spotted within 1km
15. Text "Unsubscribe" to turn that feature off again

"Simon Willison spotted a squirrel! In Finsbury Park"

And maybe... let people respond to spotted squirrels
- Ben doubts Simon's squirrel spot
- Nat congratulates Simon's squirrel spot

OMG... how about region-specific squirrel pictures? E.g. a London squirrel, a France squirrel etc...
