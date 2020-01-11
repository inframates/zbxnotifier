from modules.zabbix.elements import Host
from zbxnotifier.modules.settings import Settings
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
import sys


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class ProblemsWorker(QRunnable):

    def __init__(self):
        super(ProblemsWorker, self).__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            problems = self.get_problems()
            self.signals.result.emit(problems)
        except:
            (type, value, traceback) = sys.exc_info()
            print(type)
            print(value)

    def get_problems(self):
        # Get all the problems
        problems = Settings.zbx_api.get_problems()

        # Get all the triggers
        trigger_ids = []
        for problem in problems:
            trigger_ids.append(problem.triggerid)
        triggers = Settings.zbx_api.get_triggers(trigger_ids)

        for problem in problems:
            for trigger in triggers:
                # Sometimes, there's no trigger id for the problemid
                try:
                    if problem.triggerid == trigger.triggerid:
                        problem.trigger = trigger
                except AttributeError:
                    problem.trigger = None

        # Get all events based on the trigger IDs
        events = Settings.zbx_api.get_events(trigger_ids)

        for problem in problems:
            for event in events:
                try:
                    if problem.trigger.triggerid == event.triggerid:
                        problem.event = event
                except AttributeError:
                    problem.event = None

        # Search for faulty problems, when there's no trigger or event
        clear_problems = []
        for problem in problems:
            if problem.trigger is not None and problem.event is not None:
                clear_problems.append(problem)

        return clear_problems
