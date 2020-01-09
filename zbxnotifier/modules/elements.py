

class Host:
    def __init__(self, hostid, hostname, trigger_id):
        self.hostid = hostid
        self.hostname = hostname
        self.trigger_id = trigger_id
        self.trigger = None

    def __str__(self):
        return "Hostname: " + self.hostname + " hostid: " + str(self.hostid) + " trigger: " + str(self.trigger)

    def __repr__(self):
        return self.__str__()


class Trigger:
    def __init__(self, triggerid, description, priority):
        self.triggerid = triggerid
        self.description = description
        self.priority = priority
        self.priority_desc = None
        self.set_priority()

    def set_priority(self):
        if self.priority == '0':
            self.priority_desc = "Not Classified"
        elif self.priority == '1':
            self.priority_desc = "Information"
        elif self.priority == '2':
            self.priority_desc = "Warning"
        elif self.priority == '3':
            self.priority_desc = "Average"
        elif self.priority == '4':
            self.priority_desc = "High"
        elif self.priority == '5':
            self.priority_desc = "Critical"
        else:
            self.priority_desc = "UNKNOWN"

    def __str__(self):
        return self.priority + " " + self.description
