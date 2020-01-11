import sys
from zbxnotifier.modules.windowelements.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


class Application:
    def __init__(self):
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        sys.exit(app.exec())


if __name__=="__main__":
    a = Application()
