from pyzabbix.api import ZabbixAPI
from zbxnotifier.modules.settings import Settings
from zbxnotifier.modules.zabbix.elements import Trigger, Problem, Event, Host
from pyzabbix.api import ZabbixAPIException
import time


class ZabbixConnection:
    connection = None
    token = None
    error = False
    error_message = ""
    retry_num = 0
    backoff_num = 1

    @staticmethod
    def connect_thread():
        while True:
            # Not to rush
            time.sleep(2)

            # Set message, as we are connecting
            ZabbixConnection.error = True
            ZabbixConnection.error_message = "Connecting..."

            if ZabbixConnection.connection is None:
                print("Starting Login Process")
                url = Settings.config.get('ZabbixSettings', 'server')
                username = Settings.config.get('ZabbixSettings', 'username')
                password = Settings.config.get('ZabbixSettings', 'password')

                if url == "" or username == "" or password == "":
                    ZabbixConnection.error = True
                    ZabbixConnection.error_message = "Please set Username, Password and Server URL in Configuration!"
                    continue

                try:
                    ZabbixConnection.connection = ZabbixAPI(url=url, user=username, password=password)
                except ZabbixAPIException as e:
                    ZabbixConnection.error = True
                    ZabbixConnection.error_message = e.data
                    ZabbixConnection.retry_num += 1
                except Exception as e:
                    ZabbixConnection.error = True
                    ZabbixConnection.error_message = str(e)
                    ZabbixConnection.retry_num += 1
                else:
                    ZabbixConnection.token = ZabbixConnection.connection.auth
                    ZabbixConnection.error_message = ""
                    ZabbixConnection.error = False

                if ZabbixConnection.retry_num / ZabbixConnection.backoff_num > 3:
                    print("Backoff limit reached.")
                    ZabbixConnection.error_message += " Backoff limit reached, retying after 10 seconds.."
                    time.sleep(10)
                    ZabbixConnection.backoff_num += 1


    @staticmethod
    def re_init():
        ZabbixConnection.connection = None
        ZabbixConnection.token = None
        ZabbixConnection.error = True
        ZabbixConnection.error_message = "Connection re-initializing"

    @staticmethod
    def get_status_desc():
        if ZabbixConnection.connection is not None and ZabbixConnection.token is not None and ZabbixConnection.error is False:
            return "Connected"
        elif ZabbixConnection.connection is None and ZabbixConnection.token is None and ZabbixConnection.error is False:
            return "Logging in"
        elif ZabbixConnection.connection is None and ZabbixConnection.token is None and ZabbixConnection.error is True:
            return "Error: " + str(ZabbixConnection.error_message)
        return "Disconnected"

    @staticmethod
    def is_connected():
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




