# customers with 1000 or more fidelty points get global 5% discount.
# A discount of 10% is applied to each line item with 20 or more units.
# Orders with at least 10 distinct items get a global 7% discount
from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

class Order: # the context

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)

        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

class Promotion(ABC): # promotion is an abstract base class

    @abstractmethod
    def discount(self, order):
        """Return discount as a positive dollar amount
        """

class FidelityPromo(Promotion):
    """5% discount for customers with more than 1000 fidelity points
    """

    def discount(self, order):
        return order.total() * .05 if \
    order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):
    """discount of 10% is applied to each line item with 20 or more units
    """

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity > 20:
                discount += item.total() * .1
        return discount

class LargeOrderDiscount(Promotion):
    """7% global discount if 10 distinct items
    """

    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        return order.total() * .07 if \
    len(distinct_items) >= 10 else 0
