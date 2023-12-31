from dataclasses import dataclass, field
from typing import Protocol
import serial
import numpy as np

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

    counter: float = 0.0

    def connect(self, *args) -> bool:
        return True
    
    def disconnect(self) -> bool:
        return False

    def receive_message(self) -> str:
        msg = str()
        simulate_data = list()
        # simulate_data = [random.random() for _ in range(20)]
        simulate_data.append(np.sin(self.counter))
        simulate_data.append(np.cos(self.counter))
        simulate_data.append(np.sin(self.counter) + (np.pi / 2))
        simulate_data.append(np.cos(self.counter) + (np.pi / 2))
        simulate_data.append(np.sin(self.counter) + (np.pi))
        simulate_data.append(np.cos(self.counter) + (np.pi))
        self.counter += 0.1
        msg = '$$$' + ','.join(str(num).format() for num in simulate_data) + '###' + '\n'
        return msg
