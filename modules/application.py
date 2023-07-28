from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from modules.displayer import TextBrowserDisplayer, ConsoleDisplayer
from modules.receiver import SerialReceiver
from modules.string_parser import StringParser
from modules.event import EventType, post_event

@dataclass
class Application():
    ''' An application class that contend all the functions the user need. '''
    text_displayer: TextBrowserDisplayer
    console_displayer: ConsoleDisplayer = field(default_factory=ConsoleDisplayer)
    receiver: SerialReceiver = field(init=False, default_factory=SerialReceiver)
    parser: StringParser = field(init=False, default_factory=lambda: StringParser('Distance = ', 'mm'))

    def __post_init__(self) -> None:
        self.parser.setup_event_handler()
        self.text_displayer.setup_event_handler()
        # self.console_displayer.setup_event_handler()

    def connect(self, port: str, baudrate: int, timeout: float) -> bool:
        self.receiver.connect(port, baudrate, timeout)
        if not self.receiver.connected:
            return False
        return True

    def disconnect(self) -> bool:
        return self.receiver.disconnect()

    def receive_and_post_event(self) -> None:
        msg = self.receiver.receive_message()
        if msg != '':
            post_event(EventType.NEW_MESSAGE_EVENT, msg)
