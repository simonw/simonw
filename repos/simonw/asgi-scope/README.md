# asgi-scope

A tiny application for understanding ASGI scope

Example: https://asgi-scope.now.sh/path?qs=hello

    {'client': ('172.29.0.10', 34784),
     'headers': [[b'host', b'asgi-scope.now.sh'],
                 [b'x-forwarded-host', b'asgi-scope.now.sh'],
                 [b'x-real-ip', b'199.188.193.220'],
                 [b'x-forwarded-for', b'199.188.193.220'],
                 [b'x-forwarded-proto', b'https'],
                 [b'x-now-id', b'fb6gw-1527863960919-mjYC9OJ9WTsfnw4EiRTDmMst'],
                 [b'x-now-log-id', b'mjYC9OJ9WTsfnw4EiRTDmMst'],
                 [b'x-zeit-co-forwarded-for', b'199.188.193.220'],
                 [b'connection', b'close'],
                 [b'user-agent',
                  b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko'
                  b'/20100101 Firefox/60.0'],
                 [b'accept',
                  b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q='
                  b'0.8'],
                 [b'accept-language', b'en-US,en;q=0.5'],
                 [b'accept-encoding', b'gzip, deflate, br'],
                 [b'upgrade-insecure-requests', b'1']],
     'http_version': '0.0',
     'method': 'GET',
     'path': '/path',
     'query_string': b'qs=hello',
     'scheme': 'http',
     'server': ('172.28.0.10', 8000),
     'type': 'http'}

See also https://github.com/django/asgiref/blob/master/specs/www.rst
