django_signed
=============

This project demonstrates a proposed signing API for Django. You can run the 
test suite like so:

    cd examples
    ./manage.py test

The API is under heavy development. It is described in more detail here:

    http://code.djangoproject.com/wiki/Signing

The mailing list discussion is here:

http://groups.google.com/group/django-developers/browse_thread/thread/133509246caf1d91

TODO:

 - Add support for expiring signatures
 - Try using a class instead of functions, as suggested by Johannes Dollinger
 - Cookie signing functions
 - Middleware that illustrates the proposed request cookie signing API
 - Support key migration from an OLD_SECRET_KEY to the current one

baseconv.py
-----------

Part of this module is baseconv.py, which I hope to contribute to 
django.utils. baseconv allows you to convert between integers and various 
different string representations of those numbers. For example:

>>> import baseconv
>>> i = 102971
>>> baseconv.base2.from_int(i)
'11001001000111011'
>>> baseconv.base16.from_int(i)
'1923B'
>>> baseconv.base36.from_int(i)
'27gb'
>>> baseconv.base62.from_int(i)
'Qmp'

You can convert back again using the to_int(string) method:

>>> baseconv.base2.to_int('11001001000111011')
102971
>>> baseconv.base16.to_int('1923B')
102971
>>> baseconv.base36.to_int('27gb')
102971
>>> baseconv.base62.to_int('Qmp')
102971

This is principally useful as a compression scheme for transmitting numbers as 
ascii text - in particular for URLs (URL shortening services such as bit.ly 
use this technique). The signed cookie implementation uses this to represent 
a unix timestamp in as few characters as possible, to keep cookie lengths 
down.

If you wish to use your own shortening scheme you can use the BaseConvertor 
class. For example, you might want to just use characters that aren't easily confused with each other - the alphabet omitting i, l and o:

>>> convertor = baseconv.BaseConverter('abcdefghjkmnpqrstuvwxyz')
>>> convertor.from_int(102971)
'jmsa'
>>> convertor.to_int('jmsa')
102971
