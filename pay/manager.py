from dataclasses import dataclass, field
from typing import MutableMapping

from pay.logging import LOG
from pay.creditcard import CreditCard
from pay.utils import Singleton


@dataclass
class Manager(metaclass=Singleton):
    cards: MutableMapping[str, CreditCard] = field(default_factory=dict)

    def add(self, name, card_number, limit):
        """
        <Add>는 새로운 신용카드에 이름, 카드번호와 한도액을 전달받습니다.
        신용카드 번호는 Luhn 10 알고리즘으로 검증 받아야 합니다.
        새로운 카드는 $0 잔액에서 시작합니다.

        :param name - str
        :param card_number - int
        :param limit - int
        """

        LOG.info(f"adding - {name}, {card_number}, ${limit}")
        try:
            self.cards[name] = CreditCard(
                name=name, card_number=card_number, limit=limit
            )
            LOG.info(f"added - {self.cards[name].get_status()}")
        except Exception as ex:
            LOG.error(f"can't be created: {name}, {card_number}, ${limit}")
            LOG.error(ex)

    def charge(self, name, amount):
        """
        <Charge>는 이름과 금액이 전달되며 잔액을 증가시킵니다.
        Charge는 한도액을 넘어서면 결제 거부가 되고 무시됩니다.
        Charge는 Luhn 10 알고리즘으로 검증에 실패 하면 무시됩니다.

        :param name - str
        :param amount - int
        """

        LOG.info(f"charging - {name}: ${amount}")
        card = self.cards[name]
        ret = card.charge(amount)

        if ret:
            LOG.info(f"charged - {self.cards[name].get_status()}")

    def credit(self, name, amount):
        """
        <Credit>은 이름과 금액이 전달되며 잔액을 감소시킵니다.
        Credit는 잔고가 $0미만으로 떨어지면 마이너스 잔액이 생깁니다.
        Credit는 Luhn 10 알고리즘으로 검증에 실패 하면 무시됩니다.

        :param name - str
        :param amount - int
        """
        LOG.info(f"crediting - {name}: ${amount}")

        card = self.cards[name]
        ret = card.credit(amount)

        if ret:
            LOG.info(f"creditied- {self.cards[name].get_status()}")

    def get_cards(self):
        return self.cards

    def status(self):
        return "\n".join([f"{card.get_status()}" for _, card in self.cards.items()])
