from PyQt5 import QtWidgets
from app_main_window import App_MainWindow
import sys
import qdarktheme
import matplotlib.pyplot as plt
from modules.theme import Theme

theme = Theme.DARK
theme_setup = {
    Theme.LIGHT: lambda: qdarktheme.setup_theme('light'),
    Theme.DARK: lambda: (qdarktheme.setup_theme('dark'), plt.style.use('dark_background'))
}

if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)
    theme_setup[theme]()
    MainWindow = QtWidgets.QMainWindow()
    ui = App_MainWindow(MainWindow)
    ui.show()
    sys.exit(app.exec_())
