from PyQt5 import QtWidgets
from app_main_window import App_MainWindow
import sys
import qdarktheme

if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)
    # qdarktheme.setup_theme('dark')
    qdarktheme.setup_theme('light')
    # qdarktheme.setup_theme('auto')
    MainWindow = QtWidgets.QMainWindow()
    ui = App_MainWindow(MainWindow)
    ui.show()
    sys.exit(app.exec_())
