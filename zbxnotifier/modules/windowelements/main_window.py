from zbxnotifier.modules.settings import Settings
from zbxnotifier.modules.windowelements.zbx_problem_table import ZbxProblemTable
from zbxnotifier.modules.zabbix.problems import ProblemsWorker
from zbxnotifier.modules.windowelements.statusbar import Statusbar

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer, QThreadPool


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(Settings.main_window_title)
        self.window().resize(Settings.main_window_width, Settings.main_window_height)

        self.init_ui()

        self.problem_table_timer = QTimer()
        self.problem_table_timer.setInterval(1000)
        self.problem_table_timer.timeout.connect(self.update_problem_table_worker)
        self.problem_table_timer.start()



    def init_ui(self):
        self._create_central_widget()
        self.setStatusBar(Statusbar())

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())



    def _create_central_widget(self):
        """
        Initial setup of the widgets
        :return:
        """
        self.zbx_problem_table = ZbxProblemTable()
        self.setCentralWidget(self.zbx_problem_table)

    def update_problem_table_worker(self):
        worker = ProblemsWorker()
        worker.signals.result.connect(self.update_problem_table)

        self.threadpool.start(worker)

    def update_problem_table(self, data):
        self.zbx_problem_table.update_data(data)
        self.update()

        self.size()








