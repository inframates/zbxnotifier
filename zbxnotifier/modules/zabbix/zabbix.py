from pyzabbix.api import ZabbixAPI
from zbxnotifier.modules.settings import Settings
from modules.zabbix.elements import Trigger, Problem, Event, Host


class ZabbixConnection:
    connection = None
    token = None

    def __init__(self):
        if ZabbixConnection.connection is None:
            ZabbixConnection.connection = ZabbixAPI(url=Settings.zabbix_url, user=Settings.zabbix_user, password=Settings.zabbix_password)
            ZabbixConnection.token = ZabbixConnection.connection.auth

    def get_status_desc(self):
        if ZabbixConnection.connection is not None and ZabbixConnection.token is not None:
            return "Connected"
        return "Disconnected"

    def is_connected(self):
        if ZabbixConnection.connection is None:
            return False
        return True


class Zabbix:

    def get_problems(self):
        """
        Problems give object ids.
        If object is X, object id is:
            X=0: trigger
            X=4: item
            X=5 LLD rule
        :return: object_id list
        """
        data = ZabbixConnection.connection.problem.get(output='extend', selectAcknowledges="extend", selectTags="extend", selectSuppressionData="extend")
        problems = []
        for problem in data:
            problems.append(Problem(problem.get('objectid'), problem.get('clock')))
        return problems

    def get_events(self, trigger_ids):
        """
        Gets and event based on the event id
        objectid is always a trigger
        :param event_id:
        :return:
        """
        data = ZabbixConnection.connection.event.get(output="extend", objectids=trigger_ids, selectHosts="extend")
        events = []
        for event in data:
            hosts = []
            for host in event.get('hosts'):
                hosts.append(Host(host.get('name'), host.get('hostid')))
            events.append(Event(event.get('objectid'), event.get('eventid'), hosts))

        return events

    def get_triggers(self, trigger_ids):
        """
        Returns a trigger based on the trigger_id
        :param trigger_id:
        :return:
        """
        data = ZabbixConnection.connection.trigger.get(output="extend", triggerids=trigger_ids, expandDescription=True, status=0)
        triggers = []
        for trigger in data:
            triggers.append(Trigger(trigger.get('triggerid'), trigger.get('description'), trigger.get('priority'), trigger.get('lastchange')))

        return triggers




