# validate-utf8

[![PyPI](https://img.shields.io/pypi/v/validate-utf8.svg)](https://pypi.org/project/validate-utf8/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/validate-utf8/blob/master/LICENSE)

Python library and CLI for validating UTF-8 text.

Install it like this:

    pip3 install validate-utf8

The command-line tool works like this:

    $ validate-utf8 20081104__wv__general__mason__precinct.csv
    invalid continuation byte
    Mason,28 COURTHOUSE-GROUND FLOORá,,,REP,Straight Ticket,15
                                    ^
    invalid continuation byte
    Mason,28 COURTHOUSE-GROUND FLOORá,,,DEM,Straight Ticket,21
                                    ^

Use it as a library like this:

    from validate_utf8 import find_utf8_errors

    errrors = find_utf8_errors(bytestring):
    if not errors:
        print("It is valid")
    else:
        print(errors)
