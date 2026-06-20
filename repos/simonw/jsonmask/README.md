jsonmask
========

A mini-language for selecting a subset of a JSON document.

Based on Google's mechanism for retrieving partial responses from 
their APIs: <https://developers.google.com/+/api/#partial-responses>

Mainly ported from <https://github.com/nemtsov/json-mask/>

Example usage - apply a mask of `data/children(data/(title,permalink))`
to the JSON returned from <http://www.reddit.com/.json>

```python
import urllib, json, jsonmask
data = json.load(urllib.urlopen('http://www.reddit.com/.json'))
mask = jsonmask.Mask('data/children(data/(title,permalink))')
print mask(d)
```

Prints:

```python
{'data': {'children': [{'data': {'permalink': u'/r/technology/comments/22iipg/google_kills_fake_antivirus_app_that_hit_no_1_on/',
     'title': u'Google kills fake anti-virus app that hit No. 1 on Play charts'}},
   {'data': {'permalink': u'/r/funny/comments/22inrh/dear_diary_jackpot/',
     'title': u'Dear Diary, Jackpot.'}},
   {'data': {'permalink': u'/r/gifs/comments/22ih0v/greetings/',
     'title': u'Greetings!'}},
...
```
