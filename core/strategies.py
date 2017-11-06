'''
Created on Oct 31, 2017

@author: javier
'''
from core.async import EventQueue, Message
from core.async import MSG_TICKER_PROC, MSG_OHLCV_PROC
from order import Order
import random


class StrategyBase(EventQueue):
    def __init__(self, period, dispatcher):
        super().__init__(period)
        self.dispatcher = dispatcher
        
    def subscribe_to_ticker(self, dispatcher, symbol):
        dispatcher.subscribe_to_ticker(symbol, self)

    def subscribe_to_ohlcv(self, dispatcher, symbol):
        dispatcher.subscribe_to_ohlcv(symbol, self)


class StrategyTest(StrategyBase):
    '''
    classdocs
    '''
    def __init__(self, period, dispatcher):
        '''
        Constructor
        '''
        super().__init__(period, dispatcher)
           
    def on_message(self, msg: Message):
        print("StrategyTest::on_message")
        if msg.type == MSG_TICKER_PROC:
            print("StrategyTest::MSG_TICKER_PROC")
        elif msg.type == MSG_OHLCV_PROC:
            print("StrategyTest::MSG_OHLCV_PROC")
    def on_init(self, msg: Message):
        print("StrategyTest::on_init")
            
    def on_tick(self, msg: Message):
        print("StrategyTest::on_tick")


class DummyStrategy(StrategyBase):
    """ Dummy strategy for testing

    This strategy will send a buy order if the current price is lower than the last price received
    Other if the current price is higher it will sell
    It will do nothing is the price does not change
    """

    def __init__(self, period, dispatcher):
        '''
        Constructor
        '''
        super().__init__(period, dispatcher)
        self.previous_price = {}


    def on_message(self, msg: Message):
        print("DummyStrategy::on_message")
        if msg.type == MSG_TICKER_PROC:
            print("DummyStrategy::MSG_TICKER_PROC")
            self.process_ticker(msg)

        elif msg.type == MSG_OHLCV_PROC:
            print("DummyStrategy::MSG_OHLCV_PROC")
            #print(msg.symbol, msg.history)

    def on_init(self, msg: Message):
        print("DummyStrategy::on_init")


    def on_tick(self, msg: Message):
        print("StrategyTest2::on_tick")

    def process_ticker(self, msg: Message):
        print("DummyStrategy::process_ticker", msg.ticker)
        last_price = float(msg.ticker['Last'])
        last_price = last_price*random.choice([0.99,1.01])
        print("DummyStrategy::process_ticker", "last_price", last_price)

        if self.previous_price.get(msg.symbol):
            prev_price = self.previous_price.get(msg.symbol)

            if last_price < prev_price:
                # Send buy order
                order = Order(msg.symbol, 1, limit=last_price)
                self.dispatcher.put(order)

            elif last_price > prev_price:
                # Send sell order
                order = Order(msg.symbol, -1, limit=last_price)
                self.dispatcher.put(order)

            self.previous_price[msg.symbol] = last_price

        else:
            self.previous_price[msg.symbol] = last_price

