from dataclasses import dataclass, field
from typing import List
from modules.event import EventType, subscribe, post_event

@dataclass
class StringParser():
    start_string: str
    end_string: str

    def setup_event_handler(self) -> None:
        subscribe(EventType.NEW_MESSAGE_EVENT, self.parse_float)

    def parse_string(self, msg: str) -> str:
        if self.start_string in msg and self.end_string in msg:
            msg = msg[msg.index(self.start_string) + len(self.start_string) : msg.index(self.end_string)]
            return msg
        return ''

    def parse_float(self, msg: str) -> None:
        try:
            post_event(EventType.NEW_FLOAT_EVENT, list(map(float, self.parse_string(msg).split(','))))
        except ValueError:
            pass