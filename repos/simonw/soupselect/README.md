A single function, select(soup, selector), that can be used to select items
from a BeautifulSoup instance using CSS selector syntax.

Currently supports type selectors, class selectors, id selectors, attribute
selectors and the descendant combinator.

soupselect requires BeautifulSoup v3.0.3 or above; it will not work with v2.x

Example usage:

    >>> from BeautifulSoup import BeautifulSoup as Soup
    >>> from soupselect import select
    >>> import urllib
    >>> soup = Soup(urllib.urlopen('http://slashdot.org/'))
    >>> select(soup, 'div.title h3')
    [<h3>
    <span><a href='//science.slashdot.org/'>Science</a>:</span> ...
    </h3>, <h3>
    <a href='//slashdot.org/articles/07/02/28/0120220.shtml'>Star Trek To ...
    </h3>
    ... ]

You can also monkey-patch the BeautifulSoup class itself:

    >>> from BeautifulSoup import BeautifulSoup as Soup
    >>> import soupselect; soupselect.monkeypatch()
    >>> import urllib
    >>> soup = Soup(urllib.urlopen('http://slashdot.org/'))
    >>> soup.findSelect('div.title h3')
    [<h3>
    ...
