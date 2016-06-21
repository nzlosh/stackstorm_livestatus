from st2actions.runners.pythonrunner import Action
from st2common import log as logging

import socket
import json

LOG = logging.getLogger(__name__)



class LiveStatus(object):
    def __init__(self, host, port, max_recv=4096):
        self.host = host
        self.port = int(port)
        self.max_recv = int(max_recv)


    def execute(self, query):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        LOG.debug('Sending LiveStatus query: {}'.format(query))
        s.send(query.encode('utf-8').rstrip() + '\n')
        # Close sending direction. That way the other side knows we are
        # finished.
        s.shutdown(socket.SHUT_WR)
        answer = ''
        buf = s.recv(self.max_recv)
        while buf:
            answer += buf
            buf = s.recv(self.max_recv)
        return answer


    def get_json(self, query):
        return json.loads(query)



class Get(Action):
    """
    LiveStatus Get class.

    table: the table query.
    columns: the columns to return in the dataset.
    filters: conditions to filter result set.
    stats: Calculate statistics held in data.
    limit: Not supported by Shinken.
    output_format: Not implemented, JSON is only supported.
    """
    def run(self, table='', columns=None, filters=None, stats=None, limit=None, output_format="json"):

        host = self.config['host']
        port = self.config['port']

        LOG.debug('table: {}'.format(table))

        live_status = LiveStatus(host, port)

        query = 'GET {}\n'.format(table)

        if columns:
            query += self._process_columns(columns)

        if filters:
            query += self._process_filters(filters)

        if stats:
            query += self._process_stats(stats)

        if limit:
            query += 'Limit: {}\n'.format(limit)

        if output_format.lower() == 'json':
            query += 'OutputFormat: json\n',
            result = live_status.get_json(query)
        else:
            result = live_status.execute(query)

        return result


    def _process_columns(self, columns):
        prefix = 'Columns: '
        postfix = '\n'
        return '{}{}{}'.format(prefix, ' '.join(columns), postfix)


    def _process_filters(self, filters):
        prefix = 'Filter: '
        postfix = '\n'
        tmp = ''
        for _filter in filters:
            tmp += '{}{}{}'.format(prefix, _filter, postfix)
        else:
            postfix = ''
        tmp += postfix
        return tmp


    def _process_stats(self, stats):
        prefix = 'Stats: '
        postfix = '\n'
        tmp = ''
        for stat in stats:
            tmp += '{}{}{}'.format(prefix, stat, postfix)
        else:
            postfix = ''
        tmp += postfix
        return tmp



