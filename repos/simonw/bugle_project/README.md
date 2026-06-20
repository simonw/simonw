bugle
=====

Group collaboration tools for hackers in forts.

Dependencies:

- Several collaborating hackers
- A fort, castle or other defensive structure
- No internet connection

Bugle is a Twitter-like application for groups of hackers collaborating in a 
castle (or fort, or other defensive structure) with no internet connection.
Bugle combines Twitter-style status updates with a pastebin and a group todo
list. It also has a rudimentary API allowing automated scripts (such as the 
included subversion post-commit hook) to post messages in an unobtrusive way.

It was built as a side project during a [/dev/fort](http://devfort.com/) week 
in a Scottish castle. 

Server-side code is by Simon Willison, and the parts of the CSS that don't 
suck are by Natalie Downe (Simon's butchered it a bit since then).

Awesome/Evil Twitter API imitation by Ben Firshman.

Bugle isn't secure (vulnerable to CSRF) and probably doesn't scale.

Bugle is released under a BSD license.

Development installation
------------------------

Fabric is required:
    
    $ sudo easy_install fabric

To set up a development environment:

    $ mysql -u root
    mysql> create database bugle default charset = "utf8";
    mysql> exit
    $ fab localhost setup_dev 
    $ cd bugle_project/
    $ ./manage.py syncdb
    $ ./manage.py migrate

If ``requirements.txt`` gets updated in the future, you may need to run:

    $ fab localhost install_requirements


Test suite
----------

    $ fab localhost test


Setting up live server
----------------------

Before deploying for the first time, install Apache and mod-wsgi 
(``libapache2-mod-wsgi`` on Debian).

Create MySQL database ``bugle`` and an SSL certificate:

    $ mysql -u root
    mysql> create database bugle default charset = "utf8";
    $ make-ssl-cert generate-default-snakeoil --force-overwrite
    $ a2enmod ssl

Set up the deployment environment:

    $ fab live setup

Deployment
----------

To deploy new versions:

    $ fab live create_version deploy


Magic Twitter support
---------------------

To make Twitter clients magically work with Bugle on a network, we 
need to mess with BIND.

Create ``/etc/bind/db.twitter.com``:

    $TTL    604800
    @   IN  SOA localhost.  root.localhost. (
                        4   ; Serial
                        604800  ; Refresh
                        86400   ; Retry
                        2419200 ; Expire
                        604800  ; Negative Cache TTL
                        )

    @       IN  NS  10.0.0.1
    @       IN  NS  10.0.0.2
    @       IN  A   10.0.0.1
    api     IN  A   10.0.0.1

Add to ``/etc/bind/named.conf.local``:

    zone "twitter.com." {
            type master;
            file "/etc/bind/db.twitter.com";
    };



