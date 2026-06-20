dmigrations - a simple migrations tool for Django
=================================================

> This project was [created in 2008](https://code.google.com/archive/p/dmigrations/). It has not been updated since 2009, and is archived here for historical reference.

**Current version: 0.3.1**

dmigrations offers a simple but flexible way of managing changes to the database in your Django projects. It is a replacement for Django's built in syncdb command.

With dmigrations, every change to your database (including the creation of your initial tables) is bundled up in a migration. Migrations are Python files that live in a migrations directory. They can be applied and un-applied (reverted) in sequence.

The dmigrations app provides two sets of management commands:

**./manage.py dmigrate**

`<command> <args>`

> Commands for listing, applying and un-applying migrations to your database.

**./manage.py dmigration**

`<command> <args>`

> Add a new migration to your migrations directory, ready to be executed using ./manage.py dmigrate

For a full introduction, see the dmigrations tutorial. Read understanding migrations for more details on how migrations work and how they are managed. Check out dmigrations settings for information on additional settings.

dmigrations was presented at DjangoCon as part of the Schema Evolution panel. You can watch the video of the session, which includes a demo of dmigrations in action, here: <http://www.youtube.com/watch?v=VSq8m00p1FM>

Limitations
-----------

-   dmigrations **requires Django 1.0** - it will not work with versions prior to the database creation refactoring in [8296](http://code.djangoproject.com/changeset/8296)
-   dmigrations currently only works with MySQL. It uses InnoDB tables by default, but can be configured to use MyISAM using the `DMIGRATIONS_MYSQL_ENGINE` setting
-   dmigrations uses decorators, so requires Python 2.4 or later.
-   Django's default test framework will still use syncdb, so it won't run your tests using your migrations to create the tables.
-   A major refactoring took place to prepare the code for release. If you find any bugs, please report them [in the bug tracker](http://code.google.com/p/dmigrations/issues/list).
-   It should go without saying, but it's an extremely good idea to **back up your production database** before running any migrations against it.

dmigrations was written by [Simon Willison](http://simonwillison.net/) and [Tomasz Wegrzanowski](http://t-a-w.blogspot.com/). The code is released under a BSD license, and is © Global Radio 2008.
