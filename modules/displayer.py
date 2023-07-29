from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from modules.event import EventType, subscribe
from modules.theme import Theme
from UI.mplwidget import MplWidget
from PyQt5.QtWidgets import QTextBrowser, QScrollBar

import matplotlib.pyplot as plt

class Displayer(ABC):
    ''' An abstract class to display data. '''
    
    @abstractmethod
    def setup_event_handler(self) -> None:
        pass

    @abstractmethod
    def display_message(self, message: str) -> None:
        pass

    @abstractmethod
    def display_float(self, datas: List[float]) -> None:
        pass

@dataclass
class ConsoleDisplayer(Displayer):
    ''' An displayer class to display data and message through console. '''

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_FLOAT_EVENT, self.display_float)

    def display_message(self, message: str) -> None:
        print(message, end='')

    def display_float(self, datas: List[float]) -> None:
        print(', '.join([str(num) for num in datas]))

@dataclass
class MplDisplayer(Displayer):
    ''' An displayer class to display data and message through canvas. '''
    mpl_widget: MplWidget
    title: str = field(default='')
    xlabel: str = field(default='')
    ylabel: str = field(default='')

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_FLOAT_EVENT, self.display_float)
    
    def display_message(self, message: str) -> None:
        pass

    def display_float(self, datas: List[float]) -> None:
        x = range(len(datas))
        self.mpl_widget.canvas.axes.cla()
        if self.title != '':
            self.mpl_widget.canvas.axes.set_title(self.title)
        if self.xlabel != '':
            self.mpl_widget.canvas.axes.set_xlabel(self.xlabel)
        if self.ylabel != '':
            self.mpl_widget.canvas.axes.set_ylabel(self.ylabel)
        self.mpl_widget.canvas.axes.stem(x, datas)
        self.mpl_widget.canvas.axes.grid()
        self.mpl_widget.canvas.axes.get_figure().canvas.draw()

@dataclass
class TextBrowserDisplayer(Displayer):
    text_browser: QTextBrowser
    is_auto_scroll_enabled: bool = True

    def auto_scroll_enabled(self, enable: bool) -> None:
        self.is_auto_scroll_enabled = enable

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_MESSAGE_EVENT, self.display_message)

    def display_message(self, message: str) -> None:
        self.text_browser.insertPlainText(message)
        if self.is_auto_scroll_enabled:
            self.text_browser.verticalScrollBar().setValue(self.text_browser.verticalScrollBar().maximum())
    
    def display_float(self, datas: List[float]) -> None:
        pass
