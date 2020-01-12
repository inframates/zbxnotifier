import sys
from zbxnotifier.modules.windowelements.main_window import MainWindow
from zbxnotifier.modules.settings import Settings
from zbxnotifier.modules.zabbix.zabbix import ZabbixConnection
from PyQt5.QtWidgets import QApplication
from threading import Thread


class Application:
    def __init__(self):
        app = QApplication(sys.argv)

        Settings.init_config()

        zbx_conn_thread = Thread(target=ZabbixConnection().connect_thread)
        zbx_conn_thread.start()

        window = MainWindow()
        window.show()

        sys.exit(app.exec())

