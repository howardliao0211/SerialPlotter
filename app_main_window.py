from UI.ui_main_window import Ui_MainWindow
from modules.application import Application
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, QTimer, QEvent
from datetime import datetime
from modules.displayer import TextBrowserDisplayer, MplDisplayer, MplConfig, PlotType
from modules.save import save_log

import serial.tools.list_ports as list_ports
import os

plot_type_dict = {
    'Stem': PlotType.STEM,
    'Plot': PlotType.PLOT,
}
class App_MainWindow(QtWidgets.QMainWindow):
    """Application GUI"""

    def __init__(self, parent: QtWidgets.QMainWindow = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """ Set up class instances """
        self.timer = QTimer()
        self.timeout_ms = 20
        self.log_dir = 'logs'
        self.filename = 'saved_log'

        self.app = Application(
            TextBrowserDisplayer(self.ui.console_text_browser),
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
        self.ui.save_button.clicked.connect(self.save_button_action)
        self.ui.refresh_button.clicked.connect(self.refresh_button_action)
        self.ui.connect_button.clicked.connect(
            lambda: self.connect_button_action(
                self.ui.com_port_combo_box.currentText(),
                self.ui.baud_rate_combo_box.currentText(),
            )
        )
        self.ui.end_button.clicked.connect(
            lambda: self.app.text_displayer.auto_scroll_enabled(True)
        )
        self.ui.clear_button.clicked.connect(lambda: self.ui.console_text_browser.clear())
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
        self.ui.x_max_double_spin_box.textChanged.connect(self.graph_config_action)
        self.ui.x_min_double_spin_box.textChanged.connect(self.graph_config_action)
        self.ui.y_min_double_spin_box.textChanged.connect(self.graph_config_action)
        self.ui.y_max_double_spin_box.textChanged.connect(self.graph_config_action)
        self.ui.grid_combo_box.currentTextChanged.connect(self.graph_config_action)
        self.ui.auto_combo_box.currentTextChanged.connect(self.graph_config_action)
        self.ui.plot_type_combo_box.currentIndexChanged.connect(self.graph_config_action)
        self.ui.sample_spin_box.textChanged.connect(self.graph_config_action)
        self.ui.console_text_browser.installEventFilter(self)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if source == self.ui.console_text_browser:
            if event.type() == QEvent.Wheel:
                self.app.text_displayer.auto_scroll_enabled(False)

        return super().eventFilter(source, event)
    
    def save_button_action(self) -> None:
        filename = self.filename + datetime.now().strftime('_%Y%m%d_%H%M%S') + '.txt'
        save_log(self.ui.console_text_browser.toPlainText(), self.log_dir, filename)
        self.ui.statusbar.showMessage(f'Console log has been saved to {os.path.join(self.log_dir, filename)}')
    
    def graph_config_action(self) -> None:
        current_plot_type = PlotType
        current_plot_type = plot_type_dict[self.ui.plot_type_combo_box.currentText()]

        self.app.canvas_displayer.update_mpl_config(
            MplConfig(
                x_min=float(self.ui.x_min_double_spin_box.text()),
                x_max=float(self.ui.x_max_double_spin_box.text()),
                y_min=float(self.ui.y_min_double_spin_box.text()),
                y_max=float(self.ui.y_max_double_spin_box.text()),
                is_auto_enable=True if self.ui.auto_combo_box.currentText() == 'Enable' else False,
                is_grid_enable=True if self.ui.grid_combo_box.currentText() == 'Enable' else False,
                sample_num=int(self.ui.sample_spin_box.text()),
                plot_type=current_plot_type
            )
        )

        if current_plot_type == PlotType.PLOT:
            self.ui.x_min_double_spin_box.setEnabled(False)
            self.ui.x_max_double_spin_box.setEnabled(False)
            self.ui.sample_spin_box.setEnabled(True)

        elif current_plot_type == PlotType.STEM:
            self.ui.x_min_double_spin_box.setEnabled(True)
            self.ui.x_max_double_spin_box.setEnabled(True)
            self.ui.sample_spin_box.setEnabled(False)

    def refresh_button_action(self) -> None:
        self.ui.com_port_combo_box.clear()
        self.ui.com_port_combo_box.addItems(
            [str(port) for port in list_ports.comports()]
        )

    def connect_button_action(
        self, port_info: str, baudrate: str
    ) -> None:
        connected = bool()

        if self.ui.connect_button.text() == "Connect !":
            for port in list_ports.comports():
                if str(port) == port_info:
                    connected = self.app.connect(
                        port.name, int(baudrate)
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
