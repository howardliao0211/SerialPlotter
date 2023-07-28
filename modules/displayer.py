from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from modules.event import EventType, subscribe
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
        subscribe(EventType.NEW_MESSAGE_EVENT, self.display_message)

    def display_message(self, message: str) -> None:
        print(message, end='')

    def display_float(self, datas: List[float]) -> None:
        for data in datas:
            print(str(data))

@dataclass
class CanvasDisplayer(Displayer):
    ''' An displayer class to display data and message through canvas. '''
    canvas: plt.Axes
    title: str = field(default='')
    xlabel: str = field(default='')
    ylabel: str = field(default='')

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_MESSAGE_EVENT, self.display_message)
        subscribe(EventType.NEW_FLOAT_EVENT, self.display_float)

    def display_message(self, message: str) -> None:
        print(message)

    def display_float(self, datas: List[float]) -> None:
        x = range(len(datas))
        self.canvas.axes.clear()
        if self.title != '':
            self.canvas.axes.set_title(self.title)
        if self.xlabel != '':
            self.canvas.axes.set_xlabel(self.xlabel)
        if self.ylabel != '':
            self.canvas.axes.set_ylabel(self.ylabel)
        self.canvas.axes.stem(x, datas)
        self.canvas.axes.grid()
        # self.canvas.axes.get_figure().canvas.draw()
        plt.draw()
        plt.pause(0.01)

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
