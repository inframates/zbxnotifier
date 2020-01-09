from pyzabbix.api import ZabbixAPI
from zbxnotifier.modules.elements import Trigger


class Zabbix:

    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

        self.zapi = ZabbixAPI(url=server, user=username, password=password)

    def get_problems_ids(self):
        """
        Problems give object ids.
        If object is X, object id is:
            X=0: trigger
            X=4: item
            X=5 LLD rule
        :return: object_id list
        """
        problems = self.zapi.problem.get(output='extend', selectAcknowledges="extend", selectTags="extend")

        object_ids = []
        for problem in problems:
            object_ids.append(problem.get('objectid'))

        return object_ids

    def get_event(self, event_id):
        """
        Gets and event based on the event id
        objectid is always a trigger
        :param event_id:
        :return:
        """
        events = self.zapi.event.get(output="extend", eventid=event_id, selectHosts="extend")
        return events

    def get_trigger(self, trigger_id):
        """
        Returns a trigger based on the trigger_id
        :param trigger_id:
        :return:
        """
        trigger = self.zapi.trigger.get(output="extend", triggerids=[trigger_id], expandDescription=True, status=0)[0]
        return Trigger(trigger.get('triggerid'), trigger.get('description'), trigger.get('priority'))




