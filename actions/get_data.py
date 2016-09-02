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
        # Close sending direction to indicate end of transmission.
        s.shutdown(socket.SHUT_WR)
        answer = ''
        buf = s.recv(self.max_recv)
        while buf:
            answer += buf
            buf = s.recv(self.max_recv)
        return answer


    def get_json(self, query):
        return json.loads(self.execute(query))



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
            query += 'OutputFormat: json\n'
            result = live_status.get_json(query)
        else:
            result = live_status.execute(query)

        return result


    def _process_columns(self, columns):
        prefix = 'Columns: '
        postfix = '\n'
        return '{}{}{}'.format(prefix, ' '.join(columns), postfix)


    def _process_filters(self, filters):
        return self._build_list('Filter: ', '\n', stats)


    def _process_stats(self, stats):
        return self._build_list('Stats: ', '\n', stats)


    def _build_list(self, prefix, postfix, query_list):
        tmp = ''
        for _item in items:
            tmp += '{}{}{}'.format(prefix, _item, postfix)
        else:
            postfix = ''
        tmp += postfix
        return tmp



class Command(Action):
    """
    Execute Nagios/Shinken commands

        COMMAND [$(date +%s)] START_EXECUTING_SVC_CHECKS

    Perform acknowledges, downtimes etc.
    """
    def run():
        return True
