from dataclasses import dataclass, field
from typing import Protocol
import serial

class Receiver(Protocol):
    ''' A protocol to define how receiver should communicate with other object'''

    ''' Return the connection status. True: Connected. False: Disconnect'''
    def connect(*args) -> bool:
        ...
    
    ''' Return the connection status. True: Connected. False: Disconnect'''
    def disconnect() -> bool:
        ...
    
    ''' Return the received message. '''
    def receive_message() -> str:
        ...

@dataclass
class SerialReceiver:
    my_serial: serial.Serial() = field(init=False, default_factory=serial.Serial)
    connected: bool = field(init=False, default=False)

    def connect(self, port: str, baudrate: int, timeout: float) -> bool:
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

import random
@dataclass
class SimulationReceiver:
    
    def connect(self, *args) -> bool:
        return True
    
    def disconnect(self) -> bool:
        return False

    def receive_message(self) -> str:
        msg = str()
        random_floats = [random.random() for _ in range(3)]
        msg = '$$$' + ','.join(str(num).format() for num in random_floats) + '###' + '\n'
        return msg
