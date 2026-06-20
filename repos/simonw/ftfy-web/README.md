# ftfy-web

A simple web wrapper around [Robyn Speer](https://twitter.com/r_speer)'s [FTFY Python library](https://github.com/LuminosoInsight/python-ftfy). Paste in some broken unicode text and it will tell you how to fix it!

Try it out at https://ftfy.now.sh/

The tool outputs Python code to fix the input text, for example:

    s = "He's Justinâ\x9d¤"
    s = s.encode('latin-1')
    s = s.decode('utf-8')
    print(s)

In some cases it will output additional imports from the ftfy package, for example:

    import ftfy.bad_codecs  # enables sloppy- codecs
    from ftfy.fixes import restore_byte_a0
    s = 'It was namedÂ â€žscarsÂ´ stonesâ€ś after the rock-climbers who got hurt while climbing on it.'
    s = s.encode('sloppy-windows-1250')
    s = restore_byte_a0(s)
    s = s.decode('utf-8')
    print(s)
