from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from datetime import datetime


class CentralBox(QWidget):
    def __init__(self, hostalerttable, timewidget):
        super(CentralBox, self).__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(timewidget)
        self.layout.addWidget(hostalerttable)

        # self.layout.addWidget(TimeWidget().get_time_widget())
        # self.layout.addWidget(HostAlertTable().get_table(hosts))
        self.setLayout(self.layout)



class HostAlertTable:

    def get_bg_color(self, severity):
        if severity == '1':
            return [151, 170, 179]
        elif severity == '2':
            return [116, 153, 255]
        elif severity == '3':
            return [255, 200, 89]
        elif severity == '4':
            return [255, 160, 89]
        elif severity == '5':
            return [233, 118, 89]
        elif severity == '6':
            return [228, 89, 89]


    def get_table(self, hosts):
        table = QTableWidget()
        table.setRowCount(len(hosts)+1)
        table.setColumnCount(3)
        table.setWindowTitle("Current Zabbix Alerts")
        table.resize(400, 250)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignHCenter)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("Severity"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("Hostname"))
        table.setHorizontalHeaderItem(2, QTableWidgetItem("Problem Description"))

        row = 0
        for host in hosts:
            priority = QTableWidgetItem(host.trigger.priority_desc)
            priority.setBackground(QColor(*self.get_bg_color(host.trigger.priority)))

            hostname = QTableWidgetItem(host.hostname)

            trigger_description = QTableWidgetItem(host.trigger.description)

            table.setItem(row, 0, priority)
            table.setItem(row, 1, hostname)
            table.setItem(row, 2, trigger_description)
            row = row + 1

        return table


class TimeWidget:

    def __init__(self):
        self.last_update_time = "Never"
        self.update_time()

    def update_time(self):
        self.time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def update_last_update(self):
        self.last_update_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def get_time_widget(self):
        label = QLabel()
        current_time = "CurrentTime: " + self.time
        last_update = "LastUpdate: " + self.last_update_time

        label.setText(current_time + " | " + last_update)
        return label


