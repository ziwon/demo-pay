"""
이벤트 클래스를 정의한다.

"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, MutableMapping, List, Callable
from .manager import Manager

T = TypeVar("T")


@dataclass
class Event:
    kind: str
    name: str
    params: List[T]

    @abstractmethod
    def handle(self):
        raise NotImplemented()

    def set_manager(self, manager: Manager) -> None:
        self.manager = manager

    def __str__(self):
        return f"{self.kind}(name: {self.name}, params: {self.params})"

    def numeralize(self) -> List[int]:
        params: List[int] = []
        for param in self.params:
            if param[0] == "$":
                params.append(param[1:])
        self.params = params
        return self.params


class EventFactory:
    _event: MutableMapping[str, type] = {}

    @classmethod
    def register(cls, kind: str) -> Callable:
        def wrapper(clz: type) -> type:
            if not issubclass(clz, Event):
                raise Exception("Must be subclass of Event class.")

            cls._event[kind] = clz
            return clz

        return wrapper

    @classmethod
    def create(cls, message: str, manager: Manager) -> Event:
        kind, name, *params = message.split()
        event: Event = cls._event.get(kind)
        if event:
            return event(kind, name, params)
        raise Exception("There is no such event.")


@EventFactory.register("Add")
class AddEvent(Event):
    def handle(self):
        print(self)
        print(self.numeralize())
        # self.repository.add(name, card_number, limit)


@EventFactory.register("Charge")
class ChargeEvent(Event):
    def handle(self):
        print(self)
        print(self.numeralize())
        # self.respository.charge(name, limit)


@EventFactory.register("Credit")
class CreditEvent(Event):
    def handle(self):
        print(self)
        print(self.numeralize())
        # self.repository.credit(name, limit)
