from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import List
from constants import *
import serial
import serial.tools.list_ports as list_ports
import random
import numpy as np
import matplotlib.pyplot as plt

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

@dataclass
class SerialReceiver():
    my_serial: serial.Serial() = field(init=False, default_factory=serial.Serial)
    connected: bool = field(init=False, default=False)
    
    def connect(self) -> None:
        try:
            self.my_serial.port = self.find_device_port()
            self.my_serial.baudrate = 115200
            self.my_serial.timeout = 0.5
            self.my_serial.open()
            self.connected = True
        except serial.SerialException:
            print('Can not find device port')
            return self.connected

    def disconnect(self) -> None:
        if self.my_serial.is_open:
            self.my_serial.close()
        self.connected = False

    def find_device_port(self) -> str:
        for port, desc, hwid in list_ports.comports():
            if (DEVICE_PID in hwid) and (DEVICE_VID in hwid):
                print('Device Port: {}'.format(port))
                return port
        return ''

    def receive_message(self) -> str:
        if self.connected is not True:
            return ''
        return self.my_serial.read(self.my_serial.in_waiting).decode('utf-8')

@dataclass
class StringParser():
    start_string: str
    end_string: str

    def parse_string(self, msg: str) -> str:
        if self.start_string in msg and self.end_string in msg:
            msg = msg[msg.index(self.start_string) + len(self.start_string) : msg.index(self.end_string)]
            return msg
        return ''

    def parse_int(self, msg: str) -> List[int]:
        try:
            return list(map(int, self.parse_string(msg).split(',')))
        except ValueError:
            return []
    
    def parse_float(self, msg: str) -> List[float]:
        try:
            return list(map(float, self.parse_string(msg).split(',')))
        except ValueError:
            return []

@dataclass
class Application():
    ''' An application class that contend all the functions the user need. '''
    # serial: serial.Serial
    displayer: Displayer = field(default_factory=ConsoleDisplayer)
    receiver: SerialReceiver = field(init=False, default_factory=SerialReceiver)
    parser: StringParser = field(init=False, default_factory=lambda: StringParser('Distance = ', 'mm'))
    messages: List[str] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.receiver.connect()
        if self.receiver.connected is not True:
            raise serial.SerialException('Can not find device')

    def receive_message(self) -> None:
        msg = self.receiver.receive_message()
        self.messages.append(msg)
    
    def display_message(self) -> None:
        for message in self.messages:
            if message != '':
                self.displayer.display_message(message)
        self.messages = []
    
    def receive_and_display_message(self) -> None:
        self.receive_message()
        self.display_message()
    
    def display_parse_message(self) -> None:
        values = []
        self.receive_message()
        for message in self.messages:
            values = self.parser.parse_int(message)
        
        for value in values:
            print(value)


if __name__ == '__main__':
    fig, ax = plt.subplots()
    # displayer = CanvasDisplayer(canvas=ax)
    # displayer = ConsoleDisplayer()
    
    import time

    app = Application()
    app.displayer.display_message("Hello")
    
    while True:
        app.display_parse_message()
        time.sleep(0.1)


