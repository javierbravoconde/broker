'''
Created on Oct 31, 2017

@author: javier
'''
from core.async import EventQueue, Message
from core.dispatcher import Dispatcher
import requests
from core.async import MSG_TICKER_PROC, MSG_OHLCV_PROC


class StrategyBase(EventQueue):
    def __init__(self, period, dispatcher):
        super().__init__(period)
        self.dispatcher = dispatcher
        
    def subscribe_to_ticker_changes(self, dispatcher, market):
        dispatcher.subscribe_to_ticker_changes(market, self)

    def subscribe_to_ohlcv_changes(self, dispatcher, market):
        dispatcher.subscribe_to_ohlcv_changes(market, self)


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


class StrategyTest2(StrategyBase):
    '''
    classdocs
    '''

    def __init__(self, period, dispatcher):
        '''
        Constructor
        '''
        super().__init__(period, dispatcher)

    def on_message(self, msg: Message):
        print("StrategyTest2::on_message")
        if msg.type == MSG_TICKER_PROC:
            print("StrategyTest2::MSG_TICKER_PROC")
            print(msg.markets, msg.ticker)
        elif msg.type == MSG_OHLCV_PROC:
            print("StrategyTest2::MSG_OHLCV_PROC")

    def on_init(self, msg: Message):
        print("StrategyTest2::on_init")

    def on_tick(self, msg: Message):
        print("StrategyTest2::on_tick")