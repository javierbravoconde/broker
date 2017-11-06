from datetime import datetime
from core.async import Message
from core.async import MSG_ORDER_PROC

class Order(Message):
    """Represent an order to be executed

        Attributes:
            order_uid (string):     unique id of the order
            created (datetime):     utc date/time of the order creation
            symbol (string):        symbol of the traded asset
            amount (float):         quantity ordered
            filled (float):         quantity already filled (positive if buy order, negative if sell order)
            limit   (float):        limit price
            status  (integer):      Order status

                                    SUBMITTED = 1  # Order has been submitted.
                                    ACCEPTED = 2  # Order has been acknowledged by the broker.
                                    CANCELED = 3  # Order has been canceled.
                                    PARTIALLY_FILLED = 4  # Order has been partially filled.
                                    FILLED = 5  # Order has been completely filled.                            1=

        """

    def __init__(self, symbol, amount, limit=None):
        super().__init__(MSG_ORDER_PROC)
        self.order_uid = ""
        self.created = datetime.utcnow()
        self.symbol = symbol
        self.amount = amount
        self.filled = 0
        self.limit = limit
        self.status = 0

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

        return ', '.join(sb)

    def __repr__(self):
        return self.__str__()

