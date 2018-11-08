# Shinken/Nagios LiveStatus Integration Pack

This pack allows integration with the Shinken/Nagios LiveStatus API.

## Actions

The following actions are supported along with the arguments:

  * ``get_data``: Run a query against the livestatus interface.
    * _arguments_
    * ``table``: the table to query.
    * ``columns``: the columns to return.
    * ``filters``: the criterion to select the return rows.
    * ``stats``: perform a staticial query rather than a data query.
    * ``limit``: limit the number of returned rows.  (see Limitations section)

## Limitations

  * The query limit isn't supported under Shinken's LiveStatus implementation.
  * The author only has access to test against Shinken's LiveStatus implementation. While this should work for Nagios users, their milage may vary.

## References

  * https://github.com/shinken-monitoring/mod-livestatus
  * https://mathias-kettner.de/checkmk_livestatus.html

## Legal

This packs icon was kindly provided by https://icons8.com.
