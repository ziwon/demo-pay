from pay.creditcard import CreditCard

import pytest


def test_creditcard_luhn_valid():
    assert CreditCard.luhn_valid(5111111111111118) == True


def test_creditcard_luhn_not_valid():
    assert CreditCard.luhn_valid(1234567890123456) == False


def test_creditcard_add():
    card: CreditCard = CreditCard(name="Jane", card_number=4111111111111111, limit=1000)

    assert card.name == "Jane"
    assert card.card_number == 4111111111111111
    assert card.limit == 1000


def test_creditcard_charge():
    card: CreditCard = CreditCard(name="Jane", card_number=4111111111111111, limit=1000)

    card.charge(500)
    assert card.balance == 500


def test_creditcard_not_charge():
    card: CreditCard = CreditCard(name="Jane", card_number=4111111111111111, limit=1000)

    card.charge(500)
    card.charge(800)
    assert card.balance == 500


def test_creditcard_credit():
    card: CreditCard = CreditCard(name="Jane", card_number=4111111111111111, limit=1000)
    card.credit(500)
    assert card.balance == -500
