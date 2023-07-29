from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from modules.event import EventType, subscribe
from modules.theme import Theme
from UI.mplwidget import MplWidget
from PyQt5.QtWidgets import QTextBrowser, QScrollBar
from enum import Enum, auto
import matplotlib.pyplot as plt

class PlotType(Enum):
    STEM = auto()
    PLOT = auto()
@dataclass
class MplConfig:
    x_min: float = 0
    x_max: float = 0
    y_min: float = 0
    y_max: float = 0

    sample_num: int = 100

    title: str = ''
    xlabel: str = ''
    ylabel: str = ''

    is_auto_enable: bool = True
    is_grid_enable: bool = False

    plot_type: PlotType = PlotType.STEM

    def is_x_axis_lim_valid(self) -> bool:
        return self.x_max > self.x_min
    
    def is_y_axis_lim_valid(self) -> bool:
        return self.y_max > self.y_min

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
    sample_dict: dict = field(default_factory=dict)

    def update_mpl_config(self, mpl_config: MplConfig) -> None:
        self.mpl_config = mpl_config

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_FLOAT_EVENT, self.display_float)
    
    def display_message(self, message: str) -> None:
        pass

    def display_float(self, datas: List[float]) -> None:
        self.mpl_widget.canvas.axes.cla()
        
        if self.mpl_config.title != '':
            self.mpl_widget.canvas.axes.set_title(self.title)
        
        if self.mpl_config.xlabel != '':
            self.mpl_widget.canvas.axes.set_xlabel(self.xlabel)
        
        if self.mpl_config.ylabel != '':
            self.mpl_widget.canvas.axes.set_ylabel(self.ylabel)
        
        if not self.mpl_config.is_auto_enable:
            if self.mpl_config.plot_type is not PlotType.PLOT and self.mpl_config.is_x_axis_lim_valid():
                self.mpl_widget.canvas.axes.set_xlim(self.mpl_config.get_x_lim())

            if self.mpl_config.is_y_axis_lim_valid():
                self.mpl_widget.canvas.axes.set_ylim(self.mpl_config.get_y_lim())

        if self.mpl_config.is_grid_enable:
            self.mpl_widget.canvas.axes.grid()
        
        self.plot(datas)
        self.mpl_widget.canvas.axes.get_figure().canvas.draw()
    
    def plot(self, datas: List[float]) -> None:

        if self.mpl_config.plot_type == PlotType.STEM:
            self.mpl_widget.canvas.axes.stem(range(len(datas)), datas)

        elif self.mpl_config.plot_type == PlotType.PLOT:
            for index, data in enumerate(datas):
                if not index in self.sample_dict:
                    self.sample_dict[index] = []
                self.sample_dict[index].append(data)

            start_point = 0
            end_point = len(self.sample_dict[index])

            for index in self.sample_dict:
                if len(self.sample_dict[index]) > self.mpl_config.sample_num:
                    start_point = len(self.sample_dict[index]) - self.mpl_config.sample_num

                self.mpl_widget.canvas.axes.plot(range(start_point, end_point), self.sample_dict[index][start_point:end_point])


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
