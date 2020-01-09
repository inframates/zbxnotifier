from zbxnotifier.modules.elements import Host


class Problems:

    def __init__(self, zbx):
        self.zbx = zbx

    def get_hosts(self, event_id):
        hosts = []
        events = self.zbx.get_event(event_id)
        for event in events:
            for host in event.get('hosts'):
                if host.get('status') == '0':
                    hosts.append(Host(host.get('hostid'), host.get('host'), event.get('objectid')))
        return hosts

    def get_trigger(self, host):
        return self.zbx.get_trigger(host.trigger_id)

    def get_host_problems(self):
        print("Getting host problems")
        hosts = []

        problem_ids = self.zbx.get_problems_ids()
        for problem_id in problem_ids:
            hosts.extend(self.get_hosts(problem_id))

        for host in hosts:
            host.trigger = self.get_trigger(host)

        return hosts