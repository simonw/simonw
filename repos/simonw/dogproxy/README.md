# dogproxy

A very simple dog pile preventing proxy.

The dog pile effect (also known as a thundering herd) affects caching systems
that use time-based expiry. In a heavy traffic system, a cached item expiring
could cause dozens of parallel "update" requests to be fired at once.

dogproxy assumes that these update requests go over HTTP. It joins together
simultaneous requests for the same URL, and only performs one actual fetch to
that resource.

STATUS: highly experimental. Known bugs (Content-Type is not correctly passed
through, for example). Expect to modify this code further before use.

Usage:

    $ node dogproxy.js 
    Server running at http://127.0.0.1:8009/

Testing using ab:

    $ ab -n 10 -c 5 'http://127.0.0.1:8009/?url=http://example.com/'

dogproxy.js says:

```
Request for http://example.com/
... kicking off backend HTTP fetch
Request for http://example.com/
... already in flight, adding to queue
Request for http://example.com/
... already in flight, adding to queue
Request for http://example.com/
... already in flight, adding to queue
Request for http://example.com/
... already in flight, adding to queue
Fetched http://example.com/, alerting 5 waiting clients
Request for http://example.com/
... kicking off backend HTTP fetch
Request for http://example.com/
... already in flight, adding to queue
Request for http://example.com/
... already in flight, adding to queue
Request for http://example.com/
... already in flight, adding to queue
Request for http://example.com/
... already in flight, adding to queue
Fetched http://example.com/, alerting 5 waiting clients
```
