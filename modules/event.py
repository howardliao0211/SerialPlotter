from enum import Enum, auto

subscribers = dict()

class EventType(Enum):
    NEW_MESSAGE_EVENT = auto()
    NEW_FLOAT_EVENT = auto()

def subscribe(event: EventType, fn):
    if not event in subscribers:
        subscribers[event] = []
    subscribers[event].append(fn)

def post_event(event: EventType, data):
    if not event in subscribers:
        return

    for fn in subscribers[event]:
        fn(data)
