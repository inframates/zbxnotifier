from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStatusBar
from zbxnotifier.modules.zabbix.zabbix import ZabbixConnection
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject


class StatusSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class StatusWorker(QRunnable):
    def __init__(self):
        super(StatusWorker, self).__init__()
        self.signals = StatusSignals()

    @pyqtSlot()
    def run(self):
        connection_status = ZabbixConnection.get_status_desc()
        self.signals.result.emit(connection_status)


class Statusbar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.status_widget = QLabel("ZBX Status: " + ZabbixConnection.get_status_desc())
        self.init_elements()

    def update_elements(self):
        self.status_widget.setText("ZBX Status: " + ZabbixConnection.get_status_desc())
        self.status_widget.update()

    def init_elements(self):
        self.addWidget(self.status_widget)



