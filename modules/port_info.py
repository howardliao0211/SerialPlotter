from dataclasses import dataclass
import serial.tools.list_ports as list_ports

def get_com_port() -> List[str]:
    return [port for port, desc, hwid in list_ports.comports()]

@dataclass
class COM_Port_Info():
    
