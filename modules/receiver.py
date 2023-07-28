from dataclasses import dataclass, field
from modules.constants import *
from typing import List
import serial

@dataclass
class SerialReceiver():
    my_serial: serial.Serial() = field(init=False, default_factory=serial.Serial)
    connected: bool = field(init=False, default=False)

    def connect(self, port: str, baudrate: int, timeout: float) -> None:
        try:
            self.my_serial.port = port
            self.my_serial.baudrate = baudrate
            self.my_serial.timeout = timeout
            self.my_serial.open()
            self.connected = True
        except serial.SerialException:
            self.connected = False
            return self.connected

    def disconnect(self) -> bool:
        if self.my_serial.is_open:
            self.my_serial.close()
        self.connected = False

        return self.connected

    def receive_message(self) -> str:
        if self.connected is not True:
            return ''
        return self.my_serial.read(self.my_serial.in_waiting).decode('utf-8')

