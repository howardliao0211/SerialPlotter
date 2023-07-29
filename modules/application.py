from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from modules.displayer import TextBrowserDisplayer, ConsoleDisplayer, MplDisplayer
from modules.receiver import Receiver, SerialReceiver, SimulationReceiver
from modules.string_parser import StringParser
from modules.event import EventType, post_event

@dataclass
class Application:
    ''' An application class that contend all the functions the user need. '''
    text_displayer: TextBrowserDisplayer
    canvas_displayer: MplDisplayer
    console_displayer: ConsoleDisplayer = field(default_factory=ConsoleDisplayer)
    receiver: Receiver = field(default_factory=SerialReceiver)
    parser: StringParser = field(init=False, default_factory=StringParser)

    def __post_init__(self) -> None:
        self.canvas_displayer.setup_event_handler()
        self.text_displayer.setup_event_handler()
        self.console_displayer.setup_event_handler()
        self.parser.setup_event_handler()

    def connect(self, port: str, baudrate: int, timeout: float) -> bool:
        return self.receiver.connect(port, baudrate, timeout)

    def disconnect(self) -> bool:
        return self.receiver.disconnect()

    def receive_and_post_event(self) -> None:
        msg = self.receiver.receive_message()
        if msg != '':
            post_event(EventType.NEW_MESSAGE_EVENT, msg)
