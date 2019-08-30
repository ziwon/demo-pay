"""
이벤트 클래스를 정의한다.

"""
import logging.config

from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, MutableMapping, List, Callable, Union

from pay.manager import Manager

logging.config.fileConfig("logging.ini")
LOG = logging.getLogger(__name__)
print(LOG)

T = TypeVar("T")

LOG.info("test")


@dataclass
class Event:
    kind: str
    name: str
    params: List[T]

    def __post_init__(self):
        params: List[str] = []
        self.params = list(
            map(
                lambda param: int(param[1:]) if param[0] == "$" else int(param),
                self.params,
            )
        )

    @abstractmethod
    def handle(self) -> None:
        raise NotImplementedError

    def set_manager(self, manager: Manager) -> None:
        self.manager = manager

    def get_params(self) -> Union[List[T], T]:
        return self.params[0] if len(self.params) == 1 else self.params


class EventFactory:
    _event: MutableMapping[str, type] = {}

    @classmethod
    def register(cls, kind: str) -> Callable:
        def wrapper(clz: type) -> type:
            if not issubclass(clz, Event):
                raise Exception("Not a Event class.")
            cls._event[kind] = clz
            return clz

        return wrapper

    @classmethod
    def create(cls, message: str, manager: Manager) -> Event:
        kind, name, *params = message.split()
        event: Event = cls._event.get(kind)
        if event:
            event = event(kind, name, params)
            event.set_manager(manager)
            return event
        raise Exception("Unknown event.")


@EventFactory.register("Add")
class AddEvent(Event):
    def handle(self) -> None:
        LOG.info(self)
        card_number, limit = self.get_params()
        self.manager.add(self.name, card_number, limit)


@EventFactory.register("Charge")
class ChargeEvent(Event):
    def handle(self) -> None:
        LOG.info(self)
        amount = self.get_params()
        self.manager.charge(self.name, amount)


@EventFactory.register("Credit")
class CreditEvent(Event):
    def handle(self) -> None:
        LOG.info(self)
        amount = self.get_params()
        self.manager.credit(self.name, amount)
