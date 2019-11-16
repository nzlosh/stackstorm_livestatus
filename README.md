# livestatus integration pack v0.2.0

> Shinken/Nagios LiveStatus integration.
Carlos <nzlosh@yahoo.com>


## Configuration

The following options are required to be configured for the pack to work correctly.

| Option | Type | Required | Secret | Description |
|---|---|---|---|---|
| `host` | string | True | False | Livestatus host address |
| `port` | integer | True | False | Livestatus listening port |



## Actions


The pack provides the following actions:

### execute_command
_Execute an external command using the LiveStatus API.  Reference: https://mathias-kettner.de/checkmk_livestatus.html_
| Parameter | Type | Required | Secret | Description |
|---|---|---|---|--|
| `host_name` | string | True |  | _The table to be queried._ |
| `sticky` | boolean | False |  | _Cause the command to apply until the state changes to OK._ |
| `notify` | boolean |  |  | _Send a notification messsage._ |
| `persistent` | boolean | False |  | _Apply operation to persist between monitoring daemon restarts._ |
| `author` | string | True |  | _the name of the person who ran the command._ |
| `comment` | string | True |  | _the comment to apply to the operation._ |
### host_to_address
_Get the host address from the configuration by using the host name._
| Parameter | Type | Required | Secret | Description |
|---|---|---|---|--|
| `host` | string | True |  | __ |
### get
_Retrieve data using the LiveStatus API.  Reference: https://mathias-kettner.de/checkmk_livestatus.html_
| Parameter | Type | Required | Secret | Description |
|---|---|---|---|--|
| `table` | string | True |  | _The table to be queried._ |
| `columns` | array | False |  | _A list of columns to retrieve in the result set._ |
| `filters` | array | False |  | _A list of filters to use as criterion for the result set._ |
| `stats` | array | False |  | _A list of basic statistical operations to run._ |
| `limit` | string | False |  | _Limit the number of rows being displayed in the result set._ |
| `output_format` | string | False |  | _Result format, JSON, Python or CSV. (Only JSON is implemented)_ |
| `query_max_retries` | integer | False |  | _The number of times a query should be retried before abandonning the request._ |
| `query_duration` | integer | False |  | _The amount of time in seconds for a query to run before cancelling it._ |
| `query_retry_delay` | integer | False |  | _The amount of time to wait for retrying the query._ |
| `allow_empty_list` | boolean | False |  | _True: empty lists allowed, False: emtpy lists are treated as an error._ |
### state_overview
_Return the count of service checks by state (OK, WARNING, CRITICAL or UNKNOWN)._
| Parameter | Type | Required | Secret | Description |
|---|---|---|---|--|
| `skip_notify` |  |  |  | __ |
### host_services_overview
_Get the a hosts services state._
| Parameter | Type | Required | Secret | Description |
|---|---|---|---|--|
| `host` | string | True |  | _Host name to query._ |
### contact_email
_Get the contact name's email address._
| Parameter | Type | Required | Secret | Description |
|---|---|---|---|--|
| `name` | string | True |  | __ |




## Sensors

There are no sensors available for this pack.



## Limitations

  * The query limit isn't supported under Shinken's LiveStatus implementation.
  * The author only has access to test against Shinken's LiveStatus implementation. While this should work for Nagios users, their milage may vary.

## References

  * https://github.com/shinken-monitoring/mod-livestatus
  * https://mathias-kettner.de/checkmk_livestatus.html

## Legal

This packs icon was kindly provided by https://icons8.com.