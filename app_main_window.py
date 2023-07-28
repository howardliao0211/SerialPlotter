from UI.ui_main_window import Ui_MainWindow
from modules.application import Application
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, QTimer, QEvent
from modules.displayer import TextBrowserDisplayer

import serial.tools.list_ports as list_ports

class App_MainWindow(QtWidgets.QMainWindow):
    ''' Application GUI '''
    def __init__(self, parent: QtWidgets.QMainWindow = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QTimer()
        self.app = Application(TextBrowserDisplayer(self.ui.textBrowser))

        self.timer.timeout.connect(self.app.receive_and_post_event)
        self.ui.com_port_combo_box.addItems([str(port) for port in list_ports.comports()])
        self.ui.refresh_button.clicked.connect(self.refresh_button_action)
        self.ui.connect_button.clicked.connect(lambda: self.connect_button_action(self.ui.com_port_combo_box.currentText(), self.ui.baud_rate_combo_box.currentText(), self.ui.time_out_line_edit.text()))
        self.ui.end_button.clicked.connect(lambda: self.app.text_displayer.auto_scroll_enabled(True))
        self.ui.clear_button.clicked.connect(lambda: self.ui.textBrowser.clear())
        self.ui.textBrowser.installEventFilter(self)
    
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if source == self.ui.textBrowser:
            if event.type() == QEvent.Wheel:
                self.app.text_displayer.auto_scroll_enabled(False)
        
        return super().eventFilter(source, event)
    
    def refresh_button_action(self) -> None:
        self.ui.com_port_combo_box.clear()
        self.ui.com_port_combo_box.addItems([str(port) for port in list_ports.comports()])
    
    def connect_button_action(self, port_info: str, baudrate: str, timeout: str) -> None:
        connected = bool()

        if self.ui.connect_button.text() == 'Connect !':
            for port in list_ports.comports():
                if str(port) == port_info:
                    connected = self.app.connect(port.name, int(baudrate), float(timeout))
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
            self.ui.connect_button.setText('Disconnect !')
            self.ui.statusbar.showMessage('Connection Successful!')
            self.timer.start(1)
        else:
            self.ui.connect_button.setText('Connect !')
            self.ui.statusbar.clearMessage()
            self.timer.stop()

