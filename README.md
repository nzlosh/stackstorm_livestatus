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
|---|---|---|---|---|
| `host_name` | string | True | default | _The table to be queried._ |
| `sticky` | boolean | False | default | _Cause the command to apply until the state changes to OK._ |
| `notify` | boolean | default | default | _Send a notification message._ |
| `persistent` | boolean | False | default | _Apply operation to persist between monitoring daemon restarts._ |
| `author` | string | True | default | _the name of the person who ran the command._ |
| `comment` | string | True | default | _the comment to apply to the operation._ |
### host_to_address
_Get the host address from the configuration by using the host name._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `host` | string | True | default | _Unavailable_ |
### get
_Retrieve data using the LiveStatus API.  Reference: https://mathias-kettner.de/checkmk_livestatus.html_

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `table` | string | True | default | _The table to be queried._ |
| `columns` | array | False | default | _A list of columns to retrieve in the result set._ |
| `filters` | array | False | default | _A list of filters to use as criterion for the result set._ |
| `stats` | array | False | default | _A list of basic statistical operations to run._ |
| `limit` | string | False | default | _Limit the number of rows being displayed in the result set._ |
| `output_format` | string | False | default | _Result format, JSON, Python or CSV. (Only JSON is implemented)_ |
| `query_max_retries` | integer | False | default | _The number of times a query should be retried before abandoning the request._ |
| `query_duration` | integer | False | default | _The amount of time in seconds for a query to run before cancelling it._ |
| `query_retry_delay` | integer | False | default | _The amount of time to wait for retrying the query._ |
| `allow_empty_list` | boolean | False | default | _True: empty lists allowed, False: empty lists are treated as an error._ |
### state_overview
_Return the count of service checks by state (OK, WARNING, CRITICAL or UNKNOWN)._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `skip_notify` | n/a | default | default | _Unavailable_ |
### host_services_overview
_Get the a hosts services state._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `host` | string | True | default | _Host name to query._ |
### contact_email
_Get the contact name's email address._

| Parameter | Type | Required | Secret | Description |
|---|---|---|---|---|
| `name` | string | True | default | _Unavailable_ |



## Sensors

There are no sensors available for this pack.


## Limitations

  * The query limit isn't supported under Shinken's LiveStatus implementation.
  * The author only has access to test against Shinken's LiveStatus implementation. While this should work for Nagios users, there is not testing performed against it.

## References

  * https://github.com/shinken-monitoring/mod-livestatus
  * https://mathias-kettner.de/checkmk_livestatus.html

## Legal

This packs icon was kindly provided by https://icons8.com.
