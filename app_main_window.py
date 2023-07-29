from UI.ui_main_window import Ui_MainWindow
from modules.application import Application
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, QTimer, QEvent
from modules.displayer import TextBrowserDisplayer, MplDisplayer
from modules.theme import Theme

import serial.tools.list_ports as list_ports
import qdarktheme
import matplotlib as mpl
import matplotlib.pyplot as plt

class App_MainWindow(QtWidgets.QMainWindow):
    """Application GUI"""

    def __init__(self, parent: QtWidgets.QMainWindow = None):
        """UI Initialization"""
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """ Set up class instances """
        self.timer = QTimer()
        self.timeout_ms = 20

        self.app = Application(
            TextBrowserDisplayer(self.ui.textBrowser),
            MplDisplayer(self.ui.graph_mpl_widget),
        )
        self.app.parser.set_config(
            self.ui.start_string_line_edit.text(),
            self.ui.end_string_line_edit.text(),
            self.ui.delimiter_line_edit.text(),
        )

        """ Connect UI Signals and Events """
        self.timer.timeout.connect(self.app.receive_and_post_event)
        self.ui.com_port_combo_box.addItems(
            [str(port) for port in list_ports.comports()]
        )
        self.ui.refresh_button.clicked.connect(self.refresh_button_action)
        self.ui.connect_button.clicked.connect(
            lambda: self.connect_button_action(
                self.ui.com_port_combo_box.currentText(),
                self.ui.baud_rate_combo_box.currentText(),
                self.ui.time_out_line_edit.text(),
            )
        )
        self.ui.end_button.clicked.connect(
            lambda: self.app.text_displayer.auto_scroll_enabled(True)
        )
        self.ui.clear_button.clicked.connect(lambda: self.ui.textBrowser.clear())
        self.ui.start_string_line_edit.textChanged.connect(
            lambda: self.app.parser.set_config(
                self.ui.start_string_line_edit.text(),
                self.ui.end_string_line_edit.text(),
                self.ui.delimiter_line_edit.text(),
            )
        )
        self.ui.end_string_line_edit.textChanged.connect(
            lambda: self.app.parser.set_config(
                self.ui.start_string_line_edit.text(),
                self.ui.end_string_line_edit.text(),
                self.ui.delimiter_line_edit.text(),
            )
        )
        self.ui.delimiter_line_edit.textChanged.connect(
            lambda: self.app.parser.set_config(
                self.ui.start_string_line_edit.text(),
                self.ui.end_string_line_edit.text(),
                self.ui.delimiter_line_edit.text(),
            )
        )
        self.ui.textBrowser.installEventFilter(self)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if source == self.ui.textBrowser:
            if event.type() == QEvent.Wheel:
                self.app.text_displayer.auto_scroll_enabled(False)

        return super().eventFilter(source, event)

    def refresh_button_action(self) -> None:
        self.ui.com_port_combo_box.clear()
        self.ui.com_port_combo_box.addItems(
            [str(port) for port in list_ports.comports()]
        )

    def connect_button_action(
        self, port_info: str, baudrate: str, timeout: str
    ) -> None:
        connected = bool()

        if self.ui.connect_button.text() == "Connect !":
            for port in list_ports.comports():
                if str(port) == port_info:
                    connected = self.app.connect(
                        port.name, int(baudrate), float(timeout)
                    )
            if connected is not True:
                msg = QMessageBox(self)
                msg.setWindowTitle("Warning!")
                msg.setText("Connection Failed!")
                msg.setStandardButtons(QMessageBox.Yes)
                msg.setIcon(QMessageBox.Warning)
                msg.exec()
        else:
            connected = self.app.disconnect()

        if connected is True:
            self.ui.connect_button.setText("Disconnect !")
            self.ui.statusbar.showMessage("Connection Successful!")
            self.timer.start(self.timeout_ms)
        else:
            self.ui.connect_button.setText("Connect !")
            self.ui.statusbar.clearMessage()
            self.timer.stop()
