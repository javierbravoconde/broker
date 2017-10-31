'''
Created on Oct 30, 2017

@author: javier
'''

from queue import Queue
from threading import Thread
import time
import datetime
from core.async import EventQueue, Message
from core.async import MSG_TICKER_PROC, MSG_OHLCV_PROC


class Dispatcher(EventQueue):
    '''
    classdocs
    '''

    def __init__(self, period):
        '''
        Constructor
        '''
        super().__init__(period)
        self.ticker_observers = {}
        self.ohlcv_observers = {}
    
        
    def on_message(self, mgs: Message):
        print("dispatcher::on_message")
        if mgs.type == MSG_TICKER_PROC:
            for market_modif in mgs.markets:
                if self.ticker_observers.get(market_modif):
                    for observer in self.ticker_observers[market_modif]:
                        observer.put(mgs)
        elif mgs.type == MSG_OHLCV_PROC:
            for market_modif in mgs.markets:
                if self.ohlcv_observers.get(market_modif):
                    for observer in self.ohlcv_observers[market_modif]:
                        observer.put(mgs)
             
        

    def on_init(self, msg: Message):
        print("dispatcher::on_init")
            
    def on_tick(self, msg: Message):
        print("dispatcher::on_tick")        
    
    def subscribe_to_ticker_changes(self, market, strategy):
        print("subscribing to maket")
        if self.ticker_observers.get(market):
            self.ticker_observers[market].append(strategy)
        else:
            self.ticker_observers[market] = [strategy]

    def subscribe_to_ohlcv_changes(self, market, strategy):
        print("subscribing to maket")
        if self.ohlcv_observers.get(market):
            self.ohlcv_observers[market].append(strategy)
        else:
            self.ohlcv_observers[market] = [strategy]            
        