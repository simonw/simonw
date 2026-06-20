# sqlite-fts5-trigram

Trigram tokenizer module for SQLite FTS5

Code by Dan Kennedy, shared on [this forum thread](https://sqlite.org/forum/forumpost/ca90da691a?t=h).

See also [my weeknotes](https://simonwillison.net/2020/Sep/26/weeknotes-software-carpentry-sqlite/) describing this repository.

**This repository is now obsolete** because this shipped as a feature in December 2020 in [SQLite 3.34.0](https://www.sqlite.org/releaselog/3_34_0.html).

Example usage:
```
Python 3.8.5 (default, Jul 21 2020, 10:48:26) 
[Clang 11.0.3 (clang-1103.0.32.62)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlite3
>>> c = sqlite3.connect(":memory:")
>>> c
<sqlite3.Connection object at 0x107e137b0>
>>> c.enable_load_extension(True)
>>> c.load_extension("ftstri.so")
>>> c
<sqlite3.Connection object at 0x107e137b0>
>>> c.execute("CREATE VIRTUAL TABLE dict USING fts5(word, tokenize=tri);")
<sqlite3.Cursor object at 0x107e9f880>
>>> c.execute('INSERT INTO dict values ("simon")')
<sqlite3.Cursor object at 0x107e9f8f0>
>>> c.execute('INSERT INTO dict values ("cleo")')
<sqlite3.Cursor object at 0x107e9f880>
>>> c.execute('INSERT INTO dict values ("natalie")')
<sqlite3.Cursor object at 0x107e9f8f0>
>>> c.execute('select * from dict(?)', ['simon']).fetchall()
[('simon',)]
>>> c.execute('select * from dict(?)', ['sim']).fetchall()
[('simon',)]
>>> c.execute('select * from dict(?)', ['imo']).fetchall()
[('simon',)]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['sim']).fetchall()
[('(sim)on',)]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['simon']).fetchall()
[('(simon)',)]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['mon']).fetchall()
[('si(mon)',)]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['cl']).fetchall()
[]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['cleo']).fetchall()
[('(cleo)',)]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['cle']).fetchall()
[('(cle)o',)]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['cleop']).fetchall()
[]
>>> c.execute("select highlight(dict, 0, '(', ')') from dict(?)", ['nat']).fetchall()
[('(nat)alie',)]
```
