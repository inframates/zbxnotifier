from pyzabbix.api import ZabbixAPI
from modules.zabbix.elements import Trigger, Problem, Event, Host


class Zabbix:

    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

        self.zapi = ZabbixAPI(url=server, user=username, password=password)

    def get_problems(self):
        """
        Problems give object ids.
        If object is X, object id is:
            X=0: trigger
            X=4: item
            X=5 LLD rule
        :return: object_id list
        """
        print("Problem Query")
        data = self.zapi.problem.get(output='extend', selectAcknowledges="extend", selectTags="extend", selectSuppressionData="extend")
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
        print("Event Query")
        data = self.zapi.event.get(output="extend", objectids=trigger_ids, selectHosts="extend")
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
        print("Trigger Query")
        data = self.zapi.trigger.get(output="extend", triggerids=trigger_ids, expandDescription=True, status=0)
        triggers = []
        for trigger in data:
            triggers.append(Trigger(trigger.get('triggerid'), trigger.get('description'), trigger.get('priority'), trigger.get('lastchange')))

        return triggers




