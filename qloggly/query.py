import requests

class QLoggly:

    def __init__(self):
        import ConfigParser
        import os

        # Read account information from configuration file
        config = ConfigParser.ConfigParser()

        filename = os.path.expanduser('~/.loggly')
        if os.path.exists(filename):
            config.read(filename)

            self.account = config.get('loggly', 'account')
            self.username = config.get('loggly', 'username')
            self.password = config.get('loggly', 'password')

    def __endpoint(self, endpoint, **kwargs):
        """Generic endpoint"""
        from urllib import urlencode

        # Loggly uses 'from' in some queries, but this argument name is
        # disallowed in Python function calls, so we use 'start' instead
        try:
            kwargs['from'] = kwargs.pop('start')
        except KeyError:
            pass

        # Construct query URL
        url = 'http://{account}.loggly.com/apiv2/{endpoint}?{query}'.format(
            account=self.account,
            endpoint=endpoint,
            query=urlencode(kwargs.items()))

        # Perform request and raise exception on error
        r = requests.get(url, auth=(self.username, self.password))
        r.raise_for_status()

        # Return response
        return r.json()

    def search(self, query, **kwargs):
        """Initiate a query

        There is currently a maximum limit of 5000 individual events returned
        per search query. We don't support paging beyond this 5000 event limit
        either. If a search encompasses more than 5000 events, you will have to
        do another query to retrieve more events.

        Arguments:
            query: (required) Query string, check out the Search Query help.
            start: (optional) Start time for the search. Defaults to "-24h".
            until: (optional) End time for the search. Defaults to "now".
            order: (optional) Direction of results returned, either "asc" or
                              "desc". Defaults to "desc".
            size:  (optional) Number of rows returned by search. Defaults to 50.

        Return:
            JSON object
        """
        return self.__endpoint('search', q=query, **kwargs)

    def events(self, rsid, **kwargs):
        """Retrieve search results for given RSID

        Arguments:
            rsid:    (required) The ID that was returned in response to your
                                /search request
            page:    (optional) Which page of results you'd like returned.
                                Defaults to 0 if not defined. Pages are also
                                zero-indexed, starting at 0 for the first page.
            format:  (optional) Data format you'd like to have your results
                                returned. Options are "raw", "csv", or "json".
                                If "json" is used as a format, it will provide
                                a file to download. Default is "json".
            columns: (optional) If you'd like to limit your result set to a set
                                list of fields. Takes a comma separated list.

        Return:
            JSON object
        """
        return self.__endpoint('events', rsid=rsid, **kwargs)
