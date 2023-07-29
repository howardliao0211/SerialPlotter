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

@dataclass
class MplConfig:
    x_min: float = 0
    x_max: float = 0
    y_min: float = 0
    y_max: float = 0

    title: str = ''
    xlabel: str = ''
    ylabel: str = ''

    is_auto_enable: bool = True
    is_grid_enable: bool = False

    def auto_enabled(self, enable: bool) -> None:
        self.is_auto_enable = enable
    
    def grid_enabled(self, enable: bool) -> None:
        self.is_grid_enable = enable
    
    def is_axis_lim_valid(self) -> bool:
        if self.x_max <= self.x_min:
            return False

        if self.y_max <= self.y_min:
            return False

        return True

    def set_x_lim(self, min: float, max: float) -> None:
        self.x_min = min
        self.x_max = max
    
    def set_y_lim(self, min: float, max: float) -> None:
        self.y_min = min
        self.y_max = max
    
    def set_labels(self, title: str, x_label: str, y_label: str) -> None:
        self.title = title
        self.xlabel = x_label
        self.ylabel = y_label

    def get_x_lim(self) -> List[float]:
        return [self.x_min, self.x_max]

    def get_y_lim(self) -> List[float]:
        return [self.y_min, self.y_max]

@dataclass
class ConsoleDisplayer:
    ''' An displayer class to display data and message through console. '''

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_FLOAT_EVENT, self.display_float)

    def display_message(self, message: str) -> None:
        print(message, end='')

    def display_float(self, datas: List[float]) -> None:
        print(', '.join([str(num) for num in datas]))

@dataclass
class MplDisplayer:
    ''' An displayer class to display data and message through canvas. '''
    mpl_widget: MplWidget
    mpl_config: MplConfig = field(default_factory=MplConfig)

    def update_mpl_config(self) -> None:
        pass

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_FLOAT_EVENT, self.display_float)
    
    def display_message(self, message: str) -> None:
        pass

    def display_float(self, datas: List[float]) -> None:
        x = range(len(datas))
        self.mpl_widget.canvas.axes.cla()
        
        if self.mpl_config.title != '':
            self.mpl_widget.canvas.axes.set_title(self.title)
        
        if self.mpl_config.xlabel != '':
            self.mpl_widget.canvas.axes.set_xlabel(self.xlabel)
        
        if self.mpl_config.ylabel != '':
            self.mpl_widget.canvas.axes.set_ylabel(self.ylabel)
        
        if not self.mpl_config.is_auto_enable and self.mpl_config.is_axis_lim_valid():
            self.mpl_widget.canvas.axes.set_xlim(self.mpl_config.get_x_lim())
            self.mpl_widget.canvas.axes.set_ylim(self.mpl_config.get_y_lim())

        if self.mpl_config.is_grid_enable:
            self.mpl_widget.canvas.axes.grid()
        
        self.mpl_widget.canvas.axes.stem(x, datas)
        self.mpl_widget.canvas.axes.get_figure().canvas.draw()

@dataclass
class TextBrowserDisplayer:
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
