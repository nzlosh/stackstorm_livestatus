from st2actions.runners.pythonrunner import Action
from st2common import log as logging

import json
import socket
import parsedatetime
from time import mktime
from datetime import datetime


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


class Command(Action):
    """
    LiveStatus External Command class.  This class provides a mapping between text command names
    and their Python implementations.
    """
    def run(
        self,
        command='',
        host_name,
        service_desription,
        start_time,
        end_time,
        fixed,
        trigger_id,
        duration,
        author,
        comment
    ):
        """
        The run method to be called by Stackstorm.

        :command: the string to lookup the Python function.
        :host_name: the host_name to query
        filters - conditions to filter result set.
        stats - Calculate statistics held in data.
        limit - Not supported by Shinken.
        output_format - json or csv formats.
        """
        host = self.config['host']
        port = self.config['port']

        live_status = LiveStatus(host, port)

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


class ExternalCommand(object):

    @staticmethod
    def unix_epoch(dt):
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(dt)
        mktime(datetime(*time_struct[:6]))
        return int(time.time())

    @staticmethod
    def sticky(sticky=True):
        return {True: 2, False: 0}.get(sticky, 2)

    @staticmethod
    def notify(notify=True):
        return {True: 1, False: 0}.get(notify, 1)

    @staticmethod
    def fixed(fixed=True):
        return {True: 1, False: 0}.get(fixed, 1)

    @staticmethod
    def persistent(persistent=True):
        return {True: 1, False: 0}.get(persistent, 1)

    def __init__(self):
        self.args = None

    def execute(self):
        return "[{}] {} {}".format(Command.unix_epoch(), self.cmd, ";".join(self.args), LS_EOL)


class RemoveHostAcknowledgement(ExternalCommand):
    """
    Removes the problem acknowledgement for a particular host.
    """
    def __init__(self, host_name=""):
        self.cmd = "REMOVE_HOST_ACKNOWLEDGEMENT"
        self.args = [host_name]


class RemoveServiceAcknowledgement(ExternalCommand):
    """
    Removes the problem acknowledgement for a particular service.
    """
    def __init__(self, host_name, service_description):
        self.cmd = "REMOVE_SVC_ACKNOWLEDGEMENT"
        self.args = [host_name, service_description]


class AcknowledgeHostProblem(ExternalCommand):
    """
    Acknowledge the current problem for the specified host.
    :sticky: True - the acknowledgement will remain until the host returns to an UP state.
             Otherwise the acknowledgement will automatically be removed when the host changes
             state.
    :notify: True - a notification will be sent out to contacts indicating that the current host
             problem has been acknowledged.
    :persistent: True - the comment associated with the acknowledgement will survive across restarts
                 of the monitor daemon.
    """
    def __init__(
        self,
        host_name,
        sticky=True,
        notify=True,
        persistent=True,
        author="Unknown",
        comment="No comment provided."
    ):
        self.cmd = "ACKNOWLEDGE_HOST_PROBLEM"
        self.args = [
            host_name,
            self.sticky(sticky),
            self.notify(notify),
            self.persistent(persistent),
            author,
            comment
        ]


class AcknowledgeServiceProblem(ExternalCommand):
    """
    Acknowledge the current problem for the specified service.
    :sticky: True - the acknowledgement will remain until the service returns to an OK state.
             Otherwise the acknowledgement will automatically be removed when the service changes
             state.
    :notify: True - a notification will be sent out to contacts indicating that the current service
             problem has been acknowledged.
    :persistent: True - the comment associated with the acknowledgement will survive across restarts
                 of the monitoring daemon.
    """
    def __init__(
        self,
        host_name,
        service_description,
        sticky=True,
        notify=True,
        persistent=True,
        author="Unknown",
        comment="No comment provided."
    ):
        self.cmd = "ACKNOWLEDGE_SVC_PROBLEM"
        self.args = []
        raise NotImplementedError


class ScheduleHostDowntime(ExternalCommand):
    """
    Schedules downtime for a specified host.
    :fixed: True - the downtime will start and end at the times specified by the "start" and "end"
            arguments.
            False - the downtime will begin between the "start" and "end" times and last for
            "duration" seconds.
    :start: specified in time_t format (seconds since the UNIX epoch).
    :end: specified in time_t format (seconds since the UNIX epoch).
    :trigger_id: The specified host downtime can be triggered by another downtime entry if the
                 "trigger_id" is set to the ID of another scheduled downtime entry.
                 If set to zero (0) to indicate the specified host should not be triggered by
                 another downtime entry.
    """
    def __init__(
        self,
        host_name,
        start_time=None,
        end_time=None,
        fixed=True,
        trigger_id=0,
        duration=None,
        author="Unknown",
        comment="No comment provided."
    ):
        self.cmd = "SCHEDULE_HOST_DOWNTIME"
        if start_time is end_time is duration is None:
            # Use a default duration fo 60 mins
            start_time = "now"
            duration = "30min"
        else if start_time is not None and duration is not None:
            # handle a fixed duration.
            fixed = False
            if end_time is None:
                end_time = start_time
        else:
            # handle start/end datetime range here.
            fixed = True
            if start_time is None:
                start_time = "now"
            if end_time is None:
                end_time = "{} + 30min".format(start_time)

        self.args = [
            host_name,
            start_time,
            end_time,
            self.fixed(fixed), ]
        raise NotImplementedError


class ScheduleServiceDowntime(ExternalCommand):
    """
    Schedules downtime for a specified service.
    :fixed: True - downtime will start and end at the times specified by the "start" and "end"
                   arguments.
            False - downtime will begin between the "start" and "end" times and last for "duration"
                    seconds.
    :start: specified in time_t format (seconds since the UNIX epoch).
    :end: specified in time_t format (seconds since the UNIX epoch).
    :trigger_id: The specified service downtime can be triggered by another downtime entry if the
                 "trigger_id" is set to the ID of another scheduled downtime entry.
                 If set to zero (0) the downtime for the specified service should not be triggered
                 by another downtime entry.
    """
    def __init__(
        self,
        host_name,
        service_desription,
        start_time,
        end_time,
        fixed,
        trigger_id,
        duration,
        author,
        comment
    ):
        self.cmd = "SCHEDULE_SVC_DOWNTIME"
        raise NotImplementedError

"""
# To do:
# date parsing with parsedatetime
#
# date examples.
# .st2 sd web-450 for 5d
# .st2 sd web-450 from 5 jan 2018 to 6 jan 2018
# .st2 sd web-450 in 1 hour for 4 hours
# .st2 sd web-450 at 1pm to 2pm

GET hosts
Columns: name comments_with_info
Filter: acknowledged != 0

GET services
Columns: host_name description host_comments_with_info service_comments_with_info
Filter: acknowledged != 0

"""
