import abc
from core.apiconsumer import BaseConsumer
from core.async import Message
from core.async import MSG_ORDER_PROC


class Broker(BaseConsumer):
    """ Abstract class for a Broker

            A broker is the component in charge of passing order to the exchange
    """

    def __init__(self, period, dispatcher):
        super().__init__(period, dispatcher)

    def subscribe_to_order(self, dispatcher, symbol):
        dispatcher.subscribe_to_order(symbol, self)


    def on_message(self, msg: Message):
        raise NotImplementedError()


    def on_tick(self, msg: Message):
        raise NotImplementedError()


    def _submitOrder(self, order):
        raise NotImplementedError()


    def _cancelOrder(self, order):
        raise NotImplementedError()


class TestBroker(Broker):
    """ Test implementation of a Broker

        Print the order as they arrive
    """
    def on_message(self, msg: Message):
        if msg.type == MSG_ORDER_PROC:
            print("TestBroker::MSG_ORDER_PROC")
            print(msg)

    def on_tick(self, msg: Message):
        print("TestBroker::on_tick")

    def _submitOrder(self, order):
        raise NotImplementedError()

    def _cancelOrder(self, order):
        raise NotImplementedError()
