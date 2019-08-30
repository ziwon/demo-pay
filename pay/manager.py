"""
신용카드 정보를 저장하고 있는 저장소이다.

메모리 저장소 또는 외부 저장소로 확장 가능하다.
"""
import logging

from dataclasses import dataclass, field
from typing import MutableMapping
from pay.creditcard import CreditCard
from pay.utils import Singleton


@dataclass
class Manager(metaclass=Singleton):
    cards: MutableMapping[str, CreditCard] = field(default_factory=dict)

    def add(self, name, card_number, limit):
        """
        <Add>는 새로운 신용카드에 이름, 카드번호와 한도액을 전달받습니다.

        - 신용카드 번호는 Luhn 10 알고리즘으로 검증 받아야 합니다.
        - 새로운 카드는 $0 잔액에서 시작합니다.
        """
        self.cards[name] = CreditCard(
            name=name, card_number=card_number, limit=int(limit)
        )

        LOG = logging.getLogger(__name__)
        print(LOG)
        LOG.info("test")

        LOG.info("add")

    def charge(self, name, amount):
        """
        <Charge>는 이름과 금액이 전달되며 잔액을 증가시킵니다.

        - Charge는 한도액을 넘어서면 결제 거부가 되고 무시됩니다.
        - Charge는 Luhn 10 알고리즘으로 검증에 실패 하면 무시됩니다.
        """
        card = self.cards[name]
        card.charge(amount)

    def credit(self, name, amount):
        """
        <Credit>은 이름과 금액이 전달되며 잔액을 감소시킵니다.

        - Credit는 잔고가 $0미만으로 떨어지면 마이너스 잔액이 생깁니다.
        - Credit는 Luhn 10 알고리즘으로 검증에 실패 하면 무시됩니다.
        """
        card = self.cards[name]
        card.credit(amount)
