import logging.config
from dataclasses import dataclass

@dataclass
class CreditCard:
    name: str
    card_number: str
    balance: int = 0
    limit: int = 0

    # def __post_init__(self):
    # if not self.luhn_checksum(self.card_number):
    # raise Exception("Not a card number")
    #
    def is_valid_luhn(self):
        return True

    def charge(self, amount):
        if not self.is_valid_luhn():
            return self.balance

        if self.balance + amount > self.limit:
            return self.balance

        self.balance += amount

    def credit(self, amount):
        if not self.is_valid_luhn():
            return self.balance

        self.balance -= amount

    @staticmethod
    def luhn_checksum(card_number):
        """
        Python implementation of Luhn algorithm.
        https://en.wikipedia.org/wiki/Luhn_algorithm
        :param card_number - string
        """

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
