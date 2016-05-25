# Shinken/Nagios LiveStatus Integration Pack

This pack allows integration with the Shinken/Nagios LiveStatus API.

## Actions

The following actions are supported along with the arguments:

  * ``get_data``: Run a query against the livestatus interface.
    # parameters
       * ``table``: the table to query.
       * ``columns``: the columns to return.
       * ``filters``: the criterion to select the return rows.
       * ``stats``: perform a staticial query rather than a data query.
       * ``limit``: limit the number of returned rows.  (see Limitations section)

## Limitations

 * The response format is forced to JSON.  CSV and Python aren't supported.
 * The query limit isn't supported under Shinken's LiveStatus implementation.
 * The author only has access to test against Shinken's LiveStatus implementation. Nagios users YMMV.

## References
  https://github.com/shinken-monitoring/mod-livestatus
  https://mathias-kettner.de/checkmk_livestatus.html
