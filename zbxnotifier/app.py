from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from zbxnotifier.modules.problems import Problems
from zbxnotifier.modules.zabbix import Zabbix
from zbxnotifier.modules.table import CentralBox, HostAlertTable, TimeWidget
import sys


class AppMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.hostalert_widget = HostAlertTable()
        self.hostalert_widget_table = self.hostalert_widget.get_table(self.get_host_problems())
        self.time_widget = TimeWidget()

        self.app = QApplication([])
        self.setWindowTitle("Zabbix Ongoing Alerts")
        self.resize(500, 600)

        self.centralbox_layout = CentralBox(self.hostalert_widget_table, self.time_widget.get_time_widget())
        self.setCentralWidget(self.centralbox_layout)

        self.timer_start()

    def get_host_problems(self):
        zbx = Zabbix('http://192.168.1.160/', 'Admin', 'zabbix')
        p = Problems(zbx)
        host_problems = p.get_host_problems()
        return host_problems

    def timer_start(self):
        self.time_timer = QtCore.QTimer(self)
        self.time_timer.timeout.connect(self.timer_time)
        self.time_timer.start(1000)

        self.host_alert = QtCore.QTimer(self)
        self.host_alert.timeout.connect(self.timer_hostalert)
        self.host_alert.start(5000)


    def timer_time(self):
        self.update_gui()

    def timer_hostalert(self):
        self.update_gui(True)


    def update_gui(self, host_alert=False):
        if host_alert is False:
            self.time_widget.update_time()
            self.centralbox_layout = CentralBox(self.hostalert_widget_table, self.time_widget.get_time_widget())
            self.setCentralWidget(self.centralbox_layout)
        else:

            self.time_widget.update_time()
            self.hostalert_widget_table = self.hostalert_widget.get_table(self.get_host_problems())
            self.time_widget.update_last_update()
            self.centralbox_layout = CentralBox(self.hostalert_widget_table, self.time_widget.get_time_widget())
            self.setCentralWidget(self.centralbox_layout)






app = QtWidgets.QApplication(sys.argv)
main_window = AppMainWindow()
main_window.show()
sys.exit(app.exec_())