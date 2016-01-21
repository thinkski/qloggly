# QLoggly

Python interface to Loggly's Query API. Information on the API is available at
https://www.loggly.com/docs/api-retrieving-data/

## Quick start

Initiate a search:

    >>> from qloggly.query import QLoggly
    >>> q = QLoggly()
    >>> d = q.search('test')
    >>> d
    {u'rsid': {u'status': u'RUNNING', u'elapsed_time': 0.03364396095275879, u'date_from': 1452473225000, u'id': u'123456789', u'date_to': 1453337225000}}

Then retrieve the results:

    >>> q.events(d['rsid']['id'])
    {u'total_events': 7150, u'page': 0, u'events': ...

## Credentials

Credentials are read from a `~/.loggly` configuration file that looks
something like:

    [loggly]
    account = acmecorp
    username = joe
    password = koolkatz
