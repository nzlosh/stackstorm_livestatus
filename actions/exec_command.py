from st2actions.runners.pythonrunner import Action
from st2common import log as logging

import socket
import json

LOG = logging.getLogger(__name__)
LS_EOL = '\n'


class LiveStatus(object):
    """
    LiveStatus class provides network access to the Live status server.
    """
    def __init__(self, host, port, max_recv=4096):
        self.host = host
        self.port = int(port)
        self.max_recv = int(max_recv)


    def execute(self, query):
        """
        execute method sends the query to the live status server and
        returns the result.

        @query - a livestatus query.
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.host, self.port))
        LOG.debug('Sending LiveStatus query: {}'.format(query))
        server.send(query.encode('utf-8').rstrip() + LS_EOL)
        # Notify server that transmission has finished.
        server.shutdown(socket.SHUT_WR)
        answer = ''
        buf = server.recv(self.max_recv)
        while buf:
            answer += buf
            buf = server.recv(self.max_recv)
        return answer


    def get_json(self, query):
        """
        Parse the result of a live status query as JSON.

        @query - a livestatus query. The query MUST request the result
                 is returned in JSON format.
        """
        return json.loads(self.execute(query))



class Get(Action):
    """
    LiveStatus Get class.
    """
    def run(self, table='', columns=None, filters=None, stats=None, limit=None, output_format="json"):
        """
        The run method to be called by Stackstorm.

        table - the table query.
        columns - the columns to return in the dataset.
        filters - conditions to filter result set.
        stats - Calculate statistics held in data.
        limit - Not supported by Shinken.
        output_format - json or csv formats.
        """
        host = self.config['host']
        port = self.config['port']

        live_status = LiveStatus(host, port)
        query = 'GET {}{}'.format(table, LS_EOL)

        if columns:
            query += self._process_columns(columns)

        if filters:
            query += self._process_filters(filters)

        if stats:
            query += self._process_stats(stats)

        if limit:
            query += 'Limit: {}{}'.format(limit, LS_EOL)

        if output_format.lower() == 'json':
            query += 'OutputFormat: json{}'.format(LS_EOL)
            result = live_status.get_json(query)
        else:
            result = live_status.execute(query)

        return result


    def _process_columns(self, columns):
        """
        Convert columns list to livestatus formatted string.
        """
        return self._build_list('Columns: ', LS_EOL, [' '.join(columns)])


    def _process_filters(self, filters):
        """
        Convert filters list to livestatus formatted string.
        """
        return self._build_list('Filter: ', LS_EOL, filters)


    def _process_stats(self, stats):
        """
        Convert stats list to livestatus formatted string.
        """
        return self._build_list('Stats: ', LS_EOL, stats)


    def _build_list(self, prefix, postfix, items):
        """
        Loop over list items and apply a prefix/postfix to each element.
        Returns a livestatus formatted string.
        """
        tmp = ''
        for _item in items:
            tmp += '{}{}{}'.format(prefix, _item, postfix)
        else:
            postfix = ''
        tmp += postfix
        return tmp

