from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import List
import serial
import random

class Displayer(ABC):
    ''' An abstract class to display data. '''
    
    @abstractmethod
    def display_message(self, message: str) -> None:
        pass

    @abstractmethod
    def display_float(self, datas: List[float]) -> None:
        pass

@dataclass
class ConsoleDisplayer(Displayer):
    ''' An displayer class to display data and message through console. '''
    def display_message(self, message: str) -> None:
        print(message)

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

class Receiver(ABC):
    ''' An abstract class for receiving data. '''
    @abstractmethod
    def receive_message(message: str):
        pass

@dataclass
class Application():
    ''' An application class that contend all the functions the user need. '''
    # serial: serial.Serial
    displayer: Displayer

if __name__ == '__main__':
    fig, ax = plt.subplots()
    print(type(ax))
    displayer = CanvasDisplayer(canvas=ax)
    app = Application(displayer=displayer)
    app.displayer.display_message("Hello")

    while True:
        random_list = []
        for i in range(10):
            random_list.append(random.uniform(0, 1))
        app.displayer.display_float(random_list)
        ax.stem(range(10), random_list)
        plt.draw()
        plt.pause(0.01)

